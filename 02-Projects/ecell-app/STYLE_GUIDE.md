# Ecell Global Dashboard Ecosystem - UI/UX Style Guide

This style guide establishes the visual foundation for all internal Ecell Global dashboards (PULSE, ecell.app Hub, Sales/Conversion Intelligence, etc.). Following these guidelines ensures visual consistency, predictable user experiences, and maintainable code across all internal tools.

## 1. Color Tokens

### Primary Brand
*   **Cobalt Base:** `#0047AB` (Used for primary actions, active navigation, branding)
*   **Cobalt Light:** `#E8F0FE` (Used for subtle backgrounds, hover states)
*   **Cobalt Dark:** `#003380` (Used for hover states on primary buttons, deep emphasis)

### Neutrals (Light Mode)
*   **Background Base:** `#FAFBFC` or `#ffffff`
*   **Surface (Cards):** `#ffffff`
*   **Text Primary:** `#1a1a1a` or `#171717` (Zinc-900)
*   **Text Secondary:** `#71717a` (Zinc-500)
*   **Borders:** `#e4e4e7` (Zinc-200)

### Neutrals (Dark Mode)
*   **Background Base:** `#0a0a0a` or `#09142f` (For deep analytics dashboards)
*   **Surface (Cards):** `#09090b` (Zinc-950)
*   **Text Primary:** `#ededed` (Zinc-50)
*   **Text Secondary:** `#a1a1aa` (Zinc-400)
*   **Borders:** `#27272a` (Zinc-800)

## 2. Status & Alert Color System

We use a standard "Traffic Light" system for data health and application status.

*   **Positive / Full / Live:** Emerald (`#10b981` / `emerald-500`)
    *   *Usage:* Data ≥80%, Live apps, successful actions.
    *   *Glow:* `shadow-emerald-500/40`
*   **Warning / Partial:** Amber (`#f59e0b` / `amber-500`)
    *   *Usage:* Data 30-80%, items needing attention.
    *   *Glow:* `shadow-amber-500/40`
*   **Danger / Missing:** Red (`#ef4444` / `red-500`)
    *   *Usage:* Data <30%, critical errors.
    *   *Glow:* `shadow-red-500/40`
*   **Neutral / Coming Soon:** Muted Zinc (`#f4f4f5` / `zinc-100` background with `zinc-500` text)

## 3. Typography Scale

*   **Font Family:** `Inter`, `Geist Sans`, or system sans-serif (`-apple-system`, `BlinkMacSystemFont`).
*   **Page Titles:** `text-3xl font-semibold tracking-tight` (e.g., "Business Apps")
*   **Section Headers / Sidebar Brand:** `text-xl font-bold`
*   **Card Titles:** `text-sm font-semibold`
*   **Body Text:** `text-sm`
*   **Secondary Text / Descriptions:** `text-xs text-zinc-500`
*   **Microcopy / Footers:** `text-[10px] text-zinc-400`

## 4. Component Library & Tailwind Patterns

### Navigation (Sidebar Pattern - e.g., PULSE)
```html
<aside className="w-56 min-h-screen bg-white border-r border-gray-200 flex flex-col">
  <!-- Active Link -->
  <Link className="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm font-medium bg-cobalt text-white shadow-sm">
  <!-- Inactive Link -->
  <Link className="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-cobalt">
</aside>
```

### Navigation (Top Nav Pattern - e.g., ecell.app)
```html
<header className="border-b border-zinc-200/60 bg-white/70 backdrop-blur dark:border-zinc-800/60 dark:bg-zinc-950/60">
  <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">...</div>
</header>
```

### Cards
```html
<div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm transition hover:border-zinc-300 hover:shadow-md dark:border-zinc-800 dark:bg-zinc-950 dark:hover:border-zinc-700">
  ...
</div>
```

### Status Badges
```html
<span className="inline-flex items-center rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2 py-0.5 text-[11px] font-semibold text-emerald-700 dark:text-emerald-200">
  LIVE
</span>
```

### Traffic Light Dots
```html
<div className="w-4 h-4 bg-emerald-500 shadow-emerald-500/40 rounded-full shadow-md" />
```

## 5. Layout Templates

*   **Application Layout (Sidebar):** Use for deep-dive tools (PULSE, Product Entry). `flex h-screen` with `w-56` fixed sidebar and `flex-1` main content area.
*   **Hub/Portal Layout (Top Nav):** Use for landing pages and simple directories (ecell.app). Centered container (`max-w-6xl mx-auto px-6`), grid layouts for content (`grid-cols-1 md:grid-cols-3`).
*   **Analytics Layout (Dark/Immersive):** Use for heavy data visualization (Conversion Dashboard). Radial gradient backgrounds, dark mode forced (`color-scheme: dark`), custom scrollbars.

## 6. Chart Styling Conventions

*   **Library:** Recharts is the standard across the ecosystem.
*   **Colors:** Use the Cobalt scale for primary metrics. If comparing multiple series, use distinct contrasting colors but maintain the Tailwind palette (e.g., `emerald-500` for growth/positive metrics, `rose-500` for decline/negative metrics).
*   **Tooltips:** Ensure Recharts tooltips have a background that matches the theme (white in light mode, dark gray in dark mode) with rounded corners (`rounded-lg`) and subtle shadow.

## 7. Recommended Tailwind Config (v4 / CSS variables)

For new projects using Tailwind v4, add this to `globals.css`:

```css
@import "tailwindcss";

@theme {
  --color-cobalt: #0047AB;
  --color-cobalt-light: #E8F0FE;
  --color-cobalt-dark: #003380;
}

:root {
  --background: #FAFBFC;
  --foreground: #171717;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #0a0a0a;
    --foreground: #ededed;
  }
}

body {
  background: var(--background);
  color: var(--foreground);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
```

## 8. Do's and Don'ts

### Do
*   **DO** use semantic colors for status (Emerald/Amber/Red) across all apps so users instantly recognize meaning.
*   **DO** implement dark mode gracefully using Tailwind's `dark:` variant and Zinc neutral colors.
*   **DO** use `rounded-2xl` for large cards and `rounded-lg` for smaller interactive elements (buttons, nav links).
*   **DO** style scrollbars to be minimal, especially in dark mode analytics dashboards (e.g., `::-webkit-scrollbar { width: 6px; }`).

### Don't
*   **DON'T** use generic bright primary colors outside of the Cobalt brand (avoid standard bright blue unless intentional).
*   **DON'T** mix Sidebar and Top Nav paradigms on the same hierarchical level. Use Sidebar for dense app navigation and Top Nav for global/hub navigation.
*   **DON'T** use heavy drop shadows. Stick to `shadow-sm` or `shadow-md` for cards, and use colored glows (`shadow-[color]/40`) strictly for status indicators or primary focal points.
