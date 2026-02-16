import openpyxl
import json
import os
import datetime

# Configuration
DATA_FILE = "DecodeX_VoltRide_Dataset.xlsx"
OUTPUT_DIR = "docs/assets/data"

# Column Mapping (0-based) based on debug output
COL_RIDE_ID = 0
COL_CITY = 1
COL_DATE = 2
COL_HOUR = 3
COL_PICKUP_ZONE = 4
COL_DROP_ZONE = 5
COL_DISTANCE = 6
COL_FARE = 7
COL_SURGE = 8
COL_BATTERY = 9
COL_DRIVER_AVAIL = 10
COL_STATION_NEARBY = 11
COL_WEATHER = 12
COL_STATUS = 13
COL_CANCEL_BY = 14

def generate_full_data():
    print(f"Reading {DATA_FILE} with openpyxl...")
    
    try:
        wb = openpyxl.load_workbook(DATA_FILE, read_only=True, data_only=True)
        sheet = wb.active
    except Exception as e:
        print(f"Error loading Excel: {e}")
        return

    # Initialize Metrics
    total_rides = 0
    cancelled_rides = 0
    
    # Kill Zone
    kill_zone_total = 0
    kill_zone_cancelled = 0
    
    # Goldilocks
    goldilocks_total = 0
    goldilocks_cancelled = 0
    
    # Revenue
    revenue_lost_total = 0
    
    # Hourly Data (0-23)
    hourly_demand = [0] * 24
    hourly_cancellations = [0] * 24
    hourly_revenue_lost = [0] * 24
    
    # Heatmap (Zone x Hour). Key: ZoneName, Value: [list of 24 ints for cancellations]
    zone_heatmap = {}
    
    # Battery Cliff
    # Bins: 0-20, 20-30, 30-40, 40-50, 50-60, 60-80, 80-100
    battery_bins_total = [0] * 7
    battery_bins_cancelled = [0] * 7
    bin_labels = ["0-20%", "20-30%", "30-40%", "40-50%", "50-60%", "60-80%", "80-100%"]
    
    # Infra Paradox
    infra_no_total = 0; infra_no_cancelled = 0
    infra_yes_total = 0; infra_yes_cancelled = 0

    # Data Explorer (First 100 rows)
    raw_data = []

    rows = sheet.iter_rows(min_row=2, values_only=True)
    
    for row in rows:
        if row[COL_RIDE_ID] is None: continue # Skip empty rows
        
        total_rides += 1
        
        # Parse Fields
        try:
            city = str(row[COL_CITY])
            hour = int(row[COL_HOUR])
            zone = str(row[COL_PICKUP_ZONE])
            battery = float(row[COL_BATTERY]) if row[COL_BATTERY] is not None else 0
            station = str(row[COL_STATION_NEARBY])
            status = str(row[COL_STATUS])
            fare = float(row[COL_FARE]) if row[COL_FARE] is not None else 0
        except (ValueError, IndexError, TypeError):
            continue # specific row error

        is_cancelled = 1 if status == "Cancelled" else 0
        cancelled_rides += is_cancelled
        
        # Revenue Loss
        if is_cancelled:
            revenue_lost_total += fare
        
        # Hourly
        if 0 <= hour <= 23:
            hourly_demand[hour] += 1
            hourly_cancellations[hour] += is_cancelled
            if is_cancelled:
                hourly_revenue_lost[hour] += fare
            
        # Heatmap
        zone_id = f"{city} - Z{zone}"
        if zone_id not in zone_heatmap:
            zone_heatmap[zone_id] = {"total": [0]*24, "cancelled": [0]*24}
        zone_heatmap[zone_id]["total"][hour] += 1
        zone_heatmap[zone_id]["cancelled"][hour] += is_cancelled
        
        # Kill Zone (<20)
        if battery <= 20:
            kill_zone_total += 1
            kill_zone_cancelled += is_cancelled
        # Goldilocks (30-60)
        elif 30 < battery <= 60:
            goldilocks_total += 1
            goldilocks_cancelled += is_cancelled
            
        # Battery Bins logic
        bin_idx = 0
        if battery <= 20: bin_idx = 0
        elif battery <= 30: bin_idx = 1
        elif battery <= 40: bin_idx = 2
        elif battery <= 50: bin_idx = 3
        elif battery <= 60: bin_idx = 4
        elif battery <= 80: bin_idx = 5
        else: bin_idx = 6
        
        battery_bins_total[bin_idx] += 1
        battery_bins_cancelled[bin_idx] += is_cancelled
        
        # Infra Paradox
        if "No" in station:
            infra_no_total += 1
            infra_no_cancelled += is_cancelled
        elif "Yes" in station:
            infra_yes_total += 1
            infra_yes_cancelled += is_cancelled

        # Raw Data (Top 100)
        if len(raw_data) < 100:
            raw_data.append({
                "id": row[COL_RIDE_ID],
                "city": city,
                "hour": hour,
                "zone": zone,
                "battery": battery,
                "status": status
            })

    # Calculations
    baseline_rate = (cancelled_rides / total_rides * 100) if total_rides else 0
    kill_zone_rate = (kill_zone_cancelled / kill_zone_total * 100) if kill_zone_total else 0
    goldilocks_rate = (goldilocks_cancelled / goldilocks_total * 100) if goldilocks_total else 0
    
    # Revenue Trend - Round to integers
    revenue_trend = [round(r) for r in hourly_revenue_lost]

    # Metrics JSON
    metrics = {
        "kpis": {
            "kill_zone_rate": round(kill_zone_rate, 1),
            "baseline_rate": round(baseline_rate, 1),
            "revenue_loss": round(revenue_lost_total),
            "goldilocks_rate": round(goldilocks_rate, 1),
            "total_demand": total_rides,
            "completed_rides": total_rides - cancelled_rides
        }
    }

    # Charts JSON
    # Battery Cliff
    battery_vals = []
    for i in range(7):
        rate = (battery_bins_cancelled[i] / battery_bins_total[i] * 100) if battery_bins_total[i] else 0
        battery_vals.append(round(rate, 1))

    # Heatmap (Rate Matrix)
    heatmap_z = []
    heatmap_x = list(range(24))
    heatmap_y = sorted(list(zone_heatmap.keys()))
    
    for zone in heatmap_y:
        row = []
        for h in range(24):
            tot = zone_heatmap[zone]["total"][h]
            canc = zone_heatmap[zone]["cancelled"][h]
            rate = (canc / tot * 100) if tot > 0 else 0
            row.append(round(rate, 1))
        heatmap_z.append(row)

    # Infra
    infra_no_rate = (infra_no_cancelled / infra_no_total * 100) if infra_no_total else 0
    infra_yes_rate = (infra_yes_cancelled / infra_yes_total * 100) if infra_yes_total else 0

    charts = {
        "battery_cliff": {
            "labels": bin_labels,
            "values": battery_vals,
            "sample_sizes": battery_bins_total
        },
        "heatmap": {
            "z": heatmap_z,
            "x": heatmap_x,
            "y": heatmap_y
        },
        "hourly_trend": {
            "hours": list(range(24)),
            "demand": hourly_demand,
            "cancellations": hourly_cancellations
        },
        "revenue_trend": {
            "hours": list(range(24)),
            "lost_revenue": revenue_trend
        },
        "infra_paradox": {
            "labels": ["No Station", "Station Nearby"],
            "values": [round(infra_no_rate, 1), round(infra_yes_rate, 1)]
        }
    }

    # Output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(os.path.join(OUTPUT_DIR, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)
        
    with open(os.path.join(OUTPUT_DIR, "charts.json"), "w") as f:
        json.dump(charts, f, indent=2)
        
    with open(os.path.join(OUTPUT_DIR, "table_data.json"), "w") as f:
        json.dump(raw_data, f, indent=2)
        
    print(f"Successfully processed {total_rides} rows.")
    print(f"Total Revenue Lost: ${revenue_lost_total:,.2f}")
    print("Generated metrics.json, charts.json, table_data.json")

if __name__ == "__main__":
    generate_full_data()
