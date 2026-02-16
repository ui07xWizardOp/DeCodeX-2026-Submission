import pandas as pd

file_path = r'c:\Users\KIIT0001\Desktop\projects\DeCodeX\DecodeX_VoltRide_Dataset.xlsx'
try:
    ride_data = pd.read_excel(file_path, sheet_name='Ride_Level_Data')
    
    # 1. Overall stats
    print(f"Total Rows: {len(ride_data)}")
    print("\nRide Status Counts:")
    print(ride_data['Ride_Status'].value_counts())
    
    # 2. City-wise stats
    print("\nCity-wise Completion Rates:")
    city_stats = ride_data.groupby('City')['Ride_Status'].value_counts(normalize=True).unstack()
    print(city_stats)
    
    # 3. Cancellation breakdown (System, Driver, Rider)
    print("\nCancellation By breakdown:")
    print(ride_data['Cancellation_By'].value_counts())
    
    # 4. Battery analysis
    print("\nAverage Battery % for Cancelled vs Completed:")
    print(ride_data.groupby('Ride_Status')['EV_Battery_%'].mean())

    # 5. Check Response 3 claim: Hyderabad Zone 6 at 11:00 AM
    hyd_z6_11 = ride_data[(ride_data['City'] == 'Hyderabad') & (ride_data['Pickup_Zone'] == 6) & (ride_data['Hour'] == 11)]
    if not hyd_z6_11.empty:
        print(f"\nStats for Hyderabad Zone 6 at 11 AM (N={len(hyd_z6_11)}):")
        print(hyd_z6_11['Ride_Status'].value_counts(normalize=True))
    else:
        print("\nHyderabad Zone 6 at 11 AM has NO data points in Ride_Level_Data.")

    # 6. Check Mumbai Zone 1 at 10 AM
    mum_z1_10 = ride_data[(ride_data['City'] == 'Mumbai') & (ride_data['Pickup_Zone'] == 1) & (ride_data['Hour'] == 10)]
    if not mum_z1_10.empty:
        print(f"\nStats for Mumbai Zone 1 at 10 AM (N={len(mum_z1_10)}):")
        print(mum_z1_10['Ride_Status'].value_counts(normalize=True))

except Exception as e:
    print(f"Error: {e}")
