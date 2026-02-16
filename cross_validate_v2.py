import pandas as pd

file_path = r'c:\Users\KIIT0001\Desktop\projects\DeCodeX\DecodeX_VoltRide_Dataset.xlsx'
ride_data = pd.read_excel(file_path, sheet_name='Ride_Level_Data')

def get_stats(city, zone, hour):
    subset = ride_data[(ride_data['City'] == city) & (ride_data['Pickup_Zone'] == zone) & (ride_data['Hour'] == hour)]
    if subset.empty:
        return f"{city} Z{zone} H{hour}: NO DATA"
    total = len(subset)
    cancelled = len(subset[subset['Ride_Status'] == 'Cancelled'])
    rate = cancelled / total
    return f"{city} Z{zone} H{hour}: N={total}, Cancelled={cancelled}, Rate={rate:.2%}"

print(get_stats('Mumbai', 1, 10))
print(get_stats('Hyderabad', 6, 11))
print(get_stats('Hyderabad', 7, 7))

print("\nCancellation_By Counts:")
print(ride_data['Cancellation_By'].value_counts().to_dict())

print("\nOverall Status:")
print(ride_data['Ride_Status'].value_counts().to_dict())
