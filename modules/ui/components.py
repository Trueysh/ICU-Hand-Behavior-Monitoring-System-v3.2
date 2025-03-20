# -*- coding: utf-8 -*-
# modules/ui/components.py
# UI组件模块，包含各种UI组件类

import tkinter as tk
from tkinter import ttk
import datetime
import logging
import sv_ttk
from config import CONFIG
from styles import UIStyles
from modules.language import lang

class TimeDisplay:
    """时间显示组件"""
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text=lang.get_text("current_time"), padding=5)
        self.label = ttk.Label(self.frame, font=UIStyles.FONTS['subtitle'], anchor="center")
        self.label.pack(fill=tk.X, expand=True, pady=5)
        self.update()
    
    def update(self):
        """更新时间显示"""
        try:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.label.config(text=current_time)
        except Exception as e:
            logging.error(f"更新时间显示失败: {str(e)}")
    
    def pack(self, **kwargs):
        """打包组件"""
        self.frame.pack(**kwargs)
        
    def update_text(self):
        """更新组件文本"""
        self.frame.config(text=lang.get_text("current_time"))

class ThemeSelector:
    """主题选择器组件"""
    def __init__(self, parent, callback=None):
        self.current_theme = "light"
        self.theme_var = tk.StringVar(value="light")
        self.frame = ttk.LabelFrame(parent, text=lang.get_text("theme_settings"), padding=5)
        
        self.light_radio = ttk.Radiobutton(self.frame, text=lang.get_text("light_theme"), value="light", 
                        variable=self.theme_var, command=self._on_change)
        self.light_radio.pack(side=tk.LEFT, padx=5)
        
        self.dark_radio = ttk.Radiobutton(self.frame, text=lang.get_text("dark_theme"), value="dark", 
                        variable=self.theme_var, command=self._on_change)
        self.dark_radio.pack(side=tk.LEFT, padx=5)
        
        self.auto_radio = ttk.Radiobutton(self.frame, text=lang.get_text("auto_theme"), value="auto", 
                        variable=self.theme_var, command=self._on_change)
        self.auto_radio.pack(side=tk.LEFT, padx=5)
        
        self.callback = callback
        self.auto_mode = False
        self.auto_check_id = None
    
    def _on_change(self):
        """主题变更处理"""
        new_theme = self.theme_var.get()
        
        # 处理自动模式
        if new_theme == "auto":
            self.auto_mode = True
            # 立即应用基于时间的主题
            self._apply_auto_theme()
            # 设置定时检查
            if not self.auto_check_id:
                self._schedule_auto_check()
            logging.info("已启用自动主题模式")
        else:
            # 关闭自动模式
            self.auto_mode = False
            if self.auto_check_id:
                if hasattr(self, 'frame') and self.frame.winfo_exists():
                    self.frame.after_cancel(self.auto_check_id)
                    self.auto_check_id = None
            
            # 应用选定的主题
            if new_theme != self.current_theme:
                sv_ttk.set_theme(new_theme)
                self.current_theme = new_theme
                logging.info(f"已切换到{new_theme}主题")
                if self.callback:
                    self.callback(new_theme)
    
    def _apply_auto_theme(self):
        """根据当前时间应用相应主题"""
        current_hour = datetime.datetime.now().hour
        # 6:00-18:00使用浅色主题，其他时间使用深色主题
        new_theme = "light" if 6 <= current_hour < 18 else "dark"
        
        if new_theme != self.current_theme:
            sv_ttk.set_theme(new_theme)
            self.current_theme = new_theme
            logging.info(f"自动模式：已切换到{new_theme}主题")
            if self.callback:
                self.callback(new_theme)
    
    def _schedule_auto_check(self):
        """设置定时检查当前时间并更新主题"""
        if self.auto_mode and hasattr(self, 'frame') and self.frame.winfo_exists():
            self._apply_auto_theme()
            # 每10分钟检查一次
            self.auto_check_id = self.frame.after(600000, self._schedule_auto_check)
    
    def pack(self, **kwargs):
        """打包组件"""
        self.frame.pack(**kwargs)
        
    def update_text(self):
        """更新组件文本"""
        self.frame.config(text=lang.get_text("theme_settings"))
        self.light_radio.config(text=lang.get_text("light_theme"))
        self.dark_radio.config(text=lang.get_text("dark_theme"))
        self.auto_radio.config(text=lang.get_text("auto_theme"))

class CameraSelector:
    """摄像头选择器组件"""
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text=lang.get_text("camera_selection"), padding=10)
        self.cam_vars = []
        self.cam_checkbuttons = []
        
        cam_grid = ttk.Frame(self.frame)
        cam_grid.pack(fill=tk.X)
        
        # 使用网格布局，每行放置2个摄像头选项
        for i in range(len(CONFIG.cameras)):
            var = tk.BooleanVar(value=True)
            self.cam_vars.append(var)
            row, col = divmod(i, 2)
            checkbutton = ttk.Checkbutton(cam_grid, text=f"{lang.get_text('camera')} {i}", variable=var, padding=5)
            checkbutton.grid(row=row, column=col, sticky=tk.W, padx=10, pady=5)
            self.cam_checkbuttons.append(checkbutton)
            
        # 配置网格列权重，使选项均匀分布
        cam_grid.columnconfigure(0, weight=1)
        cam_grid.columnconfigure(1, weight=1)
    
    def get_selected(self):
        """获取选中的摄像头ID列表"""
        return [i for i, var in enumerate(self.cam_vars) if var.get()]
    
    def pack(self, **kwargs):
        """打包组件"""
        self.frame.pack(**kwargs)
        
    def update_text(self):
        """更新组件文本"""
        self.frame.config(text=lang.get_text("camera_selection"))
        for i, checkbutton in enumerate(self.cam_checkbuttons):
            checkbutton.config(text=f"{lang.get_text('camera')} {i}")

class SettingsPanel:
    """设置面板组件"""
    def __init__(self, parent, apply_callback=None):
        self.frame = ttk.LabelFrame(parent, text=lang.get_text("parameter_settings"), padding=10)
        self.apply_callback = apply_callback
        
        # 手势灵敏度设置
        ttk.Label(self.frame, text=f"{lang.get_text('gesture_sensitivity')}:").pack(anchor=tk.W)
        self.gesture_scale = ttk.Scale(self.frame, from_=0.1, to=1.0, orient=tk.HORIZONTAL)
        self.gesture_scale.set(CONFIG.gesture_threshold)
        self.gesture_scale.pack(fill=tk.X)
        
        # 网格设置
        grid_frame = ttk.Frame(self.frame)
        grid_frame.pack(fill=tk.X, pady=5)
        
        # 网格启用选项
        grid_header = ttk.Frame(grid_frame)
        grid_header.pack(fill=tk.X)
        
        ttk.Label(grid_header, text="网格设置:").pack(side=tk.LEFT, anchor=tk.W)
        
        self.grid_enabled_var = tk.BooleanVar(value=CONFIG.show_grid)
        ttk.Checkbutton(grid_header, text="显示网格", variable=self.grid_enabled_var).pack(side=tk.LEFT, padx=10)
        
        # 网格间距设置
        grid_spacing = ttk.Frame(grid_frame)
        grid_spacing.pack(fill=tk.X, pady=5)
        
        ttk.Label(grid_spacing, text="水平间距:").grid(row=0, column=0, padx=5)
        self.grid_spacing_x_var = tk.StringVar(value=str(CONFIG.grid_spacing_x))
        ttk.Entry(grid_spacing, textvariable=self.grid_spacing_x_var, width=5).grid(row=0, column=1, padx=5)
        
        ttk.Label(grid_spacing, text="垂直间距:").grid(row=0, column=2, padx=5)
        self.grid_spacing_y_var = tk.StringVar(value=str(CONFIG.grid_spacing_y))
        ttk.Entry(grid_spacing, textvariable=self.grid_spacing_y_var, width=5).grid(row=0, column=3, padx=5)
        
        # 报警间隔设置
        alarm_interval_frame = ttk.Frame(self.frame)
        alarm_interval_frame.pack(fill=tk.X, pady=5)
        ttk.Label(alarm_interval_frame, text=f"{lang.get_text('alarm_interval')}:").pack(anchor=tk.W)
        
        # 报警间隔输入框
        alarm_inputs = ttk.Frame(alarm_interval_frame)
        alarm_inputs.pack(fill=tk.X)
        
        self.alarm_vars = []
        for i, trigger in enumerate(CONFIG.alarm_triggers):
            var = tk.StringVar(value=str(trigger))
            self.alarm_vars.append(var)
            ttk.Label(alarm_inputs, text=f"{lang.get_text('level')}{i+1}:").grid(row=0, column=i*2, padx=5)
            ttk.Entry(alarm_inputs, textvariable=var, width=5).grid(row=0, column=i*2+1, padx=5)
        
        # ROI设置 - 为每个摄像头创建单独的ROI设置
        roi_notebook = ttk.Notebook(self.frame)
        roi_notebook.pack(fill=tk.X, pady=5)
        
        self.roi_vars = {}
        for cam_id in range(len(CONFIG.cameras)):
            roi_frame = ttk.Frame(roi_notebook)
            roi_notebook.add(roi_frame, text=f"{lang.get_text('camera')} {cam_id} ROI")
            
            roi_inputs = ttk.Frame(roi_frame)
            roi_inputs.pack(fill=tk.X, pady=5)
            
            # 为每个摄像头创建ROI输入框
            self.roi_vars[cam_id] = {}
            # 使用固定的键名存储width和height参数
            roi_labels = ['X', 'Y', 'width', 'height']
            roi_display_labels = ['X', 'Y', lang.get_text('width'), lang.get_text('height')]
            roi_keys = ['x', 'y', 'w', 'h']
            
            for i, (label, display_label) in enumerate(zip(roi_labels, roi_display_labels)):
                ttk.Label(roi_inputs, text=display_label).grid(row=0, column=i*2)
                var = tk.StringVar(value=str(CONFIG.cameras[cam_id].roi[roi_keys[i]]))
                self.roi_vars[cam_id][label] = var
                ttk.Entry(roi_inputs, textvariable=var, width=8).grid(row=0, column=i*2+1, padx=5)
        
        # 应用按钮
        ttk.Button(self.frame, text=lang.get_text("apply_settings"), command=self._on_apply).pack(fill=tk.X, pady=5)
    
    def _on_apply(self):
        """应用设置按钮点击处理"""
        if self.apply_callback:
            self.apply_callback()
    
    def get_settings(self):
        """获取当前设置值"""
        settings = {
            'gesture_threshold': self.gesture_scale.get(),
            'alarm_triggers': [],
            'roi_settings': {},
            'grid_settings': {}
        }
        
        # 获取报警间隔设置
        for var in self.alarm_vars:
            try:
                value = int(var.get())
                if value > 0:
                    settings['alarm_triggers'].append(value)
            except ValueError:
                pass
        
        # 获取ROI设置
        for cam_id in self.roi_vars:
            settings['roi_settings'][cam_id] = {
                'x': int(self.roi_vars[cam_id]['X'].get()),
                'y': int(self.roi_vars[cam_id]['Y'].get()),
                'w': int(self.roi_vars[cam_id]['width'].get()),
                'h': int(self.roi_vars[cam_id]['height'].get())
            }
            
        # 获取网格设置
        try:
            settings['grid_settings'] = {
                'grid_enabled': self.grid_enabled_var.get(),
                'grid_spacing_x': int(self.grid_spacing_x_var.get()),
                'grid_spacing_y': int(self.grid_spacing_y_var.get())
            }
        except (ValueError, AttributeError):
            # 如果转换失败，使用默认值
            settings['grid_settings'] = {
                'grid_enabled': CONFIG.show_grid,
                'grid_spacing_x': CONFIG.grid_spacing_x,
                'grid_spacing_y': CONFIG.grid_spacing_y
            }
        
        return settings
    
    def pack(self, **kwargs):
        """打包组件"""
        self.frame.pack(**kwargs)
        
    def update_text(self):
        """更新组件文本"""
        self.frame.config(text=lang.get_text("parameter_settings"))
        
        # 更新手势灵敏度标签
        for child in self.frame.winfo_children():
            if isinstance(child, ttk.Label) and child.cget("text").startswith(lang.get_text("gesture_sensitivity")):
                child.config(text=f"{lang.get_text('gesture_sensitivity')}:")
        
        # 更新报警间隔标签
        for child in self.frame.winfo_children():
            if isinstance(child, ttk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.Label) and subchild.cget("text").startswith(lang.get_text("alarm_interval")):
                        subchild.config(text=f"{lang.get_text('alarm_interval')}:")
        
        # 更新报警级别标签
        for i in range(len(CONFIG.alarm_triggers)):
            for child in self.frame.winfo_children():
                if isinstance(child, ttk.Frame):
                    for subchild in child.winfo_children():
                        if isinstance(subchild, ttk.Frame):
                            for label in subchild.winfo_children():
                                if isinstance(label, ttk.Label) and label.cget("text") == f"{lang.get_text('level')}{i+1}:":
                                    label.config(text=f"{lang.get_text('level')}{i+1}:")
        
        # 更新ROI设置标签
        for cam_id in range(len(CONFIG.cameras)):
            # 更新标签页标题
            for child in self.frame.winfo_children():
                if isinstance(child, ttk.Notebook):
                    for i in range(child.index("end")):
                        if child.tab(i, "text").startswith(f"{lang.get_text('camera')}"):
                            child.tab(i, text=f"{lang.get_text('camera')} {i} ROI")
                    
                    # 更新ROI输入框标签
                    for tab_id in range(child.index("end")):
                        tab = child.winfo_children()[tab_id]
                        for frame in tab.winfo_children():
                            if isinstance(frame, ttk.Frame):
                                labels = frame.winfo_children()
                                for j, label in enumerate(labels):
                                    if isinstance(label, ttk.Label):
                                        if j == 2:  # width标签
                                            label.config(text=lang.get_text('width'))
                                        elif j == 3:  # height标签
                                            label.config(text=lang.get_text('height'))
        
        # 更新应用按钮文本
        for child in self.frame.winfo_children():
            if isinstance(child, ttk.Button) and child.cget("text") == lang.get_text("apply_settings"):
                child.config(text=lang.get_text("apply_settings"))

class ControlButtons:
    """控制按钮组件"""
    def __init__(self, parent, callbacks=None):
        self.frame = ttk.LabelFrame(parent, text=lang.get_text("control_buttons"), padding=10)
        self.callbacks = callbacks or {}
        
        # 使用网格布局，每行放置2个按钮
        button_grid = ttk.Frame(self.frame)
        button_grid.pack(fill=tk.X, pady=5)
        
        # 第一行按钮
        start_btn = ttk.Button(button_grid, text=lang.get_text("start_selected"), 
                              command=self._on_start, style="Accent.TButton")
        start_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        stop_btn = ttk.Button(button_grid, text=lang.get_text("stop_all"), 
                             command=self._on_stop)
        stop_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # 第二行按钮
        pause_btn = ttk.Button(button_grid, text=lang.get_text("pause_alarm"), 
                              command=self._on_pause)
        pause_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        reset_btn = ttk.Button(button_grid, text=lang.get_text("reset_status"), 
                              command=self._on_reset)
        reset_btn.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # 配置网格列权重，使按钮均匀分布
        button_grid.columnconfigure(0, weight=1)
        button_grid.columnconfigure(1, weight=1)
    
    def _on_start(self):
        if 'start' in self.callbacks:
            self.callbacks['start']()
    
    def _on_stop(self):
        if 'stop' in self.callbacks:
            self.callbacks['stop']()
    
    def _on_pause(self):
        if 'pause' in self.callbacks:
            self.callbacks['pause']()
    
    def _on_reset(self):
        if 'reset' in self.callbacks:
            self.callbacks['reset']()
    
    def pack(self, **kwargs):
        """打包组件"""
        self.frame.pack(**kwargs)
        
    def update_text(self):
        """更新组件文本"""
        self.frame.config(text=lang.get_text("control_buttons"))

class StatusDisplay:
    """状态显示组件"""
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text=lang.get_text("system_status"), padding=10)
        
        # 摄像头状态指示区域
        self.cam_status_frame = ttk.Frame(self.frame)
        self.cam_status_frame.pack(fill=tk.X, pady=5)
        
        # 添加状态标题行 - 使用更美观的标题样式
        header_frame = ttk.Frame(self.cam_status_frame, style="Header.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(header_frame, text=lang.get_text("status"), width=6, font=UIStyles.FONTS['subtitle']).pack(side=tk.LEFT, padx=5)
        ttk.Label(header_frame, text=lang.get_text("camera"), width=10, font=UIStyles.FONTS['subtitle']).pack(side=tk.LEFT, padx=5)
        ttk.Label(header_frame, text=lang.get_text("alarm_level"), width=30, font=UIStyles.FONTS['subtitle']).pack(side=tk.LEFT, padx=5)
        
        # 分隔线
        separator = ttk.Separator(self.cam_status_frame, orient="horizontal")
        separator.pack(fill=tk.X, pady=5)
        
        self.cam_status_labels = []
        self.alarm_count_labels = []
        for i in range(len(CONFIG.cameras)):
            cam_label_frame = ttk.Frame(self.cam_status_frame)
            cam_label_frame.pack(fill=tk.X, pady=4)
            
            # 状态指示器
            status_indicator = tk.Label(cam_label_frame, width=4, height=2, 
                                       bg=UIStyles.STATUS_COLORS['disabled'])
            status_indicator.pack(side=tk.LEFT, padx=5)
            
            cam_label = ttk.Label(cam_label_frame, text=f"{lang.get_text('camera')} {i}", font=UIStyles.FONTS['body'])
            cam_label.pack(side=tk.LEFT, padx=5)
            
            # 报警计数显示
            alarm_count_frame = ttk.Frame(cam_label_frame)
            alarm_count_frame.pack(side=tk.LEFT, padx=10)
            
            alarm_counts = {}
            for j, trigger in enumerate(CONFIG.alarm_triggers):
                # 使用更美观的标签样式
                count_frame = ttk.Frame(alarm_count_frame)
                count_frame.pack(side=tk.LEFT, padx=5)
                
                level_label = ttk.Label(count_frame, text=f"L{j+1}", font=UIStyles.FONTS['small'])
                level_label.pack(anchor=tk.CENTER)
                
                count_label = ttk.Label(count_frame, text="0", width=2, font=UIStyles.FONTS['body'])
                count_label.pack(anchor=tk.CENTER)
                
                alarm_counts[trigger] = count_label
            
            self.alarm_count_labels.append(alarm_counts)
            self.cam_status_labels.append(status_indicator)
        
        # 状态信息显示区域
        info_frame = ttk.LabelFrame(self.frame, text=lang.get_text("system_info"), padding=5)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.status_label = ttk.Label(info_frame, text=lang.get_text("system_ready"), font=UIStyles.FONTS['subtitle'])
        self.status_label.pack(anchor=tk.W, pady=5)
        
        self.status_text = tk.Text(info_frame, height=8, wrap=tk.WORD, font=UIStyles.FONTS['body'])
        self.status_text.pack(fill=tk.BOTH, expand=True)
        self.status_text.config(state='disabled')
    
    def update_status(self, camera_processors):
        """更新摄像头状态显示"""
        try:
            status_str = ""
            self.status_text.config(state='normal')
            self.status_text.delete(1.0, tk.END)
            
            for i, processor in enumerate(camera_processors):
                if processor:
                    status = processor.get_status()
                    
                    # 更新状态指示器颜色
                    if status['alarm_level'] > 0:
                        status_color = UIStyles.get_alarm_level_color(status['alarm_level'])
                        self.cam_status_labels[i].config(bg=status_color)
                    elif status['detection_time'] > 0:
                        self.cam_status_labels[i].config(bg=UIStyles.STATUS_COLORS['detecting'])
                    else:
                        self.cam_status_labels[i].config(bg=UIStyles.STATUS_COLORS['normal'])
                    
                    # 更新报警计数显示
                    if i < len(self.alarm_count_labels):
                        alarm_counts = {}
                        for trigger in CONFIG.alarm_triggers:
                            alarm_counts[trigger] = 0
                        
                        # 从processor获取已触发的报警
                        for trigger in processor.played_sounds:
                            if trigger in alarm_counts:
                                alarm_counts[trigger] = 1
                        
                        # 更新显示
                        for j, trigger in enumerate(CONFIG.alarm_triggers):
                            if trigger in self.alarm_count_labels[i]:
                                count = alarm_counts[trigger]
                                level_color = UIStyles.get_alarm_level_color(j+1) if count > 0 else 'black'
                                self.alarm_count_labels[i][trigger].config(
                                    text=str(count),
                                    foreground=level_color
                                )
                    
                    # 格式化状态信息
                    status_str += f"{lang.get_text('camera')} {i}: "
                    status_str += f"{lang.get_text('status')}: {status['status']} "
                    if status['fps'] > 0:
                        status_str += f"FPS: {status['fps']:.1f} "
                    if status['detection_time'] > 0:
                        status_str += f"{lang.get_text('detection_time')}: {status['detection_time']:.1f}{lang.get_text('seconds')} "
                    if status['alarm_level'] > 0:
                        status_str += f"{lang.get_text('alarm_level')}: {status['alarm_level']} "
                    status_str += "\n"
                else:
                    # 摄像头未运行，显示为禁用状态
                    self.cam_status_labels[i].config(bg=UIStyles.STATUS_COLORS['disabled'])
            
            if not status_str:
                status_str = lang.get_text("no_active_camera")
                
            self.status_text.insert(tk.END, status_str)
            self.status_text.config(state='disabled')
        except Exception as e:
            logging.error(f"更新状态失败: {str(e)}")
    
    def set_status_text(self, text):
        """设置状态文本"""
        self.status_label.config(text=text)
    
    def pack(self, **kwargs):
        """打包组件"""
        self.frame.pack(**kwargs)
        
    def update_text(self):
        """更新组件文本"""
        self.frame.config(text=lang.get_text("system_status"))
        # 更新状态信息区域的标题
        for child in self.frame.winfo_children():
            if isinstance(child, ttk.LabelFrame):
                if child.cget("text") in ["系统信息", "System Info", "System Information"]:
                    child.config(text=lang.get_text("system_info"))