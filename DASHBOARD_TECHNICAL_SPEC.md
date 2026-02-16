# DECODEX DASHBOARD TECHNICAL SPECIFICATION
## "The VoltRide Operations Command Center"

**Version:** 1.0
**Target Platform:** GitHub Pages (Static Web App)
**Theme:** "Electric Insight" (Dark Mode + Neon Accents)

---

## 1. ARCHITECTURE OVERVIEW

### 1.1 Core Philosophy
A "Masterpiece of Analysis" must be:
-   **Instant:** Load in <1s (Pre-computed JSON, no backend queries).
-   **Immersive:** Dark mode default, smooth transitions, high-contrast data.
-   **Narrative-Driven:** The dashboard tells the story (The "Kill Zone", The "Goldilocks Zone").
-   **Device Agnostic:** Fully responsive (Mobile-first grid).

### 1.2 Technology Stack
-   **Core:** HTML5, CSS3 (Modern Flexbox/Grid), ES6+ JavaScript.
-   **Styling:** Tailwind CSS (via CDN for zero-build deployment) + Custom CSS variables.
-   **Visualization:** Plotly.js (Robust, interactive, scientific grade).
-   **Icons:** FontAwesome 6 (Free CDN).
-   **Animation:** Anime.js or CSS Transitions.

### 1.3 Folder Structure
```
/docs
  index.html            # The "Masterpiece" entry point
  /assets
    /css
      style.css         # Custom overrides & animations
    /js
      app.js            # Core logic & routing
      charts.js         # Plotly configurations
      data-loader.js    # JSON fetcher
    /data
      metrics.json      # KPI cards data
      charts.json       # Pre-processed chart data
    /images             # Static assets
```

---

## 2. VISUAL DESIGN SYSTEM ("Electric Insight")

### 2.1 Color Palette
| Token | Hex Value | Usage |
| :--- | :--- | :--- |
| `bg-core` | `#0f172a` | Main background (Slate 900) |
| `bg-card` | `#1e293b` | Card background (Slate 800) |
| `accent-primary` | `#3b82f6` | Primary action (Blue 500) |
| `accent-danger` | `#ef4444` | "Kill Zone" highlight (Red 500) |
| `accent-success` | `#10b981` | "Goldilocks Zone" highlight (Emerald 500) |
| `accent-warn` | `#f59e0b` | Warnings (Amber 500) |
| `text-main` | `#f8fafc` | Primary text (Slate 50) |
| `text-muted` | `#94a3b8` | Secondary text (Slate 400) |

### 2.2 Typography
-   **Headings:** `Inter` or `Outfit` (Google Fonts) - Clean, geometric, modern.
-   **Data/Numbers:** `JetBrains Mono` or `Roboto Mono` - Tabular usage.

### 2.3 UI Components
-   **Glassmorphism:** Slight translucency on floating headers (`backdrop-filter: blur(10px)`).
-   **Neon Glows:** Box shadows on active elements (`box-shadow: 0 0 15px rgba(59, 130, 246, 0.5)`).
-   **Cards:** Rounded corners (`border-radius: 12px`), subtle border (`1px solid rgba(255,255,255,0.1)`).

---

## 3. DASHBOARD COMPONENTS & LAYOUT

### 3.1 Layout Grid
A classic "Bento Box" grid layout that adapts to screen size.
-   **Desktop:** 4 columns, auto-rows.
-   **Mobile:** Single column stack.

### 3.2 Component Breakdown

#### A. The Hero Header
-   **Content:** "VoltRide Operational Intelligence" + "DeCodeX 2026 Submission".
-   **Action:** "Download Full Report" button.
-   **Live ticker:** "Analysis Period: Jan 2025 | Riders: 2,500".

#### B. The "Kill Zone" KPI Card (Critical)
-   **Visual:** Large RED counter "87.5%".
-   **Label:** "Failure Rate at <20% Battery".
-   **Micro-chart:** Sparkline showing the jump from 25% (baseline) to 87.5%.

#### C. The "Goldilocks" KPI Card (Success)
-   **Visual:** Large GREEN counter "30-60%".
-   **Label:** "Optimal Dispatch Window".
-   **Insight:** "Safest Zone (Range Anxiety is a Myth)".

#### D. Chart 1: The Battery Cliff (Bar Chart)
-   **Type:** Categorical Bar.
-   **X-Axis:** Battery Bins (0-20, 20-30, etc.).
-   **Y-Axis:** Cancellation Rate.
-   **Annotations:**
    -   Red annotation box over 0-20%: "SYSTEM FAILURE".
    -   Green annotation over 30-60%: "OPTIMAL".
    -   Yellow annotation over >80%: "CHERRY PICKING".

#### E. Chart 2: The Timing Trap (Heatmap)
-   **Type:** 2D Heatmap.
-   **X-Axis:** Hour of Day (0-23).
-   **Y-Axis:** Zones (City-Zone).
-   **Z-Axis (Color):** Cancellation Rate (Red = High).
-   **Story:** Highlights the Mumbai 10 AM and Hyderabad 7 AM red zones.

#### F. Chart 3: Infrastructure Paradox (Grouped Bar)
-   **Comparison:** "Stations Nearby" vs "No Stations".
-   **Metric:** Cancellation Rate.
-   **Insight:** Shows the counter-intuitive +1% cancellation rate near stations.

---

## 4. INTERACTIVITY REQUIREMENTS

1.  **Hover Effects:**
    -   All chart points must show detailed tooltips (Sample Size, Exact %).
    -   KPI cards lift and glow on hover.

2.  **Filtering (If data permits):**
    -   Simple toggle: "Show All" vs "Exclude <20% System Failure" (Demonstrates how the system *could* perform).

3.  **Story Mode:**
    -   A "Next Insight" floating button that scrolls/highlights specific charts in narrative order (Kill Zone -> Goldilocks -> Timing -> Paradox).

---

## 5. DATA SCHEMA (JSON)

**`data/metrics.json`**
```json
{
  "kpis": {
    "kill_zone_rate": 87.5,
    "baseline_rate": 29.6,
    "revenue_loss": 18500,
    "goldilocks_rate": 23.7
  }
}
```

**`data/charts.json`**
```json
{
  "battery_cliff": {
    "labels": ["0-20%", "20-30%", "30-40%", "40-50%", "50-60%", "60-80%", "80-100%"],
    "values": [87.5, 25.3, 23.7, 24.0, 25.6, 26.3, 27.8],
    "sample_sizes": [8, 95, 450, 600, 550, 400, 397]
  },
  "heatmap": {
    "z": [[...], [...]], // Matrix of cancellation rates
    "x": [0, 1, 2, ... 23],
    "y": ["Mum-Z1", "Hyd-Z7", ...]
  }
}
```

---

## 6. DEPLOYMENT PIPELINE

1.  **Build:** Python script (`generate_dashboard_data.py`) reads `analysis_results.txt` / Excel and dumps JSON to `/docs/data`.
2.  **Test:** Open `docs/index.html` locally.
3.  **Push:** Git commit & push.
4.  **Serve:** GitHub Pages auto-deploys `/docs`.

---

## 7. SUCCESS METRICS
-   **Lighthouse Score:** 95+ Performance, 100 SEO.
-   **Mobile:** Fully functional touch interactions.
-   **Narrative:** A user spends >60s exploring because it's engaging.
