# Modern Ecell Global UI/UX Style Guide 2.0

This style guide establishes the visual and interactive foundation for all next-generation Ecell Global internal dashboards and applications. It builds upon our core brand values while injecting modern aesthetics—such as glassmorphism, fluid micro-interactions, dynamic data visualization, and depth.

---

## 1. Core Atmosphere & Color Tokens

Our modern aesthetic moves away from flat, solid backgrounds and leans into subtle ambient gradients and deep contrast.

### 1.1 Primary Brand (Dynamic Cobalt)
*   **Cobalt Base:** `#0047AB` (Primary actions, active states)
*   **Cobalt Gradient:** `bg-gradient-to-r from-[#0047AB] to-[#0ea5e9]` (Used for hero buttons, active sidebar tabs)
*   **Cobalt Glow:** `shadow-[0_0_15px_rgba(0,71,171,0.4)]` (Hover states for primary elements)

### 1.2 Ambient Backgrounds
*   **Light Mode:** `bg-gradient-to-br from-slate-50 to-blue-50` (Creates a soft, premium depth rather than flat white)
*   **Dark Mode / Deep Analytics:** `bg-gradient-to-br from-zinc-950 via-[#09142f] to-zinc-950`

### 1.3 Fluid Neutrals
*   **Surfaces (Cards):** Light: `bg-white/90 backdrop-blur-md` | Dark: `bg-zinc-900/80 backdrop-blur-xl`
*   **Borders:** `border-zinc-200/50` (Light) | `border-zinc-800/50` (Dark)
*   **Text Hierarchy:** 
    *   Primary: `text-zinc-900` / `text-zinc-50`
    *   Secondary: `text-zinc-500` / `text-zinc-400`
    *   Tertiary/Empty States: `text-zinc-400` / `text-zinc-600`

---

## 2. Dynamic Interactions & Hover States

Modern apps feel tactile and responsive. Every interactable element should respond gracefully to user input.

### 2.1 Micro-Animations
All interactive elements must utilize smooth, standardized transitions:
*   **Base Transition:** `transition-all duration-300 ease-out`
*   **Button Hover:** Scale slightly up and increase glow.
    `hover:-translate-y-0.5 hover:shadow-lg active:translate-y-0 active:shadow-sm`
*   **Card Hover:** Subtle lift and border highlight.
    `hover:-translate-y-1 hover:shadow-xl hover:border-cobalt/30`

### 2.2 Data Loading States (Dynamic Attainment)
Never use blank screens or freeze the UI during data fetches.
*   **Skeleton Loaders:** Use pulsing, rounded shapes that match the final layout.
    `animate-pulse bg-zinc-200/50 dark:bg-zinc-800/50 rounded-xl`
*   **Gentle Spinners:** Use brand colors for loading rings, localized to the component waiting for data.

---

## 3. Tailwind Component Patterns

### 3.1 Glassmorphic Top Navigation
Provides depth and retains context as users scroll through long dashboards.
```jsx
<header className="fixed top-0 left-0 right-0 z-50 border-b border-zinc-200/50 bg-white/70 backdrop-blur-lg dark:border-zinc-800/50 dark:bg-zinc-950/70 transition-all">
  <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
    {/* Navigation Items */}
  </div>
</header>
```

### 3.2 Dynamic Data Cards (Interactive)
Cards should feel like physical, layered objects.
```jsx
<div className="group relative rounded-2xl border border-zinc-200/60 bg-white/80 p-6 shadow-sm backdrop-blur-sm transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-lg hover:border-cobalt/30 dark:border-zinc-800/60 dark:bg-zinc-900/60">
  <div className="absolute inset-0 bg-gradient-to-br from-cobalt/5 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100 rounded-2xl" />
  <div className="relative z-10">
    <h3 className="text-sm font-medium text-zinc-500">Live Revenue</h3>
    <p className="mt-2 text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
      $124,500
    </p>
  </div>
</div>
```

### 3.3 Status Pills with Pulse Effects
Used for real-time data health monitoring.
```jsx
<span className="relative flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-700 dark:text-emerald-400">
  <span className="relative flex h-2 w-2">
    <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
    <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></span>
  </span>
  System Operational
</span>
```

---

## 4. Typography & Information Architecture

*   **Font Stack:** `Inter`, `Manrope`, or `Outfit` for numbers/headings to give a modern geometric feel.
*   **Metric Typography:** Large numbers should use tabular lining (`tabular-nums tracking-tight`) to prevent layout shifts during live data ticks.
*   **Empty States:** Use muted icons alongside friendly, actionable typography when data is missing.

---

## 5. Dynamic Charting & Data Visualization (Recharts)

Charts must animate smoothly and provide interactive feedback.

### 5.1 Animation Guidelines
*   Always enable `isAnimationActive={true}` in Recharts.
*   Set a staggered or customized duration: `<Bar animationDuration={1200} animationEasing="ease-in-out" />`

### 5.2 Interactive Tooltips
Tooltips should look like hovering cards that follow the cursor.
```jsx
const ModernTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="rounded-xl border border-zinc-200/50 bg-white/90 p-4 shadow-xl backdrop-blur-md dark:border-zinc-800/50 dark:bg-zinc-950/90 transform transition-all">
        <p className="mb-2 text-xs font-semibold text-zinc-500">{label}</p>
        {payload.map((entry, index) => (
          <div key={index} className="flex items-center gap-2">
             <div className="h-2 w-2 rounded-full" style={{ backgroundColor: entry.color }} />
             <span className="text-sm font-bold text-zinc-900 dark:text-zinc-50">
               {entry.value.toLocaleString()}
             </span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};
```

### 5.3 Responsive & Liquid Layouts
*   Charts must always be wrapped in `<ResponsiveContainer width="100%" height="100%">`.
*   Grid layouts should use auto-fits (`grid-cols-1 md:grid-cols-2 lg:grid-cols-auto-fit`) to gracefully scale as dashboard filters are toggled.

---

## 6. Implementation Do's & Don'ts

### ✅ DO
*   **DO** use **Skeleton loaders** with `animate-pulse` instead of blocking entire screens with an overarching spinner.
*   **DO** use **Backdrop-blur** (`backdrop-blur-md`) on persistent UI elements like headers and floating sidebars.
*   **DO** style numbers and live tickers with `tabular-nums` so the UI doesn't shake.
*   **DO** use staggered animations for lists and grid cards to create a "waterfall" effect when the page loads.

### ❌ DON'T
*   **DON'T** use harsh, solid black (`#000000`) or plain white backgrounds. Always prefer `zinc-900`/`zinc-950` and `slate-50`.
*   **DON'T** snap data into place immediately upon load if it causes layout jumpiness; reserve space utilizing skeletons.
*   **DON'T** use flat hover states; always pair color shifts with a slight transform or glow.
