# Request for Modern Device Jig Rows

To: Dickel Pineda / PH IT Team
From: Ava / Creative Pipeline Automation
Subject: URGENT: SQL Exports for Modern Device Jigs (IREN/DRECO)

Hi Dickel,

We are currently building the next generation of the image automation pipeline (ListingForge) to replace the legacy IREN/DRECO system and eliminate the need for manual Photoshop replication.

We have successfully reverse-engineered the coordinate math from the 2014-era `t_jig_measurement` table (e.g., iPhone 4/5, S4), but we need the current ground-truth data for modern devices to test the new Python compositing engine.

Could you please provide a raw SQL dump or CSV export of the `t_jig_measurement` rows for the following priority champion devices?
- iPhone 15, 15 Pro, 15 Pro Max, 15 Plus
- iPhone 16, 16 Pro, 16 Pro Max, 16 Plus
- iPhone 17 (if available)
- Galaxy S24, S24+, S24 Ultra

**Required Columns:**
`f_DeviceCode`, `f_PhoneWidth`, `f_PhoneHeight`, `f_PhoneMarginX`, `f_PhoneMarginY`, `f_PaddingX`, `f_PaddingY`, `f_ImageRotation`, `f_CornerRadius`, `f_Columns`, `f_Rows`, `f_CanvasWidth`, `f_CanvasHeight`

Once we have this, we can run a full Lane 1 parity test and move toward automating the HB401 gaps instantly.

Thanks!