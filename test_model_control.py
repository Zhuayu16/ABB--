#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型选择和方向调整功能测试脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_model_control():
    """测试模型控制功能"""
    try:
        from PyQt5.QtWidgets import QApplication
        from v3 import MainSlicerWindow
        
        # 创建应用程序
        app = QApplication(sys.argv)
        
        # 创建主窗口
        window = MainSlicerWindow()
        window.show()
        
        print("✅ 模型控制功能测试启动成功！")
        print("📋 功能说明：")
        print("   1. 左侧控制面板包含模型选择、旋转、缩放、位置控制")
        print("   2. 点击'选择模型'按钮可以加载STL或STEP文件")
        print("   3. 使用滑块或数值输入框调整模型旋转角度")
        print("   4. 使用缩放控制调整模型大小")
        print("   5. 使用位置控制调整模型位置")
        print("   6. 快速操作按钮：重置变换、居中模型、适应视图")
        print("   7. 所有变换都是实时预览的")
        
        # 运行应用程序
        sys.exit(app.exec_())
        
    except ImportError as e:
        print(f"❌ 导入错误：{e}")
        print("请确保已安装所需的依赖包：")
        print("pip install PyQt5 pyvista trimesh numpy")
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_model_control() 