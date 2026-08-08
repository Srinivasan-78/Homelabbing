@echo off
setlocal enabledelayedexpansion
set ZIMLIST=
for %%f in (E:\zim-assistant\Kiwix-Tools\*.zim) do set ZIMLIST=!ZIMLIST! "%%f"

start "Kiwix" cmd /k "cd /d E:\zim-assistant\Kiwix-Tools && kiwix-serve.exe --port 8080 !ZIMLIST!"
start "Backend" cmd /k "cd /d E:\zim-assistant && venv\Scripts\activate && uvicorn app:app --host 0.0.0.0 --port 8000"
start "UI" cmd /k "cd /d E:\zim-assistant && venv\Scripts\activate && streamlit run ui.py"