# 路径切片与仿真系统启动脚本 (PowerShell版本)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "路径切片与仿真系统启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "正在切换到工作目录..." -ForegroundColor Yellow
Set-Location "D:\HXJS"

Write-Host "正在激活conda环境..." -ForegroundColor Yellow
& "D:\software\Anaconda3\Scripts\activate.bat" base
conda activate weld

Write-Host "正在启动路径切片与仿真系统..." -ForegroundColor Green
python v3.py

Write-Host ""
Write-Host "系统已退出" -ForegroundColor Red
Read-Host "按任意键继续" 