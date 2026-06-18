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
                    07 de Abril - 18 de Junho, 2026
                </p>
            </div>
            
            <div class="glass-card px-4 py-3 flex items-center gap-4">
                <div class="flex flex-col items-end">
                    <label for="weekSelector" class="text-xs text-slate-400 uppercase tracking-wider font-semibold mb-1">Período de Análise</label>
                    <select id="weekSelector" class="bg-[#0B0F19] border border-white/10 text-white text-sm rounded-lg focus:ring-brand focus:border-brand block w-full p-2 outline-none cursor-pointer">
                        <option value="global">Visão Global (Toda a Campanha)</option>
"""
for week in data['weekly']:
    html_content += f"""                        <option value="{week['label']}">{week['label']}</option>
"""
html_content += f"""                    </select>
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
                    <span id="val-organic-sales" class="px-2 py-0.5 rounded-md bg-emerald-400/20 text-emerald-400 text-xs font-medium">{int(data['metrics']['organic_sales'])} Orgânicas</span>
                </div>
            </div>
        </div>

        <!-- Charts Row -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-fade-in delay-200">
            <!-- Age Chart -->
            <div class="glass-card p-6 lg:col-span-2">
                <h3 class="text-lg font-semibold mb-6 flex items-center gap-2">
                    <i class="ph ph-users text-brand-light"></i>
                    Vendas por Faixa Etária <span class="text-xs text-slate-500 font-normal ml-2">(Visão Global)</span>
                </h3>
                <div class="h-[300px] w-full relative">
                    <canvas id="ageChart"></canvas>
                </div>
            </div>
            
            <!-- Placements Chart -->
            <div class="glass-card p-6">
                <h3 class="text-lg font-semibold mb-6 flex items-center gap-2">
                    <i class="ph ph-device-mobile text-sky-400"></i>
                    Posicionamentos <span class="text-xs text-slate-500 font-normal ml-2">(Visão Global)</span>
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
                        Top 5 Anúncios <span class="text-xs text-slate-500 font-normal ml-2">(Visão Global)</span>
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
                        <tbody class="text-slate-300">
"""
for ad in data['top_ads']:
    html_content += f"""
                            <tr class="hover:bg-white/5 transition-colors">
                                <td class="px-6 py-4 font-medium text-white truncate max-w-[200px]" title="{ad['name']}">{ad['name']}</td>
                                <td class="px-6 py-4 text-right whitespace-nowrap">R$ {format_ptbr(ad['spend'])}</td>
                                <td class="px-6 py-4 text-right"><span class="bg-brand/20 text-brand-light py-1 px-2 rounded-md font-medium">{int(ad['purchases'])}</span></td>
                                <td class="px-6 py-4 text-right text-emerald-400 font-medium whitespace-nowrap">R$ {format_ptbr(ad['revenue'])}</td>
                                <td class="px-6 py-4 text-right font-medium">{format_ptbr(ad['roas'])}x</td>
                            </tr>
"""

html_content += f"""
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
                                <span>Campanha paga positiva com ROAS geral de 2,20x.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-emerald-400 mt-1">•</span>
                                <span>Remarketing validado: ROAS 3,95x e CPA saudável.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-emerald-400 mt-1">•</span>
                                <span>Campanhas temáticas tiveram bons sinais, principalmente Dia das Mães e Namorados.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-emerald-400 mt-1">•</span>
                                <span>Público comprador bem definido: 35-44 como faixa principal.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-emerald-400 mt-1">•</span>
                                <span>Mensagens sobre tecnologia, diferença ao vestir e bioestimulação demonstraram força.</span>
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
                                <span>345 carrinhos para 20 compras pagas: perda grande na finalização.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-red-400 mt-1">•</span>
                                <span>Junho faturou mais, mas ficou com CPA maior.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-red-400 mt-1">•</span>
                                <span>Conjunto aberto trouxe volume, porém com ROAS baixo.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-red-400 mt-1">•</span>
                                <span>Reels teve menos compras do que Stories e Feed.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-red-400 mt-1">•</span>
                                <span>Criativo campeão de volume precisa de variações para melhorar eficiência.</span>
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
                                <span>Manter remarketing ativo e testar novas provas sociais/ofertas para quem abandonou carrinho.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-amber-400 mt-1">•</span>
                                <span>Criar variações dos criativos vencedores com foco em tecnologia, resultado percebido e alto padrão.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-amber-400 mt-1">•</span>
                                <span>Priorizar 35-54 anos nos testes principais, sem eliminar aprendizado aberto.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-amber-400 mt-1">•</span>
                                <span>Revisar site/checkout: frete, prazo, formas de pagamento, Pix, parcelamento e confiança.</span>
                            </li>
                            <li class="flex items-start gap-2">
                                <span class="text-amber-400 mt-1">•</span>
                                <span>Separar campanha de escala e campanha de validação para não misturar leitura de criativo.</span>
                            </li>
                        </ul>
                    </div>
                </div>

            </div>
        </div>
        
        <footer class="py-6 mt-8 border-t border-white/5 text-center text-sm text-slate-500">
            Relatório gerado automaticamente • Dados atualizados em 18 de Junho de 2026
        </footer>
    </div>

    <!-- Chart Config -->
    <script>
        // Set Chart.js defaults for dark theme
        Chart.defaults.color = '#94a3b8';
        Chart.defaults.font.family = "'Outfit', sans-serif";
        
        const rawData = {json.dumps(data)};
        
        function formatPtBr(value, decimals=2) {{
            return value.toLocaleString('pt-BR', {{ minimumFractionDigits: decimals, maximumFractionDigits: decimals }});
        }}

        document.getElementById('weekSelector').addEventListener('change', function(e) {{
            const selected = e.target.value;
            let m;
            let organicText = "{int(data['metrics']['organic_sales'])} Orgânicas";
            let totalSalesAdd = {int(data['metrics']['organic_sales'])};

            if(selected === 'global') {{
                m = rawData.metrics;
            }} else {{
                const wData = rawData.weekly.find(w => w.label === selected);
                m = wData.metrics;
                organicText = "Sem info (Orgânico)";
                totalSalesAdd = 0;
            }}

            document.getElementById('val-spend').innerText = 'R$ ' + formatPtBr(m.total_spend);
            document.getElementById('val-revenue').innerText = 'R$ ' + formatPtBr(m.total_revenue);
            document.getElementById('val-roas').innerText = formatPtBr(m.roas) + 'x';
            document.getElementById('val-cpa').innerText = 'R$ ' + formatPtBr(m.cpa);
            document.getElementById('val-sales').innerText = Math.round(m.paid_sales + totalSalesAdd);
            document.getElementById('val-paid-sales').innerText = Math.round(m.paid_sales) + ' Pagas';
            document.getElementById('val-organic-sales').innerText = organicText;
            document.getElementById('val-impressions').innerText = Math.round(m.impressions).toLocaleString('pt-BR');
            document.getElementById('val-clicks').innerText = Math.round(m.clicks).toLocaleString('pt-BR');
            document.getElementById('val-ctr').innerText = formatPtBr(m.ctr) + '%';
            document.getElementById('val-cpc').innerText = 'R$ ' + formatPtBr(m.cpc);
        }});

        // Age Chart
        const ageCtx = document.getElementById('ageChart').getContext('2d');
        const ageGradient = ageCtx.createLinearGradient(0, 0, 0, 400);
        ageGradient.addColorStop(0, 'rgba(139, 92, 246, 0.8)');
        ageGradient.addColorStop(1, 'rgba(139, 92, 246, 0.1)');

        new Chart(ageCtx, {{
            type: 'bar',
            data: {{
                labels: Object.keys(rawData.audience.age),
                datasets: [{{
                    label: 'Vendas por Idade',
                    data: Object.values(rawData.audience.age),
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

        // Placements Chart
        const placementCtx = document.getElementById('placementChart').getContext('2d');
        new Chart(placementCtx, {{
            type: 'doughnut',
            data: {{
                labels: Object.keys(rawData.audience.placements),
                datasets: [{{
                    data: Object.values(rawData.audience.placements),
                    backgroundColor: [
                        '#8b5cf6', // Stories - Purple
                        '#38bdf8', // Feed - Sky
                        '#f472b6'  // Reels - Pink
                    ],
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
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Relatorio gerado: index.html")
