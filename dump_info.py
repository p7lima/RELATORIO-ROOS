import pandas as pd

files = [
    r"c:\Users\Nitro 5\Downloads\RELATORIO ROOS\data\DIA-A-DIA-18-25-06.xlsx",
    r"c:\Users\Nitro 5\Downloads\RELATORIO ROOS\data\DIA-A-DIA-COM-IDADE.xlsx",
    r"c:\Users\Nitro 5\Downloads\RELATORIO ROOS\data\DIA-A-DIA-CRIATIVO-18-25-06.xlsx",
    r"c:\Users\Nitro 5\Downloads\RELATORIO ROOS\data\DIA-A-DIA-POSICIONAMENTO-18-25-06.xlsx"
]

for f in files:
    print(f"--- {f} ---")
    try:
        df1 = pd.read_excel(f)
        print("Default read:")
        print(df1.head(3))
        print("Columns:")
        print(df1.columns.tolist())
    except Exception as e:
        print(e)
    try:
        df2 = pd.read_excel(f, header=2)
        print("\nRead with header=2:")
        print(df2.head(3))
        print("Columns:")
        print(df2.columns.tolist())
    except Exception as e:
        print(e)
    print("\n\n")
