@echo off
cls
echo ================================================
echo   TVKCampaignAI - Web Interface Launcher
echo ================================================
echo.
echo Starting the correct app...
echo.
cd /d "%~dp0"
echo Current directory: %CD%
echo.
echo Launching Streamlit app...
echo.
streamlit run app.py
echo.
echo App closed. Press any key to exit...
pause >nul

