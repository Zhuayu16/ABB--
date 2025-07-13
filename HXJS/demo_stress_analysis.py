#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
受力分析功能演示脚本
展示路径切片与仿真系统的受力分析功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_stress_analysis():
    """演示受力分析功能"""
    print("=" * 60)
    print("路径切片与仿真系统 - 受力分析功能演示")
    print("=" * 60)
    
    print("\n🎯 功能概述")
    print("受力分析功能为路径切片与仿真系统添加了专业的结构分析能力，")
    print("用不同颜色显示模型的结构和受力情况。")
    
    print("\n🔧 主要功能")
    print("1. 专业受力分析")
    print("   - 基于有限元分析原理")
    print("   - 支持多种材料类型（钢材、铝合金、钛合金等）")
    print("   - 支持多种载荷类型（重力、压力、集中力等）")
    print("   - 支持多种约束条件（固定底面、侧面、顶面等）")
    
    print("\n2. 可视化应力分布")
    print("   - 使用jet颜色映射显示应力分布")
    print("   - 蓝色：低应力区域")
    print("   - 绿色：中等应力区域")
    print("   - 红色：高应力区域")
    print("   - 实时显示von Mises应力分布")
    
    print("\n3. 安全评估")
    print("   - 自动计算结构安全系数")
    print("   - 根据安全系数判断结构是否安全")
    print("   - 提供结构优化建议")
    
    print("\n4. 分析报告")
    print("   - 生成详细的分析报告")
    print("   - 包含应力、位移统计信息")
    print("   - 支持导出为文本文件")
    
    print("\n📋 使用方法")
    print("1. 启动路径切片与仿真系统")
    print("2. 加载3D模型（STL或STEP格式）")
    print("3. 点击'预览'标签页")
    print("4. 点击'受力分析'按钮")
    print("5. 在参数设置对话框中配置分析参数")
    print("6. 点击'开始分析'执行受力分析")
    print("7. 查看3D应力云图和分析报告")
    
    print("\n⚙️ 参数设置")
    print("材料属性：")
    print("  - 材料类型：钢材、铝合金、钛合金、不锈钢、铸铁")
    print("  - 弹性模量：1-1000 GPa")
    print("  - 泊松比：0.1-0.5")
    print("  - 密度：100-20000 kg/m³")
    
    print("\n边界条件：")
    print("  - 约束类型：固定底面、固定侧面、固定顶面、简支")
    print("  - 载荷类型：重力、压力、集中力、弯矩、扭矩、组合载荷")
    print("  - 载荷大小：0.1-10000 N")
    
    print("\n分析设置：")
    print("  - 网格密度：粗糙、中等、精细、超精细")
    print("  - 分析类型：静力分析、模态分析、热应力分析、疲劳分析")
    print("  - 安全系数：1.0-10.0")
    
    print("\n🎨 颜色显示说明")
    print("应力分布颜色映射：")
    print("  🔵 蓝色区域：低应力区域，结构安全")
    print("  🟢 绿色区域：中等应力区域，需要注意")
    print("  🔴 红色区域：高应力区域，可能存在风险")
    print("  📊 颜色条：显示应力值范围和单位")
    
    print("\n📊 分析结果")
    print("1. 应力分析结果")
    print("   - 最大Von Mises应力")
    print("   - 最小Von Mises应力")
    print("   - 平均Von Mises应力")
    print("   - 应力标准差")
    
    print("\n2. 位移分析结果")
    print("   - 最大位移")
    print("   - 平均位移")
    
    print("\n3. 安全评估")
    print("   - 计算安全系数")
    print("   - 安全状态判断")
    print("   - 优化建议")
    
    print("\n💡 应用场景")
    print("1. 结构设计：验证结构强度，优化结构设计")
    print("2. 模具分析：模具受力分析，应力集中识别")
    print("3. 机械零件：零件强度校核，应力分布分析")
    print("4. 教学演示：力学原理演示，应力分析教学")
    
    print("\n⚠️ 注意事项")
    print("1. 模型要求：模型应为封闭体，网格质量影响计算精度")
    print("2. 参数设置：材料属性应准确，载荷大小应合理")
    print("3. 结果解释：应力单位为Pa，位移单位为m")
    print("4. 局限性：使用简化的有限元算法，适用于线性弹性分析")
    
    print("\n🚀 技术特点")
    print("✅ 专业性：基于有限元分析理论，符合工程力学原理")
    print("✅ 实用性：支持多种材料类型，提供多种载荷和约束")
    print("✅ 可视化：直观的应力云图显示，清晰的颜色映射")
    print("✅ 扩展性：模块化设计，易于添加新材料和算法")
    
    print("\n" + "=" * 60)
    print("🎉 受力分析功能演示完成！")
    print("请启动路径切片与仿真系统体验完整功能。")
    print("=" * 60)

def show_material_properties():
    """显示材料属性表"""
    print("\n📋 预定义材料属性表")
    print("=" * 80)
    print(f"{'材料类型':<12} {'弹性模量(GPa)':<15} {'泊松比':<10} {'密度(kg/m³)':<15}")
    print("-" * 80)
    materials = [
        ("钢材", 210, 0.30, 7850),
        ("铝合金", 70, 0.33, 2700),
        ("钛合金", 116, 0.32, 4500),
        ("不锈钢", 200, 0.29, 8000),
        ("铸铁", 100, 0.25, 7200)
    ]
    
    for material, elastic, poisson, density in materials:
        print(f"{material:<12} {elastic:<15} {poisson:<10} {density:<15}")
    
    print("=" * 80)

def show_load_types():
    """显示载荷类型说明"""
    print("\n📋 载荷类型说明")
    print("=" * 60)
    loads = [
        ("重力", "Z轴负方向", "F = m * g", "结构自重分析"),
        ("压力", "均匀分布压力", "根据面面积分配", "流体压力、接触压力"),
        ("集中力", "模型最高点", "Z轴负方向", "点载荷分析"),
        ("弯矩", "弯曲力矩", "根据几何计算", "弯曲分析"),
        ("扭矩", "扭转力矩", "根据几何计算", "扭转分析"),
        ("组合载荷", "多种载荷组合", "叠加计算", "复杂工况分析")
    ]
    
    for load_type, direction, formula, application in loads:
        print(f"🔸 {load_type}")
        print(f"   作用方向：{direction}")
        print(f"   计算公式：{formula}")
        print(f"   适用场景：{application}")
        print()

def show_constraint_types():
    """显示约束类型说明"""
    print("\n📋 约束类型说明")
    print("=" * 60)
    constraints = [
        ("固定底面", "Z坐标最小的节点", "底座固定结构"),
        ("固定侧面", "X坐标最小和最大的节点", "侧壁固定结构"),
        ("固定顶面", "Z坐标最大的节点", "顶部固定结构"),
        ("简支", "简支边界条件", "简支梁分析"),
        ("自定义", "用户自定义约束", "特殊约束条件")
    ]
    
    for constraint, nodes, application in constraints:
        print(f"🔸 {constraint}")
        print(f"   约束节点：{nodes}")
        print(f"   适用场景：{application}")
        print()

def main():
    """主函数"""
    print("路径切片与仿真系统 - 受力分析功能演示")
    print("演示时间：", __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # 运行演示
    demo_stress_analysis()
    
    # 显示详细信息
    show_material_properties()
    show_load_types()
    show_constraint_types()
    
    print("\n🎯 下一步操作")
    print("1. 确保已安装所需依赖：")
    print("   pip install numpy trimesh PyQt5 pyvista")
    print("2. 启动路径切片与仿真系统：")
    print("   python v3.py")
    print("3. 加载模型并体验受力分析功能")

if __name__ == "__main__":
    main() 