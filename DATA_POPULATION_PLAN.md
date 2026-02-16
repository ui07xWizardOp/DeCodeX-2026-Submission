# IMPLEMENTATION PLAN: Granular Dashboard Population

**Goal:** Populate the dashboard with rich, granular data from the Excel source, bypassing the broken Pandas environment. Add new "Advanced Metrics" and "Data Explorer" sections.

## 1. Data Ingestion (Openpyxl-Only)
Since `pandas` is broken in the environment, we will use `openpyxl` to read `DecodeX_VoltRide_Dataset.xlsx`.
**Script:** `scripts/generate_full_data.py`

### Column Mapping (To Verify)
- `Ride_ID` (Col 0)
- `City` (Col 1)
- `Date` (Col 2)
- `Hour` (Col 3)
- `Pickup_Zone` (Col 4)
- `Battery_Level` (Col 5)
- `Driver_Available` (Col 6)
- `Charging_Station_Nearby` (Col 7)
- `Weather` (Col 8)
- `Ride_Status` (Col 9)

### Outputs
1.  `metrics.json`:
    -   Existing KPIs (Kill Zone, Baseline).
    -   *New*: `revenue_lost`, `total_demand`, `worst_zone`.
2.  `charts.json`:
    -   `battery_cliff`: Existing logic.
    -   `heatmap`: Existing logic.
    -   *New*: `hourly_trend` (Demand vs Cancellations), `revenue_trend` (Lost Revenue per Hour).
3.  `table_data.json` (New):
    -   First 100 rows for the "Raw Data Explorer".

## 2. Dashboard UI Updates (`index.html`)
-   **New Section: "Advanced Analytics"**
    -   **Hourly Trends Chart**: Line chart showing Demand vs Supply gap.
    -   **Revenue Impact Chart**: Bar chart of lost revenue by hour.
-   **New Section: "Data Explorer"**
    -   **Table**: Paginated table showing raw ride data.
    -   **Download Button**: Link to download the full dataset (mock or real).

## 3. Dashboard Logic Updates (`app.js`)
-   **Render New Charts**: `renderHourlyTrend`, `renderRevenueChart`.
-   **Render Table**: `renderDataTable` with simple pagination.
-   **Format Currency**: Ensure revenue numbers are formatted as currency.

## Verification Plan
1.  **Run Pipeline**: Execute `python scripts/generate_full_data.py`.
2.  **Verify JSON**: Check `docs/assets/data/` for non-empty files.
3.  **Serve & Test**: Open `docs/index.html` and verify:
    -   KPIs are populated.
    -   Charts are rendering (no empty canvas).
    -   Table shows rows.
