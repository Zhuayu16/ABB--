@echo off
chcp 65001 >nul
echo ========================================
echo 环境检查和依赖安装脚本
echo ========================================
echo.

echo 正在切换到工作目录...
cd /d D:\HXJS

echo 正在激活conda环境...
call D:\software\Anaconda3\Scripts\activate.bat base
call conda activate weld

echo.
echo 检查Python版本...
python --version

echo.
echo 检查conda环境...
conda info --envs

echo.
echo 检查已安装的包...
pip list

echo.
echo 安装/更新必要的依赖包...
echo 正在安装numpy...
pip install numpy

echo 正在安装pandas...
pip install pandas

echo 正在安装matplotlib...
pip install matplotlib

echo 正在安装PyQt5...
pip install PyQt5

echo 正在安装trimesh...
pip install trimesh

echo 正在安装pyvista...
pip install pyvista

echo 正在安装pyvistaqt...
pip install pyvistaqt

echo 正在安装scipy...
pip install scipy

echo 正在安装pyqtgraph...
pip install pyqtgraph

echo 正在安装jinja2...
pip install jinja2

echo 正在安装PIL...
pip install Pillow

echo 正在安装requests...
pip install requests

echo 正在安装networkx...
pip install networkx

echo.
echo 尝试安装pythonocc-core (可选)...
pip install pythonocc-core

echo.
echo 环境设置完成！
echo 现在可以运行 start_system.bat 或 quick_start.bat 来启动系统
echo.
pause 