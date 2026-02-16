import json
import os

FILE = "docs/assets/data/charts.json"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} does not exist!")
else:
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
        print(f"Keys in {FILE}:")
        for k in data.keys():
            print(f"- {k}")
            
        # Specific check
        if "weather_impact" in data:
            print("\nFound weather_impact!")
            print(json.dumps(data["weather_impact"], indent=2))
        else:
            print("\nERROR: weather_impact NOT FOUND!")
            
    except Exception as e:
        print(f"Error reading JSON: {e}")
