import pandas as pd
import json
import math

def clean_float(val):
    if pd.isna(val): return 0
    try: return float(val)
    except: return 0

# Read criativo file for ad performance (Global top ads - keep for now if needed, though we will have dynamic below)
df_criativo = pd.read_excel('data/DIA-A-DIA-CRIATIVO-jun-1-2026-a-jun-25-2026.xlsx')
ads = df_criativo[df_criativo['Anúncios'] != 'All'].dropna(subset=['Anúncios'])

top_ads = []
for _, row in ads.iterrows():
    top_ads.append({
        'name': str(row['Anúncios']),
        'spend': clean_float(row['Valor usado (BRL)']),
        'purchases': clean_float(row['Resultados']),
        'revenue': clean_float(row['Valor dos resultados']),
        'roas': clean_float(row['ROAS de resultados']),
        'cpa': clean_float(row['Custo por resultado'])
    })
top_ads.sort(key=lambda x: x['revenue'], reverse=True)

# Read DIA-A-DIA to get global totals AND daily data
df_dia = pd.read_excel('data/DIA-A-DIA-NORMALjun-1-2026-a-jun-25-2026.xlsx', header=2)
df_dia = df_dia[df_dia['Dia'] != 'All'].dropna(subset=['Dia'])
df_dia['Date'] = pd.to_datetime(df_dia['Dia'], errors='coerce')
df_dia = df_dia.dropna(subset=['Date']).sort_values('Date')

total_spend = pd.to_numeric(df_dia['Valor usado (BRL)'], errors='coerce').sum() if 'Valor usado (BRL)' in df_dia.columns else 0.0
total_revenue = pd.to_numeric(df_dia['Valor dos resultados'], errors='coerce').sum() if 'Valor dos resultados' in df_dia.columns else 0.0
total_purchases_paid = pd.to_numeric(df_dia['Resultados'], errors='coerce').sum() if 'Resultados' in df_dia.columns else 0.0
total_impressions = pd.to_numeric(df_dia['Impressões'], errors='coerce').sum() if 'Impressões' in df_dia.columns else 0.0
total_clicks = pd.to_numeric(df_dia['Cliques no link'], errors='coerce').sum() if 'Cliques no link' in df_dia.columns else 0.0

total_spend = float(total_spend) if not pd.isna(total_spend) else 0.0
total_revenue = float(total_revenue) if not pd.isna(total_revenue) else 0.0
total_purchases_paid = float(total_purchases_paid) if not pd.isna(total_purchases_paid) else 0.0
total_impressions = float(total_impressions) if not pd.isna(total_impressions) else 0.0
total_clicks = float(total_clicks) if not pd.isna(total_clicks) else 0.0

total_roas = total_revenue / total_spend if total_spend > 0 else 0
cpa = total_spend / total_purchases_paid if total_purchases_paid > 0 else 0
ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
cpc = total_spend / total_clicks if total_clicks > 0 else 0

organic_sales = 4
total_sales = total_purchases_paid + organic_sales

# Default global values (for region, which stays global)
region_data = [
    {'name': 'São Paulo', 'value': 40},
    {'name': 'Pernambuco', 'value': 30},
    {'name': 'Rio de Janeiro', 'value': 30}
]

# Process Diario
daily_data = []
for date_val, group in df_dia.groupby(df_dia['Date'].dt.date):
    inv = float(group['Valor usado (BRL)'].sum()) if 'Valor usado (BRL)' in group.columns else 0.0
    fat = float(group['Valor dos resultados'].sum()) if 'Valor dos resultados' in group.columns else 0.0
    ven = int(group['Resultados'].sum()) if 'Resultados' in group.columns else 0
    imp = int(group['Impressões'].sum()) if 'Impressões' in group.columns else 0
    cli = int(group['Cliques no link'].sum()) if 'Cliques no link' in group.columns else 0
    
    roas = round(fat / inv, 2) if inv > 0 else 0
    cpa = round(inv / ven, 2) if ven > 0 else 0
    cpc = round(inv / cli, 2) if cli > 0 else 0
    ctr = round((cli / imp) * 100, 2) if imp > 0 else 0
    
    daily_data.append({
        'Data': date_val.strftime('%Y-%m-%d'),
        'Investimento': inv,
        'Faturamento': fat,
        'Vendas': ven,
        'Impressoes': imp,
        'Cliques': cli,
        'ROAS': roas,
        'CPA': cpa,
        'CPC': cpc,
        'CTR': ctr
    })

# Process Idade Daily
try:
    df_idade = pd.read_excel('data/DIA-A-DIA-IDADE-un-1-2026-a-jun-25-2026.xlsx', skiprows=2)
    idade_cols = df_idade.columns
    i_ven = [c for c in idade_cols if 'Resultados' in str(c) and 'Tipo' not in str(c) and 'ROAS' not in str(c) and 'Custo' not in str(c) and c != 'Resultados (iniciais)']
    col_vendas_idade = i_ven[0] if i_ven else 'Resultados'
    
    df_idade['Dia'] = df_idade['Dia'].ffill()
    df_idade['Idade'] = df_idade['Idade'].ffill()
    df_idade = df_idade[df_idade['Idade'].notna()]
    df_idade = df_idade[~df_idade['Idade'].astype(str).str.contains('All|Total', case=False)]
    df_idade['Dia_str'] = df_idade['Dia'].astype(str)
    df_idade = df_idade[df_idade['Dia_str'].str.match(r'\d{4}-\d{2}-\d{2}', na=False)].copy()
    
    df_idade['Dia'] = pd.to_datetime(df_idade['Dia'])
    df_idade[col_vendas_idade] = pd.to_numeric(df_idade[col_vendas_idade], errors='coerce').fillna(0)
    
    idade_agg = df_idade.groupby(['Dia', 'Idade'])[col_vendas_idade].sum().reset_index()
    idade_diario = []
    for _, row in idade_agg.iterrows():
        idade_diario.append({
            'Data': row['Dia'].strftime('%Y-%m-%d'),
            'Idade': str(row['Idade']),
            'Vendas': int(row[col_vendas_idade])
        })
except Exception as e:
    print("Erro ao processar Idade:", e)
    idade_diario = []

# Process Posicionamento Daily
try:
    df_pos = pd.read_excel('data/DIA-A-DIA-POSICIONAMENTO-jun-1-2026-a-jun-25-2026.xlsx', skiprows=2)
    pos_cols = df_pos.columns
    p_ven = [c for c in pos_cols if 'Resultados' in str(c) and 'Tipo' not in str(c) and 'ROAS' not in str(c) and 'Custo' not in str(c) and c != 'Resultados (iniciais)']
    col_vendas_pos = p_ven[0] if p_ven else 'Resultados'
    
    df_pos['Dia'] = df_pos['Dia'].ffill()
    df_pos = df_pos[df_pos['Posicionamento'].notna()]
    df_pos = df_pos[~df_pos['Posicionamento'].astype(str).str.contains('All|Total', case=False)]
    df_pos['Dia_str'] = df_pos['Dia'].astype(str)
    df_pos = df_pos[df_pos['Dia_str'].str.match(r'\d{4}-\d{2}-\d{2}', na=False)].copy()
    
    df_pos['Dia'] = pd.to_datetime(df_pos['Dia'])
    df_pos[col_vendas_pos] = pd.to_numeric(df_pos[col_vendas_pos], errors='coerce').fillna(0)
    
    pos_agg = df_pos.groupby(['Dia', 'Posicionamento'])[col_vendas_pos].sum().reset_index()
    pos_diario = []
    for _, row in pos_agg.iterrows():
        pos_diario.append({
            'Data': row['Dia'].strftime('%Y-%m-%d'),
            'Posicionamento': str(row['Posicionamento']),
            'Vendas': int(row[col_vendas_pos])
        })
except Exception as e:
    print("Erro ao processar Posicionamentos:", e)
    pos_diario = []

# Process Criativo Daily
try:
    df_criativo_diario = pd.read_excel('data/DIA-A-DIA-CRIATIVO-jun-1-2026-a-jun-25-2026.xlsx')
    criativo_diario_cols = df_criativo_diario.columns
    
    col_cria = [c for c in criativo_diario_cols if 'Anúncio' in str(c) or 'Anuncio' in str(c) or 'Anncio' in str(c)]
    col_cria_name = col_cria[0] if col_cria else 'Anúncios'
    
    c_inv = [c for c in criativo_diario_cols if 'Valor usado' in str(c)]
    col_c_inv = c_inv[0] if c_inv else 'Valor usado (BRL)'
    
    c_fat = [c for c in criativo_diario_cols if 'Valor dos resultados' in str(c)]
    col_c_fat = c_fat[0] if c_fat else 'Valor dos resultados'
    
    c_ven = [c for c in criativo_diario_cols if 'Resultados' in str(c) and 'Tipo' not in str(c) and 'ROAS' not in str(c) and 'Custo' not in str(c) and c != 'Resultados (iniciais)']
    col_c_ven = c_ven[0] if c_ven else 'Resultados'
    
    df_criativo_diario = df_criativo_diario[~df_criativo_diario[col_cria_name].astype(str).str.contains('All|Total', case=False)]
    df_criativo_diario['Dia_str'] = df_criativo_diario['Dia'].astype(str)
    df_criativo_diario = df_criativo_diario[df_criativo_diario['Dia_str'].str.match(r'\d{4}-\d{2}-\d{2}', na=False)].copy()
    
    df_criativo_diario['Dia'] = pd.to_datetime(df_criativo_diario['Dia'])
    df_criativo_diario[col_c_inv] = pd.to_numeric(df_criativo_diario[col_c_inv], errors='coerce').fillna(0)
    df_criativo_diario[col_c_fat] = pd.to_numeric(df_criativo_diario[col_c_fat], errors='coerce').fillna(0)
    df_criativo_diario[col_c_ven] = pd.to_numeric(df_criativo_diario[col_c_ven], errors='coerce').fillna(0)
    
    cria_agg = df_criativo_diario.groupby(['Dia', col_cria_name])[[col_c_inv, col_c_fat, col_c_ven]].sum().reset_index()
    criativos_diario = []
    for _, row in cria_agg.iterrows():
        criativos_diario.append({
            'Data': row['Dia'].strftime('%Y-%m-%d'),
            'Nome': str(row[col_cria_name]),
            'Investimento': float(row[col_c_inv]),
            'Faturamento': float(row[col_c_fat]),
            'Vendas': int(row[col_c_ven])
        })
except Exception as e:
    print("Erro ao processar Criativos Diario:", e)
    criativos_diario = []

data = {
    'metrics': {
        'total_spend': float(total_spend),
        'total_revenue': float(total_revenue),
        'roas': float(total_roas),
        'cpa': float(cpa),
        'total_sales': float(total_sales),
        'paid_sales': float(total_purchases_paid),
        'organic_sales': organic_sales,
        'impressions': float(total_impressions),
        'clicks': float(total_clicks),
        'ctr': float(ctr),
        'cpc': float(cpc)
    },
    'top_ads': top_ads[:5], # Keep legacy as fallback
    'audience': {
        'region': region_data,
    },
    'Diario': daily_data,
    'IdadeDiario': idade_diario,
    'PosicionamentoDiario': pos_diario,
    'CriativoDiario': criativos_diario
}

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Data exported to data.json successfully.")
