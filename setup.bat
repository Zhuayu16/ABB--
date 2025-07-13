@echo off
cd /d D:\software\Anaconda3\Scripts
call activate base
call conda activate weld
call conda install -c conda-forge pythonocc-core -y
cd /d D:\HXJS
python v3.py
pause