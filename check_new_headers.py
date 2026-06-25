import pandas as pd

files = [
    r"c:\Users\Nitro 5\Downloads\RELATORIO ROOS\data\DIA-A-DIA-jun-1-2026-a-jun-25-2026.xlsx",
    r"c:\Users\Nitro 5\Downloads\RELATORIO ROOS\data\DIA-A-DIA-IDADE-un-1-2026-a-jun-25-2026.xlsx",
    r"c:\Users\Nitro 5\Downloads\RELATORIO ROOS\data\DIA-A-DIA-CRIATIVO-jun-1-2026-a-jun-25-2026.xlsx",
    r"c:\Users\Nitro 5\Downloads\RELATORIO ROOS\data\DIA-A-DIA-POSICIONAMENTO-jun-1-2026-a-jun-25-2026.xlsx"
]

for f in files:
    print(f"--- {f} ---")
    try:
        df1 = pd.read_excel(f)
        print("Default read:", df1.columns.tolist()[:5])
    except Exception as e:
        print(e)
    try:
        df2 = pd.read_excel(f, header=2)
        print("Read with header=2:", df2.columns.tolist()[:5])
    except Exception as e:
        print(e)
    print("\n")
