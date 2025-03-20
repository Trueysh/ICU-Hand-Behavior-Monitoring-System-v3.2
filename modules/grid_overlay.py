# -*- coding: utf-8 -*-
# modules/grid_overlay.py
# 网格叠加模块

import cv2
import numpy as np
from config import CONFIG

class GridOverlay:
    """网格叠加类，负责在视频上绘制刻度网格线，帮助用户更直观地选择ROI区域。
    
    主要功能：
    - 在视频上绘制可配置的网格线
    - 显示坐标刻度
    - 支持自定义网格间距和样式
    """
    
    def __init__(self, camera_id):
        """初始化网格叠加器
        
        Args:
            camera_id: 摄像头ID
        """
        self.camera_id = camera_id
        self.config = CONFIG.cameras[camera_id]
        # 网格配置
        self.grid_enabled = True  # 是否启用网格
        self.grid_color = (0, 255, 255)  # 黄色网格线
        self.grid_thickness = 1  # 网格线粗细
        self.grid_alpha = 0.3  # 网格透明度
        self.grid_spacing_x = 50  # 水平网格间距
        self.grid_spacing_y = 50  # 垂直网格间距
        self.show_coordinates = True  # 是否显示坐标
        self.coordinate_font = cv2.FONT_HERSHEY_SIMPLEX
        self.coordinate_font_scale = 0.4
        self.coordinate_color = (255, 255, 255)  # 白色坐标文字
        
    def draw_grid(self, frame):
        """在图像上绘制网格
        
        Args:
            frame: 原始图像帧
            
        Returns:
            添加了网格的图像帧
        """
        if not self.grid_enabled:
            return frame
            
        # 创建一个与原始帧相同大小的透明叠加层
        overlay = frame.copy()
        h, w = frame.shape[:2]
        
        # 绘制垂直网格线
        for x in range(0, w, self.grid_spacing_x):
            cv2.line(overlay, (x, 0), (x, h), self.grid_color, self.grid_thickness)
            # 在顶部绘制坐标
            if self.show_coordinates and x > 0:
                cv2.putText(overlay, str(x), (x - 15, 15), 
                            self.coordinate_font, self.coordinate_font_scale, 
                            self.coordinate_color, 1)
        
        # 绘制水平网格线
        for y in range(0, h, self.grid_spacing_y):
            cv2.line(overlay, (0, y), (w, y), self.grid_color, self.grid_thickness)
            # 在左侧绘制坐标
            if self.show_coordinates and y > 0:
                cv2.putText(overlay, str(y), (5, y + 5), 
                            self.coordinate_font, self.coordinate_font_scale, 
                            self.coordinate_color, 1)
        
        # 将网格叠加到原始帧上，使用透明度
        cv2.addWeighted(overlay, self.grid_alpha, frame, 1 - self.grid_alpha, 0, frame)
        
        # 如果当前有设置ROI，在网格上标注ROI区域的尺寸
        roi = self.config.roi
        if CONFIG.show_roi:
            roi_text = f"ROI: ({roi['x']},{roi['y']},{roi['w']},{roi['h']})"
            cv2.putText(frame, roi_text, (10, h - 10), 
                        self.coordinate_font, self.coordinate_font_scale * 1.5, 
                        (0, 255, 0), 1)
        
        return frame
    
    def update_settings(self, settings):
        """更新网格设置
        
        Args:
            settings: 包含网格设置的字典
            
        Returns:
            bool: 设置是否成功更新
        """
        try:
            if 'grid_enabled' in settings:
                self.grid_enabled = settings['grid_enabled']
            if 'grid_spacing_x' in settings:
                self.grid_spacing_x = max(10, min(200, settings['grid_spacing_x']))
            if 'grid_spacing_y' in settings:
                self.grid_spacing_y = max(10, min(200, settings['grid_spacing_y']))
            if 'grid_alpha' in settings:
                self.grid_alpha = max(0.1, min(0.5, settings['grid_alpha']))
            if 'show_coordinates' in settings:
                self.show_coordinates = settings['show_coordinates']
            return True
        except Exception as e:
            print(f"更新网格设置失败: {str(e)}")
            return False