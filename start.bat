@echo off
echo 正在安装必要的Python包...
"C:\Users\JUNG\AppData\Local\Programs\Python\Python313\python.exe" -m pip install -r requirements.txt

echo 启动文件上传网站...
"C:\Users\JUNG\AppData\Local\Programs\Python\Python313\python.exe" app.py
pause
