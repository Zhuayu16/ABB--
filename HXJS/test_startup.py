#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动测试脚本
测试路径切片与仿真系统是否能正常启动
"""

import sys
import os

def test_imports():
    """测试必要的模块导入"""
    print("=" * 60)
    print("模块导入测试")
    print("=" * 60)
    
    modules = [
        ("sys", "系统模块"),
        ("os", "操作系统模块"),
        ("datetime", "日期时间模块"),
        ("json", "JSON处理模块"),
        ("time", "时间模块")
    ]
    
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - {description}")
        except ImportError as e:
            print(f"❌ {module_name} - {description}: {e}")
    
    # 测试可选模块
    optional_modules = [
        ("numpy", "数值计算"),
        ("pandas", "数据处理"),
        ("matplotlib", "图表绘制"),
        ("PyQt5", "图形界面"),
        ("trimesh", "3D网格处理"),
        ("pyvista", "3D可视化"),
        ("scipy", "科学计算")
    ]
    
    print("\n可选模块测试:")
    for module_name, description in optional_modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - {description}")
        except ImportError:
            print(f"⚠️  {module_name} - {description} (未安装)")

def test_main_program():
    """测试主程序文件"""
    print("\n" + "=" * 60)
    print("主程序文件测试")
    print("=" * 60)
    
    # 检查主程序文件是否存在
    main_file = "v3.py"
    if os.path.exists(main_file):
        print(f"✅ 主程序文件存在: {main_file}")
        
        # 检查文件大小
        file_size = os.path.getsize(main_file)
        print(f"   文件大小: {file_size:,} 字节")
        
        # 尝试读取文件头部
        try:
            with open(main_file, 'r', encoding='utf-8') as f:
                first_lines = [f.readline().strip() for _ in range(5)]
            
            print("   文件头部:")
            for i, line in enumerate(first_lines, 1):
                if line:
                    print(f"   {i}: {line}")
                    
        except Exception as e:
            print(f"   ❌ 读取文件失败: {e}")
    else:
        print(f"❌ 主程序文件不存在: {main_file}")

def test_startup_scripts():
    """测试启动脚本"""
    print("\n" + "=" * 60)
    print("启动脚本测试")
    print("=" * 60)
    
    scripts = [
        ("quick_start.bat", "快速启动脚本"),
        ("start_system.bat", "详细启动脚本"),
        ("start_system.ps1", "PowerShell启动脚本"),
        ("setup_environment.bat", "环境设置脚本")
    ]
    
    for script_name, description in scripts:
        if os.path.exists(script_name):
            file_size = os.path.getsize(script_name)
            print(f"✅ {script_name} - {description} ({file_size} 字节)")
        else:
            print(f"❌ {script_name} - {description} (不存在)")

def test_environment():
    """测试环境信息"""
    print("\n" + "=" * 60)
    print("环境信息")
    print("=" * 60)
    
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"操作系统: {sys.platform}")
    
    # 检查conda环境
    conda_env = os.environ.get('CONDA_DEFAULT_ENV', '未检测到')
    print(f"Conda环境: {conda_env}")

def test_directories():
    """测试目录结构"""
    print("\n" + "=" * 60)
    print("目录结构测试")
    print("=" * 60)
    
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    
    # 检查关键文件
    key_files = [
        "v3.py",
        "quick_start.bat",
        "start_system.bat",
        "setup_environment.bat",
        "启动说明.md",
        "受力分析功能说明.md"
    ]
    
    print("\n关键文件检查:")
    for file_name in key_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name}")

def main():
    """主测试函数"""
    print("路径切片与仿真系统 - 启动测试")
    print("测试时间:", __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # 运行所有测试
    test_imports()
    test_main_program()
    test_startup_scripts()
    test_environment()
    test_directories()
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    
    print("\n🎯 下一步操作建议:")
    print("1. 如果所有测试通过，可以尝试启动系统:")
    print("   - 双击 quick_start.bat")
    print("   - 或运行 python v3.py")
    print("2. 如果缺少依赖包，请运行:")
    print("   - setup_environment.bat")
    print("3. 如果遇到问题，请查看:")
    print("   - 启动说明.md")
    print("   - 受力分析功能说明.md")

if __name__ == "__main__":
    main() 