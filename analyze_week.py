import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter for the week 18-06 to 25-06
start_date = '2026-06-18'
end_date = '2026-06-25'

diario = [d for d in data['Diario'] if start_date <= d['Data'] <= end_date]
idade = [d for d in data['IdadeDiario'] if start_date <= d['Data'] <= end_date]
pos = [d for d in data['PosicionamentoDiario'] if start_date <= d['Data'] <= end_date]
criativo = [d for d in data['CriativoDiario'] if start_date <= d['Data'] <= end_date]

total_inv = sum(d['Investimento'] for d in diario)
total_fat = sum(d['Faturamento'] for d in diario)
total_ven = sum(d['Vendas'] for d in diario)
total_cli = sum(d['Cliques'] for d in diario)
total_imp = sum(d['Impressoes'] for d in diario)

print(f"Metrics {start_date} to {end_date}")
print(f"Investimento: {total_inv:.2f}")
print(f"Faturamento: {total_fat:.2f}")
print(f"Vendas: {total_ven}")
print(f"ROAS: {total_fat/total_inv if total_inv > 0 else 0:.2f}")
print(f"CPA: {total_inv/total_ven if total_ven > 0 else 0:.2f}")
print(f"CTR: {(total_cli/total_imp*100) if total_imp > 0 else 0:.2f}%")

print("\nTop Criativos (Week):")
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
for c in cria_list[:5]:
    print(f"- {c['name'][:50]}: Inv={c['inv']:.2f}, Fat={c['fat']:.2f}, Ven={c['ven']}, ROAS={c['fat']/c['inv'] if c['inv']>0 else 0:.2f}")

print("\nAge:")
age_summary = {}
for a in idade:
    age = a['Idade']
    if age not in age_summary: age_summary[age] = 0
    age_summary[age] += a['Vendas']
print(age_summary)

print("\nPosicionamentos:")
pos_summary = {}
for p in pos:
    pos_name = p['Posicionamento']
    if pos_name not in pos_summary: pos_summary[pos_name] = 0
    pos_summary[pos_name] += p['Vendas']
for k, v in sorted(pos_summary.items(), key=lambda item: item[1], reverse=True)[:5]:
    print(f"{k}: {v}")

