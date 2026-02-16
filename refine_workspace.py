import pandas as pd
import numpy as np
import os

# Paths
base_path = r'c:\Users\KIIT0001\Desktop\projects\DeCodeX'
dataset_path = os.path.join(base_path, 'DecodeX_VoltRide_Dataset.xlsx')
final_excel_path = os.path.join(base_path, 'Final_Submission', 'DeCodeX_VoltRide_Analysis_Workspace.xlsx')

def analyze_and_update():
    print("Loading data...")
    ride_data = pd.read_excel(dataset_path, sheet_name='Ride_Level_Data')
    
    # Recalculate Ghost Cancellations
    ride_data['is_cancelled'] = ride_data['Ride_Status'].apply(lambda x: 1 if x == 'Cancelled' else 0)
    
    # --- WINNING EDGE FEATURE 1: Battery "Cliff" Analysis ---
    # Bin battery data to show the non-linear drop
    ride_data['Battery_Bin'] = pd.cut(ride_data['EV_Battery_%'], bins=range(0, 101, 10))
    battery_curve = ride_data.groupby('Battery_Bin')['is_cancelled'].agg(['mean', 'count']).rename(columns={'mean': 'Cancellation_Rate', 'count': 'Ride_Volume'})
    
    # --- WINNING EDGE FEATURE 2: Synthetic Queue Model ---
    # Proxy queue: Rides ending in a zone / Chargers in that zone
    # We need Charging_Stations sheet for this
    stations = pd.read_excel(dataset_path, sheet_name='Charging_Stations')
    # Aggregate chargers by zone (assuming City is constant or we group by City-Zone)
    zone_chargers = stations.groupby(['City', 'Zone'])['Chargers_Available'].sum().reset_index()
    
    # Count rides ending in each zone-hour
    # ride_data['Drop_Zone'] is float, need to match types
    demand_influx = ride_data.groupby(['City', 'Drop_Zone', 'Hour']).size().reset_index(name='Influx')
    
    # Merge (careful with types)
    merged = pd.merge(demand_influx, zone_chargers, left_on=['City', 'Drop_Zone'], right_on=['City', 'Zone'], how='left')
    merged['Chargers_Available'] = merged['Chargers_Available'].fillna(0)
    
    # Calculate "Pressure Index" = Influx / (Chargers + 1)
    merged['Queue_Pressure_Index'] = merged['Influx'] / (merged['Chargers_Available'] + 1)
    top_pressure_zones = merged.sort_values('Queue_Pressure_Index', ascending=False).head(20)

    # --- UPDATE EXCEL ---
    print("Updating Excel workspace...")
    with pd.ExcelWriter(final_excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        battery_curve.to_excel(writer, sheet_name='Battery_Cliff_Analysis')
        top_pressure_zones.to_excel(writer, sheet_name='Synthetic_Queue_Model')
        
    print("Excel updated successfully.")

if __name__ == "__main__":
    try:
        analyze_and_update()
    except Exception as e:
        print(f"Error: {e}")
