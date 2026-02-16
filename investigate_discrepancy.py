import pandas as pd

file_path = r'c:\Users\KIIT0001\Desktop\projects\DeCodeX\DecodeX_VoltRide_Dataset.xlsx'
ride_data = pd.read_excel(file_path, sheet_name='Ride_Level_Data')

print("Ride_Status vs Cancellation_By mapping:")
mapping = ride_data.groupby(['Ride_Status', 'Cancellation_By']).size().unstack(fill_value=0)
print(mapping)

print("\nRows where Ride_Status is Cancelled but Cancellation_By is NA or unknown:")
nan_cancels = ride_data[(ride_data['Ride_Status'] == 'Cancelled') & (ride_data['Cancellation_By'].isna() | (ride_data['Cancellation_By'] == 'NA'))]
print(f"Count: {len(nan_cancels)}")

# Check Response 3's "20.7%" system cancellation claim
# Maybe it's (System) / (Driver + System)? 
# 80 / (156 + 80) = 80 / 236 = 33% (No)
# 80 / 386? (No)
# Let's see if there are other values in Cancellation_By.
print("\nUnique values in Cancellation_By:")
print(ride_data['Cancellation_By'].unique())
