# Relatório de Campanha - ROOS Dashboard

Este repositório contém a lógica e o front-end do Dashboard de performance de Tráfego Pago da ROOS.

## Como funciona?
O dashboard é um arquivo estático (`index.html`) alimentado pelos dados JSON consolidados (`data.json`).
Todo o processo de leitura e cálculos das planilhas brutas é automatizado através de scripts em Python.

## Como atualizar o Relatório (Semanal/Mensal)

1. **Baixe as planilhas** atualizadas de anúncios (apenas **DIA-A-DIA** e **CRIATIVOS**) e cole dentro da pasta `data/`. Você pode apagar as planilhas de Mês e Brutos se quiser, não precisamos mais delas!
   - *Atenção: O `.gitignore` está configurado para não subir as planilhas para o GitHub, preservando os dados da cliente.*
2. Dê **dois cliques** no arquivo `update.bat`.
   - Ele irá rodar os scripts (`scripts/process_data.py` e `scripts/generate_html.py`).
   - O arquivo `index.html` e `data.json` serão atualizados automaticamente na sua pasta.
3. Suba as alterações para o GitHub:
   ```bash
   git add .
   git commit -m "feat: atualiza dados do relatorio"
   git push origin main
   ```
4. A **Vercel** fará o deploy automático e o link da sua cliente será atualizado!

## Estrutura do Projeto
- `data/` -> Coloque as planilhas brutas aqui (protegido pelo .gitignore).
- `scripts/` -> Códigos Python que geram o relatório.
- `index.html` -> Arquivo principal do site.
- `update.bat` -> Automação para atualizar os dados no Windows.
