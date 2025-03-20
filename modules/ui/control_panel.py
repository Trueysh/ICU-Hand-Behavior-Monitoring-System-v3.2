# -*- coding: utf-8 -*-
# modules/ui/control_panel.py
# 控制面板模块，负责系统的图形用户界面和用户交互

import tkinter as tk
from tkinter import ttk, messagebox
import logging
import datetime
import sv_ttk

from config import CONFIG
from modules import CameraManager
from modules.language import lang
from .components import (
    TimeDisplay,
    ThemeSelector,
    CameraSelector,
    SettingsPanel,
    ControlButtons,
    StatusDisplay
)
from .language_selector import LanguageSelector

class ControlPanel:
    """控制面板类，负责系统的图形用户界面和用户交互。
    
    主要功能：
    - 提供摄像头选择和控制界面
    - 显示摄像头状态和报警信息
    - 处理用户交互事件
    
    此类使用组件化设计，将UI元素拆分为多个独立组件，提高代码可维护性。
    """
    def __init__(self):
        """初始化控制面板"""
        try:
            self.root = tk.Tk()
            self.root.title(lang.get_text("window_title"))
            self.root.geometry("1000x800")  # 调整窗口大小为更合理的尺寸
            self.root.minsize(800, 600)  # 设置最小窗口大小
            self.manager = CameraManager()
            self._setup_ui()
            self._center_window()
            self._start_status_update()
            logging.info("控制面板初始化完成")
        except Exception as e:
            logging.critical(f"控制面板初始化失败: {str(e)}")
            messagebox.showerror(lang.get_text("init_error"), f"{lang.get_text('system_init_failed')}: {str(e)}")
            raise
            
    def _center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"+{x}+{y}")
        
    def _setup_ui(self):
        """设置用户界面组件"""
        try:
            # 应用Sun Valley主题
            sv_ttk.set_theme("light")
            self.current_theme = "light"
            
            # 创建主框架 - 使用更宽敞的内边距
            main_frame = ttk.Frame(self.root, padding=15)
            main_frame.pack(expand=True, fill=tk.BOTH)
            
            # 创建左右分栏布局 - 使用更合理的比例
            left_panel = ttk.Frame(main_frame)
            left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
            
            # 添加垂直分隔线
            separator = ttk.Separator(main_frame, orient="vertical")
            separator.pack(side=tk.LEFT, fill=tk.Y, padx=2)
            
            right_panel = ttk.Frame(main_frame)
            right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))
            
            # 顶部工具栏 - 放在左侧面板顶部
            toolbar = ttk.Frame(left_panel)
            toolbar.pack(fill=tk.X, pady=(0, 10))
            
            # 添加语言选择器
            self.language_selector = LanguageSelector(toolbar, callback=self._on_language_change)
            self.language_selector.pack(side=tk.LEFT, padx=5)
            
            # 添加主题切换按钮
            self.theme_selector = ThemeSelector(toolbar, callback=self._on_theme_change)
            self.theme_selector.pack(side=tk.RIGHT, padx=5)
            
            # 添加时间显示 - 放在右侧面板顶部
            self.time_display = TimeDisplay(right_panel)
            self.time_display.pack(fill=tk.X, pady=(0, 10))
            
            # 摄像头选择区域 - 放在左侧面板
            self.camera_selector = CameraSelector(left_panel)
            self.camera_selector.pack(fill=tk.X, pady=5)
            
            # 参数设置区域 - 放在左侧面板
            self.settings_panel = SettingsPanel(left_panel, apply_callback=self._apply_settings)
            self.settings_panel.pack(fill=tk.X, pady=5)
            
            # 控制按钮区域 - 放在左侧面板底部
            self.control_buttons = ControlButtons(
                left_panel,
                callbacks={
                    'start': self.start_selected,
                    'stop': self.stop_all,
                    'pause': self.pause_alarm,
                    'reset': self.reset_status
                }
            )
            self.control_buttons.pack(fill=tk.X, pady=5)
            
            # 状态显示区域 - 放在右侧面板
            self.status_display = StatusDisplay(right_panel)
            self.status_display.pack(fill=tk.BOTH, expand=True, pady=5)
            
            # 绑定关闭事件
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            
            logging.info("界面组件初始化完成")
        except Exception as e:
            logging.error(f"界面组件初始化失败: {str(e)}")
            raise
            
    def _on_theme_change(self, theme):
        """主题变更回调"""
        self.current_theme = theme
        
    def _on_language_change(self):
        """语言变更回调，更新所有UI组件的文本"""
        # 更新窗口标题
        self.root.title(lang.get_text("window_title"))
        
        # 更新各组件文本
        self.theme_selector.update_text()
        self.camera_selector.update_text()
        self.time_display.update_text()
        self.settings_panel.frame.config(text=lang.get_text("parameter_settings"))
        self.control_buttons.frame.config(text=lang.get_text("control_buttons"))
        self.status_display.frame.config(text=lang.get_text("system_status"))
        self.language_selector.update_text()
        
        # 更新设置面板中的文本
        # 更新手势灵敏度标签
        for child in self.settings_panel.frame.winfo_children():
            if isinstance(child, ttk.Label) and ("手势检测灵敏度" in child.cget("text") or "Gesture Detection" in child.cget("text")):
                child.config(text=f"{lang.get_text('gesture_sensitivity')}:")
        
        # 更新报警间隔标签
        for child in self.settings_panel.frame.winfo_children():
            if isinstance(child, ttk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.Label) and ("报警间隔" in subchild.cget("text") or "Alarm Interval" in subchild.cget("text")):
                        subchild.config(text=f"{lang.get_text('alarm_interval')}:")
        
        # 更新级别标签
        for child in self.settings_panel.frame.winfo_children():
            if isinstance(child, ttk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.Frame):
                        for label in subchild.winfo_children():
                            if isinstance(label, ttk.Label) and (label.cget("text").startswith("级别") or label.cget("text").startswith("Level")):
                                level_num = label.cget("text").replace("级别", "").replace("Level", "")
                                label.config(text=f"{lang.get_text('level')}{level_num}")
        
        # 更新ROI设置中的宽度和高度标签
        for notebook in self.settings_panel.frame.winfo_children():
            if isinstance(notebook, ttk.Notebook):
                # 更新每个标签页的标题
                for i, tab_id in enumerate(notebook.tabs()):
                    notebook.tab(tab_id, text=f"{lang.get_text('camera')} {i} ROI")
                    
                    # 更新标签页内容
                    tab = notebook.nametowidget(tab_id)
                    for frame in tab.winfo_children():
                        if isinstance(frame, ttk.Frame):
                            for label in frame.winfo_children():
                                if isinstance(label, ttk.Label):
                                    if label.cget("text") == "宽度" or label.cget("text") == "Width":
                                        label.config(text=lang.get_text("width"))
                                    elif label.cget("text") == "高度" or label.cget("text") == "Height":
                                        label.config(text=lang.get_text("height"))
        
        # 更新应用按钮文本
        for child in self.settings_panel.frame.winfo_children():
            if isinstance(child, ttk.Button):
                child.config(text=lang.get_text("apply_settings"))
        
        # 更新摄像头选择器中的复选框文本
        for child in self.camera_selector.frame.winfo_children():
            if isinstance(child, ttk.Frame):  # 找到网格布局框架
                for checkbox in child.winfo_children():
                    if isinstance(checkbox, ttk.Checkbutton):
                        text = checkbox.cget("text")
                        if "摄像头" in text or "Camera" in text:
                            # 提取摄像头编号
                            cam_num = text.split()[-1] if " " in text else text[-1]
                            checkbox.config(text=f"{lang.get_text('camera')} {cam_num}")
        
        # 更新控制按钮文本
        for child in self.control_buttons.frame.winfo_children():
            if isinstance(child, ttk.Frame):  # 找到按钮网格布局框架
                for button in child.winfo_children():
                    if isinstance(button, ttk.Button):
                        text = button.cget("text")
                        if "启动选中" in text or "Start Selected" in text:
                            button.config(text=lang.get_text("start_selected"))
                        elif "停止所有" in text or "Stop All" in text:
                            button.config(text=lang.get_text("stop_all"))
                        elif "暂停报警" in text or "Pause Alarm" in text:
                            button.config(text=lang.get_text("pause_alarm"))
                        elif "重置状态" in text or "Reset Status" in text:
                            button.config(text=lang.get_text("reset_status"))
        
        # 更新状态显示组件中的标题行
        for child in self.status_display.cam_status_frame.winfo_children():
            if isinstance(child, ttk.Frame) and child.winfo_children():  # 找到标题行框架
                header_labels = [widget for widget in child.winfo_children() if isinstance(widget, ttk.Label)]
                if header_labels:  # 确保有标签
                    for label in header_labels:
                        text = label.cget("text")
                        if text in ["状态", "Status"]:
                            label.config(text=lang.get_text("status"))
                        elif text in ["摄像头", "Camera"]:
                            label.config(text=lang.get_text("camera"))
                        elif text in ["报警级别", "Alarm Level"]:
                            label.config(text=lang.get_text("alarm_level"))
        
        # 更新摄像头状态标签
        for i, cam_label in enumerate(self.status_display.cam_status_labels):
            cam_label_parent = cam_label.master
            for child in cam_label_parent.winfo_children():
                if isinstance(child, ttk.Label):
                    text = child.cget("text")
                    if "摄像头" in text or "Camera" in text:
                        child.config(text=f"{lang.get_text('camera')} {i}")
        
        # 更新系统信息标签框
        for child in self.status_display.frame.winfo_children():
            if isinstance(child, ttk.LabelFrame):
                if child.cget("text") in ["系统信息", "System Info", "System Information"]:
                    child.config(text=lang.get_text("system_info"))
        
        # 更新状态文本
        self.status_display.set_status_text(lang.get_text("settings_updated"))
        
        logging.info(f"界面语言已更新为: {lang.get_language_name()}")
        
    def _apply_settings(self):
        """应用参数设置更新"""
        try:
            # 记录当前运行的摄像头
            running_cameras = []
            for cam_id in range(len(CONFIG.cameras)):
                if self.manager.get_processor(cam_id):
                    running_cameras.append(cam_id)
            
            # 获取设置面板的设置值
            settings = self.settings_panel.get_settings()
            
            # 更新手势检测灵敏度
            CONFIG.gesture_threshold = settings['gesture_threshold']
            
            # 更新报警间隔设置
            new_triggers = settings['alarm_triggers']
            if new_triggers:
                new_triggers.sort()
                CONFIG.alarm_triggers = new_triggers
                # 更新报警音频映射
                CONFIG.alarm_sounds = {
                    t: f"sounds/{t}S报警音.wav" if t < 30 else "sounds/alarm.wav"
                    for t in CONFIG.alarm_triggers
                }
                
            # 更新网格设置
            if 'grid_settings' in settings:
                grid_settings = settings['grid_settings']
                CONFIG.show_grid = grid_settings.get('grid_enabled', CONFIG.show_grid)
                CONFIG.grid_spacing_x = grid_settings.get('grid_spacing_x', CONFIG.grid_spacing_x)
                CONFIG.grid_spacing_y = grid_settings.get('grid_spacing_y', CONFIG.grid_spacing_y)
                
                # 更新所有运行中的摄像头的网格设置
                for cam_id, processor in self.manager.processors.items():
                    if hasattr(processor, 'grid_overlay'):
                        processor.grid_overlay.grid_enabled = CONFIG.show_grid
                        processor.grid_overlay.grid_spacing_x = CONFIG.grid_spacing_x
                        processor.grid_overlay.grid_spacing_y = CONFIG.grid_spacing_y
            
            # 更新ROI设置 - 为每个摄像头单独更新
            roi_updated = False
            for cam_id, roi in settings['roi_settings'].items():
                CONFIG.cameras[cam_id].roi = roi
                roi_updated = True
            
            # 如果ROI设置已更新且有摄像头正在运行，询问用户是否重启摄像头
            if roi_updated and running_cameras:
                restart = messagebox.askyesno(
                    lang.get_text("apply_settings"), 
                    "ROI设置已更新，是否重启摄像头以应用新设置？\n\n选择'是'将重启摄像头\n选择'否'将动态更新ROI设置（不中断监测）"
                )
                if restart:
                    # 停止所有运行的摄像头
                    self.manager.stop_all()
                    # 重新启动之前运行的摄像头
                    for cam_id in running_cameras:
                        try:
                            self.manager.start_camera(cam_id)
                            logging.info(f"摄像头 {cam_id} 已重启以应用新的ROI设置")
                        except Exception as e:
                            logging.error(f"重启摄像头 {cam_id} 失败: {str(e)}")
                            messagebox.showerror(lang.get_text("runtime_error"), f"{lang.get_text('camera_start_failed', cam_id)}: {str(e)}")
                else:
                    # 动态更新ROI设置，不重启摄像头
                    update_success = True
                    failed_cameras = []
                    for cam_id in running_cameras:
                        processor = self.manager.get_processor(cam_id)
                        if processor:
                            if not processor.update_roi():
                                update_success = False
                                failed_cameras.append(cam_id)
                                logging.warning(f"摄像头 {cam_id} ROI设置动态更新失败")
                    
                    if update_success:
                        self.status_display.set_status_text(lang.get_text("settings_updated"))
                        logging.info("ROI设置已动态更新，无需重启摄像头")
                    else:
                        if len(failed_cameras) == len(running_cameras):
                            # 所有摄像头更新失败
                            messagebox.showwarning(lang.get_text("config_error"), "所有摄像头ROI设置更新失败，建议重启摄像头以应用新设置。")
                            self.status_display.set_status_text(lang.get_text("settings_updated"))
                            logging.warning("所有摄像头ROI设置更新失败")
                        else:
                            # 部分摄像头更新失败
                            failed_str = ", ".join([str(cam) for cam in failed_cameras])
                            messagebox.showwarning(lang.get_text("config_error"), f"摄像头 {failed_str} 的ROI设置未能动态更新，建议重启这些摄像头以确保设置生效。")
                            self.status_display.set_status_text("ROI设置部分更新，建议重启部分摄像头")
                            logging.warning(f"摄像头 {failed_str} ROI设置更新失败")
            
            self.status_display.set_status_text(lang.get_text("settings_updated"))
            logging.info("参数设置已更新")
        except ValueError as e:
            messagebox.showerror(lang.get_text("config_error"), "请确保所有输入都是有效的数字")
            logging.error(f"参数设置更新失败: {str(e)}")
        except Exception as e:
            messagebox.showerror(lang.get_text("unknown_error"), f"更新设置失败: {str(e)}")
            logging.error(f"参数设置更新失败: {str(e)}")
            
    def start_selected(self):
        """启动选中的摄像头"""
        selected_cameras = self.camera_selector.get_selected()
        started_cameras = []
        
        for i in selected_cameras:
            try:
                self.manager.start_camera(i)
                started_cameras.append(i)
                self.status_display.set_status_text(lang.get_text("camera_running", i))
                logging.info(f"摄像头 {i} 已启动")
            except ValueError as e:
                messagebox.showerror(lang.get_text("config_error"), str(e))
                logging.error(f"摄像头{i}配置错误: {str(e)}")
            except RuntimeError as e:
                messagebox.showerror(lang.get_text("runtime_error"), str(e))
                logging.error(f"摄像头{i}运行错误: {str(e)}")
            except Exception as e:
                messagebox.showerror(lang.get_text("unknown_error"), f"摄像头{i}启动失败: {str(e)}")
                logging.error(f"摄像头{i}启动失败: {str(e)}")
        
        if not started_cameras:
            self.status_display.set_status_text(lang.get_text("select_camera"))
        elif len(started_cameras) > 1:
            self.status_display.set_status_text(lang.get_text("cameras_started", len(started_cameras)))
            
    def stop_all(self):
        """停止所有摄像头"""
        try:
            self.manager.stop_all()
            self.status_display.set_status_text(lang.get_text("system_stopped"))
            self._update_status()
            logging.info("所有摄像头已停止")
        except Exception as e:
            logging.error(f"停止摄像头失败: {str(e)}")
            messagebox.showerror("错误", f"停止摄像头失败: {str(e)}")
            
    def pause_alarm(self):
        """暂停所有报警声音"""
        try:
            for i in range(len(CONFIG.cameras)):
                processor = self.manager.get_processor(i)
                if processor:
                    processor.alarm_channel.stop()
            self.status_display.set_status_text(lang.get_text("alarm_paused"))
            logging.info("报警已暂停")
        except Exception as e:
            logging.error(f"暂停报警失败: {str(e)}")
            messagebox.showerror("错误", f"暂停报警失败: {str(e)}")
            
    def reset_status(self):
        """重置所有摄像头的检测状态"""
        try:
            for i in range(len(CONFIG.cameras)):
                processor = self.manager.get_processor(i)
                if processor:
                    processor._reset_alarm()
                    processor.alarm_channel.stop()
            self.status_display.set_status_text(lang.get_text("status_reset"))
            self._update_status()
            logging.info("所有摄像头状态已重置")
        except Exception as e:
            logging.error(f"重置状态失败: {str(e)}")
            messagebox.showerror("错误", f"重置状态失败: {str(e)}")
            
    def on_close(self):
        """窗口关闭事件处理"""
        try:
            logging.info("系统正在关闭...")
            self.stop_all()
            self.root.destroy()
        except Exception as e:
            logging.error(f"系统关闭异常: {str(e)}")
            
    def run(self):
        """运行主循环"""
        self.root.mainloop()
        
    def _start_status_update(self):
        """启动状态更新定时器"""
        self._update_status()
        self.time_display.update()  # 更新时间显示
        self.root.after(int(CONFIG.status_update_interval * 1000), self._start_status_update)
    
    def _update_status(self):
        """更新摄像头状态显示"""
        try:
            # 获取所有摄像头处理器
            processors = []
            for i in range(len(CONFIG.cameras)):
                processors.append(self.manager.get_processor(i))
            
            # 更新状态显示
            self.status_display.update_status(processors)
        except Exception as e:
            logging.error(f"更新状态失败: {str(e)}")