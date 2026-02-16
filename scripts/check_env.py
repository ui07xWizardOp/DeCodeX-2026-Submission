import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")

try:
    import pandas as pd
    print(f"Pandas Version: {pd.__version__}")
except ImportError as e:
    print(f"Pandas Import Failed: {e}")

try:
    import openpyxl
    print(f"Openpyxl Version: {openpyxl.__version__}")
except ImportError as e:
    print(f"Openpyxl Import Failed: {e}")

data_file = "DecodeX_VoltRide_Dataset.xlsx"
if os.path.exists(data_file):
    print(f"Found {data_file}")
    try:
        df = pd.read_excel(data_file, engine='openpyxl')
        print("Successfully read Excel file!")
        print(f"Columns: {list(df.columns)}")
        print(f"Shape: {df.shape}")
    except Exception as e:
        print(f"Failed to read Excel: {e}")
else:
    print(f"File not found: {data_file}")
