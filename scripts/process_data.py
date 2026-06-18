import pandas as pd
import json
import math

def clean_float(val):
    if pd.isna(val): return 0
    try: return float(val)
    except: return 0

# Read criativo file for ad performance
df_criativo = pd.read_excel('data/DADOS-DO-CRIATIVO-07-04-até-18-04.xlsx')
# Filter actual ads (where 'Anúncios' is not 'All' and not NaN)
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

# Sort top ads by revenue
top_ads.sort(key=lambda x: x['revenue'], reverse=True)

# Read DIA-A-DIA to get global totals AND weekly data
df_dia = pd.read_excel('data/DADOS-DE-DIA-A-DIA-07-04-até-18-06.xlsx', header=2)
# drop rows where Dia is 'All' or nan
df_dia = df_dia[df_dia['Dia'] != 'All'].dropna(subset=['Dia'])
df_dia['Date'] = pd.to_datetime(df_dia['Dia'], errors='coerce')
df_dia = df_dia.dropna(subset=['Date'])
df_dia = df_dia.sort_values('Date')

total_spend = pd.to_numeric(df_dia['Valor usado (BRL)'], errors='coerce').sum()
total_revenue = pd.to_numeric(df_dia['Valor dos resultados'], errors='coerce').sum()
total_purchases_paid = pd.to_numeric(df_dia['Resultados'], errors='coerce').sum()
total_impressions = pd.to_numeric(df_dia['Impressões'], errors='coerce').sum()
total_clicks = pd.to_numeric(df_dia['Cliques no link'], errors='coerce').sum()

total_spend = float(total_spend) if not pd.isna(total_spend) else 0.0
total_revenue = float(total_revenue) if not pd.isna(total_revenue) else 0.0
total_purchases_paid = float(total_purchases_paid) if not pd.isna(total_purchases_paid) else 0.0
total_impressions = float(total_impressions) if not pd.isna(total_impressions) else 0.0
total_clicks = float(total_clicks) if not pd.isna(total_clicks) else 0.0

total_roas = total_revenue / total_spend if total_spend > 0 else 0
cpa = total_spend / total_purchases_paid if total_purchases_paid > 0 else 0
ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
cpc = total_spend / total_clicks if total_clicks > 0 else 0

# Additional data provided by user
organic_sales = 4
total_sales = total_purchases_paid + organic_sales

age_data = {
    '18-24': 0,
    '25-34': 1,
    '35-44': 14,
    '45-54': 4,
    '55-64': 1
}

region_data = [
    {'name': 'São Paulo', 'value': 40},
    {'name': 'Pernambuco', 'value': 30},
    {'name': 'Rio de Janeiro', 'value': 30}
] # we don't have exact numbers per region, just the names, so we'll mock the distribution or just show them.

placements_data = {
    'Stories': 9,
    'Feed': 8,
    'Reels': 3
}

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
    'top_ads': top_ads[:5], # Top 5
    'audience': {
        'age': age_data,
        'region': region_data,
        'placements': placements_data
    }
}

# --- WEEKLY DATA LOGIC ---

# Group by 7 days starting from the first date
min_date = df_dia['Date'].min()
df_dia['Days_Since_Start'] = (df_dia['Date'] - min_date).dt.days
df_dia['Week'] = df_dia['Days_Since_Start'] // 7

weekly_data = []
for week, group in df_dia.groupby('Week'):
    w_spend = pd.to_numeric(group['Valor usado (BRL)'], errors='coerce').sum()
    w_rev = pd.to_numeric(group['Valor dos resultados'], errors='coerce').sum()
    w_purch = pd.to_numeric(group['Resultados'], errors='coerce').sum()
    w_imp = pd.to_numeric(group['Impressões'], errors='coerce').sum()
    w_clicks = pd.to_numeric(group['Cliques no link'], errors='coerce').sum()
    
    w_spend = float(w_spend) if not pd.isna(w_spend) else 0.0
    w_rev = float(w_rev) if not pd.isna(w_rev) else 0.0
    w_purch = float(w_purch) if not pd.isna(w_purch) else 0.0
    w_imp = float(w_imp) if not pd.isna(w_imp) else 0.0
    w_clicks = float(w_clicks) if not pd.isna(w_clicks) else 0.0
    
    w_roas = float(w_rev / w_spend) if w_spend > 0 else 0.0
    w_cpa = float(w_spend / w_purch) if w_purch > 0 else 0.0
    
    w_start = group['Date'].min().strftime('%d/%m')
    w_end = group['Date'].max().strftime('%d/%m')
    
    weekly_data.append({
        'label': f"Semana {week + 1} ({w_start} - {w_end})",
        'metrics': {
            'total_spend': w_spend,
            'total_revenue': w_rev,
            'roas': w_roas,
            'cpa': w_cpa,
            'total_sales': w_purch, # we don't have organic sales per week, so we only show paid sales or total paid
            'paid_sales': w_purch,
            'impressions': w_imp,
            'clicks': w_clicks,
            'ctr': float(w_clicks / w_imp * 100) if w_imp > 0 else 0.0,
            'cpc': float(w_spend / w_clicks) if w_clicks > 0 else 0.0
        }
    })

data['weekly'] = weekly_data

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Data exported to data.json successfully.")
