#!/usr/bin/env python3
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable


PROJECT_DIR = Path("/Users/openclaw/.openclaw/workspace/projects/weekly-listing-audit")
DB_PATH = Path("/Users/openclaw/.openclaw/workspace/data/local_listings.db")
BQ_TABLE = "instant-contact-479316-i4.zero_dataset.orders"
OUTPUT_JSON = PROJECT_DIR / "cross_region_gap_champions.json"
OUTPUT_MD = PROJECT_DIR / "CROSS_REGION_GAP_REPORT.md"
DEFAULT_LOOKBACK_DAYS = 90
TOP_CHAMPIONS = 500
TOP_GAP_CHAMPIONS = 200
VALID_TYPES = {"HTPCR", "HC", "HB401"}
F_PREFIX_EXCEPTIONS = {"FLAG", "F1309", "FRND", "FKFLOR"}
IMGC_PREFIX = "IMGC"


@dataclass(frozen=True)
class ChampionRow:
    design: str
    revenue: float
    orders: int
    market: str


def canonical_product_type(raw_type: str | None) -> str | None:
    if raw_type is None:
        return None
    value = raw_type.strip().upper()
    if not value:
        return None
    if value.startswith("F") and value not in F_PREFIX_EXCEPTIONS:
        return value[1:] or None
    return value


def extract_design_from_sku(sku: str | None) -> str | None:
    if sku is None:
        return None
    text = sku.strip().upper()
    if not text:
        return None
    parts = [part.strip().upper() for part in text.split("-")]
    if len(parts) < 3:
        return None
    design = parts[2]
    return design or None


def prepare_gcloud_config() -> str | None:
    source = Path.home() / ".config" / "gcloud"
    if not source.exists():
        return None

    temp_dir = tempfile.mkdtemp(prefix="codex-gcloud-")
    target = Path(temp_dir)
    for child in source.iterdir():
        destination = target / child.name
        if child.is_dir():
            shutil.copytree(child, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(child, destination)
    return temp_dir


def build_bq_sql(country: str, start_date: date, end_date: date) -> str:
    return f"""
WITH parsed AS (
  SELECT
    SPLIT(Custom_Label, '-')[SAFE_OFFSET(0)] AS product_type_raw,
    SPLIT(Custom_Label, '-')[SAFE_OFFSET(2)] AS design_code,
    SAFE_CAST(Net_Sale AS FLOAT64) AS net_sale
  FROM `{BQ_TABLE}`
  WHERE DATE(Paid_Date) >= DATE '{start_date.isoformat()}'
    AND DATE(Paid_Date) < DATE '{end_date.isoformat()}'
    AND Buyer_Country = '{country}'
),
normalized AS (
  SELECT
    CASE
      WHEN STARTS_WITH(product_type_raw, 'F') AND product_type_raw NOT IN ('FLAG', 'F1309', 'FRND', 'FKFLOR')
        THEN SUBSTR(product_type_raw, 2)
      ELSE product_type_raw
    END AS canonical_type,
    design_code,
    net_sale
  FROM parsed
)
SELECT
  design_code AS design,
  ROUND(SUM(COALESCE(net_sale, 0)), 2) AS revenue,
  COUNT(1) AS orders
FROM normalized
WHERE canonical_type IN ('HTPCR', 'HC', 'HB401')
  AND design_code IS NOT NULL
  AND design_code != ''
GROUP BY design
ORDER BY revenue DESC, orders DESC, design ASC
LIMIT {TOP_CHAMPIONS}
""".strip()


def run_bq_query(country: str, start_date: date, end_date: date) -> list[ChampionRow]:
    sql = build_bq_sql(country=country, start_date=start_date, end_date=end_date)
    env = os.environ.copy()
    temp_config = prepare_gcloud_config()
    if temp_config:
        env["CLOUDSDK_CONFIG"] = temp_config

    try:
        result = subprocess.run(
            ["bq", "query", "--use_legacy_sql=false", "--format=json", sql],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("`bq` CLI is not installed or not on PATH.") from exc
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        stdout = (exc.stdout or "").strip()
        message = stderr or stdout or str(exc)
        raise RuntimeError(f"BigQuery query failed for {country}: {message}") from exc
    finally:
        if temp_config:
            shutil.rmtree(temp_config, ignore_errors=True)

    payload = json.loads(result.stdout)
    rows: list[ChampionRow] = []
    for entry in payload:
        design = str(entry.get("design") or "").strip().upper()
        if not design:
            continue
        rows.append(
            ChampionRow(
                design=design,
                revenue=round(float(entry.get("revenue") or 0.0), 2),
                orders=int(entry.get("orders") or 0),
                market=country,
            )
        )
    return rows


def iter_listing_skus(conn: sqlite3.Connection, table_name: str) -> Iterable[str | None]:
    cursor = conn.execute(f"SELECT seller_sku FROM {table_name}")
    for row in cursor:
        yield row[0]


def build_listing_design_set(table_name: str) -> set[str]:
    conn = sqlite3.connect(DB_PATH)
    try:
        designs: set[str] = set()
        for seller_sku in iter_listing_skus(conn, table_name):
            design = extract_design_from_sku(seller_sku)
            if design:
                designs.add(design)
        return designs
    finally:
        conn.close()


def compute_gaps(
    source_rows: list[ChampionRow],
    target_designs: set[str],
    selling_market: str,
    missing_market: str,
) -> list[dict]:
    gaps: list[dict] = []
    for row in source_rows[:TOP_GAP_CHAMPIONS]:
        if row.design.startswith(IMGC_PREFIX):
            continue
        if row.design in target_designs:
            continue
        gaps.append(
            {
                "design": row.design,
                "revenue": round(row.revenue, 2),
                "orders": row.orders,
                "sells_in": selling_market,
                "missing_from": missing_market,
            }
        )
    return gaps


def write_json_report(payload: dict) -> None:
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def format_currency(value: float) -> str:
    return f"${value:,.2f}"


def render_gap_lines(gaps: list[dict]) -> str:
    if not gaps:
        return "_None_"
    lines = []
    for idx, gap in enumerate(gaps, start=1):
        lines.append(
            f"{idx}. `{gap['design']}` | {format_currency(gap['revenue'])} | "
            f"{gap['orders']} orders | sells in {gap['sells_in']} | missing from {gap['missing_from']}"
        )
    return "\n".join(lines)


def write_markdown_report(payload: dict) -> None:
    us_to_uk = payload["gaps"]["us_champions_missing_in_uk"]
    uk_to_us = payload["gaps"]["uk_champions_missing_in_us"]
    summary = payload["summary"]
    md = "\n".join(
        [
            "# Cross-Region Champion Gap Report",
            "",
            f"- Generated: {payload['generated_on']}",
            f"- Lookback window: {payload['window']['start_date']} to {payload['window']['end_date_exclusive']} (90 days)",
            f"- BQ source: `{BQ_TABLE}`",
            f"- SQLite source: `{DB_PATH}`",
            "",
            "## Summary",
            "",
            f"- US active listing designs: {summary['us_active_listing_designs']:,}",
            f"- UK active listing designs: {summary['uk_active_listing_designs']:,}",
            f"- US top 500 champions pulled: {summary['us_top_500_count']}",
            f"- UK top 500 champions pulled: {summary['uk_top_500_count']}",
            f"- US champions missing in UK: {summary['us_missing_in_uk_count']}",
            f"- UK champions missing in US: {summary['uk_missing_in_us_count']}",
            f"- Total revenue at risk: {format_currency(summary['total_revenue_at_risk'])}",
            "",
            "## UK Champions Missing In US",
            "",
            render_gap_lines(uk_to_us),
            "",
            "## US Champions Missing In UK",
            "",
            render_gap_lines(us_to_uk),
            "",
        ]
    )
    OUTPUT_MD.write_text(md, encoding="utf-8")


def build_payload(
    start_date: date,
    end_date: date,
    us_rows: list[ChampionRow],
    uk_rows: list[ChampionRow],
    us_designs: set[str],
    uk_designs: set[str],
) -> dict:
    uk_missing_in_us = compute_gaps(uk_rows, us_designs, "UK", "US")
    us_missing_in_uk = compute_gaps(us_rows, uk_designs, "US", "UK")
    total_revenue_at_risk = round(
        sum(item["revenue"] for item in uk_missing_in_us) + sum(item["revenue"] for item in us_missing_in_uk),
        2,
    )

    return {
        "generated_on": date.today().isoformat(),
        "window": {
            "start_date": start_date.isoformat(),
            "end_date_exclusive": end_date.isoformat(),
            "lookback_days": DEFAULT_LOOKBACK_DAYS,
        },
        "summary": {
            "us_active_listing_designs": len(us_designs),
            "uk_active_listing_designs": len(uk_designs),
            "us_top_500_count": len(us_rows),
            "uk_top_500_count": len(uk_rows),
            "us_missing_in_uk_count": len(us_missing_in_uk),
            "uk_missing_in_us_count": len(uk_missing_in_us),
            "total_revenue_at_risk": total_revenue_at_risk,
        },
        "gaps": {
            "uk_champions_missing_in_us": uk_missing_in_us,
            "us_champions_missing_in_uk": us_missing_in_uk,
        },
    }


def print_summary(payload: dict) -> None:
    summary = payload["summary"]
    print(
        "Cross-region champion gap analysis complete: "
        f"{summary['uk_missing_in_us_count']} UK->US gaps, "
        f"{summary['us_missing_in_uk_count']} US->UK gaps, "
        f"revenue at risk {format_currency(summary['total_revenue_at_risk'])}."
    )
    print(f"JSON: {OUTPUT_JSON}")
    print(f"Report: {OUTPUT_MD}")


def main() -> int:
    start_date = date.today() - timedelta(days=DEFAULT_LOOKBACK_DAYS)
    end_date = date.today()

    try:
        us_rows = run_bq_query("US", start_date, end_date)
        uk_rows = run_bq_query("UK", start_date, end_date)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    us_designs = build_listing_design_set("listings_current")
    uk_designs = build_listing_design_set("listings_uk_current")

    payload = build_payload(start_date, end_date, us_rows, uk_rows, us_designs, uk_designs)
    write_json_report(payload)
    write_markdown_report(payload)
    print_summary(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
