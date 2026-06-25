import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def format_ptbr(value):
    return f"{value:,.2f}".translate(str.maketrans(',.', '.,'))

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Campanha | ROOS</title>
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Outfit', 'sans-serif'],
                    }},
                    colors: {{
                        brand: {{
                            DEFAULT: '#8b5cf6',
                            dark: '#6d28d9',
                            light: '#a78bfa',
                        }},
                        dark: {{
                            bg: '#0B0F19',
                            card: 'rgba(255, 255, 255, 0.03)',
                            border: 'rgba(255, 255, 255, 0.08)'
                        }}
                    }}
                }}
            }}
        }}
    </script>

    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <!-- Phosphor Icons -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>

    <style>
        body {{
            background-color: #0B0F19;
            color: #f8fafc;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(139, 92, 246, 0.15), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(56, 189, 248, 0.15), transparent 25%);
            background-attachment: fixed;
        }}
        .glass-card {{
            background: rgba(20, 25, 40, 0.6);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 1.5rem;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }}
        
        .metric-value {{
            background: linear-gradient(to right, #a78bfa, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        /* Table styling */
        table {{
            border-collapse: separate;
            border-spacing: 0;
        }}
        th {{
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }}
        tr:not(:last-child) td {{
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        }}
        
        /* Animation */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .animate-fade-in {{
            animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }}
        .delay-100 {{ animation-delay: 100ms; }}
        .delay-200 {{ animation-delay: 200ms; }}
        .delay-300 {{ animation-delay: 300ms; }}
    </style>
</head>
<body class="min-h-screen p-4 md:p-8 font-sans antialiased selection:bg-brand selection:text-white">

    <div class="max-w-7xl mx-auto space-y-8">
        
        <!-- Header -->
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 animate-fade-in">
            <div>
                <div class="flex items-center gap-3 mb-2">
                    <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-brand to-sky-400 flex items-center justify-center shadow-lg shadow-brand/20">
                        <i class="ph ph-chart-line-up text-2xl text-white"></i>
                    </div>
                    <h1 class="text-3xl md:text-4xl font-bold tracking-tight">Relatório de Desempenho</h1>
                </div>
                <p class="text-slate-400 flex items-center gap-2">
                    <i class="ph ph-calendar-blank"></i>
                    01 de Junho - 25 de Junho, 2026
                </p>
            </div>
            
            <div class="mt-4 md:mt-0 flex flex-row flex-wrap items-center gap-4">
                <div class="flex items-center gap-2">
                    <button onclick="setDateRange('month')" class="text-xs text-brand-light hover:text-white border border-brand/30 px-3 py-1.5 rounded-lg transition-colors">Este Mês</button>
                    <button onclick="setDateRange('all')" class="text-xs text-brand-light hover:text-white border border-brand/30 px-3 py-1.5 rounded-lg transition-colors">Global</button>
                </div>
                <div class="glass-card px-3 py-2 flex items-center gap-2">
                    <label class="text-xs text-slate-400 uppercase tracking-wider font-semibold">De:</label>
                    <input type="date" id="dateStart" onchange="updateDashboard()" class="bg-[#0B0F19] border border-white/10 text-brand-light text-sm rounded-lg focus:ring-brand focus:border-brand p-1.5 outline-none cursor-pointer [color-scheme:dark]">
                </div>
                <div class="glass-card px-3 py-2 flex items-center gap-2">
                    <label class="text-xs text-slate-400 uppercase tracking-wider font-semibold">Até:</label>
                    <input type="date" id="dateEnd" onchange="updateDashboard()" class="bg-[#0B0F19] border border-white/10 text-brand-light text-sm rounded-lg focus:ring-brand focus:border-brand p-1.5 outline-none cursor-pointer [color-scheme:dark]">
                </div>
            </div>
        </header>

        <!-- Top Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 animate-fade-in delay-100">
            <!-- Valor Investido -->
            <div class="glass-card p-6 relative overflow-hidden group">
                <div class="absolute -right-4 -top-4 w-24 h-24 bg-brand/10 rounded-full blur-2xl group-hover:bg-brand/20 transition-all"></div>
                <p class="text-slate-400 text-sm font-medium mb-1">Valor Investido</p>
                <h3 id="val-spend" class="text-3xl font-bold text-white mb-2">R$ {format_ptbr(data['metrics']['total_spend'])}</h3>
                <div class="flex items-center gap-2 text-sm">
                    <span class="text-slate-500">Total gasto em anúncios</span>
                </div>
            </div>

            <!-- Faturamento -->
            <div class="glass-card p-6 relative overflow-hidden group">
                <div class="absolute -right-4 -top-4 w-24 h-24 bg-sky-400/10 rounded-full blur-2xl group-hover:bg-sky-400/20 transition-all"></div>
                <p class="text-slate-400 text-sm font-medium mb-1">Faturamento Total</p>
                <h3 id="val-revenue" class="text-3xl font-bold metric-value mb-2">R$ {format_ptbr(data['metrics']['total_revenue'])}</h3>
                <div class="flex items-center gap-2 text-sm">
                    <i class="ph ph-trend-up text-emerald-400"></i>
                    <span class="text-emerald-400 font-medium">Receita gerada</span>
                </div>
            </div>

            <!-- ROAS -->
            <div class="glass-card p-6 relative overflow-hidden group">
                <div class="absolute -right-4 -top-4 w-24 h-24 bg-emerald-400/10 rounded-full blur-2xl group-hover:bg-emerald-400/20 transition-all"></div>
                <p class="text-slate-400 text-sm font-medium mb-1">ROAS Global</p>
                <h3 id="val-roas" class="text-3xl font-bold text-white mb-2">{format_ptbr(data['metrics']['roas'])}x</h3>
                <div class="flex items-center gap-2 text-sm">
                    <span class="text-slate-500">Retorno sobre investimento</span>
                </div>
            </div>

            <!-- CPA -->
            <div class="glass-card p-6 relative overflow-hidden group">
                <div class="absolute -right-4 -top-4 w-24 h-24 bg-amber-400/10 rounded-full blur-2xl group-hover:bg-amber-400/20 transition-all"></div>
                <p class="text-slate-400 text-sm font-medium mb-1">Custo por Venda (CPA)</p>
                <h3 id="val-cpa" class="text-3xl font-bold text-white mb-2">R$ {format_ptbr(data['metrics']['cpa'])}</h3>
                <div class="flex items-center gap-2 text-sm">
                    <span class="text-slate-500">Média por aquisição</span>
                </div>
            </div>

            <!-- Vendas Totais -->
            <div class="glass-card p-6 relative overflow-hidden group">
                <div class="absolute -right-4 -top-4 w-24 h-24 bg-pink-400/10 rounded-full blur-2xl group-hover:bg-pink-400/20 transition-all"></div>
                <p class="text-slate-400 text-sm font-medium mb-1">Vendas Totais</p>
                <h3 id="val-sales" class="text-3xl font-bold text-white mb-2">{int(data['metrics']['total_sales'])}</h3>
                <div class="flex items-center gap-2 text-sm">
                    <span id="val-paid-sales" class="px-2 py-0.5 rounded-md bg-brand/20 text-brand-light text-xs font-medium">{int(data['metrics']['paid_sales'])} Pagas</span>
                </div>
            </div>
        </div>

        <!-- Charts Row -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-fade-in delay-200">
            <!-- Age Chart -->
            <div class="glass-card p-6 lg:col-span-2">
                <h3 class="text-lg font-semibold mb-6 flex items-center gap-2">
                    <i class="ph ph-users text-brand-light"></i>
                    Vendas por Faixa Etária <span class="text-xs text-slate-500 font-normal ml-2">(Período Selecionado)</span>
                </h3>
                <div class="h-[300px] w-full relative">
                    <canvas id="ageChart"></canvas>
                </div>
            </div>
            
            <!-- Placements Chart -->
            <div class="glass-card p-6">
                <h3 class="text-lg font-semibold mb-6 flex items-center gap-2">
                    <i class="ph ph-device-mobile text-sky-400"></i>
                    Posicionamentos <span class="text-xs text-slate-500 font-normal ml-2">(Período Selecionado)</span>
                </h3>
                <div class="h-[300px] w-full relative flex justify-center">
                    <canvas id="placementChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Bottom Row -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-fade-in delay-300">
            <!-- Top Ads Table -->
            <div class="glass-card p-0 lg:col-span-2 overflow-hidden">
                <div class="p-6 border-b border-white/5">
                    <h3 class="text-lg font-semibold flex items-center gap-2">
                        <i class="ph ph-star text-amber-400"></i>
                        Top 5 Anúncios <span class="text-xs text-slate-500 font-normal ml-2">(Período Selecionado)</span>
                    </h3>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm">
                        <thead class="text-slate-400 bg-white/5">
                            <tr>
                                <th class="px-6 py-4 font-medium">Anúncio</th>
                                <th class="px-6 py-4 font-medium text-right">Gasto</th>
                                <th class="px-6 py-4 font-medium text-right">Vendas</th>
                                <th class="px-6 py-4 font-medium text-right">Receita</th>
                                <th class="px-6 py-4 font-medium text-right">ROAS</th>
                            </tr>
                        </thead>
                        <tbody class="text-slate-300" id="topCreativesBody">
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- Secondary Metrics -->
            <div class="glass-card p-6 flex flex-col justify-between">
                <div>
                    <h3 class="text-lg font-semibold mb-6 flex items-center gap-2">
                        <i class="ph ph-target text-pink-400"></i>
                        Métricas de Tráfego
                    </h3>
                    
                    <div class="space-y-6">
                        <div>
                            <div class="flex justify-between text-sm mb-1">
                                <span class="text-slate-400">Impressões Totais</span>
                                <span id="val-impressions" class="text-white font-medium">{int(data['metrics']['impressions']):,}</span>
                            </div>
                            <div class="w-full bg-white/5 rounded-full h-2">
                                <div class="bg-brand h-2 rounded-full" style="width: 100%"></div>
                            </div>
                        </div>
                        
                        <div>
                            <div class="flex justify-between text-sm mb-1">
                                <span class="text-slate-400">Cliques no Link</span>
                                <span id="val-clicks" class="text-white font-medium">{int(data['metrics']['clicks']):,}</span>
                            </div>
                            <div class="w-full bg-white/5 rounded-full h-2">
                                <div class="bg-sky-400 h-2 rounded-full" style="width: 75%"></div>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-4 pt-4 border-t border-white/5 mt-6">
                            <div>
                                <p class="text-xs text-slate-400 mb-1">CTR Médio</p>
                                <p id="val-ctr" class="text-xl font-semibold text-white">{format_ptbr(data['metrics']['ctr'])}%</p>
                            </div>
                            <div>
                                <p class="text-xs text-slate-400 mb-1">CPC Médio</p>
                                <p id="val-cpc" class="text-xl font-semibold text-white">R$ {format_ptbr(data['metrics']['cpc'])}</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="mt-8 p-4 rounded-xl bg-white/5 border border-white/10">
                    <p class="text-xs text-slate-400 mb-2">Principais Regiões <span class="text-xs text-slate-500 font-normal ml-1">(Visão Global)</span></p>
                    <div class="flex flex-wrap gap-2">
                        <span class="px-3 py-1 rounded-full bg-slate-800 text-xs font-medium text-slate-300 border border-slate-700">São Paulo</span>
                        <span class="px-3 py-1 rounded-full bg-slate-800 text-xs font-medium text-slate-300 border border-slate-700">Rio de Janeiro</span>
                        <span class="px-3 py-1 rounded-full bg-slate-800 text-xs font-medium text-slate-300 border border-slate-700">Pernambuco</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Insights Section -->
        <div class="mt-8 animate-fade-in delay-300">
            <h3 class="text-2xl font-bold mb-6 flex items-center gap-3">
                <i class="ph ph-lightbulb text-amber-400"></i>
                Insights e Próximos Passos
            </h3>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                
                <!-- O que funcionou -->
                <div class="glass-card relative overflow-hidden flex flex-col h-full">
                    <div class="absolute top-0 left-0 w-full h-1.5 bg-emerald-500"></div>
                    <div class="p-6 flex-1">
                        <h4 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
                            <i class="ph ph-check-circle text-emerald-400"></i>
                            O que funcionou
                        </h4>
                        <ul class="space-y-4 text-sm text-slate-300">
                            <li class="flex items-start gap-2">
                                <span class="text-emerald-400 mt-1">•</span>
                                <span>O faturamento global de Junho manteve um bom nível (ROAS geral do mês de 2,99x e receita de ~R$ 6.900).</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-emerald-400 mt-1">•</span>
                                <span>O criativo focado no Inverno ("10 - O inverno chega...") dominou a conversão da semana 18-25, puxando R$ 1.666 em vendas com ROAS de 2,45x.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-emerald-400 mt-1">•</span>
                                <span>A campanha de Remarketing continua mostrando que consegue cercar e converter os usuários que já conhecem a marca.</span>
                            </li>
                        </ul>
                    </div>
                </div>

                <!-- Gargalos -->
                <div class="glass-card relative overflow-hidden flex flex-col h-full">
                    <div class="absolute top-0 left-0 w-full h-1.5 bg-red-500"></div>
                    <div class="p-6 flex-1">
                        <h4 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
                            <i class="ph ph-warning-circle text-red-400"></i>
                            Onde está o gargalo
                        </h4>
                        <ul class="space-y-4 text-sm text-slate-300">
                            <li class="flex items-start gap-2">
                                <span class="text-red-400 mt-1">•</span>
                                <span>Houve forte desaceleração na performance entre os dias 18 e 25, onde a semana isolada fechou com ROAS de 1,46x.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-red-400 mt-1">•</span>
                                <span>A campanha de Vendas enfrentou dificuldade com os novos anúncios. Criativos como "Bioestimulação" e "i-Red" gastaram parte significativa da verba na última semana sem fechar vendas.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-red-400 mt-1">•</span>
                                <span>O custo por clique e CPA subiram consideravelmente nos dias finais, prejudicando a margem geral.</span>
                            </li>
                        </ul>
                    </div>
                </div>

                <!-- Próximas Ações -->
                <div class="glass-card relative overflow-hidden flex flex-col h-full">
                    <div class="absolute top-0 left-0 w-full h-1.5 bg-amber-500"></div>
                    <div class="p-6 flex-1">
                        <h4 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
                            <i class="ph ph-arrow-right text-amber-400"></i>
                            Próximas ações
                        </h4>
                        <ul class="space-y-4 text-sm text-slate-300">
                            <li class="flex items-start gap-2">
                                <span class="text-amber-400 mt-1">•</span>
                                <span>Desligar e/ou reduzir a verba dos anúncios de "Bioestimulação" e "i-Red" que não converteram na campanha de Vendas.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-amber-400 mt-1">•</span>
                                <span>Concentrar o esforço financeiro na narrativa de Inverno, escalando o anúncio "10" que já provou conversão.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-amber-400 mt-1">•</span>
                                <span>Continuar apostando forte na campanha de Remarketing com as peças que deram certo, empurrando a recompra.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-amber-400 mt-1">•</span>
                                <span>Testar novas angulações sobre a coleção de inverno nas campanhas de captação (topo de funil).</span>
                            </li>
                        </ul>
                    </div>
                </div>

            </div>
        </div>
        
        <footer class="py-6 mt-8 border-t border-white/5 text-center text-sm text-slate-500">
            Relatório gerado automaticamente • Dados atualizados em 25 de Junho de 2026
        </footer>
    </div>

    <!-- Chart Config -->
    <script>
        // Set Chart.js defaults for dark theme
        Chart.defaults.color = '#94a3b8';
        Chart.defaults.font.family = "'Outfit', sans-serif";
        
        const rawData = {json.dumps(data)};
        let ageChartInst = null;
        let placementChartInst = null;

        function formatPtBr(value, decimals=2) {{
            return value.toLocaleString('pt-BR', {{ minimumFractionDigits: decimals, maximumFractionDigits: decimals }});
        }}

        function updateDashboard() {{
            const startVal = document.getElementById('dateStart').value;
            const endVal = document.getElementById('dateEnd').value;
            
            if (!startVal || !endVal) return;
            
            const startDate = new Date(startVal + 'T00:00:00');
            const endDate = new Date(endVal + 'T23:59:59');
            
            let totalInv = 0;
            let totalFat = 0;
            let totalVen = 0;
            let totalImp = 0;
            let totalCli = 0;
            
            if (rawData.Diario) {{
                rawData.Diario.forEach(dayData => {{
                    const dayDate = new Date(dayData.Data + 'T12:00:00');
                    if (dayDate >= startDate && dayDate <= endDate) {{
                        totalInv += dayData.Investimento;
                        totalFat += dayData.Faturamento;
                        totalVen += dayData.Vendas;
                        totalImp += dayData.Impressoes;
                        totalCli += dayData.Cliques;
                    }}
                }});
            }}
            
            let idadeDataMap = {{}};
            let posDataMap = {{}};
            
            if (rawData.IdadeDiario) {{
                rawData.IdadeDiario.forEach(dayData => {{
                    const dayDate = new Date(dayData.Data + 'T12:00:00');
                    if (dayDate >= startDate && dayDate <= endDate) {{
                        idadeDataMap[dayData.Idade] = (idadeDataMap[dayData.Idade] || 0) + dayData.Vendas;
                    }}
                }});
            }}
            
            if (rawData.PosicionamentoDiario) {{
                rawData.PosicionamentoDiario.forEach(dayData => {{
                    const dayDate = new Date(dayData.Data + 'T12:00:00');
                    if (dayDate >= startDate && dayDate <= endDate) {{
                        posDataMap[dayData.Posicionamento] = (posDataMap[dayData.Posicionamento] || 0) + dayData.Vendas;
                    }}
                }});
            }}
            
            let criativosDataMap = {{}};
            if (rawData.CriativoDiario) {{
                rawData.CriativoDiario.forEach(dayData => {{
                    const dayDate = new Date(dayData.Data + 'T12:00:00');
                    if (dayDate >= startDate && dayDate <= endDate) {{
                        if (!criativosDataMap[dayData.Nome]) {{
                            criativosDataMap[dayData.Nome] = {{Faturamento: 0, Vendas: 0, Investimento: 0}};
                        }}
                        criativosDataMap[dayData.Nome].Faturamento += dayData.Faturamento;
                        criativosDataMap[dayData.Nome].Vendas += dayData.Vendas;
                        criativosDataMap[dayData.Nome].Investimento += dayData.Investimento;
                    }}
                }});
            }}

            let criativosArray = Object.keys(criativosDataMap).map(nome => {{
                const c = criativosDataMap[nome];
                c.Nome = nome;
                c.ROAS = c.Investimento > 0 ? c.Faturamento / c.Investimento : 0;
                return c;
            }});
            
            criativosArray.sort((a, b) => b.Vendas - a.Vendas);
            const top5 = criativosArray.slice(0, 5);
            
            const tbody = document.getElementById('topCreativesBody');
            if (tbody) {{
                tbody.innerHTML = '';
                top5.forEach((creative, i) => {{
                    const highlightBg = i === 0 ? "bg-brand/10" : "";
                    const medal = i === 0 ? "🥇 " : (i === 1 ? "🥈 " : (i === 2 ? "🥉 " : ""));
                    
                    const faturamentoStr = new Intl.NumberFormat('pt-BR', {{ style: 'currency', currency: 'BRL' }}).format(creative.Faturamento);
                    const roasStr = creative.ROAS.toFixed(2).replace('.', ',') + 'x';
                    
                    const tr = document.createElement('tr');
                    tr.className = 'hover:bg-white/5 transition-colors ' + highlightBg;
                    tr.innerHTML = `
                        <td class="px-6 py-4 font-medium text-white truncate max-w-[200px]" title="${{creative.Nome}}">${{medal}}${{creative.Nome}}</td>
                        <td class="px-6 py-4 text-right whitespace-nowrap">R$ ${{formatPtBr(creative.Investimento)}}</td>
                        <td class="px-6 py-4 text-right"><span class="bg-brand/20 text-brand-light py-1 px-2 rounded-md font-medium">${{creative.Vendas}}</span></td>
                        <td class="px-6 py-4 text-right text-emerald-400 font-medium whitespace-nowrap">${{faturamentoStr}}</td>
                        <td class="px-6 py-4 text-right font-medium">${{roasStr}}</td>
                    `;
                    tbody.appendChild(tr);
                }});
            }}
            
            if (ageChartInst) {{
                ageChartInst.data.labels = Object.keys(idadeDataMap);
                ageChartInst.data.datasets[0].data = Object.values(idadeDataMap);
                ageChartInst.update();
            }}
            
            if (placementChartInst) {{
                const filteredPosMap = Object.entries(posDataMap)
                    .filter(([pos, val]) => val > 0)
                    .sort((a, b) => b[1] - a[1]);
                
                let finalLabels = [];
                let finalData = [];
                
                if (filteredPosMap.length > 5) {{
                    finalLabels = filteredPosMap.slice(0, 5).map(e => e[0]);
                    finalData = filteredPosMap.slice(0, 5).map(e => e[1]);
                    const othersSum = filteredPosMap.slice(5).reduce((acc, curr) => acc + curr[1], 0);
                    if (othersSum > 0) {{
                        finalLabels.push('Outros');
                        finalData.push(othersSum);
                    }}
                }} else {{
                    finalLabels = filteredPosMap.map(e => e[0]);
                    finalData = filteredPosMap.map(e => e[1]);
                }}
                
                placementChartInst.data.labels = finalLabels;
                placementChartInst.data.datasets[0].data = finalData;
                
                const pieColors = ['#8b5cf6', '#38bdf8', '#f472b6', '#a78bfa', '#0ea5e9', '#fb7185'];
                placementChartInst.data.datasets[0].backgroundColor = finalLabels.map((_, i) => pieColors[i % pieColors.length]);
                placementChartInst.update();
            }}
            
            const roas = totalInv > 0 ? totalFat / totalInv : 0;
            const cpa = totalVen > 0 ? totalInv / totalVen : 0;
            const ctr = totalImp > 0 ? (totalCli / totalImp) * 100 : 0;
            const cpc = totalCli > 0 ? totalInv / totalCli : 0;
            
            document.getElementById('val-spend').innerText = 'R$ ' + formatPtBr(totalInv);
            document.getElementById('val-revenue').innerText = 'R$ ' + formatPtBr(totalFat);
            document.getElementById('val-roas').innerText = formatPtBr(roas) + 'x';
            document.getElementById('val-cpa').innerText = 'R$ ' + formatPtBr(cpa);
            document.getElementById('val-sales').innerText = totalVen;
            document.getElementById('val-paid-sales').innerText = totalVen + ' Pagas';
            document.getElementById('val-impressions').innerText = Math.round(totalImp).toLocaleString('pt-BR');
            document.getElementById('val-clicks').innerText = Math.round(totalCli).toLocaleString('pt-BR');
            document.getElementById('val-ctr').innerText = formatPtBr(ctr) + '%';
            document.getElementById('val-cpc').innerText = 'R$ ' + formatPtBr(cpc);
        }}

        function setDateRange(type) {{
            if (!rawData.Diario || rawData.Diario.length === 0) return;
            const firstDate = rawData.Diario[0].Data;
            const lastDate = rawData.Diario[rawData.Diario.length - 1].Data;
            
            if (type === 'all') {{
                document.getElementById('dateStart').value = firstDate;
                document.getElementById('dateEnd').value = lastDate;
            }} else if (type === 'month') {{
                const lastDateObj = new Date(lastDate + 'T12:00:00');
                const year = lastDateObj.getFullYear();
                const month = String(lastDateObj.getMonth() + 1).padStart(2, '0');
                const startOfMonth = `${{year}}-${{month}}-01`;
                const lastDay = new Date(year, lastDateObj.getMonth() + 1, 0).getDate();
                const endOfMonth = `${{year}}-${{month}}-${{lastDay}}`;
                
                document.getElementById('dateStart').value = startOfMonth;
                document.getElementById('dateEnd').value = endOfMonth;
            }}
            updateDashboard();
        }}

        if (rawData.Diario && rawData.Diario.length > 0) {{
            document.getElementById('dateStart').value = rawData.Diario[0].Data;
            document.getElementById('dateEnd').value = rawData.Diario[rawData.Diario.length - 1].Data;
        }}

        const ageCtx = document.getElementById('ageChart').getContext('2d');
        const ageGradient = ageCtx.createLinearGradient(0, 0, 0, 400);
        ageGradient.addColorStop(0, 'rgba(139, 92, 246, 0.8)');
        ageGradient.addColorStop(1, 'rgba(139, 92, 246, 0.1)');

        ageChartInst = new Chart(ageCtx, {{
            type: 'bar',
            data: {{
                labels: [],
                datasets: [{{
                    label: 'Vendas por Idade',
                    data: [],
                    backgroundColor: ageGradient,
                    borderColor: '#8b5cf6',
                    borderWidth: 1,
                    borderRadius: 6,
                    barPercentage: 0.6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleFont: {{ size: 14 }},
                        bodyFont: {{ size: 14 }},
                        padding: 12,
                        cornerRadius: 8,
                        displayColors: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{
                            color: 'rgba(255, 255, 255, 0.05)',
                            drawBorder: false
                        }},
                        ticks: {{ stepSize: 2 }}
                    }},
                    x: {{
                        grid: {{ display: false, drawBorder: false }}
                    }}
                }}
            }}
        }});

        const placementCtx = document.getElementById('placementChart').getContext('2d');
        placementChartInst = new Chart(placementCtx, {{
            type: 'doughnut',
            data: {{
                labels: [],
                datasets: [{{
                    data: [],
                    backgroundColor: [],
                    borderWidth: 0,
                    hoverOffset: 4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 20,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }}
                    }},
                    tooltip: {{
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        padding: 12,
                        cornerRadius: 8
                    }}
                }}
            }}
        }});

        updateDashboard();
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Relatorio gerado: index.html")
