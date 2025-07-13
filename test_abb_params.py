#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ABB机械臂专业参数配置功能测试脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_abb_params():
    """测试ABB参数配置功能"""
    try:
        from PyQt5.QtWidgets import QApplication
        from v3 import ABBParamDialog
        
        # 创建应用程序
        app = QApplication(sys.argv)
        
        # 创建ABB参数对话框
        dialog = ABBParamDialog()
        
        print("✅ ABB参数配置功能测试启动成功！")
        print("📋 功能说明：")
        print("   1. 基础参数：机器人型号、负载、坐标系、运动参数")
        print("   2. TCP调整：位置偏移、姿态调整、校准功能")
        print("   3. 运动控制：运动模式、路径规划、运动参数")
        print("   4. 焊接参数：工艺参数、路径参数、质量监控")
        print("   5. 安全参数：安全区域、安全功能、力限制")
        print("   6. 通信参数：网络通信、数据采集、外部设备")
        print("   7. 预设管理：加载/保存预设、重置默认")
        
        # 显示对话框
        if dialog.exec_() == dialog.Accepted:
            params = dialog.get_params()
            print("\n📊 获取到的参数：")
            for key, value in params.items():
                print(f"   {key}: {value}")
        else:
            print("\n❌ 用户取消了参数配置")
        
        print("\n🎉 测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败：{str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_abb_params() 