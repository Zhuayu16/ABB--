#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试STEP文件三角网格显示功能
"""

import sys
import numpy as np

def test_step_mesh_loading():
    """测试STEP文件三角网格加载功能"""
    
    # 检查pythonocc-core是否可用
    try:
        from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
        from OCC.Core.BRep import BRep_Tool
        from OCC.Core.Poly import Poly_Triangulation
        from OCC.Core.TopLoc import TopLoc_Location
        from OCC.Core.TopExp import TopExp_Explorer
        from OCC.Core.TopAbs import TopAbs_FACE
        from OCC.Extend.DataExchange import read_step_file
        print("✓ pythonocc-core 导入成功")
    except ImportError as e:
        print(f"✗ pythonocc-core 导入失败: {e}")
        return False
    
    # 创建一个简单的测试STEP文件路径
    test_file = "test_cube.step"  # 假设有这个文件
    
    try:
        # 加载STEP文件
        print(f"正在加载STEP文件: {test_file}")
        shape = read_step_file(test_file)
        print("✓ STEP文件加载成功")
        
        # 生成三角网格
        print("正在生成三角网格...")
        mesh = BRepMesh_IncrementalMesh(shape, 0.1, False, 0.1, True)
        mesh.Perform()
        
        if not mesh.IsDone():
            print("✗ 网格生成失败")
            return False
        
        print("✓ 网格生成成功")
        
        # 收集顶点和面
        all_vertices = []
        all_faces = []
        vertex_index = 0
        
        explorer = TopExp_Explorer(shape, TopAbs_FACE)
        face_count = 0
        
        while explorer.More():
            face = explorer.Current()
            face_count += 1
            
            location = TopLoc_Location()
            triangulation = BRep_Tool.Triangulation(face, location)
            
            if triangulation is not None:
                # 获取顶点
                nodes = triangulation.Nodes()
                if hasattr(nodes, 'Length'):
                    # 新版本API
                    for i in range(1, nodes.Length() + 1):
                        node = nodes.Value(i)
                        all_vertices.append([node.X(), node.Y(), node.Z()])
                else:
                    # 旧版本API
                    for i in range(nodes.Length()):
                        node = nodes.Value(i + 1)
                        all_vertices.append([node.X(), node.Y(), node.Z()])
                
                # 获取三角形
                triangles = triangulation.Triangles()
                if hasattr(triangles, 'Length'):
                    # 新版本API
                    for i in range(1, triangles.Length() + 1):
                        triangle = triangles.Value(i)
                        if hasattr(triangle, 'Get'):
                            n1, n2, n3 = triangle.Get()
                            all_faces.append([n1 - 1 + vertex_index, n2 - 1 + vertex_index, n3 - 1 + vertex_index])
                        else:
                            n1, n2, n3 = triangle.Value(1), triangle.Value(2), triangle.Value(3)
                            all_faces.append([n1 - 1 + vertex_index, n2 - 1 + vertex_index, n3 - 1 + vertex_index])
                else:
                    # 旧版本API
                    for i in range(triangles.Length()):
                        triangle = triangles.Value(i + 1)
                        n1, n2, n3 = triangle.Value(1), triangle.Value(2), triangle.Value(3)
                        all_faces.append([n1 - 1 + vertex_index, n2 - 1 + vertex_index, n3 - 1 + vertex_index])
                
                vertex_index += nodes.Length()
            
            explorer.Next()
        
        # 转换为numpy数组
        vertices = np.array(all_vertices, dtype=np.float32)
        faces = np.array(all_faces, dtype=np.int32)
        
        print(f"✓ 三角网格生成完成:")
        print(f"  - 面数: {face_count}")
        print(f"  - 顶点数: {len(vertices)}")
        print(f"  - 三角形数: {len(faces)}")
        
        # 测试PyVista显示
        try:
            import pyvista as pv
            print("✓ PyVista 导入成功")
            
            # 转换为PyVista格式
            if faces.shape[1] == 3:
                faces = np.hstack([np.full((faces.shape[0], 1), 3), faces])
            
            pv_mesh = pv.PolyData(vertices, faces)
            print("✓ PyVista网格创建成功")
            
            # 测试显示（可选）
            # plotter = pv.Plotter()
            # plotter.add_mesh(pv_mesh, color='silver', show_edges=True)
            # plotter.show()
            
        except ImportError as e:
            print(f"✗ PyVista 导入失败: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def create_test_step_file():
    """创建一个简单的测试STEP文件"""
    try:
        from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
        from OCC.Core.gp import gp_Pnt
        from OCC.Extend.DataExchange import write_step_file
        
        # 创建一个简单的立方体
        box_maker = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), 10, 10, 10)
        box = box_maker.Shape()
        
        # 保存为STEP文件
        write_step_file(box, "test_cube.step")
        print("✓ 测试STEP文件创建成功: test_cube.step")
        return True
        
    except Exception as e:
        print(f"✗ 创建测试STEP文件失败: {e}")
        return False

if __name__ == "__main__":
    print("=== STEP文件三角网格显示功能测试 ===")
    
    # 创建测试文件
    if create_test_step_file():
        # 测试加载
        if test_step_mesh_loading():
            print("\n🎉 所有测试通过！STEP文件三角网格显示功能正常。")
        else:
            print("\n❌ 测试失败！")
    else:
        print("\n❌ 无法创建测试文件！") 