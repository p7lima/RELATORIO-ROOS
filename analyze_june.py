import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Analyze overall June
total_inv = data['metrics']['total_spend']
total_fat = data['metrics']['total_revenue']
total_ven = data['metrics']['total_sales']

print(f"Overall June:")
print(f"Investimento: {total_inv:.2f}, Faturamento: {total_fat:.2f}, Vendas: {total_ven}")
print(f"ROAS: {total_fat/total_inv if total_inv else 0:.2f}")

# Filter for the week 18-06 to 25-06
start_date = '2026-06-18'
end_date = '2026-06-25'

diario = [d for d in data['Diario'] if start_date <= d['Data'] <= end_date]
criativo = [d for d in data['CriativoDiario'] if start_date <= d['Data'] <= end_date]

week_inv = sum(d['Investimento'] for d in diario)
week_fat = sum(d['Faturamento'] for d in diario)
week_ven = sum(d['Vendas'] for d in diario)

print(f"\nWeek {start_date} to {end_date}:")
print(f"Investimento: {week_inv:.2f}")
print(f"Faturamento: {week_fat:.2f}")
print(f"Vendas: {week_ven}")
print(f"ROAS: {week_fat/week_inv if week_inv > 0 else 0:.2f}")

print("\nTop Criativos (Week 18-25):")
cria_summary = {}
for c in criativo:
    name = c['Nome']
    if name not in cria_summary:
        cria_summary[name] = {'inv':0, 'fat':0, 'ven':0}
    cria_summary[name]['inv'] += c['Investimento']
    cria_summary[name]['fat'] += c['Faturamento']
    cria_summary[name]['ven'] += c['Vendas']

cria_list = [{'name': k, **v} for k, v in cria_summary.items()]
cria_list.sort(key=lambda x: x['fat'], reverse=True)
for c in cria_list:
    print(f"- {c['name'][:50]}: Inv={c['inv']:.2f}, Fat={c['fat']:.2f}, Ven={c['ven']}, ROAS={c['fat']/c['inv'] if c['inv']>0 else 0:.2f}")
