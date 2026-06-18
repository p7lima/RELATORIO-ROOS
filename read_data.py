import pandas as pd
import json

files = {
    'brutos': 'DADOS-BRUTOS-07-04-até-18-06.xlsx',
    'mes': 'DADOS-DO-MÊS-07-04-até-18-06.xlsx',
    'dia': 'DADOS-DE-DIA-A-DIA-07-04-até-18-06.xlsx',
    'criativo': 'DADOS-DO-CRIATIVO-07-04-até-18-04.xlsx'
}

for name, path in files.items():
    try:
        df = pd.read_excel(path)
        print(f"--- {name} ---")
        print(df.columns.tolist())
        print(df.head(3).to_dict(orient='records'))
        print("\n")
    except Exception as e:
        print(f"Error reading {name}: {e}")
