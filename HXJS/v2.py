import sys
import numpy as np
import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QSlider, QLabel, QComboBox, QPushButton, 
                            QGroupBox, QSplitter, QMessageBox, QFrame,
                            QGridLayout, QStackedWidget, QProgressBar, QStatusBar, 
                            QTextEdit, QScrollBar, QScrollArea, QFormLayout,
                            QTabWidget, QTabBar, QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem,
                            QDoubleSpinBox, QSpinBox, QMenuBar, QDialog)  # 新增QDialog
from PyQt5.QtCore import (
    Qt, 
    QTimer, 
    QThread, 
    pyqtSignal, 
    QObject, 
    QPropertyAnimation, 
    QEasingCurve, 
    pyqtSlot
)
from PyQt5.QtGui import QColor, QPalette, QFont, QPainter, QPen, QBrush, QLinearGradient, QIcon, QPixmap, QImage
import matplotlib.pyplot as plt
import matplotlib.cm as cm  # 新增：导入颜色映射模块
# 添加缺失的导入
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
import requests
# 添加缺失的导入
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# 新增：导入字体管理模块
import matplotlib.font_manager as font_manager
# 导入Figure类
from matplotlib.figure import Figure  # 新增：解决Figure未定义问题
from PIL import Image
import os
from http import HTTPStatus
try:
    from dashscope import Application
except ImportError:
    Application = None  # 若未安装dashscope，避免报错
import csv  # 新增：用于知识库导出
import pyqtgraph as pg
# ========== PyQt界面集成 ==========
# 替换pyqtgraph.opengl为PyVista
import pyvista as pv
from pyvistaqt import QtInteractor
import networkx as nx
from jinja2 import Template
# pythonocc-core为可选依赖，避免导入报错
OCC_AVAILABLE = False
try:
    from importlib import util
    if util.find_spec('OCC.Core.STEPControl') and util.find_spec('OCC.Core.IFSelect') and util.find_spec('OCC.Extend.DataExchange'):
        from OCC.Core.STEPControl import STEPControl_Reader
        from OCC.Core.IFSelect import IFSelect_RetDone
        from OCC.Extend.DataExchange import read_step_file
        OCC_AVAILABLE = True
except Exception:
    OCC_AVAILABLE = False

# 设置 matplotlib 中文显示 - 简化字体设置
plt.rcParams["font.family"] = ["Misans"]  # 设置字体为Misans"]  # 只保留最常见的中文字体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

class Communicate(QObject):
    """信号通信类，用于跨组件传递数据"""
    prediction_updated = pyqtSignal(float, float)  # 电压, 预测值
    optimize_updated = pyqtSignal(float, float, float)  # 电压, 送丝速度, 质量值
    path_selected = pyqtSignal(str, str)  # 路径, 材料

class CustomFigureCanvas(FigureCanvas):
    """自定义Matplotlib画布，增强绘图功能"""
    def __init__(self, parent=None, width=5, height=4, dpi=100, fig=None):
        if fig is None:
            self.fig = Figure(figsize=(width, height), dpi=dpi)
        else:
            self.fig = fig
        self.axes = self.fig.add_subplot(111)
        super(CustomFigureCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.fig.tight_layout()
        
    def update_style(self):
        """更新图表样式，使其更符合工业风格"""
        self.axes.set_facecolor('#1E1E1E')
        self.fig.patch.set_facecolor('#1E1E1E')
        self.axes.tick_params(axis='both', colors='#CCCCCC')
        self.axes.spines['bottom'].set_color('#4A4A4A')
        self.axes.spines['top'].set_color('#4A4A4A')
        self.axes.spines['left'].set_color('#4A4A4A')
        self.axes.spines['right'].set_color('#4A4A4A')
        
        # 设置字体为Misans
        font_properties = {'family':'Misans', 'color': '#FFFFFF', 'size': 10}
        for text in self.axes.texts:
            text.set_fontproperties(font_manager.FontProperties(family='Misans'))  # 修改：统一字体
            
        # 设置网格线颜色
        for line in self.axes.get_xgridlines() + self.axes.get_ygridlines():
            line.set_color('#3A3A3A')

class PredictionChart(CustomFigureCanvas):
    """预测结果实时折线图，增强版"""
    def __init__(self, *args, **kwargs):
        super(PredictionChart, self).__init__(*args, **kwargs)
        self.times = []
        self.values = []
        self.voltage_values = []  # 存储电压值用于颜色映射
        
        self.axes.set_title('焊接质量预测趋势', color='#FFFFFF')
        self.axes.set_xlabel('时间', color='#CCCCCC')
        self.axes.set_ylabel('质量评分 (0-100)', color='#CCCCCC')
        self.axes.grid(True, linestyle='--', alpha=0.5, color='#3A3A3A')
        self.axes.set_ylim(0, 100)
        
        # 质量阈值线
        self.threshold_line = self.axes.axhline(y=80, color='#FF4500', linestyle='--', alpha=0.7)
        
        # 质量等级区域
        self.axes.axhspan(0, 70, alpha=0.1, color='#FF4500')  # 不合格区域
        self.axes.axhspan(70, 85, alpha=0.1, color='#FF9900')  # 良好区域
        self.axes.axhspan(85, 100, alpha=0.1, color='#32CD32')  # 优秀区域
        
        # 初始空线
        self.line, = self.axes.plot([], [], 'o-', linewidth=2, markersize=6)
        
        # 添加图例
        self.axes.legend(['质量评分', '质量阈值'], loc='upper right', facecolor='#2A2A2A', edgecolor='#4A4A4A', labelcolor='#FFFFFF')
        
        # 应用样式更新
        self.update_style()
        
    def update_plot(self, voltage, value):
        """更新图表数据"""
        now = datetime.now()
        self.times.append(now)
        self.values.append(value)
        self.voltage_values.append(voltage)
        
        # 只保留最近20个数据点
        if len(self.times) > 20:
            self.times = self.times[-20:]
            self.values = self.values[-20:]
            self.voltage_values = self.voltage_values[-20:]
            
        # 归一化电压值用于颜色映射
        if self.voltage_values:
            v_min, v_max = min(self.voltage_values), max(self.voltage_values)
            v_norm = [(v - v_min) / (v_max - v_min) if v_max > v_min else 0.5 for v in self.voltage_values]
            
            # 创建颜色映射
            colors = [plt.cm.coolwarm(v) for v in v_norm]
            
            # 更新线的颜色
            self.line.set_color(colors[-1])
            
            # 更新散点颜色
            for collection in self.axes.collections:
                collection.remove()
            self.axes.scatter(self.times, self.values, c=colors, s=60, alpha=0.8, edgecolors='w', linewidth=0.5)
        
        # 更新线的数据
        self.line.set_data(self.times, self.values)
        
        # 设置X轴范围
        if len(self.times) > 1:
            self.axes.set_xlim(min(self.times), max(self.times))
        else:
            self.axes.set_xlim(now, now + pd.Timedelta(minutes=1))
            
        # 格式化X轴日期
        self.fig.autofmt_xdate()
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        
        # 动态调整Y轴范围
        min_val = max(0, min(self.values) - 10) if self.values else 0
        max_val = min(100, max(self.values) + 10) if self.values else 100
        self.axes.set_ylim(min_val, max_val)
        
        # 重新应用样式
        self.update_style()
        
        # 重绘
        self.draw()
        
        # 返回当前状态（是否达标）
        return value >= 80

class HeatMap3D(QWidget):
    """三维热力图，展示电压-送丝速度-质量关系，pyqtgraph.opengl实现"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.glview = gl.GLViewWidget()
        self.glview.setBackgroundColor('#1E1E1E')
        layout.addWidget(self.glview)
        self.voltage_data = []
        self.speed_data = []
        self.quality_data = []
        self.surf_item = None
        self.scatter_item = None
        # 初始化坐标网格
        grid = gl.GLGridItem()
        grid.setSize(100, 100)
        grid.setSpacing(10, 10)
        self.glview.addItem(grid)
        # 视角
        self.glview.setCameraPosition(elevation=30, azimuth=45, distance=200)
    def update_data(self, voltage, speed, quality):
        self.voltage_data.append(voltage)
        self.speed_data.append(speed)
        self.quality_data.append(quality)
        if len(self.voltage_data) > 50:
            self.voltage_data = self.voltage_data[-50:]
            self.speed_data = self.speed_data[-50:]
            self.quality_data = self.quality_data[-50:]
        # 清理旧图元
        if self.surf_item:
            self.glview.removeItem(self.surf_item)
            self.surf_item = None
        if self.scatter_item:
            self.glview.removeItem(self.scatter_item)
            self.scatter_item = None
        # 画散点
        pts = np.column_stack([self.voltage_data, self.speed_data, self.quality_data]).astype(np.float32)
        # 颜色映射：红-橙-绿
        colors = np.zeros((len(self.quality_data), 4))
        for i, q in enumerate(self.quality_data):
            if q < 70:
                colors[i] = (1, 0, 0, 0.8)
            elif q < 85:
                colors[i] = (1, 0.5, 0, 0.8)
            else:
                colors[i] = (0, 1, 0, 0.8)
        if len(pts) > 0:
            self.scatter_item = gl.GLScatterPlotItem(pos=pts, color=colors, size=6, pxMode=False)
            self.glview.addItem(self.scatter_item)
        # 曲面插值
        if len(pts) >= 10:
            try:
                from scipy.interpolate import griddata
                v_range = np.linspace(min(self.voltage_data), max(self.voltage_data), 20)
                s_range = np.linspace(min(self.speed_data), max(self.speed_data), 20)
                V, S = np.meshgrid(v_range, s_range)
                Q = griddata(pts[:, :2], pts[:, 2], (V, S), method='cubic', fill_value=np.min(self.quality_data))
                # 归一化颜色
                normQ = (Q - np.min(Q)) / (np.max(Q) - np.min(Q) + 1e-6)
                surf_colors = np.empty(Q.shape + (4,), dtype=np.float32)
                for i in range(Q.shape[0]):
                    for j in range(Q.shape[1]):
                        q = Q[i, j]
                        if q < 70:
                            surf_colors[i, j] = (1, 0, 0, 0.5)
                        elif q < 85:
                            surf_colors[i, j] = (1, 0.5, 0, 0.5)
                        else:
                            surf_colors[i, j] = (0, 1, 0, 0.5)
                verts = np.empty(V.shape + (3,), dtype=np.float32)
                verts[..., 0] = V
                verts[..., 1] = S
                verts[..., 2] = Q
                self.surf_item = gl.GLSurfacePlotItem(x=v_range, y=s_range, z=Q, colors=surf_colors, shader='shaded', smooth=False)
                self.surf_item.setGLOptions('opaque')
                self.glview.addItem(self.surf_item)
            except Exception as e:
                print(f"[HeatMap3D] 曲面插值失败: {e}")

class CompareBarChart(CustomFigureCanvas):
    """优化前后对比柱状图，增强版"""
    def __init__(self, *args, **kwargs):
        super(CompareBarChart, self).__init__(*args, **kwargs)
        self.axes.set_title('参数优化效果对比', color='#FFFFFF')
        self.axes.set_ylabel('质量评分', color='#FFFFFF')
        self.axes.set_ylim(0, 100)
        self.axes.grid(True, axis='y', linestyle='--', alpha=0.5, color='#3A3A3A')
        
        # 初始数据
        self.categories = ['优化前', '优化后']
        self.values = [60, 85]  # 初始示例值
        
        # 自定义颜色
        self.colors = ['#FF7F50', '#32CD32']
        
        # 绘制柱状图
        self.bars = self.axes.bar(
            self.categories, self.values, 
            color=self.colors, 
            width=0.5, alpha=0.8, edgecolor='#4A4A4A', linewidth=1.5
        )
        
        # 添加数值标签
        self.add_labels()
        
        # 应用样式更新
        self.update_style()
        
    def add_labels(self):
        """为柱状图添加数值标签"""
        for bar in self.bars:
            height = bar.get_height()
            self.axes.text(
                bar.get_x() + bar.get_width()/2., height + 2,
                f'{height:.1f}', ha='center', va='bottom', fontsize=10, color='#FFFFFF'
            )
            
    def update_data(self, before, after):
        """更新对比数据"""
        self.values = [before, after]
        
        # 更新柱状图高度
        for i, bar in enumerate(self.bars):
            bar.set_height(self.values[i])
            
        # 更新标签（删除旧标签后重新添加）
        for text in self.axes.texts:
            text.set_visible(False)  # 隐藏旧标签
        self.add_labels()  # 重新添加新标签
        
        # 重绘
        self.draw()

class QualityMeter(QWidget):
    """质量仪表盘（pyqtgraph实现）"""
    def __init__(self, parent=None, width=4, height=4, dpi=100):
        super().__init__(parent)
        from pyqtgraph import PlotWidget
        layout = QVBoxLayout(self)
        self.plot = PlotWidget()
        self.plot.setBackground('#1E1E1E')
        self.plot.hideAxis('bottom')
        self.plot.hideAxis('left')
        self.plot.setFixedHeight(220)
        self.plot.setFixedWidth(320)
        layout.addWidget(self.plot)
        self.quality = 50
        self.pointer = None
        self.value_text = None
        self.arc_items = []
        self._draw_meter()
        self.update_quality(self.quality)
    def _draw_meter(self):
        import numpy as np
        self.plot.clear()
        self.arc_items = []
        # 画半圆弧区间
        theta = np.linspace(np.pi, 0, 100)
        r = 1
        # 红色区
        t1 = theta[theta <= np.pi*0.7]
        self.arc_items.append(self.plot.plot(r*np.cos(t1), r*np.sin(t1), pen=pg.mkPen('#FF4500', width=16)))
        # 橙色区
        t2 = theta[(theta > np.pi*0.7) & (theta <= np.pi*0.85)]
        self.arc_items.append(self.plot.plot(r*np.cos(t2), r*np.sin(t2), pen=pg.mkPen('#FF9900', width=16)))
        # 绿色区
        t3 = theta[theta > np.pi*0.85]
        self.arc_items.append(self.plot.plot(r*np.cos(t3), r*np.sin(t3), pen=pg.mkPen('#32CD32', width=16)))
        # 刻度
        for i in range(0, 101, 10):
            angle = np.pi - (i/100)*np.pi
            x0, y0 = 0.85*np.cos(angle), 0.85*np.sin(angle)
            x1, y1 = 1.05*np.cos(angle), 1.05*np.sin(angle)
            self.plot.plot([x0, x1], [y0, y1], pen=pg.mkPen('#CCCCCC', width=2))
            text = pg.TextItem(str(i), color='#CCCCCC', anchor=(0.5,0.5))
            text.setPos(1.18*np.cos(angle), 1.18*np.sin(angle))
            self.plot.addItem(text)
        # 中心圆
        self.plot.plot([0], [0], pen=None, symbol='o', symbolSize=60, symbolBrush='#1E1E1E', symbolPen=pg.mkPen('#4A4A4A', width=3))
        # 指针（初始化）
        self.pointer = self.plot.plot([0, 0], [0, 0.7], pen=pg.mkPen('#FF9900', width=5))
        # 数值文本
        self.value_text = pg.TextItem(str(self.quality), color='#FFFFFF', anchor=(0.5,0.5))
        self.value_text.setPos(0, 0.4)
        self.plot.addItem(self.value_text)
        # 标题
        self.title_text = pg.TextItem("质量评分", color='#FFFFFF', anchor=(0.5,0.5))
        self.title_text.setPos(0, 1.1)
        self.plot.addItem(self.title_text)
        self.plot.setXRange(-1.3, 1.3)
        self.plot.setYRange(-0.2, 1.3)
    def update_quality(self, quality):
        import numpy as np
        self.quality = quality
        # 指针角度
        angle = np.pi - (self.quality/100)*np.pi
        x = [0, 0.7*np.cos(angle)]
        y = [0, 0.7*np.sin(angle)]
        if self.pointer is not None:
            self.pointer.setData(x, y)
        # 数值文本
        if self.value_text is not None:
            self.value_text.setText(f"{self.quality:.1f}")
        # 指针颜色
        if self.quality < 70:
            color = '#FF4500'
        elif self.quality < 85:
            color = '#FF9900'
        else:
            color = '#32CD32'
        if self.pointer is not None:
            self.pointer.setPen({'color': color, 'width': 5})

class ParameterDial(QWidget):
    """参数调节旋钮"""
    valueChanged = pyqtSignal(float)
    
    def __init__(self, parent=None, min_val=0, max_val=100, initial_val=50, scale=100, title="参数"):
        super().__init__(parent)
        self.min_val = int(min_val)
        self.max_val = int(max_val)
        self.scale = scale
        self.value = int(initial_val)
        self.title = title
        self.dragging = False
        
        # 设置窗口属性
        self.setFixedSize(120, 150)
        self.setMouseTracking(True)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制背景
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(42, 42, 42))
        gradient.setColorAt(1, QColor(30, 30, 30))
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor(66, 66, 66), 2))
        painter.drawRoundedRect(5, 5, self.width()-10, self.height()-10, 10, 10)
        
        # 绘制标题
        painter.setPen(QColor(200, 200, 200))
        painter.setFont(QFont('Arial', 10, QFont.Bold))
        painter.drawText(10, 25, self.title)
        
        # 计算中心点和半径
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = min(center_x, center_y) - 20
        
        # 绘制旋钮背景
        painter.setPen(QPen(QColor(66, 66, 66), 2))
        painter.setBrush(QColor(42, 42, 42))
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
        
        # 计算角度（将值映射到270度范围，从135度到405度）
        normalized_value = (self.value - self.min_val) / (self.max_val - self.min_val)
        angle = 135 + normalized_value * 270
        
        # 绘制刻度
        painter.setPen(QPen(QColor(100, 100, 100), 1))
        for i in range(0, 28, 2):
            tick_angle = 135 + i * 10
            tick_x1 = center_x + (radius - 5) * np.cos(np.radians(tick_angle))
            tick_y1 = center_y - (radius - 5) * np.sin(np.radians(tick_angle))
            tick_x2 = center_x + radius * np.cos(np.radians(tick_angle))
            tick_y2 = center_y - radius * np.sin(np.radians(tick_angle))
            painter.drawLine(int(tick_x1), int(tick_y1), int(tick_x2), int(tick_y2))
        
        # 绘制指针
        pointer_length = radius - 10
        pointer_x = center_x + pointer_length * np.cos(np.radians(angle))
        pointer_y = center_y - pointer_length * np.sin(np.radians(angle))
        
        # 根据值设置指针颜色
        if normalized_value < 0.3:
            pointer_color = QColor(255, 69, 0)  # 红色
        elif normalized_value < 0.7:
            pointer_color = QColor(255, 153, 0)  # 橙色
        else:
            pointer_color = QColor(50, 205, 50)  # 绿色
            
        painter.setPen(QPen(pointer_color, 3))
        painter.drawLine(center_x, center_y, int(pointer_x), int(pointer_y))
        
        # 绘制中心圆
        painter.setPen(QPen(QColor(66, 66, 66), 1))
        painter.setBrush(QColor(42, 42, 42))
        painter.drawEllipse(center_x - 8, center_y - 8, 16, 16)
        
        # 绘制当前值
        painter.setPen(QColor(200, 200, 200))
        painter.setFont(QFont('Arial', 12, QFont.Bold))
        painter.drawText(0, center_y + 40, self.width(), 20, Qt.AlignCenter, f"{self.value / self.scale:.2f}")
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.update_value_from_position(event.pos())
            
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.update_value_from_position(event.pos())
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            
    def update_value_from_position(self, pos):
        # 计算鼠标相对于中心点的角度
        center_x = self.width() // 2
        center_y = self.height() // 2
        
        dx = pos.x() - center_x
        dy = center_y - pos.y()  # 注意y轴方向相反
        
        # 计算角度（弧度）
        angle = np.arctan2(dy, dx)
        
        # 转换为度数并调整范围（0-360）
        degrees = np.degrees(angle)
        if degrees < 0:
            degrees += 360
            
        # 将角度映射到值范围（135-405度映射到最小值-最大值）
        if 135 <= degrees <= 405:
            normalized_value = (degrees - 135) / 270
            new_value = int(self.min_val + normalized_value * (self.max_val - self.min_val))
            
            # 限制在范围内
            new_value = max(self.min_val, min(self.max_val, new_value))
            
            if new_value != self.value:
                self.value = new_value
                self.valueChanged.emit(self.value / self.scale)
                self.update()
                
    def set_value(self, value):
        """设置旋钮值"""
        int_value = int(round(value * self.scale))
        if self.min_val <= int_value <= self.max_val and int_value != self.value:
            self.value = int_value
            self.valueChanged.emit(self.value / self.scale)
            self.update()
            
    def get_value(self):
        """获取旋钮值"""
        return self.value / self.scale

class AnimatedButton(QPushButton):
    """带动画效果的按钮"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setMinimumWidth(120)
        
        # 初始样式
        self.default_style = """
            QPushButton {
                background-color: #3A3A3A;
                color: #FFFFFF;
                border: 1px solid #5C5C5C;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #4A4A4A;
                border: 1px solid #7C7C7C;
            }
            QPushButton:pressed {
                background-color: #2A2A2A;
            }
        """
        
        # 激活样式
        self.active_style = """
            QPushButton {
                background-color: #FF9900;
                color: #FFFFFF;
                border: 1px solid #FFCC66;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #FFAA33;
                border: 1px solid #FFDD77;
            }
            QPushButton:pressed {
                background-color: #EE8800;
            }
        """
        
        self.setStyleSheet(self.default_style)
        self.animation = None
        
    def set_active(self, active):
        """设置按钮状态"""
        if active:
            self.setStyleSheet(self.active_style)
        else:
            self.setStyleSheet(self.default_style)
            
    def animate_click(self):
        """执行点击动画"""
        self.set_active(True)
        
        # 创建延迟动画
        if self.animation:
            self.animation.stop()
            
        self.animation = QTimer(self)
        self.animation.timeout.connect(lambda: self.set_active(False))
        self.animation.start(300)  # 300毫秒后恢复默认样式

class LLMProvider:
    """阿里云Qwen大模型服务提供者"""
    def __init__(self, config):
        """
        初始化LLM提供者
        :param config: 配置字典，包含api_key和model_id
        """
        self.api_key = config.get('sk-a8c0f511762f41358c24cbc6c37afd8f')
        self.model_id = config.get('1991256', 'qwen-max-2025-01-25')  # 默认使用qwen-max模型
        self.endpoint = 'https://api.aliyun.com/api/v1/services/aigc/text-generation/generation'
    
    def generate_text(self, prompt):
        """
        生成文本响应
        :param prompt: 输入提示词
        :return: 生成的文本
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'X-Model-ID': self.model_id
        }
        
        data = {
            "input": {
                "prompt": prompt
            }
        }
        
        try:
            response = requests.post(
                self.endpoint,
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            # 添加调试日志
            print(f"[DEBUG] 响应状态码: {response.status_code}")
            print(f"[DEBUG] 响应头: {response.headers}")
            print(f"[DEBUG] 响应内容: {response.text[:200]}...")  # 只显示前200字符
            
            result = response.json()
            # 确保返回有效的文本格式
            if 'output' in result and 'text' in result['output']:
                return result['output']['text']
            else:
                print("[ERROR] API响应格式不符合预期")
                print(f"完整响应: {response.text[:500]}...")
                return '无有效响应'
                
        except requests.exceptions.RequestException as e:
            return f"API调用失败：{str(e)}"
        except ValueError as e:
            return f"API返回数据格式错误: {str(e)}"

class IndustrialStyle(QMainWindow):
    """工业风格的主界面，适配ABB机械臂"""
    def __init__(self):
        super().__init__()
        self.comm = Communicate()
        self.resize(1500, 1000)
        self.llm_provider = LLMProvider({
            "api_key": "sk-a8c0f511762f41358c24cbc6c37afd8f",
            "model_id": "1991256"
        })
        self.language_input = QComboBox()
        self.language_input.addItems(["中文", "English", "日本語", "Español"])
        self.language_input.setCurrentText("中文")
        self.knowledge_base = []
        self.last_alarm_time = {}  # 新增：报警冷却记录
        self.log_records = []
        self.init_ui()
        self.setup_connections()
        self.setup_multisource_data()

    def setup_multisource_data(self):
        # 模拟ABB机械臂多源数据采集
        self.multisource_data = {
            '电流': 120.0,
            '电压': 220.0,
            'TCP坐标': [0.0, 0.0, 0.0],
            '关节角': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            '机械臂速度': 0.0,
            '温度': 25.0,
            '视觉': 0.0,  # 缺陷概率
            '声学': 0.0   # 噪声分贝
        }
        self.data_history = {k: [] for k in self.multisource_data}  # 新增：历史曲线
        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self.update_multisource_data)
        self.data_timer.start(500)
        self.alarm_history = []  # 新增：报警历史

    def update_multisource_data(self):
        import random, time
        # 随机模拟数据（ABB机械臂）
        self.multisource_data['电流'] = random.uniform(110, 160)
        self.multisource_data['电压'] = random.uniform(200, 240)
        self.multisource_data['TCP坐标'] = [round(random.uniform(-500, 500), 2) for _ in range(3)]
        self.multisource_data['关节角'] = [round(random.uniform(-180, 180), 2) for _ in range(6)]
        self.multisource_data['机械臂速度'] = random.uniform(10, 120)
        self.multisource_data['温度'] = random.uniform(25, 60)
        self.multisource_data['视觉'] = random.uniform(0, 0.7)
        self.multisource_data['声学'] = random.uniform(45, 80)
        # 记录历史
        for k in self.multisource_data:
            self.data_history[k].append(self.multisource_data[k])
            if len(self.data_history[k]) > 60:
                self.data_history[k] = self.data_history[k][-60:]
        # 简单缺陷预测+报警冷却
        alarm = None
        now = time.time()
        alarm_types = []
        if self.multisource_data['电流'] > 150:
            alarm_types.append('电流过高')
        if self.multisource_data['电压'] > 235:
            alarm_types.append('电压过高')
        if self.multisource_data['温度'] > 55:
            alarm_types.append('温度过高')
        if self.multisource_data['视觉'] > 0.6:
            alarm_types.append('视觉检测疑似缺陷')
        if self.multisource_data['声学'] > 75:
            alarm_types.append('声学异常')
        # 合并报警弹窗逻辑
        show_alarm = False
        alarm_msgs = []
        for atype in alarm_types:
            last = self.last_alarm_time.get(atype, 0)
            if now - last > 10:  # 10秒冷却
                alarm_msgs.append(atype)
                self.last_alarm_time[atype] = now
                self.append_log(f"ABB机械臂检测到异常：{atype}")
                self.alarm_history.append((time.strftime('%H:%M:%S'), atype))
                show_alarm = True
        if show_alarm and alarm_msgs:
            msg = "ABB机械臂检测到异常：" + ", ".join(alarm_msgs)
            if hasattr(self, 'alarm_label'):
                self.alarm_label.setText(f"报警: {', '.join(alarm_msgs)}")
                self.alarm_label.setStyleSheet("color: #FF4500; font-weight: bold;")
            # 删除弹窗 QMessageBox.warning(self, "异常报警", msg)
        elif not alarm_types and hasattr(self, 'alarm_label'):
            self.alarm_label.setText("无报警")
            self.alarm_label.setStyleSheet("color: #32CD32; font-weight: bold;")
        # 更新界面
        if hasattr(self, 'multisource_table'):
            self.refresh_multisource_table()
        if hasattr(self, 'realtime_param_table'):
            self.refresh_realtime_param_table()
        if hasattr(self, 'alarm_table'):
            self.refresh_alarm_table()
        if hasattr(self, 'curve_canvas'):
            self.update_realtime_curves()

    def refresh_multisource_table(self):
        d = self.multisource_data
        self.multisource_table.setItem(0, 1, QTableWidgetItem(f"{d['电流']:.2f} A"))
        self.multisource_table.setItem(1, 1, QTableWidgetItem(f"{d['电压']:.2f} V"))
        self.multisource_table.setItem(2, 1, QTableWidgetItem(f"{d['TCP坐标']}"))
        self.multisource_table.setItem(3, 1, QTableWidgetItem(f"{d['关节角']}"))
        self.multisource_table.setItem(4, 1, QTableWidgetItem(f"{d['机械臂速度']:.2f} mm/s"))
        self.multisource_table.setItem(5, 1, QTableWidgetItem(f"{d['温度']:.2f} ℃"))
        self.multisource_table.setItem(6, 1, QTableWidgetItem(f"{d['视觉']:.2f}"))
        self.multisource_table.setItem(7, 1, QTableWidgetItem(f"{d['声学']:.2f} dB"))

    def refresh_realtime_param_table(self):
        d = self.multisource_data
        self.realtime_param_table.setItem(0, 1, QTableWidgetItem(f"{d['电流']:.2f} A"))
        self.realtime_param_table.setItem(1, 1, QTableWidgetItem(f"{d['电压']:.2f} V"))
        self.realtime_param_table.setItem(2, 1, QTableWidgetItem(f"{d['温度']:.2f} ℃"))
        self.realtime_param_table.setItem(3, 1, QTableWidgetItem(f"{d['机械臂速度']:.2f} mm/s"))
        self.realtime_param_table.setItem(4, 1, QTableWidgetItem(f"{d['TCP坐标']}"))
        self.realtime_param_table.setItem(5, 1, QTableWidgetItem(f"{d['关节角']}"))

    def refresh_alarm_table(self):
        self.alarm_table.setRowCount(len(self.alarm_history))
        for i, (t, msg) in enumerate(self.alarm_history[-20:]):
            self.alarm_table.setItem(i, 0, QTableWidgetItem(t))
            self.alarm_table.setItem(i, 1, QTableWidgetItem(msg))

    def update_realtime_curves(self):
        import numpy as np
        self.curve_fig.clear()
        ax1 = self.curve_fig.add_subplot(311)
        ax2 = self.curve_fig.add_subplot(312)
        ax3 = self.curve_fig.add_subplot(313)
        x = np.arange(len(self.data_history['电流']))
        ax1.plot(x, self.data_history['电流'], color='#FF9900')
        ax1.set_ylabel('电流(A)')
        ax2.plot(x, self.data_history['电压'], color='#0099FF')
        ax2.set_ylabel('电压(V)')
        ax3.plot(x, self.data_history['温度'], color='#32CD32')
        ax3.set_ylabel('温度(℃)')
        for ax in [ax1, ax2, ax3]:
            ax.grid(True, linestyle='--', alpha=0.3)
        self.curve_fig.tight_layout()
        self.curve_canvas.draw()

    def init_ui(self):
        # 初始化所有需要的图表实例，确保不会AttributeError
        self.prediction_chart = PredictionChart(width=8, height=4)
        self.heatmap_3d = HeatMap3D(width=8, height=4)
        self.correlation_chart = HeatMap3D(width=6, height=4)
        self.compare_chart2 = CompareBarChart(width=6, height=4)
        self.compare_chart3 = CompareBarChart(width=6, height=4)
        self.stability_chart = PredictionChart(width=6, height=4)
        self.distribution_chart1 = HeatMap3D(width=6, height=4)
        self.distribution_chart2 = HeatMap3D(width=6, height=4)
        self.prediction_chart_extra = PredictionChart(width=6, height=4)
        self.heatmap_extra = HeatMap3D(width=6, height=4)
        """初始化界面"""
        # 设置窗口标题和大小
        self.setWindowTitle("梯网化焊接修复参数优化系统")
        self.resize(1500, 1000)  # 窗口尺寸扩大到1500x1000
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 添加语言输入框到顶部标题栏
        self.language_input = QComboBox()
        self.language_input.addItems(["中文", "English", "日本語", "Español"])
        self.language_input.setCurrentText("中文")
        self.language_input.setFixedWidth(100)
        self.language_input.setStyleSheet("margin-right: 20px;")
        
        # 设置工业风格主题
        self.setStyleSheet('''
            QMainWindow {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QWidget {
                background-color: #1E1E1E;
                color: #FFFFFF;
                font-family: Consolas, MiSans;
            }
            QGroupBox {
                border: 2px solid #3A3A3A;
                border-radius: 5px;
                margin-top: 1ex;
                font-weight: bold;
                padding-top: 15px;
                background-color: #2A2A2A;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
                color: #FF9900;
            }
            QSlider::groove:horizontal {
                border: 1px solid #4A4A4A;
                height: 8px;
                background: #3A3A3A;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF9900, stop:1 #FF6600);
                border: 1px solid #5C5C5C;
                width: 18px;
                margin: -4px 0;
                border-radius: 9px;
            }
            QComboBox {
                border: 1px solid #4A4A4A;
                border-radius: 3px;
                padding: 5px;
                min-width: 6em;
                background: #3A3A3A;
                selection-background-color: #FF9900;
                selection-color: #FFFFFF;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #4A4A4A;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QPushButton {
                background-color: #3A3A3A;
                color: #FFFFFF;
                border: 1px solid #5C5C5C;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4A4A4A;
                border: 1px solid #7C7C7C;
            }
            QPushButton:pressed {
                background-color: #2A2A2A;
            }
            QLabel {
                color: #FFFFFF;
            }
            QTabWidget::pane {
                border: 2px solid #3A3A3A;
                background-color: #1E1E1E;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #2A2A2A;
                color: #CCCCCC;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #FF9900;
                color: #FFFFFF;
                border: 1px solid #FFCC66;
                border-bottom: none;
            }
            QTabBar::tab:!selected:hover {
                background: #4A4A4A;
                color: #FFFFFF;
            }
            QProgressBar {
                border: 1px solid #4A4A4A;
                border-radius: 3px;
                text-align: center;
                background-color: #3A3A3A;
            }
            QProgressBar::chunk {
                background-color: #FF9900;
                width: 10px;
                margin: 0.5px;
            }
            QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: 1px solid #4A4A4A;
                padding: 5px;
            }
        ''')
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 顶部标题栏
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: #2A2A2A; border-bottom: 2px solid #FF9900; padding: 10px;")
        title_layout = QHBoxLayout(title_bar)
        
        # 系统标题
        title_label = QLabel("梯网化焊接修复参数优化系统")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FF9900;")
        title_layout.addWidget(title_label)
        
        # 系统状态指示器
        status_indicator = QWidget()
        status_indicator.setFixedSize(15, 15)
        status_indicator.setStyleSheet("background-color: #32CD32; border-radius: 7.5px;")
        
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("系统状态:"))
        status_layout.addWidget(status_indicator)
        status_layout.addWidget(QLabel("运行中"))
        status_layout.addStretch()
        
        title_layout.addLayout(status_layout)
        
        # 添加标题栏到主布局
        main_layout.addWidget(title_bar)
        
        # 创建主内容区域
        content_splitter = QSplitter(Qt.Vertical)
        horizontal_splitter = QSplitter(Qt.Horizontal)
        
        # 左侧控制面板
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        control_panel.setMaximumWidth(400)
        
        # 新增：图片识别按钮（保留）
        self.image_recognition_btn = QPushButton("图片识别")
        control_layout.addWidget(self.image_recognition_btn)
        self.image_recognition_btn.clicked.connect(self.show_image_recognition_window)
        self.image_recognition_window = None
        # self.mold_repair_btn = QPushButton("AI模具修复")  # 删除AI模具修复按钮
        # control_layout.addWidget(self.mold_repair_btn)
        # self.mold_repair_btn.clicked.connect(self.show_mold_repair_window)
        # self.mold_repair_window = None
        
        # 材料选择
        material_group = QGroupBox("材料选择")
        material_layout = QVBoxLayout(material_group)
        material_label = QLabel("焊接材料:")
        material_combo = QComboBox()
        material_combo.addItems([
            "碳钢", "不锈钢", "铝合金", "铜合金", "镍基合金", "钛合金", "高强钢", "低合金钢", "铸铁", "镁合金", "银合金", "锌合金", "钨合金", "钼合金", "钽合金", "铬合金", "钴合金", "蒙乃尔合金", "哈氏合金", "因科镍合金", "超级奥氏体不锈钢", "双相不锈钢", "超高分子量聚乙烯", "陶瓷基复合材料", "其他"]
        )
        material_combo.currentTextChanged.connect(lambda text: self.append_log(f"选择焊接材料: {text}"))
        material_layout.addWidget(material_label)
        material_layout.addWidget(material_combo)
        control_layout.addWidget(material_group)
        
        # 路径选择
        path_group = QGroupBox("路径选择")
        path_layout = QVBoxLayout(path_group)
        path_label = QLabel("焊接路径:")
        path_combo = QComboBox()
        path_combo.addItems([
            "直线", "曲线", "圆形", "自定义", "螺旋", "波浪", "锯齿", "多段折线", "矩形", "椭圆", "S形", "U形", "V形", "环形", "点焊", "缝焊", "交叉", "网格", "多层多道", "复杂轮廓", "其他"]
        )
        path_combo.currentTextChanged.connect(lambda text: self.append_log(f"选择焊接路径: {text}"))
        path_layout.addWidget(path_label)
        path_layout.addWidget(path_combo)
        control_layout.addWidget(path_group)
        
        # 参数控制
        params_group = QGroupBox("参数控制")
        params_layout = QFormLayout(params_group)
        
        # 电压控制
        self.voltage_slider = QSlider(Qt.Horizontal)
        self.voltage_slider.setRange(18000, 26000)  # 支持0.01精度
        self.voltage_slider.setValue(22000)
        self.voltage_slider.valueChanged.connect(lambda v: (self.update_slider_value(v / 100, self.voltage_value, self.voltage_dial, self.voltage_input), self.append_log(f"调整电压: {v/100:.2f}V")))
        self.voltage_value = QLabel("220.00")
        self.voltage_value.setMinimumWidth(40)
        self.voltage_input = QLineEdit("220.00")
        self.voltage_input.setFixedWidth(60)
        self.voltage_input.editingFinished.connect(lambda: (self.handle_manual_input(self.voltage_input, self.voltage_slider, self.voltage_dial, 18000, 26000), self.append_log(f"手动输入电压: {self.voltage_input.text()}V")))
        params_layout.addRow("电压 (V):", self.create_slider_with_value(self.voltage_slider, self.voltage_value, self.voltage_input))
        
        # 送丝速度控制
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(10000, 30000)
        self.speed_slider.setValue(20000)
        self.speed_slider.valueChanged.connect(lambda s: (self.update_slider_value(s / 100, self.speed_value, self.speed_dial, self.speed_input), self.append_log(f"调整送丝速度: {s/100:.2f}cm/min")))
        self.speed_value = QLabel("200.00")
        self.speed_value.setMinimumWidth(40)
        self.speed_input = QLineEdit("200.00")
        self.speed_input.setFixedWidth(60)
        self.speed_input.editingFinished.connect(lambda: (self.handle_manual_input(self.speed_input, self.speed_slider, self.speed_dial, 10000, 30000), self.append_log(f"手动输入送丝速度: {self.speed_input.text()}cm/min")))
        params_layout.addRow("送丝速度 (cm/min):", self.create_slider_with_value(self.speed_slider, self.speed_value, self.speed_input))
        
        # 焊接电流控制
        self.current_slider = QSlider(Qt.Horizontal)
        self.current_slider.setRange(5000, 20000)
        self.current_slider.setValue(12000)
        self.current_slider.valueChanged.connect(lambda c: (self.update_slider_value(c / 100, self.current_value, self.current_dial, self.current_input), self.append_log(f"调整焊接电流: {c/100:.2f}A")))
        self.current_value = QLabel("120.00")
        self.current_value.setMinimumWidth(40)
        self.current_input = QLineEdit("120.00")
        self.current_input.setFixedWidth(60)
        self.current_input.editingFinished.connect(lambda: (self.handle_manual_input(self.current_input, self.current_slider, self.current_dial, 5000, 20000), self.append_log(f"手动输入焊接电流: {self.current_input.text()}A")))
        params_layout.addRow("焊接电流 (A):", self.create_slider_with_value(self.current_slider, self.current_value, self.current_input))
        
        # 焊接速度控制（新增）
        self.weld_speed_slider = QSlider(Qt.Horizontal)
        self.weld_speed_slider.setRange(500, 5000)
        self.weld_speed_slider.setValue(2000)
        self.weld_speed_slider.valueChanged.connect(lambda w: (self.update_slider_value(w / 100, self.weld_speed_value, self.weld_speed_dial, self.weld_speed_input), self.append_log(f"调整焊接速度: {w/100:.2f}mm/s")))
        self.weld_speed_value = QLabel("20.00")
        self.weld_speed_value.setMinimumWidth(40)
        self.weld_speed_input = QLineEdit("20.00")
        self.weld_speed_input.setFixedWidth(60)
        self.weld_speed_input.editingFinished.connect(lambda: (self.handle_manual_input(self.weld_speed_input, self.weld_speed_slider, self.weld_speed_dial, 500, 5000), self.append_log(f"手动输入焊接速度: {self.weld_speed_input.text()}mm/s")))
        params_layout.addRow("焊接速度 (mm/s):", self.create_slider_with_value(self.weld_speed_slider, self.weld_speed_value, self.weld_speed_input))
        
        # 材料厚度控制（新增）
        self.thickness_slider = QSlider(Qt.Horizontal)
        self.thickness_slider.setRange(100, 2000)
        self.thickness_slider.setValue(500)
        self.thickness_slider.valueChanged.connect(lambda t: (self.update_slider_value(t / 100, self.thickness_value, self.thickness_dial, self.thickness_input), self.append_log(f"调整材料厚度: {t/100:.2f}mm")))
        self.thickness_value = QLabel("5.00")
        self.thickness_value.setMinimumWidth(40)
        self.thickness_input = QLineEdit("5.00")
        self.thickness_input.setFixedWidth(60)
        self.thickness_input.editingFinished.connect(lambda: (self.handle_manual_input(self.thickness_input, self.thickness_slider, self.thickness_dial, 100, 2000), self.append_log(f"手动输入材料厚度: {self.thickness_input.text()}mm")))
        params_layout.addRow("材料厚度 (mm):", self.create_slider_with_value(self.thickness_slider, self.thickness_value, self.thickness_input))
        
        control_layout.addWidget(params_group)
        
        # 添加旋钮控制
        dial_group = QGroupBox("旋钮控制")
        dial_layout = QGridLayout(dial_group)
        dial_layout.setSpacing(10)
        dial_layout.setContentsMargins(10, 10, 10, 10)

        # 创建参数旋钮
        self.voltage_dial = ParameterDial(min_val=18000, max_val=26000, initial_val=22000, title="电压", scale=100)
        self.speed_dial = ParameterDial(min_val=10000, max_val=30000, initial_val=20000, title="速度", scale=100)
        self.current_dial = ParameterDial(min_val=5000, max_val=20000, initial_val=12000, title="电流", scale=100)
        self.weld_speed_dial = ParameterDial(min_val=500, max_val=5000, initial_val=2000, title="焊接速度", scale=100)
        self.thickness_dial = ParameterDial(min_val=100, max_val=2000, initial_val=500, title="厚度", scale=100)

        # 连接信号
        self.voltage_dial.valueChanged.connect(lambda v: self.update_from_dial(v, self.voltage_slider, self.voltage_value, self.voltage_input))
        self.speed_dial.valueChanged.connect(lambda v: self.update_from_dial(v, self.speed_slider, self.speed_value, self.speed_input))
        self.current_dial.valueChanged.connect(lambda v: self.update_from_dial(v, self.current_slider, self.current_value, self.current_input))
        self.weld_speed_dial.valueChanged.connect(lambda v: self.update_from_dial(v, self.weld_speed_slider, self.weld_speed_value, self.weld_speed_input))
        self.thickness_dial.valueChanged.connect(lambda v: self.update_from_dial(v, self.thickness_slider, self.thickness_value, self.thickness_input))

        # 两行三列排布（最后一格空着）
        dial_layout.addWidget(self.voltage_dial, 0, 0)
        dial_layout.addWidget(self.speed_dial, 0, 1)
        dial_layout.addWidget(self.current_dial, 0, 2)
        dial_layout.addWidget(self.weld_speed_dial, 1, 0)
        dial_layout.addWidget(self.thickness_dial, 1, 1)

        control_layout.addWidget(dial_group)
        
        # 操作按钮
        button_group = QGroupBox("操作控制")
        button_layout = QVBoxLayout(button_group)
        
        self.start_button = AnimatedButton("开始焊接")
        self.stop_button = AnimatedButton("停止焊接")
        self.optimize_button = AnimatedButton("参数优化")
        
        # 连接按钮点击事件
        self.start_button.clicked.connect(self._start_welding_slot)
        self.stop_button.clicked.connect(self._stop_welding_slot)
        self.optimize_button.clicked.connect(self._optimize_parameters_slot)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.optimize_button)
        
        control_layout.addWidget(button_group)
        
        # 添加弹性空间
        control_layout.addStretch()
        
        # 右侧图表区域
        chart_area = QWidget()
        chart_layout = QVBoxLayout(chart_area)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 实时监控标签页
        monitor_tab = QWidget()
        monitor_layout = QVBoxLayout(monitor_tab)
        
        # 质量仪表盘
        meter_layout = QHBoxLayout()
        self.quality_meter = QualityMeter(width=3, height=3)
        meter_layout.addWidget(self.quality_meter)
        
        # 状态信息
        status_group = QGroupBox("当前状态")
        status_layout = QVBoxLayout(status_group)
        
        status_layout.addWidget(QLabel("焊接质量评分:"))
        self.quality_label = QLabel("85.2")
        self.quality_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #32CD32;")
        status_layout.addWidget(self.quality_label)
        
        status_layout.addWidget(QLabel("焊接状态:"))
        self.status_value = QLabel("正常")
        self.status_value.setStyleSheet("color: #32CD32;")
        status_layout.addWidget(self.status_value)
        
        status_layout.addWidget(QLabel("参数稳定性:"))
        self.stability_bar = QProgressBar()
        self.stability_bar.setValue(92)
        self.stability_bar.setTextVisible(True)
        self.stability_bar.setFormat("%v%")
        status_layout.addWidget(self.stability_bar)
        
        meter_layout.addWidget(status_group)
        monitor_layout.addLayout(meter_layout)
        
        # 实时趋势图
        trend_group = QGroupBox("质量趋势")
        trend_layout = QHBoxLayout(trend_group)  # 改为水平布局
        # 左侧为预测图
        self.prediction_chart = PredictionChart(width=8, height=4)
        trend_layout.addWidget(self.prediction_chart, 2)
        # 右侧为AI模具修复区
        ai_mold_widget = QWidget()
        ai_mold_layout = QVBoxLayout(ai_mold_widget)
        self.mold_output = QTextEdit()
        self.mold_output.setReadOnly(True)
        self.mold_output.setPlaceholderText("AI模具修复输出...")
        self.mold_input = QLineEdit()
        self.mold_input.setPlaceholderText("请输入修复问题或描述...")
        self.mold_ask_btn = QPushButton("提交到AI")
        ai_mold_layout.addWidget(self.mold_output)
        ai_mold_layout.addWidget(self.mold_input)
        ai_mold_layout.addWidget(self.mold_ask_btn)
        trend_layout.addWidget(ai_mold_widget, 1)
        self.mold_ask_btn.clicked.connect(lambda: (self.call_mold_ai_inline(), self.append_log(f"提交AI模具修复问题: {self.mold_input.text().strip()}")))
        
        monitor_layout.addWidget(trend_group)
        
        # AI建议板块
        ai_group = QGroupBox("AI参数优化建议")
        ai_layout = QVBoxLayout(ai_group)
        
        self.ai_recommendation = QLabel("AI建议：\n欢迎使用焊接修复预测与参数优化系统V4.3\n请输入参数点击参数优化\nAI参数优化建议")
        self.ai_recommendation.setWordWrap(True)
        self.ai_recommendation.setStyleSheet("padding: 10px;")
        
        ai_layout.addWidget(self.ai_recommendation)
        
        # 添加AI建议到监控标签页
        monitor_layout.addWidget(ai_group)
        
        # 添加到标签页
        self.tab_widget.addTab(monitor_tab, "实时监控")
        
        # 参数分析标签页
        analysis_tab = QWidget()
        analysis_layout = QHBoxLayout(analysis_tab)
        
        # 3D热力图
        heatmap_group = QGroupBox("参数-质量关系")
        heatmap_layout = QVBoxLayout(heatmap_group)
        # 修改：使用已初始化的图表实例
        heatmap_layout.addWidget(self.heatmap_3d)
        
        # 创建参数相关性矩阵
        correlation_group = QGroupBox("参数相关性分析")
        correlation_layout = QVBoxLayout(correlation_group)
        # 修改：使用已初始化的图表实例
        correlation_layout.addWidget(self.correlation_chart)
        
        # 创建left_charts容器，包含heatmap_group和correlation_group
        left_charts = QWidget()
        left_charts_layout = QVBoxLayout(left_charts)
        left_charts_layout.addWidget(heatmap_group)
        left_charts_layout.addWidget(correlation_group)
        
        # 新增：创建右侧图表容器
        right_charts = QWidget()
        right_charts_layout = QVBoxLayout(right_charts)
        
        # 添加两个对比柱状图
        compare_group = QGroupBox("多维度对比")
        compare_layout = QHBoxLayout(compare_group)
        compare_layout.addWidget(self.compare_chart2)
        compare_layout.addWidget(self.compare_chart3)
        
        # 添加稳定性图表和分布图表
        stability_group = QGroupBox("稳定性分析")
        stability_layout = QHBoxLayout(stability_group)
        stability_layout.addWidget(self.stability_chart)
        stability_layout.addWidget(self.distribution_chart1)
        
        # 组合所有图表
        right_charts_layout.addWidget(compare_group)
        right_charts_layout.addWidget(stability_group)

        # 新增：增加更多数据展示区域
        more_data_group = QGroupBox("更多数据展示")
        more_data_layout = QHBoxLayout(more_data_group)
        self.prediction_chart_extra = PredictionChart(width=6, height=4)
        self.heatmap_extra = HeatMap3D(width=6, height=4)
        more_data_layout.addWidget(self.prediction_chart_extra)
        more_data_layout.addWidget(self.heatmap_extra)
        right_charts_layout.addWidget(more_data_group)

        # 将参数分析标签页添加到标签页控件
        analysis_layout.addWidget(left_charts)
        analysis_layout.addWidget(right_charts)
        self.tab_widget.addTab(analysis_tab, "参数分析")

        # 操作日志标签页
        log_tab = QWidget()
        log_layout = QVBoxLayout(log_tab)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("font-family: Consolas;")
        log_layout.addWidget(self.log_text)
        self.tab_widget.addTab(log_tab, "操作日志")

        # 新增：多源数据监控Tab
        multisource_tab = QWidget()
        multisource_layout = QVBoxLayout(multisource_tab)
        multisource_layout.addWidget(QLabel("ABB机械臂多源数据融合实时监测说明：本页展示所有采集参数的原始值，适合工程师调试和数据分析。"))
        self.multisource_table = QTableWidget(8, 2)
        self.multisource_table.setHorizontalHeaderLabels(["参数", "当前值"])
        for i, name in enumerate(["电流", "电压", "TCP坐标", "关节角", "机械臂速度", "温度", "视觉", "声学"]):
            self.multisource_table.setItem(i, 0, QTableWidgetItem(name))
        self.multisource_table.setEditTriggers(QTableWidget.NoEditTriggers)
        multisource_layout.addWidget(self.multisource_table)
        self.tab_widget.addTab(multisource_tab, "多源监测")
        # 新增：梯网化结构设计Tab
        structure_tab = QWidget()
        structure_layout = QVBoxLayout(structure_tab)
        structure_layout.addWidget(QLabel("梯网化增材结构设计示意：本页可调整止裂材料延展性，动态查看结构变化。"))
        self.structure_fig = Figure(figsize=(5, 4))
        self.structure_canvas = FigureCanvas(self.structure_fig)
        structure_layout.addWidget(self.structure_canvas)
        param_layout = QHBoxLayout()
        self.structure_softness = QSlider(Qt.Horizontal)
        self.structure_softness.setRange(1, 100)
        self.structure_softness.setValue(50)
        param_layout.addWidget(QLabel("止裂材料延展性"))
        param_layout.addWidget(self.structure_softness)
        self.structure_softness.valueChanged.connect(self.update_structure_plot)
        structure_layout.addLayout(param_layout)
        self.tab_widget.addTab(structure_tab, "梯网化结构")
        # 新增：增材控形工艺Tab
        forming_tab = QWidget()
        forming_layout = QVBoxLayout(forming_tab)
        forming_layout.addWidget(QLabel("增材控形路径与修复层形状：本页可选择不同路径类型，动态查看控形效果。"))
        self.forming_fig = Figure(figsize=(5, 4))
        self.forming_canvas = FigureCanvas(self.forming_fig)
        forming_layout.addWidget(self.forming_canvas)
        path_layout = QHBoxLayout()
        self.path_combo = QComboBox()
        self.path_combo.addItems(["螺旋", "网格", "直线", "波浪"])
        path_layout.addWidget(QLabel("增材路径"))
        path_layout.addWidget(self.path_combo)
        self.path_combo.currentTextChanged.connect(self.update_forming_plot)
        forming_layout.addLayout(path_layout)
        self.tab_widget.addTab(forming_tab, "增材控形")
        # 新增：知识库Tab
        kb_tab = QWidget()
        kb_layout = QVBoxLayout(kb_tab)
        kb_layout.addWidget(QLabel("参数-结果知识库：本页可导出所有优化参数记录，支持后续分析。"))
        self.kb_table = QTableWidget(0, 5)
        self.kb_table.setHorizontalHeaderLabels(["电压", "送丝速度", "电流", "焊接速度", "厚度"])
        self.kb_table.setEditTriggers(QTableWidget.NoEditTriggers)
        kb_layout.addWidget(self.kb_table)
        export_btn = QPushButton("导出知识库")
        export_btn.clicked.connect(self.export_knowledge_base)
        kb_layout.addWidget(export_btn)
        self.tab_widget.addTab(kb_tab, "知识库")

        # 将标签页添加到图表区域
        chart_layout.addWidget(self.tab_widget)

        # 将控制面板和图表区域添加到分割器
        horizontal_splitter.addWidget(control_panel)
        horizontal_splitter.addWidget(chart_area)
        content_splitter.addWidget(horizontal_splitter)

        # 设置初始分割比例
        content_splitter.setSizes([600, 900])

        # 将分割器添加到主布局
        main_layout.addWidget(content_splitter)

        # 底部状态栏
        status_bar = QStatusBar()
        status_bar.setStyleSheet("background-color: #2A2A2A; border-top: 1px solid #4A4A4A;")
        status_bar.showMessage("系统就绪 2025")
        self.setStatusBar(status_bar)

        # 自动刷新更多数据图表（定时器放在最后）
        self.more_data_timer = QTimer()
        self.more_data_timer.timeout.connect(self.update_more_data_charts)
        self.more_data_timer.start(1000)

        # 新增：实时监控Tab（ABB机械臂）
        monitor_tab = QWidget()
        monitor_layout = QVBoxLayout(monitor_tab)
        monitor_layout.addWidget(QLabel("ABB机械臂实时监控与报警（多源融合）"))
        # 参数表格
        self.realtime_param_table = QTableWidget(6, 2)
        self.realtime_param_table.setHorizontalHeaderLabels(["参数", "当前值"])
        for i, name in enumerate(["电流", "电压", "温度", "机械臂速度", "TCP坐标", "关节角"]):
            self.realtime_param_table.setItem(i, 0, QTableWidgetItem(name))
        self.realtime_param_table.setEditTriggers(QTableWidget.NoEditTriggers)
        monitor_layout.addWidget(self.realtime_param_table)
        # 实时曲线
        self.curve_fig = Figure(figsize=(6, 3))
        self.curve_canvas = FigureCanvas(self.curve_fig)
        monitor_layout.addWidget(self.curve_canvas)
        # 报警状态
        alarm_status_layout = QHBoxLayout()
        self.alarm_label = QLabel("无报警")
        self.alarm_label.setStyleSheet("color: #32CD32; font-weight: bold;")
        alarm_status_layout.addWidget(QLabel("报警状态:"))
        alarm_status_layout.addWidget(self.alarm_label)
        alarm_status_layout.addStretch()
        monitor_layout.addLayout(alarm_status_layout)
        # 报警历史
        self.alarm_table = QTableWidget(0, 2)
        self.alarm_table.setHorizontalHeaderLabels(["时间", "报警内容"])
        self.alarm_table.setEditTriggers(QTableWidget.NoEditTriggers)
        monitor_layout.addWidget(QLabel("报警历史记录（最近20条）"))
        monitor_layout.addWidget(self.alarm_table)
        self.tab_widget.addTab(monitor_tab, "实时监控")

        # 新增：路径切片中间件Tab（功能集成版）
        slicer_tab = ABBPathSlicerTab()
        self.tab_widget.insertTab(0, slicer_tab, "路径切片与仿真")

        # 修改init_ui默认显示第0个Tab
        self.tab_widget.setCurrentIndex(0)
        # 自动刷新参数分析页图表
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        # “参数分析”标签页的索引，需根据实际顺序调整
        # 0: 路径切片中间件, 1: 实时监控, 2: 参数分析 ...
        # 你实际的参数分析Tab索引可能是2，请根据实际顺序调整
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "参数分析":
                analysis_tab_index = i
                break
        else:
            analysis_tab_index = -1
        if index == analysis_tab_index:
            self.update_analysis_charts()

    def update_more_data_charts(self):
        import random
        voltage = random.uniform(180, 260)
        value = random.uniform(60, 100)
        speed = random.uniform(100, 300)
        self.prediction_chart_extra.update_plot(voltage, value)
        self.heatmap_extra.update_data(voltage, speed, value)

    def create_slider_with_value(self, slider, value_label, input_box):
        """创建包含滑块、值标签和手动输入框的容器"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        layout.addWidget(slider, 1)
        layout.addWidget(value_label, 0)
        layout.addWidget(input_box, 0)
        
        return container
    
    def update_slider_value(self, value, label, dial, input_box):
        label.setText(f"{value:.2f}")
        input_box.setText(f"{value:.2f}")
        if dial is not None:
            dial.set_value(value)

    def update_from_dial(self, value, slider, label, input_box):
        slider.setValue(int(round(value * 100)))
        label.setText(f"{value:.2f}")
        input_box.setText(f"{value:.2f}")

    def handle_manual_input(self, input_box, slider, dial, min_int, max_int):
        try:
            value = float(input_box.text())
            int_value = int(round(value * 100))
            if min_int <= int_value <= max_int:
                slider.setValue(int_value)
                if dial is not None:
                    dial.set_value(value)
        except Exception:
            pass
        
    def _start_welding_slot(self):
        self.start_welding()
        self.append_log("点击开始焊接")
    def _stop_welding_slot(self):
        self.stop_welding()
        self.append_log("点击停止焊接")
    def _optimize_parameters_slot(self):
        self.optimize_parameters()
        self.append_log("点击参数优化")

    def start_welding(self):
        """开始焊接操作"""
        try:
            if not self.welding_started:
                self.welding_started = True
                self.start_button.animate_click()
                self.append_log("开始焊接操作")
                
                # 验证所有图表实例存在性
                required_charts = [
                    'prediction_chart', 'heatmap_3d', 'correlation_chart',
                    'compare_chart2', 'compare_chart3', 'stability_chart'
                ]
                
                for chart in required_charts:
                    if not hasattr(self, chart) or getattr(self, chart) is None:
                        raise RuntimeError(f"缺失必要图表实例: {chart}")
                
                # 可以在这里添加实际开始焊接的逻辑
                self.statusBar().showMessage("焊接进行中...")
                
        except Exception as e:
            error_msg = f"开始焊接失败: {str(e)}"
            self.append_log(error_msg)
            QMessageBox.critical(self, "致命错误", error_msg)
            self.welding_started = False

    def stop_welding(self):
        """停止焊接操作"""
        if self.welding_started:
            self.welding_started = False
            self.stop_button.animate_click()
            self.append_log("停止焊接操作")
            # 可以在这里添加实际停止焊接的逻辑
            
    def optimize_parameters(self):
        try:
            self.optimize_button.animate_click()
            self.append_log("执行参数优化")
            voltage = self.voltage_slider.value()
            speed = self.speed_slider.value()
            current = self.current_slider.value()
            weld_speed = self.weld_speed_slider.value()
            thickness = self.thickness_slider.value()
            language = self.language_input.currentText()
            # 简单优化算法：推荐参数略微提升质量
            best_voltage = min(max(voltage + 500, 18000), 26000)
            best_speed = min(max(speed + 500, 10000), 30000)
            best_current = min(max(current + 200, 5000), 20000)
            best_weld_speed = min(max(weld_speed + 100, 500), 5000)
            best_thickness = thickness
            # 自动下发
            self.voltage_slider.setValue(int(best_voltage))
            self.speed_slider.setValue(int(best_speed))
            self.current_slider.setValue(int(best_current))
            self.weld_speed_slider.setValue(int(best_weld_speed))
            self.thickness_slider.setValue(int(best_thickness))
            self.append_log(f"参数优化建议: 电压{best_voltage/100:.2f}V, 送丝{best_speed/100:.2f}cm/min, 电流{best_current/100:.2f}A, 焊接速度{best_weld_speed/100:.2f}mm/s, 厚度{best_thickness/100:.2f}mm (已自动下发)")
            # 知识库记录
            self.knowledge_base.append({
                '电压': best_voltage/100, '送丝速度': best_speed/100, '电流': best_current/100, '焊接速度': best_weld_speed/100, '厚度': best_thickness/100
            })
            # AI建议
            prompt_templates = {#AI参数优化建议设置
                "中文": "当前焊接参数：电压{voltage}V，送丝速度{speed}cm/min，焊接电流{current}A，焊接速度{weld_speed}mm/s，材料厚度{thickness}mm。\n请从以下方面给出优化建议50字以内：\n1. 参数调整方向\n2. 预期质量提升\n3. 潜在风险提示\n4. 最优参数组合建议\n请以{language}简洁说明，分点列出，不使用Markdown格式。",
                "English": "Current welding parameters: Voltage {voltage}V, Wire feeding speed {speed}cm/min, Welding current {current}A, Welding speed {weld_speed}mm/s, Material thickness {thickness}mm.\nPlease provide optimization suggestions in the following aspects:\n1. Parameter adjustment direction\n2. Expected quality improvement\n3. Potential risk warnings\n4. Optimal parameter combination suggestions\nPlease explain in {language}, list in points, no Markdown format.",
                "日本語": "現在の溶接パラメータ：電圧{voltage}V、ワイヤ送り速度{speed}cm/min、溶接電流{current}A、溶接速度{weld_speed}mm/s、材質の厚さ{thickness}mm。\n次の側面から最適化提案を提供してください：\n1. パラメータ調整方向\n2. 予想される品質向上\n3. 潜在的なリスクの警告\n4. 最適なパラメータ組み合わせ提案\n{language}で簡潔に説明し、箇条書きで表示してください。",
                "Español": "Parámetros actuales: voltaje {voltage}V, velocidad de alimentación de alambre {speed}cm/min, corriente de soldadura {current}A, velocidad de soldadura {weld_speed}mm/s, espesor del material {thickness}mm.\nPor favor proporcione recomendaciones de optimización en los siguientes aspectos:\n1. Dirección de ajuste de parámetros\n2. Mejora de calidad esperada\n3. Advertencias de riesgos potenciales\n4. Sugerencias de combinación óptima de parámetros\nExplique en {language}, liste por puntos, sin formato Markdown."
            }
            prompt = prompt_templates[language].format(
                voltage=best_voltage/100,
                speed=best_speed/100,
                current=best_current/100,
                weld_speed=best_weld_speed/100,
                thickness=best_thickness/100,
                language=language
            )
            self.ai_recommendation.setText("AI建议：\nAI处理中，请稍候...")
            self.llm_worker = LLMWorker(prompt)
            self.llm_worker.result_ready.connect(self.handle_llm_response)
            self.llm_worker.start()
            try:
                if hasattr(self, 'compare_chart2'):
                    self.compare_chart2.update_data(75, 85)
                if hasattr(self, 'compare_chart3'):
                    self.compare_chart3.update_data(70, 90)
                if hasattr(self, 'stability_chart'):
                    self.stability_chart.update_plot(220, 85)
                if hasattr(self, 'distribution_chart1'):
                    self.distribution_chart1.update_data(220, 150, 80)
                if hasattr(self, 'distribution_chart2'):
                    self.distribution_chart2.update_data(220, 150, 80)
                if hasattr(self, 'heatmap_extra'):
                    self.heatmap_extra.update_data(220, 150, 80)
            except Exception as e:
                print(f"[ERROR] 图表更新失败: {str(e)}")
                self.append_log(f"图表更新失败: {str(e)}")
        except Exception as e:
            print(f"[ERROR] 参数优化异常: {str(e)}")
            self.append_log(f"参数优化异常: {str(e)}")
            QMessageBox.critical(self, "错误", f"发生致命错误：{str(e)}")

    def export_knowledge_base(self):
        # 导出知识库到CSV
        if not self.knowledge_base:
            QMessageBox.information(self, "导出", "知识库为空！")
            return
        path, _ = QFileDialog.getSaveFileName(self, "导出知识库", "knowledge_base.csv", "CSV Files (*.csv)")
        if path:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.knowledge_base[0].keys())
                writer.writeheader()
                writer.writerows(self.knowledge_base)
            QMessageBox.information(self, "导出", f"知识库已导出到 {path}")

    def handle_llm_response(self, response):
        self.ai_recommendation.setText(f"AI建议：\n{response}")
        if hasattr(self, 'llm_worker') and self.llm_worker:
            self.llm_worker.deleteLater()
            self.llm_worker = None

    def append_log(self, message):
        """添加日志记录"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        self.log_records.append(full_message)
        
        # 更新日志显示
        self.log_text.append(full_message)
        
        # 自动滚动到底部
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        # 知识库同步到表格
        if hasattr(self, 'kb_table') and self.knowledge_base:
            self.kb_table.setRowCount(len(self.knowledge_base))
            for i, row in enumerate(self.knowledge_base):
                self.kb_table.setItem(i, 0, QTableWidgetItem(str(row['电压'])))
                self.kb_table.setItem(i, 1, QTableWidgetItem(str(row['送丝速度'])))
                self.kb_table.setItem(i, 2, QTableWidgetItem(str(row['电流'])))
                self.kb_table.setItem(i, 3, QTableWidgetItem(str(row['焊接速度'])))
                self.kb_table.setItem(i, 4, QTableWidgetItem(str(row['厚度'])))
        
    def update_prediction(self):
        """定时更新预测图表"""
        try:
            # 直接获取当前滑块值
            voltage = self.voltage_slider.value()
            quality = float(self.quality_label.text()) + np.random.normal(0, 2)

            # 更新图表
            status = self.prediction_chart.update_plot(voltage, quality)

            # 更新质量仪表盘
            self.quality_meter.update_quality(quality)

            # 更新状态标签
            self.quality_label.setText(f"{quality:.1f}")
            if quality >= 80:
                self.quality_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #32CD32;")
                self.status_value.setText("正常")
                self.status_value.setStyleSheet("color: #32CD32;")
            elif quality >= 70:
                self.quality_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FF9900;")
                self.status_value.setText("警告")
                self.status_value.setStyleSheet("color: #FF9900;")
            else:
                self.quality_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FF4500;")
                self.status_value.setText("异常")
                self.status_value.setStyleSheet("color: #FF4500;")

            # 更新参数稳定性
            self.stability_bar.setValue(int(100 - abs(quality - 85)))

        except Exception as e:
            print(f"[ERROR] 更新预测图表异常: {str(e)}")
            self.statusBar().showMessage("图表更新异常")

    def update_heatmap(self):
        """定时更新热力图"""
        try:
            # 直接获取当前滑块值
            voltage = self.voltage_slider.value()
            speed = self.speed_slider.value()
            quality = float(self.quality_label.text()) + np.random.normal(0, 2)

            # 更新热力图
            self.heatmap_3d.update_data(voltage, speed, quality)

        except Exception as e:
            print(f"[ERROR] 热力图更新异常: {str(e)}")

    def update_meter(self):
        """定时更新质量仪表盘"""
        if self.welding_started:
            # 模拟质量值变化
            quality = float(self.quality_label.text()) + np.random.normal(0, 0.5)
            quality = max(0, min(100, quality))
            
            # 更新仪表盘
            self.quality_meter.update_quality(quality)
            
    def setup_connections(self):
        """设置信号连接"""
        # 这里可以添加各种信号连接
        pass
        
    def resizeEvent(self, event):
        """窗口大小变化事件"""
        # 确保控制面板宽度不超过窗口宽度的30%
        control_panel = self.findChild(QWidget, "control_panel")
        if control_panel:
            control_panel.setMaximumWidth(int(self.width() * 0.3))
        
        super().resizeEvent(event)

    def show_image_recognition_window(self):
        if self.image_recognition_window is None:
            self.image_recognition_window = ImageRecognitionWindow(self)
        self.image_recognition_window.show()
        self.image_recognition_window.raise_()
        self.image_recognition_window.activateWindow()

    def show_mold_repair_window(self):
        if self.mold_repair_window is None:
            self.mold_repair_window = AIMoldRepairWindow(self)
        self.mold_repair_window.show()
        self.mold_repair_window.raise_()
        self.mold_repair_window.activateWindow()

    def call_mold_ai_inline(self):
        prompt = self.mold_input.text().strip()
        if not prompt:
            self.mold_output.setText("请输入问题描述！")
            return
        self.mold_ask_btn.setEnabled(False)
        self.mold_output.setText("AI处理中，请稍候...")
        self.llm_worker = LLMWorker(prompt)
        self.llm_worker.result_ready.connect(self.handle_mold_ai_response)
        self.llm_worker.start()

    def handle_mold_ai_response(self, text):
        self.mold_output.setText(text)
        self.mold_ask_btn.setEnabled(True)
        self.llm_worker = None

    def update_analysis_charts(self):
        import random
        # 清空旧数据，防止数据无限增长
        for chart in [self.heatmap_3d, self.correlation_chart, self.distribution_chart1, self.distribution_chart2, self.heatmap_extra]:
            chart.voltage_data.clear()
            chart.speed_data.clear()
            chart.quality_data.clear()
        # 多次生成数据，提升到50组
        for _ in range(50):
            voltage = random.uniform(180, 260)
            speed = random.uniform(100, 300)
            quality = random.uniform(60, 100)
            self.heatmap_3d.update_data(voltage, speed, quality)
            self.correlation_chart.update_data(voltage, speed, quality)
            self.distribution_chart1.update_data(voltage, speed, quality)
            self.distribution_chart2.update_data(voltage, speed, quality)
            self.heatmap_extra.update_data(voltage, speed, quality)
        # 其它2D图表
        self.compare_chart2.update_data(random.uniform(60, 90), random.uniform(80, 100))
        self.compare_chart3.update_data(random.uniform(60, 90), random.uniform(80, 100))
        voltage = random.uniform(180, 260)
        quality = random.uniform(60, 100)
        self.stability_chart.update_plot(voltage, quality)

    def update_structure_plot(self):
        # 梯度+网格结构示意
        self.structure_fig.clear()
        ax = self.structure_fig.add_subplot(111)
        ax.set_title("梯网化复合结构示意")
        # 梯度层
        for i in range(5):
            ax.fill_between([0, 10], i, i+1, color=(1-i*0.15, 0.8-i*0.1, 0.6-i*0.1), alpha=0.5)
        # 网格层
        softness = self.structure_softness.value()/100
        for x in range(1, 10, 2):
            ax.plot([x, x], [0, 5], color=(1-softness, 0.5, softness), lw=2)
        for y in range(1, 5, 2):
            ax.plot([0, 10], [y, y], color=(1-softness, 0.5, softness), lw=2)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 5)
        ax.axis('off')
        self.structure_canvas.draw()

    def update_forming_plot(self):
        # 增材路径与修复层形状
        self.forming_fig.clear()
        ax = self.forming_fig.add_subplot(111)
        ax.set_title("增材控形路径")
        path = self.path_combo.currentText()
        import numpy as np
        if path == "螺旋":
            t = np.linspace(0, 4*np.pi, 200)
            x = t*np.cos(t)
            y = t*np.sin(t)
            ax.plot(x, y, color='#FF9900')
        elif path == "网格":
            for i in range(-5, 6):
                ax.plot([i, i], [-5, 5], color='#32CD32')
                ax.plot([-5, 5], [i, i], color='#32CD32')
        elif path == "直线":
            ax.plot([-5, 5], [0, 0], color='#0099FF', lw=3)
        elif path == "波浪":
            t = np.linspace(-5, 5, 200)
            y = np.sin(t)*2
            ax.plot(t, y, color='#FF00FF')
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.axis('off')
        self.forming_canvas.draw()

class ImageRecognitionWindow(QWidget):
    """图片识别窗口"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("图片识别")
        self.resize(600, 400)
        layout = QVBoxLayout(self)
        self.image_label = QLabel("请上传图片")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #ccc; background: #222; color: #fff;")
        layout.addWidget(self.image_label)
        self.upload_btn = QPushButton("上传图片")
        layout.addWidget(self.upload_btn)
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        self.upload_btn.clicked.connect(self.open_image)
        self.current_image_path = None
        # 新增关闭按钮
        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.close)
        layout.addWidget(self.close_btn)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.current_image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.result_text.setText("图片已加载，待识别...")
            # 这里可以调用识别API
            self.recognize_image(file_path)

    def recognize_image(self, file_path):
        try:
            import base64
            import requests
            import json

            with open(file_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode("utf-8")

            url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
            headers = {
                "Authorization": "Bearer sk-826eeb8efd04404aad99a51bf012622c",
                "Content-Type": "application/json"
            }
            data = {
                "model": "qwen-vl-plus",
                "input": {
                    "prompt": "请描述图片内容",
                    "image": image_base64
                },
                "use_raw_prompt": True
            }

            print(json.dumps(data, ensure_ascii=False, indent=2))  # 调试用

            response = requests.post(url, headers=headers, json=data, timeout=60)

            if response.status_code == 200:
                result = response.json()
                text = result.get("output", {}).get("text", "未识别到内容")
                self.result_text.setText(text)
            else:
                self.result_text.setText(f"API调用失败: {response.status_code}\\n{response.text}")

        except ImportError:
            self.result_text.setText("请确保已安装 requests 库：pip install requests")
        except Exception as e:
            self.result_text.setText(f"API调用异常: {str(e)}")

class AIMoldRepairWindow(QWidget):
    """AI模具修复窗口，显示大模型返回的文字"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AI模具修复")
        self.resize(600, 400)
        layout = QVBoxLayout(self)
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        self.input_prompt = QLineEdit()
        self.input_prompt.setPlaceholderText("请输入修复问题或描述...")
        layout.addWidget(self.input_prompt)
        self.ask_btn = QPushButton("提交到AI")
        layout.addWidget(self.ask_btn)
        self.ask_btn.clicked.connect(self.call_aliyun_api)
    def set_result(self, text):
        self.result_text.setText(text)
    def call_aliyun_api(self):
        prompt = self.input_prompt.text().strip()
        if not prompt:
            self.set_result("请输入问题描述！")
            return
        if Application is None:
            self.set_result("未安装dashscope库，请先安装：pip install dashscope")
            return
        try:
            response = Application.call(
                api_key=os.getenv("sk-826eeb8efd04404aad99a51bf012622c"),
                app_id='268dd5307e2c404f925f9c5767290f88',
                prompt=prompt
            )
            if response.status_code != HTTPStatus.OK:
                msg = f"request_id={getattr(response, 'request_id', '')}\ncode={response.status_code}\nmessage={getattr(response, 'message', '')}\n请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code"
                self.set_result(msg)
            else:
                self.set_result(response.output.text)
        except Exception as e:
            self.set_result(f"API调用异常: {str(e)}")

class LLMWorker(QThread):
    result_ready = pyqtSignal(str)
    def __init__(self, prompt, parent=None):
        super().__init__(parent)
        self.prompt = prompt
    def run(self):
        try:
            import dashscope
            from dashscope import Application
            dashscope.api_key = "sk-826eeb8efd04404aad99a51bf012622c"
        except ImportError:
            self.result_ready.emit("未安装dashscope库，请先安装：pip install dashscope")
            return
        from http import HTTPStatus
        try:
            response = Application.call(
                app_id='268dd5307e2c404f925f9c5767290f88',
                prompt=self.prompt
            )
            if response.status_code != HTTPStatus.OK:
                msg = f"request_id={getattr(response, 'request_id', '')}\ncode={response.status_code}\nmessage={getattr(response, 'message', '')}\n请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code"
                self.result_ready.emit(msg)
            else:
                self.result_ready.emit(response.output.text)
        except Exception as e:
            self.result_ready.emit(f"API调用异常: {str(e)}")

# ========== 路径切片核心功能实现 ==========
import numpy as np
import os
from typing import Literal, Tuple

def ensure_libs():
    import importlib.util, subprocess, sys
    for pkg in ["trimesh", "scipy"]:
        if importlib.util.find_spec(pkg) is None:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
try:
    import trimesh
    from scipy.spatial import KDTree, Delaunay
except ImportError:
    ensure_libs()
    import trimesh
    from scipy.spatial import KDTree, Delaunay

def path_slicer(
    input_file: str,
    output_type: Literal["gcode", "urscript"] = "gcode",
    grid_spacing: float = 1.0,
    layer_height: float = 0.3,
    optimize_level: int = 1,
    min_defect_area: float = 5.0,
    gradient_factor: int = 3,
    math_logger=None
) -> Tuple[str, np.ndarray]:
    """
    输入STL文件，输出G代码/URScript和路径点
    math_logger: 可选，传入函数用于输出数学过程
    """
    try:
        mesh = trimesh.load(input_file, force='mesh')
        if math_logger:
            math_logger(f"STL加载完成，顶点数: {len(mesh.vertices)}, 面数: {len(mesh.faces)}")
        # 1. 过滤小组件
        if hasattr(mesh, 'split') and callable(mesh.split):
            try:
                components = mesh.split(only_watertight=False)
                mesh = trimesh.util.concatenate([c for c in components if getattr(c, 'area', 0) > min_defect_area])
                if math_logger:
                    math_logger(f"过滤后组件数: {len(components)}，保留面积>{min_defect_area} mm²")
            except Exception:
                pass
        # 2. 分层切片
        z_min, z_max = mesh.bounds[0][2], mesh.bounds[1][2]
        layers = []
        z = z_min + layer_height/2
        layer_idx = 0
        while z < z_max:
            try:
                section = mesh.section(plane_origin=[0,0,z], plane_normal=[0,0,1])
            except Exception:
                section = None
            if section is None:
                z += layer_height
                continue
            try:
                poly = section.to_planar()
                points = np.array(poly.vertices)
            except Exception:
                z += layer_height
                continue
            if len(points) < 3:
                z += layer_height
                continue
            # 梯度加密：靠近中心的点加密
            center = points.mean(axis=0)
            dists = np.linalg.norm(points - center, axis=1)
            mask = dists < dists.mean()
            dense_points = points[mask]
            if len(dense_points) > 0:
                dense_points = np.repeat(dense_points, gradient_factor, axis=0)
            all_points = np.vstack([points, dense_points])
            try:
                from scipy.spatial import Delaunay
                tri = Delaunay(all_points)
                layer_points = all_points[tri.vertices].reshape(-1,2)
                layer_points = np.unique(layer_points, axis=0)
                if math_logger:
                    math_logger(f"第{layer_idx+1}层 Z={z:.3f}mm: Delaunay点数={len(all_points)}, 三角形数={len(tri.simplices)}，最终点数={len(layer_points)}")
            except Exception:
                layer_points = all_points
                if math_logger:
                    math_logger(f"第{layer_idx+1}层 Z={z:.3f}mm: Delaunay失败，直接用原始点，点数={len(layer_points)}")
            layer_points3d = np.hstack([layer_points, np.full((layer_points.shape[0],1), z)])
            layers.append(layer_points3d)
            z += layer_height
            layer_idx += 1
        if math_logger:
            math_logger(f"总层数: {len(layers)}")
        # 4. 路径优化
        all_path = []
        for i, pts in enumerate(layers):
            if len(pts) < 2:
                continue
            if optimize_level == 0:
                order = np.arange(len(pts))
                if math_logger:
                    math_logger(f"第{i+1}层: 无优化，直接顺序遍历")
            else:
                from scipy.spatial import KDTree
                tree = KDTree(pts)
                order = [0]
                used = set(order)
                for _ in range(1, len(pts)):
                    dists, idxs = tree.query(pts[order[-1]], k=len(pts))
                    if isinstance(idxs, (int, np.integer)):
                        idxs = [idxs]
                    for idx in np.atleast_1d(idxs):
                        if idx not in used:
                            order.append(int(idx))
                            used.add(int(idx))
                            break
                if math_logger:
                    math_logger(f"第{i+1}层: KDTree最近邻优化，路径点数={len(order)}")
            path = pts[order]
            all_path.append(path)
        if not all_path:
            if math_logger:
                math_logger("未生成任何有效路径！")
            return ("未生成路径", np.zeros((0,3)))
        path_points = np.vstack(all_path)
        if math_logger:
            math_logger(f"总路径点数: {path_points.shape[0]}")
        # 5. 输出G代码/URScript
        if isinstance(output_type, str):
            output_type = output_type.lower()
        if output_type == "gcode":
            lines = ["G21 ; mm模式", "G90 ; 绝对坐标"]
            for pt in path_points:
                lines.append(f"G1 X{pt[0]:.3f} Y{pt[1]:.3f} Z{pt[2]:.3f} F{{speed}} S{{power}}")
            code = "\n".join(lines)
        else:
            lines = ["def weld_path():"]
            lines.append("  set_tcp(p[0,0,0,0,0,0])")
            for pt in path_points:
                lines.append(f"  movel(p[{pt[0]:.3f},{pt[1]:.3f},{pt[2]:.3f},0,0,0], a=1.2, v=0.25)")
            lines.append("end")
            code = "\n".join(lines)
        return code, path_points
    except Exception as e:
        if math_logger:
            math_logger(f"切片失败: {str(e)}")
        return f"切片失败: {str(e)}", np.zeros((0,3))

# ========== PyQt界面集成 ==========
# 替换matplotlib 3D为pyqtgraph.opengl
import pyqtgraph as pg
import pyqtgraph.opengl as gl
class PathSlicerTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        # --- 切片操作页 ---
        op_widget = QWidget()
        op_layout = QHBoxLayout(op_widget)
        # 左侧3D预览（pyqtgraph.opengl）
        self.glview = gl.GLViewWidget()
        self.glview.setBackgroundColor('w')
        op_layout.addWidget(self.glview, 2)
        # 右侧参数与过程
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        # 文件选择
        file_layout = QHBoxLayout()
        self.file_label = QLabel("未选择STL文件")
        self.file_btn = QPushButton("选择STL文件")
        self.file_btn.clicked.connect(self.choose_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_btn)
        right_layout.addLayout(file_layout)
        # 参数设置
        param_layout = QFormLayout()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["gcode", "urscript"])
        param_layout.addRow("输出类型:", self.type_combo)
        self.grid_spin = QDoubleSpinBox()
        self.grid_spin.setRange(0.5, 2.0)
        self.grid_spin.setValue(1.0)
        param_layout.addRow("网格间距(mm):", self.grid_spin)
        self.layer_spin = QDoubleSpinBox()
        self.layer_spin.setRange(0.2, 0.5)
        self.layer_spin.setValue(0.3)
        param_layout.addRow("层高(mm):", self.layer_spin)
        self.opt_spin = QSpinBox()
        self.opt_spin.setRange(0,2)
        self.opt_spin.setValue(1)
        param_layout.addRow("优化等级:", self.opt_spin)
        # 新增可调参数
        self.min_area_spin = QDoubleSpinBox()
        self.min_area_spin.setRange(0.1, 100.0)
        self.min_area_spin.setValue(5.0)
        param_layout.addRow("最小缺陷面积(mm²):", self.min_area_spin)
        self.grad_factor_spin = QSpinBox()
        self.grad_factor_spin.setRange(1, 5)
        self.grad_factor_spin.setValue(3)
        param_layout.addRow("梯度加密倍数:", self.grad_factor_spin)
        # 新增：模型缩放与旋转参数
        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(0.1, 10.0)
        self.scale_spin.setValue(1.0)
        param_layout.addRow("模型缩放因子:", self.scale_spin)
        self.rot_x_spin = QDoubleSpinBox(); self.rot_x_spin.setRange(-180, 180); self.rot_x_spin.setValue(0)
        self.rot_y_spin = QDoubleSpinBox(); self.rot_y_spin.setRange(-180, 180); self.rot_y_spin.setValue(0)
        self.rot_z_spin = QDoubleSpinBox(); self.rot_z_spin.setRange(-180, 180); self.rot_z_spin.setValue(0)
        param_layout.addRow("旋转角度X(°):", self.rot_x_spin)
        param_layout.addRow("旋转角度Y(°):", self.rot_y_spin)
        param_layout.addRow("旋转角度Z(°):", self.rot_z_spin)
        # 旋转/缩放参数变化时自动刷新预览
        self.scale_spin.valueChanged.connect(self.preview_mesh)
        self.rot_x_spin.valueChanged.connect(self.preview_mesh)
        self.rot_y_spin.valueChanged.connect(self.preview_mesh)
        self.rot_z_spin.valueChanged.connect(self.preview_mesh)
        right_layout.addLayout(param_layout)
        # 运行按钮
        self.run_btn = QPushButton("运行切片")
        self.run_btn.clicked.connect(self.run_slicer)
        right_layout.addWidget(self.run_btn)
        # 导出按钮
        self.export_btn = QPushButton("导出G代码/URScript")
        self.export_btn.clicked.connect(self.export_code)
        right_layout.addWidget(self.export_btn)
        # 数学运算过程显示
        right_layout.addWidget(QLabel("切片数学运算过程："))
        self.process_text = QTextEdit()
        self.process_text.setReadOnly(True)
        self.process_text.setMinimumHeight(200)
        right_layout.addWidget(self.process_text, 1)
        op_layout.addWidget(right_panel, 1)
        self.path_points = None
        self.code = ""
        self.input_file = None
        self.mesh = None
        self.mesh_item = None
        self.path_item = None
        self.show_empty_preview()
        self.op_widget = op_widget
        # --- 日志页 ---
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.tabs.addTab(self.op_widget, "切片操作")
        self.tabs.addTab(self.log_text, "切片日志")
        main_layout.addWidget(self.tabs)
    def show_empty_preview(self):
        self.glview.clear()
        grid = gl.GLGridItem()
        grid.setSize(100, 100)
        grid.setSpacing(10, 10)
        self.glview.addItem(grid)
    def choose_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "选择STL文件", "", "STL Files (*.stl)")
        if file:
            self.input_file = file
            self.file_label.setText(os.path.basename(file))
            try:
                import trimesh
                self.mesh = trimesh.load(file, force='mesh')
                self.preview_mesh()
                self.append_log(f"成功加载模型: {os.path.basename(file)}")
                if hasattr(self.mesh, 'bounds'):
                    zmin, zmax = self.mesh.bounds[0][2], self.mesh.bounds[1][2]
                    self.append_log(f"模型Z范围: {zmin:.3f} ~ {zmax:.3f} mm, 总高: {zmax-zmin:.3f} mm")
                # 检查闭合性
                if hasattr(self.mesh, 'is_watertight'):
                    if not self.mesh.is_watertight:
                        self.append_log("<font color='red'>警告：模型不是封闭体，切片可能失败！</font>")
                # 检查连通区域面积
                if hasattr(self.mesh, 'split'):
                    components = list(self.mesh.split(only_watertight=False))
                    areas = [getattr(c, 'area', 0) for c in components]
                    self.append_log(f"模型包含{len(components)}个连通区域，面积分别为: {areas}")
                    if all(a < self.min_area_spin.value() for a in areas):
                        self.append_log("<font color='red'>所有区域面积均小于最小缺陷面积参数，建议调小该参数！</font>")
            except Exception as e:
                self.mesh = None
                self.show_empty_preview()
                self.append_log(f"模型加载失败: {e}")
    def preview_mesh(self):
        self.glview.clear()
        grid = gl.GLGridItem()
        grid.setSize(100, 100)
        grid.setSpacing(10, 10)
        self.glview.addItem(grid)
        if self.mesh is not None and hasattr(self.mesh, 'vertices') and hasattr(self.mesh, 'faces'):
            v = self.mesh.vertices.copy()
            f = self.mesh.faces
            # 应用缩放和旋转
            scale = self.scale_spin.value()
            rx, ry, rz = np.deg2rad(self.rot_x_spin.value()), np.deg2rad(self.rot_y_spin.value()), np.deg2rad(self.rot_z_spin.value())
            # 旋转矩阵
            Rx = np.array([[1,0,0],[0,np.cos(rx),-np.sin(rx)],[0,np.sin(rx),np.cos(rx)]])
            Ry = np.array([[np.cos(ry),0,np.sin(ry)],[0,1,0],[-np.sin(ry),0,np.cos(ry)]])
            Rz = np.array([[np.cos(rz),-np.sin(rz),0],[np.sin(rz),np.cos(rz),0],[0,0,1]])
            R = Rz @ Ry @ Rx
            v = (v - v.mean(axis=0)) * scale
            v = v @ R.T
            v = v + v.mean(axis=0)
            # pyqtgraph要求float32
            v = v.astype(np.float32)
            # 画mesh
            if self.mesh_item:
                self.glview.removeItem(self.mesh_item)
            self.mesh_item = gl.GLMeshItem(vertexes=v, faces=f, faceColors=None, drawEdges=True, edgeColor=(0.3,0.3,0.3,1), smooth=False, shader='shaded', drawFaces=True)
            self.mesh_item.setGLOptions('opaque')
            self.glview.addItem(self.mesh_item)
            # 自动居中
            center = v.mean(axis=0)
            self.glview.opts['center'] = pg.Vector(center[0], center[1], center[2])
            self.glview.setCameraPosition(distance=max((v.max(axis=0)-v.min(axis=0))) * 2)
    def run_slicer(self):
        if not self.input_file:
            self.append_log("请先选择STL文件！")
            self.tabs.setCurrentIndex(1)
            return
        # 输出当前参数和模型信息
        self.append_log(f"\n--- 切片参数 ---")
        self.append_log(f"输出类型: {self.type_combo.currentText()}  网格间距: {self.grid_spin.value()} mm  层高: {self.layer_spin.value()} mm  优化等级: {self.opt_spin.value()}  最小缺陷面积: {self.min_area_spin.value()} mm²  梯度加密倍数: {self.grad_factor_spin.value()}")
        if self.mesh is not None and hasattr(self.mesh, 'bounds'):
            zmin, zmax = self.mesh.bounds[0][2], self.mesh.bounds[1][2]
            total_h = zmax - zmin
            self.append_log(f"模型Z范围: {zmin:.3f} ~ {zmax:.3f} mm, 总高: {total_h:.3f} mm")
            # 自动修正层高、网格间距
            if self.layer_spin.value() > total_h / 2:
                self.layer_spin.setValue(max(0.1, total_h / 10))
                self.append_log(f"<font color='orange'>层高过大，已自动调整为{self.layer_spin.value()} mm</font>")
            if self.grid_spin.value() > total_h:
                self.grid_spin.setValue(max(0.1, total_h / 10))
                self.append_log(f"<font color='orange'>网格间距过大，已自动调整为{self.grid_spin.value()} mm</font>")
        # 数学过程收集
        math_log = []
        def math_logger(msg):
            math_log.append(msg)
            self.append_log(msg)
        code, path = path_slicer(
            input_file=self.input_file,
            output_type=self.type_combo.currentText(),
            grid_spacing=self.grid_spin.value(),
            layer_height=self.layer_spin.value(),
            optimize_level=self.opt_spin.value(),
            min_defect_area=self.min_area_spin.value(),
            gradient_factor=self.grad_factor_spin.value(),
            math_logger=math_logger
        )
        self.code = code
        self.path_points = path
        self.process_text.setPlainText("\n".join(math_log))
        # 实时3D预览
        self.glview.clear()
        grid = gl.GLGridItem()
        grid.setSize(100, 100)
        grid.setSpacing(10, 10)
        self.glview.addItem(grid)
        # 画mesh
        if self.mesh is not None and hasattr(self.mesh, 'vertices') and hasattr(self.mesh, 'faces'):
            v = self.mesh.vertices.copy()
            f = self.mesh.faces
            scale = self.scale_spin.value()
            rx, ry, rz = np.deg2rad(self.rot_x_spin.value()), np.deg2rad(self.rot_y_spin.value()), np.deg2rad(self.rot_z_spin.value())
            Rx = np.array([[1,0,0],[0,np.cos(rx),-np.sin(rx)],[0,np.sin(rx),np.cos(rx)]])
            Ry = np.array([[np.cos(ry),0,np.sin(ry)],[0,1,0],[-np.sin(ry),0,np.cos(ry)]])
            Rz = np.array([[np.cos(rz),-np.sin(rz),0],[np.sin(rz),np.cos(rz),0],[0,0,1]])
            R = Rz @ Ry @ Rx
            v = (v - v.mean(axis=0)) * scale
            v = v @ R.T
            v = v + v.mean(axis=0)
            v = v.astype(np.float32)
            if self.mesh_item:
                self.glview.removeItem(self.mesh_item)
            self.mesh_item = gl.GLMeshItem(vertexes=v, faces=f, faceColors=None, drawEdges=True, edgeColor=(0.3,0.3,0.3,1), smooth=False, shader='shaded', drawFaces=True)
            self.mesh_item.setGLOptions('opaque')
            self.glview.addItem(self.mesh_item)
            center = v.mean(axis=0)
            self.glview.opts['center'] = pg.Vector(center[0], center[1], center[2])
            self.glview.setCameraPosition(distance=max((v.max(axis=0)-v.min(axis=0))) * 2)
        # 画路径点
        if path is not None and path.shape[0] > 0:
            if self.path_item:
                self.glview.removeItem(self.path_item)
            pts = path.astype(np.float32)
            self.path_item = gl.GLScatterPlotItem(pos=pts, color=(0,0,1,1), size=3, pxMode=False)
            self.glview.addItem(self.path_item)
            self.append_log(f"切片成功，生成路径点数: {path.shape[0]}")
            self.tabs.setCurrentIndex(0)
        else:
            self.append_log("<font color='red'>切片无有效路径，请检查模型或参数！</font>")
            self.tabs.setCurrentIndex(1)
    def export_code(self):
        if not self.code:
            self.append_log("请先运行切片！")
            self.tabs.setCurrentIndex(1)
            return
        file, _ = QFileDialog.getSaveFileName(self, "导出代码", "weld_path.txt", "Text Files (*.txt)")
        if file:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(self.code)
            self.append_log(f"已导出到: {file}")
            self.tabs.setCurrentIndex(1)
    def append_log(self, msg):
        from datetime import datetime
        now = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{now}] {msg}")

# ========== 集成到主界面Tab ==========
# 在IndustrialStyle.init_ui最后插入：
# slicer_tab = PathSlicerTab()
# self.tab_widget.insertTab(0, slicer_tab, "路径切片中间件")

class ABBPathSlicerTab(QWidget):
    """ABB路径切片与轨迹仿真Tab（PyVista可视化）"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("abb_path_slicer_tab")
        main_layout = QVBoxLayout(self)
        # 平铺操作按钮区
        btn_bar = QHBoxLayout()
        self.btn_open = QPushButton("导入模型")
        self.btn_param = QPushButton("参数配置")
        self.btn_slice = QPushButton("执行切片")
        self.btn_opt = QPushButton("路径优化")
        self.btn_sim = QPushButton("轨迹仿真")
        self.btn_export = QPushButton("导出RAPID")
        self.btn_about = QPushButton("关于")
        btn_bar.addWidget(self.btn_open)
        btn_bar.addWidget(self.btn_param)
        btn_bar.addWidget(self.btn_slice)
        btn_bar.addWidget(self.btn_opt)
        btn_bar.addWidget(self.btn_sim)
        btn_bar.addWidget(self.btn_export)
        btn_bar.addWidget(self.btn_about)
        btn_bar.addStretch()
        main_layout.addLayout(btn_bar)
        # 3D可视化区
        self.pv_widget = QtInteractor(self)
        main_layout.addWidget(self.pv_widget, 10)
        self.pv_widget.set_background('dimgray')
        self.pv_widget.add_axes()
        self.pv_widget.show_grid()
        # 右侧参数区
        self.param_panel = self._create_param_panel()
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.pv_widget, 8)
        h_layout.addWidget(self.param_panel, 2)
        main_layout.addLayout(h_layout, 10)
        # 底部日志区
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(80)
        main_layout.addWidget(self.log_text)
        # 状态
        self.mesh = None
        self.path_points = None
        self.abb_params = {}
        self.rapid_code = ""
        self.model_file = None
        self.slice_data = None
        self.optimized_path = None
        self.setMinimumWidth(900)
        self.setMinimumHeight(600)
        self.append_log("ABB路径切片与轨迹仿真模块已初始化。")
        # 绑定按钮事件
        self.btn_open.clicked.connect(self.open_model)
        self.btn_param.clicked.connect(self.open_abb_param_dialog)
        self.btn_slice.clicked.connect(self.run_slice)
        self.btn_opt.clicked.connect(self.run_optimize)
        self.btn_sim.clicked.connect(self.run_simulation)
        self.btn_export.clicked.connect(self.export_rapid_code)
        self.btn_about.clicked.connect(self.show_about)
    def _create_param_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.addWidget(QLabel("切片参数："))
        self.slice_dir_combo = QComboBox()
        self.slice_dir_combo.addItems(["Z轴切片", "法向切片"])
        layout.addWidget(self.slice_dir_combo)
        layout.addStretch()
        return panel
    def _show_model(self, mesh):
        # 显示模型，带金属高光
        import numpy as np
        faces = mesh.faces
        if faces.shape[1] == 3:
            faces = np.hstack([np.full((faces.shape[0],1), 3), faces])
        pv_mesh = pv.PolyData(mesh.vertices, faces)
        self.pv_widget.add_mesh(
            pv_mesh,
            color='silver',
            specular=1.0,
            specular_power=100,
            metallic=1.0,
            show_edges=True,
            opacity=1.0
        )
    def open_model(self):
        from PyQt5.QtWidgets import QFileDialog
        import trimesh
        file_path, _ = QFileDialog.getOpenFileName(self, "选择模型文件", "", "模型文件 (*.stl *.step *.stp)")
        if not file_path:
            self.append_log("用户取消了模型导入。")
            return
        self.model_file = file_path
        ext = file_path.lower().split('.')[-1]
        self.pv_widget.clear()
        self.pv_widget.set_background('dimgray')
        self.pv_widget.add_axes()
        self.pv_widget.show_grid()
        try:
            if ext == 'stl':
                mesh = trimesh.load(file_path, force='mesh')
                if not mesh.is_watertight:
                    self.append_log("<font color='orange'>警告：STL模型不是封闭体，切片可能异常！</font>")
                self._show_model(mesh)
                self.mesh = mesh
                self.append_log(f"成功导入STL模型：{file_path}")
            elif ext in ('step', 'stp'):
                if not OCC_AVAILABLE:
                    self.append_log("<font color='red'>未安装pythonocc-core，无法导入STEP文件！</font>")
                    return
                from OCC.Core.STEPControl import STEPControl_Reader
                from OCC.Core.IFSelect import IFSelect_RetDone
                from OCC.Extend.DataExchange import read_step_file
                shape = read_step_file(file_path)
                from OCC.Extend.ShapeFactory import discretize_shape
                tris = discretize_shape(shape, linear_deflection=0.1)
                import numpy as np
                vertices = np.array([p for tri in tris for p in tri]).reshape(-1,3)
                faces = np.arange(len(vertices)).reshape(-1,3)
                faces = np.hstack([np.full((faces.shape[0],1), 3), faces])
                pv_mesh = pv.PolyData(vertices, faces)
                self.pv_widget.add_mesh(pv_mesh, color='lightblue', show_edges=True, opacity=1.0)
                self.mesh = shape
                self.append_log(f"成功导入STEP模型：{file_path}")
            else:
                self.append_log(f"<font color='red'>不支持的文件格式: {file_path}</font>")
                return
            self.pv_widget.reset_camera()
        except Exception as e:
            self.append_log(f"<font color='red'>模型导入失败: {str(e)}</font>")
            self.mesh = None
    def open_abb_param_dialog(self):
        dlg = ABBParamDialog(self)
        if dlg.exec_():
            self.abb_params = dlg.get_params()
            self.append_log(f"ABB参数已设置: {self.abb_params}")
        else:
            self.append_log("取消ABB参数设置")
    def export_rapid_code(self):
        # RAPID代码导出
        if not hasattr(self, 'optimized_path') or self.optimized_path is None:
            self.append_log("<font color='red'>请先完成路径优化！</font>")
            return
        from PyQt5.QtWidgets import QFileDialog
        import numpy as np
        try:
            from jinja2 import Template
        except ImportError:
            self.append_log("<font color='red'>未安装jinja2库，无法导出RAPID代码！</font>")
            return
        path = self.optimized_path
        # 默认参数，可后续支持自定义
        tcp = [0,0,0,0,0,0]
        wobj = [0,0,0,0,0,0]
        speed = 100
        zone = 10
        tool = "tool0"
        workobj = "wobj0"
        # RAPID模板
        rapid_tpl = '''
MODULE WeldPath
VAR robtarget p{{'%03d' % 1}}:=[[%0.3f,%0.3f,%0.3f],[1,0,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
{% for i,pt in enumerate(points) %}
VAR robtarget p{{'%03d' % (i+1)}}:=[ [{{'%.3f' % pt[0]}},{{'%.3f' % pt[1]}},{{'%.3f' % pt[2]}}], [1,0,0,0], [0,0,0,0], [9E9,9E9,9E9,9E9,9E9,9E9] ];
{% endfor %}
PROC main()
    ConfL\Off;
    ConfJ\Off;
    ! 轨迹运动
    MoveJ p001, v100, z10, tool0\WObj:=wobj0;
{% for i,pt in enumerate(points) %}
    MoveL p{{'%03d' % (i+1)}}, v{{speed}}, z{{zone}}, {{tool}}\WObj:={{workobj}};
{% endfor %}
ENDPROC
ENDMODULE
'''
        tpl = Template(rapid_tpl)
        code = tpl.render(points=path, speed=speed, zone=zone, tool=tool, workobj=workobj)
        file_path, _ = QFileDialog.getSaveFileName(self, "导出RAPID代码", "weld_path.mod", "RAPID模块文件 (*.mod)")
        if not file_path:
            self.append_log("用户取消了导出操作。")
            return
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            self.append_log(f"RAPID代码已导出到: {file_path}")
        except Exception as e:
            self.append_log(f"<font color='red'>导出失败: {str(e)}</font>")
    def run_slice(self):
        # 仅支持STL（三角网格）切片
        if self.mesh is None:
            self.append_log("<font color='red'>请先导入STL模型！</font>")
            return
        import trimesh
        if not isinstance(self.mesh, trimesh.Trimesh):
            self.append_log("<font color='orange'>当前仅支持STL切片，STEP切片后续支持！</font>")
            return
        # 切片参数
        slice_mode = self.slice_dir_combo.currentText()
        layer_height = 0.5  # 可后续做成参数
        mesh = self.mesh
        zmin, zmax = mesh.bounds[0][2], mesh.bounds[1][2]
        zs = []
        z = zmin + layer_height/2
        while z < zmax:
            zs.append(z)
            z += layer_height
        contours = []
        self.pv_widget.clear()
        # 重新显示原始模型
        import numpy as np
        faces = mesh.faces
        if faces.shape[1] == 3:
            faces = np.hstack([np.full((faces.shape[0],1), 3), faces])
        pv_mesh = pv.PolyData(mesh.vertices, faces)
        self.pv_widget.add_mesh(pv_mesh, color='lightgray', show_edges=True, opacity=0.3)
        # 切片
        for zi in zs:
            try:
                section = mesh.section(plane_origin=[0,0,zi], plane_normal=[0,0,1])
                if section is not None:
                    segs = section.discrete
                    if segs is not None and len(segs) > 1:
                        for seg in segs:
                            if len(seg) >= 2:
                                # 用PyVista画线
                                pts = np.array(seg)
                                if pts.shape[0] >= 2:
                                    self.pv_widget.add_lines(pts, color='red', width=2)
                                    contours.append(pts)
            except Exception as e:
                self.append_log(f"<font color='orange'>切片层异常: {zi:.2f}mm {str(e)}</font>")
        self.append_log(f"切片完成，层数: {len(zs)}，提取轮廓: {len(contours)}")
    def run_optimize(self):
        # 路径优化：对切片轮廓点做最近邻排序，生成连续轨迹（用QThread异步处理）
        if self.mesh is None:
            self.append_log("<font color='red'>请先导入并切片STL模型！</font>")
            return
        import trimesh
        import numpy as np
        from scipy.spatial import KDTree
        from PyQt5.QtCore import QThread, pyqtSignal
        class OptThread(QThread):
            finished = pyqtSignal(np.ndarray)
            def __init__(self, mesh):
                super().__init__()
                self.mesh = mesh
            def run(self):
                mesh = self.mesh
                layer_height = 0.5
                zmin, zmax = mesh.bounds[0][2], mesh.bounds[1][2]
                zs = []
                z = zmin + layer_height/2
                while z < zmax:
                    zs.append(z)
                    z += layer_height
                all_points = []
                for zi in zs:
                    try:
                        section = mesh.section(plane_origin=[0,0,zi], plane_normal=[0,0,1])
                        if section is not None:
                            segs = section.discrete
                            if segs is not None and len(segs) > 1:
                                for seg in segs:
                                    if len(seg) >= 2:
                                        pts = np.array(seg)
                                        all_points.append(pts)
                    except Exception:
                        pass
                if not all_points:
                    self.finished.emit(None)
                    return
                points = np.vstack(all_points)
                kdtree = KDTree(points)
                visited = set()
                path = [0]
                visited.add(0)
                for _ in range(1, len(points)):
                    dists, idxs = kdtree.query(points[path[-1]], k=min(10, len(points)))
                    if isinstance(idxs, int):
                        idxs = [idxs]
                    found = False
                    for idx in idxs:
                        if idx not in visited:
                            path.append(idx)
                            visited.add(idx)
                            found = True
                            break
                    if not found:
                        for i in range(len(points)):
                            if i not in visited:
                                path.append(i)
                                visited.add(i)
                                break
                opt_points = points[path]
                self.finished.emit(opt_points)
        self.append_log("路径优化中...（大模型请耐心等待）")
        self.opt_thread = OptThread(self.mesh)
        self.opt_thread.finished.connect(self._on_optimize_done)
        self.opt_thread.start()
    def _on_optimize_done(self, opt_points):
        if opt_points is None or len(opt_points) < 2:
            self.append_log("<font color='red'>未找到切片轮廓点，请先执行切片！</font>")
            return
        self.pv_widget.clear()
        self.pv_widget.add_axes()
        # 重新显示原始模型
        mesh = self.mesh
        faces = mesh.faces
        import numpy as np
        if faces.shape[1] == 3:
            faces = np.hstack([np.full((faces.shape[0],1), 3), faces])
        pv_mesh = pv.PolyData(mesh.vertices, faces)
        self.pv_widget.add_mesh(pv_mesh, color='lightgray', show_edges=True, opacity=0.3)
        self.pv_widget.add_lines(opt_points, color='blue', width=3)
        self.optimized_path = opt_points
        self.append_log(f"路径优化完成，轨迹点数: {len(opt_points)}")
    def run_simulation(self):
        # 轨迹仿真：动态高亮轨迹点，模拟机械臂运动（QTimer动画）
        if not hasattr(self, 'optimized_path') or self.optimized_path is None:
            self.append_log("<font color='red'>请先完成路径优化！</font>")
            return
        import numpy as np
        from PyQt5.QtCore import QTimer
        path = self.optimized_path
        n = len(path)
        if n < 2:
            self.append_log("<font color='red'>轨迹点数不足，无法仿真！</font>")
            return
        self.btn_sim.setEnabled(False)
        self.append_log("轨迹仿真开始...")
        self.sim_idx = 0
        self.sim_sphere = None
        self.sim_line = None
        self.pv_widget.clear()
        self.pv_widget.set_background('dimgray')
        self.pv_widget.add_axes()
        self.pv_widget.show_grid()
        # 显示原始模型
        if self.mesh is not None:
            self._show_model(self.mesh)
        def step():
            if self.sim_idx > 1:
                pts = path[:self.sim_idx]
                if self.sim_line:
                    self.pv_widget.remove_actor(self.sim_line)
                self.sim_line = self.pv_widget.add_lines(pts, color='blue', width=4)
            if self.sim_sphere:
                self.pv_widget.remove_actor(self.sim_sphere)
            pt = path[self.sim_idx]
            self.sim_sphere = self.pv_widget.add_mesh(pv.Sphere(center=pt, radius=0.5), color='red')
            self.pv_widget.render()
            self.sim_idx += 1
            if self.sim_idx >= n:
                timer.stop()
                self.btn_sim.setEnabled(True)
                self.append_log("轨迹仿真完成！")
        timer = QTimer(self)
        timer.timeout.connect(step)
        timer.start(60)
    def show_about(self):
        QMessageBox.information(self, "关于", "ABB焊接修复路径切片与仿真系统\nPowered by PyQt5 + PyVista + Trimesh + pythonocc-core + Jinja2 + NetworkX")
    def append_log(self, msg):
        from datetime import datetime
        now = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{now}] {msg}")

# ========== 集成到主界面Tab ==========
# 在IndustrialStyle.init_ui最后插入：
# slicer_tab = PathSlicerTab()
# self.tab_widget.insertTab(0, slicer_tab, "路径切片中间件")

class ABBParamDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ABB参数配置")
        layout = QFormLayout(self)
        self.tcp_edit = QLineEdit("[0,0,0,0,0,0]")
        self.wobj_edit = QLineEdit("[0,0,0,0,0,0]")
        self.speed_spin = QDoubleSpinBox(); self.speed_spin.setRange(1,1000); self.speed_spin.setValue(100)
        self.zone_spin = QDoubleSpinBox(); self.zone_spin.setRange(1,100); self.zone_spin.setValue(10)
        layout.addRow("TCP:", self.tcp_edit)
        layout.addRow("工件坐标系:", self.wobj_edit)
        layout.addRow("速度(mm/s):", self.speed_spin)
        layout.addRow("区段(mm):", self.zone_spin)
        btns = QHBoxLayout()
        ok_btn = QPushButton("确定"); cancel_btn = QPushButton("取消")
        ok_btn.clicked.connect(self.accept); cancel_btn.clicked.connect(self.reject)
        btns.addWidget(ok_btn); btns.addWidget(cancel_btn)
        layout.addRow(btns)
    def get_params(self):
        return {
            'tcp': self.tcp_edit.text(),
            'wobj': self.wobj_edit.text(),
            'speed': self.speed_spin.value(),
            'zone': self.zone_spin.value()
        }

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("用户登录 | ABB焊接修复系统")
        self.setFixedSize(480, 360)
        # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 移除置顶，避免兼容性问题
        self.setStyleSheet('''
            QDialog {
                background-color: #232323;
                border-radius: 12px;
                font-family: Misans, Arial, sans-serif;
            }
            QLabel {
                color: #FF9900;
                font-size: 20px;
                font-family: Misans, Arial, sans-serif;
                font-weight: bold;
            }
            QLineEdit {
                background: #fff;
                color: #232323;
                border: 2px solid #FF9900;
                border-radius: 8px;
                padding: 10px;
                font-size: 20px;
                font-family: Misans, Arial, sans-serif;
                selection-background-color: #FF9900;
                selection-color: #fff;
            }
            QLineEdit:focus {
                border: 2.5px solid #FF9900;
                background: #fffbe6;
            }
            QPushButton {
                background-color: #FF9900;
                color: #fff;
                border-radius: 8px;
                font-size: 20px;
                font-family: Misans, Arial, sans-serif;
                font-weight: bold;
                padding: 12px 0;
            }
            QPushButton:hover {
                background-color: #FFA733;
            }
            QPushButton:pressed {
                background-color: #EE8800;
            }
            #tipLabel {
                color: #CCCCCC;
                font-size: 16px;
                font-family: Misans, Arial, sans-serif;
                padding-top: 8px;
            }
            #errLabel {
                color: #FF4500;
                font-size: 18px;
                font-family: Misans, Arial, sans-serif;
                font-weight: bold;
                padding-top: 4px;
            }
        ''')
        layout = QVBoxLayout(self)
        layout.setSpacing(28)
        layout.setContentsMargins(36, 32, 36, 32)
        # 标题
        title = QLabel("梯网化焊接修复参数优化系统")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-family: Misans, Arial, sans-serif; font-weight: bold; color: #FF9900;")
        layout.addWidget(title)
        # 用户名
        user_layout = QVBoxLayout()
        user_label = QLabel("用户名：")
        user_label.setStyleSheet("color: #CCCCCC; font-size: 18px; font-family: Misans, Arial, sans-serif;")
        self.user_edit = QLineEdit("admin")
        self.user_edit.setPlaceholderText("请输入用户名")
        self.user_edit.setMaxLength(32)
        self.user_edit.setMinimumHeight(40)
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_edit)
        layout.addLayout(user_layout)
        # 密码
        pwd_layout = QVBoxLayout()
        pwd_label = QLabel("密码：")
        pwd_label.setStyleSheet("color: #CCCCCC; font-size: 18px; font-family: Misans, Arial, sans-serif;")
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setPlaceholderText("请输入密码")
        self.pwd_edit.setEchoMode(QLineEdit.Password)
        self.pwd_edit.setMinimumHeight(40)
        pwd_layout.addWidget(pwd_label)
        pwd_layout.addWidget(self.pwd_edit)
        layout.addLayout(pwd_layout)
        # 错误提示
        self.err_label = QLabel("")
        self.err_label.setObjectName("errLabel")
        layout.addWidget(self.err_label)
        # 登录按钮
        btns = QHBoxLayout()
        self.login_btn = QPushButton("登录")
        self.cancel_btn = QPushButton("退出")
        self.login_btn.setMinimumWidth(140)
        self.cancel_btn.setMinimumWidth(140)
        btns.addWidget(self.login_btn)
        btns.addWidget(self.cancel_btn)
        layout.addLayout(btns)
        # 温馨提示
        tip = QLabel("版权所有")
        tip.setObjectName("tipLabel")
        tip.setAlignment(Qt.AlignCenter)
        layout.addWidget(tip)
        self.login_btn.clicked.connect(self.try_login)
        self.cancel_btn.clicked.connect(self.reject)
        self.pwd_edit.returnPressed.connect(self.try_login)
        self.user_edit.returnPressed.connect(self.try_login)
    def showEvent(self, event):
        super().showEvent(event)
        # 居中显示（兼容新版PyQt5）
        screen = QApplication.primaryScreen()
        if screen:
            cp = screen.availableGeometry().center()
            qr = self.frameGeometry()
            qr.moveCenter(cp)
            self.move(qr.topLeft())
    def try_login(self):
        user = self.user_edit.text().strip()
        pwd = self.pwd_edit.text().strip()
        if user == "admin" and pwd == "123456":
            self.accept()
        else:
            self.err_label.setText("用户名或密码错误，请重试！")
            self.pwd_edit.clear()
            self.pwd_edit.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        window = IndustrialStyle()
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)