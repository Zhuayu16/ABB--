@echo off
chcp 65001 >nul
echo ========================================
echo 路径切片与仿真系统启动脚本
echo ========================================
echo.

echo 正在切换到工作目录...
cd /d D:\HXJS

echo 正在激活conda环境...
call D:\software\Anaconda3\Scripts\activate.bat base
call conda activate weld

echo 正在启动路径切片与仿真系统...
python v3.py

echo.
echo 系统已退出
pause 