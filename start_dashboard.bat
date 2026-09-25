@echo off
echo =====================================================================
echo  ContractLens — Visual Contract Intelligence Dashboard (Local AI)
echo =====================================================================
echo.
echo Starting FastAPI Local AI Backend Service...
echo Serving Dashboard & API at http://localhost:8000
echo.
start http://localhost:8000
python backend_server.py
pause
