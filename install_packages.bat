@echo off
cd /d "%~dp0"
echo Installing Flask...
"C:\Users\JUNG\AppData\Local\Programs\Python\Python313\python.exe" -m pip install flask==2.0.1
"C:\Users\JUNG\AppData\Local\Programs\Python\Python313\python.exe" -m pip install werkzeug==2.0.1
echo Installation complete!
pause
