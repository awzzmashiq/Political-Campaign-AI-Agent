@echo off
echo ================================================
echo   TVKCampaignAI Web Interface Launcher
echo ================================================
echo.
echo Starting the web interface...
echo.
cd /d "%~dp0"
streamlit run app.py
pause

