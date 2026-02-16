import pandas as pd
import numpy as np
import sys

# Load the dataset
file_path = r'c:\Users\KIIT0001\Desktop\projects\DeCodeX\DecodeX_VoltRide_Dataset.xlsx'

with open(r'c:\Users\KIIT0001\Desktop\projects\DeCodeX\analysis_results.txt', 'w') as f:
    sys.stdout = f
    
    try:
        ride_data = pd.read_excel(file_path, sheet_name='Ride_Level_Data')
        print("Dataset loaded successfully.")
        
        # --- TASK 1: Demand-Supply Stress Mapping ---
        print("\n--- TASK 1: Demand-Supply Stress Mapping ---")
        
        # Ride Status Breakdown
        print("\nRide Status Breakdown:")
        print(ride_data['Ride_Status'].value_counts())
        
        # Risk Mapping (City-Zone-Hour)
        ride_data['is_cancelled'] = ride_data['Ride_Status'].apply(lambda x: 1 if x == 'Cancelled' else 0)
        risk_mapping = ride_data.groupby(['City', 'Pickup_Zone', 'Hour']).agg({
            'Ride_ID': 'count',
            'is_cancelled': 'mean'
        }).rename(columns={'Ride_ID': 'Total_Requests', 'is_cancelled': 'Cancellation_Rate'})
        
        print("\nTop 10 Highest Operational Risk Windows:")
        print(risk_mapping[risk_mapping['Total_Requests'] > 5].sort_values(by='Cancellation_Rate', ascending=False).head(10))
        
        # Weather Impact
        print("\nWeather Impact on Cancellations:")
        print(ride_data.groupby('Weather')['is_cancelled'].mean().sort_values(ascending=False))

        # --- TASK 2: Driver & Battery Decomposition ---
        print("\n--- TASK 2: Driver & Battery Decomposition ---")
        
        # Battery Bins
        ride_data['Battery_Bin'] = pd.cut(ride_data['EV_Battery_%'], bins=[0, 20, 30, 40, 50, 60, 80, 100])
        print("\nCancellation Rate by Battery Level Bin:")
        print(ride_data.groupby('Battery_Bin')['is_cancelled'].mean())
        
        # Driver Availability vs Cancellation
        print("\nDriver Availability vs Cancellation Rate:")
        print(ride_data.groupby('Driver_Available')['is_cancelled'].mean())

        # --- TASK 3: Fleet Utilization Efficiency ---
        print("\n--- TASK 3: Fleet Utilization Efficiency ---")
        
        # Correlation between Charging Nearby and Status
        print("\nCharging Station Nearby vs Cancellation Rate:")
        print(ride_data.groupby('Charging_Station_Nearby')['is_cancelled'].mean())

    except Exception as e:
        print(f"Error: {e}")

sys.stdout = sys.__stdout__
print("Analysis complete. Results saved to analysis_results.txt")
