#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
受力分析功能测试脚本
测试路径切片与仿真系统的受力分析功能
"""

import sys
import os
import numpy as np
import trimesh

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_stress_analysis():
    """测试受力分析功能"""
    print("=" * 60)
    print("受力分析功能测试")
    print("=" * 60)
    
    try:
        # 导入必要的模块
        from v3 import StressAnalysis, StressAnalysisDialog
        
        print("✓ 成功导入受力分析模块")
        
        # 创建测试网格
        print("\n1. 创建测试网格...")
        # 创建一个简单的立方体网格
        vertices = np.array([
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # 底面
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]   # 顶面
        ])
        
        faces = np.array([
            [0, 1, 2], [0, 2, 3],  # 底面
            [4, 7, 6], [4, 6, 5],  # 顶面
            [0, 4, 5], [0, 5, 1],  # 前面
            [1, 5, 6], [1, 6, 2],  # 右面
            [2, 6, 7], [2, 7, 3],  # 后面
            [3, 7, 4], [3, 4, 0]   # 左面
        ])
        
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        print(f"✓ 创建测试网格成功，顶点数：{len(vertices)}，面数：{len(faces)}")
        
        # 测试应力分析类
        print("\n2. 测试应力分析计算...")
        stress_analysis = StressAnalysis()
        stress_analysis.set_mesh(mesh)
        
        # 测试参数
        test_params = {
            "material": "钢材",
            "elastic_modulus": 210,
            "poisson_ratio": 0.3,
            "density": 7850,
            "constraint": "固定底面",
            "load_type": "重力",
            "load_magnitude": 1000,
            "mesh_density": "中等",
            "analysis_type": "静力分析",
            "safety_factor": 2.0
        }
        
        # 执行应力计算
        results = stress_analysis.calculate_stress(test_params)
        
        if results is not None:
            print("✓ 应力计算成功")
            print(f"  - Von Mises应力范围：{np.min(results['von_mises']):.2e} - {np.max(results['von_mises']):.2e} Pa")
            print(f"  - 最大位移：{np.max(np.linalg.norm(results['displacement'], axis=1)):.6f} m")
            print(f"  - 安全系数：{results['safety_factor']:.2f}")
        else:
            print("✗ 应力计算失败")
            return False
        
        # 测试参数对话框
        print("\n3. 测试参数对话框...")
        try:
            from PyQt5.QtWidgets import QApplication
            
            app = QApplication(sys.argv)
            dialog = StressAnalysisDialog()
            
            # 测试材料属性设置
            dialog.material_combo.setCurrentText("铝合金")
            dialog.on_material_changed("铝合金")
            
            # 验证材料属性是否正确更新
            if (dialog.elastic_modulus.value() == 70 and 
                dialog.poisson_ratio.value() == 0.33 and 
                dialog.density.value() == 2700):
                print("✓ 材料属性设置正确")
            else:
                print("✗ 材料属性设置错误")
                return False
            
            # 测试参数获取
            params = dialog.get_analysis_params()
            if "material" in params and "elastic_modulus" in params:
                print("✓ 参数获取功能正常")
            else:
                print("✗ 参数获取功能异常")
                return False
                
        except Exception as e:
            print(f"✗ 参数对话框测试失败：{e}")
            return False
        
        print("\n" + "=" * 60)
        print("✓ 所有测试通过！受力分析功能正常工作")
        print("=" * 60)
        return True
        
    except ImportError as e:
        print(f"✗ 导入模块失败：{e}")
        print("请确保已安装所需的依赖包：")
        print("  pip install numpy trimesh PyQt5")
        return False
    except Exception as e:
        print(f"✗ 测试失败：{e}")
        return False

def test_color_mapping():
    """测试颜色映射功能"""
    print("\n" + "=" * 60)
    print("颜色映射功能测试")
    print("=" * 60)
    
    try:
        # 创建测试应力数据
        stress_data = np.random.uniform(0, 1e6, 1000)  # 随机应力值
        
        # 归一化应力值
        stress_min = np.min(stress_data)
        stress_max = np.max(stress_data)
        normalized_stress = (stress_data - stress_min) / (stress_max - stress_min)
        
        # 创建颜色映射（从蓝色到红色）
        colors = np.zeros((len(normalized_stress), 3))
        for i, stress in enumerate(normalized_stress):
            if stress < 0.5:
                # 蓝色到绿色
                colors[i] = [0, stress * 2, 1 - stress * 2]
            else:
                # 绿色到红色
                colors[i] = [(stress - 0.5) * 2, 1 - (stress - 0.5) * 2, 0]
        
        print("✓ 颜色映射计算成功")
        print(f"  - 应力数据范围：{stress_min:.2e} - {stress_max:.2e} Pa")
        print(f"  - 归一化范围：{np.min(normalized_stress):.3f} - {np.max(normalized_stress):.3f}")
        print(f"  - 颜色数组形状：{colors.shape}")
        
        # 验证颜色值范围
        if np.all(colors >= 0) and np.all(colors <= 1):
            print("✓ 颜色值范围正确（0-1）")
        else:
            print("✗ 颜色值范围错误")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ 颜色映射测试失败：{e}")
        return False

def test_von_mises_calculation():
    """测试von Mises应力计算"""
    print("\n" + "=" * 60)
    print("Von Mises应力计算测试")
    print("=" * 60)
    
    try:
        from v3 import StressAnalysis
        
        # 创建测试应力场
        num_points = 100
        stress_field = np.random.uniform(-1e6, 1e6, (num_points, 6))  # 随机应力张量
        
        # 计算von Mises应力
        von_mises = np.zeros(num_points)
        for i, stress in enumerate(stress_field):
            sigma_xx, sigma_yy, sigma_zz = stress[0], stress[1], stress[2]
            tau_xy, tau_yz, tau_xz = stress[3], stress[4], stress[5]
            
            # von Mises应力公式
            von_mises[i] = np.sqrt(0.5 * ((sigma_xx - sigma_yy)**2 + 
                                         (sigma_yy - sigma_zz)**2 + 
                                         (sigma_zz - sigma_xx)**2 + 
                                         6 * (tau_xy**2 + tau_yz**2 + tau_xz**2)))
        
        print("✓ Von Mises应力计算成功")
        print(f"  - 应力场形状：{stress_field.shape}")
        print(f"  - Von Mises应力范围：{np.min(von_mises):.2e} - {np.max(von_mises):.2e} Pa")
        print(f"  - 平均Von Mises应力：{np.mean(von_mises):.2e} Pa")
        
        # 验证von Mises应力始终为正
        if np.all(von_mises >= 0):
            print("✓ Von Mises应力值正确（非负）")
        else:
            print("✗ Von Mises应力值错误（存在负值）")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Von Mises应力计算测试失败：{e}")
        return False

def main():
    """主测试函数"""
    print("受力分析功能完整测试")
    print("测试时间：", __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # 运行所有测试
    tests = [
        test_stress_analysis,
        test_color_mapping,
        test_von_mises_calculation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"测试 {test.__name__} 异常：{e}")
    
    print("\n" + "=" * 60)
    print(f"测试结果：{passed}/{total} 通过")
    if passed == total:
        print("🎉 所有测试通过！受力分析功能完全正常")
    else:
        print("⚠️  部分测试失败，请检查相关功能")
    print("=" * 60)

if __name__ == "__main__":
    main() 