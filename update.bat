@echo off
echo ==========================================
echo Atualizando Relatorio ROOS...
echo ==========================================

echo [1/2] Processando planilhas da pasta data/...
python scripts\process_data.py

echo.
echo [2/2] Gerando novo index.html...
python scripts\generate_html.py

echo.
echo ==========================================
echo Atualizacao concluida com sucesso!
echo ==========================================
pause
