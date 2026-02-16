import sys
print("--- PART 1: DATASET INSPECTION ---")
try:
    import pandas as pd
    file_path = r'c:\Users\KIIT0001\Desktop\projects\DeCodeX\DecodeX_VoltRide_Dataset.xlsx'
    xl = pd.ExcelFile(file_path)
    print(f"Sheet names: {xl.sheet_names}")
    for sheet in xl.sheet_names:
        print(f"\n=== Sheet: {sheet} ===")
        df = xl.parse(sheet, nrows=5)
        print(f"Shape: {df.shape}")
        print(f"Columns ({len(df.columns)}): {list(df.columns)}")
        print(f"\nSample Data:")
        print(df.to_string())
        print(f"\nData Types:\n{df.dtypes}")
        # Also get full shape
        df_full = xl.parse(sheet)
        print(f"\nFull shape: {df_full.shape}")
except Exception as e:
    print(f"Error reading Excel: {e}")

print("\n\n--- PART 2: PDF EXTRACTION ---")
try:
    from PyPDF2 import PdfReader
    
    for pdf_name in ['DecodeX - Case study overview.docx.pdf', 'Supplementary Notes.docx.pdf']:
        pdf_path = rf'c:\Users\KIIT0001\Desktop\projects\DeCodeX\{pdf_name}'
        print(f"\n=== {pdf_name} ===")
        reader = PdfReader(pdf_path)
        print(f"Number of pages: {len(reader.pages)}")
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            print(f"\n--- Page {i+1} ---")
            print(text)
except Exception as e:
    print(f"Error reading PDFs: {e}")
