# -*- coding: utf-8 -*-
# modules/language.py
# 语言配置模块，负责管理系统的多语言支持

import logging
from config import CONFIG

class LanguageManager:
    """语言管理器类
    
    负责管理系统的多语言支持，提供中英文切换功能。
    使用单例模式确保全局只有一个语言管理器实例。
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageManager, cls).__new__(cls)
            cls._instance._init_language()
        return cls._instance
    
    def _init_language(self):
        """初始化语言设置"""
        # 从配置中加载默认语言设置
        self.current_language = CONFIG.language_preference
        self.languages = ["zh_CN", "en_US"]  # 支持的语言列表
        self.language_names = {
            "zh_CN": "中文",
            "en_US": "English"
        }
        
        # 初始化翻译字典
        self._init_translations()
    
    def _init_translations(self):
        """初始化翻译字典"""
        self.translations = {
            # 窗口标题
            "window_title": {
                "zh_CN": "ICU手部行为监测系统 v3.2",
                "en_US": "ICU Hand Behavior Monitoring System v3.2"
            },
            
            # 主题设置
            "theme_settings": {
                "zh_CN": "主题设置",
                "en_US": "Theme Settings"
            },
            "light_theme": {
                "zh_CN": "浅色",
                "en_US": "Light"
            },
            "dark_theme": {
                "zh_CN": "深色",
                "en_US": "Dark"
            },
            "auto_theme": {
                "zh_CN": "自动",
                "en_US": "Auto"
            },
            
            # 摄像头选择
            "camera_selection": {
                "zh_CN": "摄像头选择",
                "en_US": "Camera Selection"
            },
            "camera": {
                "zh_CN": "摄像头",
                "en_US": "Camera"
            },
            
            # 参数设置
            "parameter_settings": {
                "zh_CN": "参数设置",
                "en_US": "Parameter Settings"
            },
            "gesture_sensitivity": {
                "zh_CN": "手势检测灵敏度",
                "en_US": "Gesture Detection Sensitivity"
            },
            "alarm_interval": {
                "zh_CN": "报警间隔设置(秒)",
                "en_US": "Alarm Interval Settings (sec)"
            },
            "level": {
                "zh_CN": "级别",
                "en_US": "Level"
            },
            "roi_settings": {
                "zh_CN": "ROI设置",
                "en_US": "ROI Settings"
            },
            "width": {
                "zh_CN": "宽度",
                "en_US": "Width"
            },
            "height": {
                "zh_CN": "高度",
                "en_US": "Height"
            },
            "apply_settings": {
                "zh_CN": "应用设置",
                "en_US": "Apply Settings"
            },
            
            # 控制按钮
            "control_buttons": {
                "zh_CN": "控制按钮",
                "en_US": "Control Buttons"
            },
            "start_selected": {
                "zh_CN": "启动选中",
                "en_US": "Start Selected"
            },
            "stop_all": {
                "zh_CN": "停止所有",
                "en_US": "Stop All"
            },
            "pause_alarm": {
                "zh_CN": "暂停报警",
                "en_US": "Pause Alarm"
            },
            "reset_status": {
                "zh_CN": "重置状态",
                "en_US": "Reset Status"
            },
            
            # 状态信息
            "system_status": {
                "zh_CN": "系统状态",
                "en_US": "System Status"
            },
            "system_info": {
                "zh_CN": "系统信息",
                "en_US": "System Information"
            },
            "system_ready": {
                "zh_CN": "系统就绪",
                "en_US": "System Ready"
            },
            "status": {
                "zh_CN": "状态",
                "en_US": "Status"
            },
            "alarm_level": {
                "zh_CN": "报警级别",
                "en_US": "Alarm Level"
            },
            "detection_time": {
                "zh_CN": "检测时间",
                "en_US": "Detection Time"
            },
            "seconds": {
                "zh_CN": "秒",
                "en_US": "s"
            },
            "no_active_camera": {
                "zh_CN": "无活动摄像头",
                "en_US": "No Active Camera"
            },
            "system_running": {
                "zh_CN": "系统运行中",
                "en_US": "System Running"
            },
            "system_stopped": {
                "zh_CN": "系统已停止",
                "en_US": "System Stopped"
            },
            "camera_running": {
                "zh_CN": "摄像头 {} 运行中",
                "en_US": "Camera {} Running"
            },
            "select_camera": {
                "zh_CN": "请选择要启动的摄像头",
                "en_US": "Please select cameras to start"
            },
            "cameras_started": {
                "zh_CN": "已启动 {} 个摄像头",
                "en_US": "{} cameras started"
            },
            "alarm_paused": {
                "zh_CN": "报警已暂停",
                "en_US": "Alarm Paused"
            },
            "status_reset": {
                "zh_CN": "状态已重置",
                "en_US": "Status Reset"
            },
            "settings_updated": {
                "zh_CN": "设置已更新",
                "en_US": "Settings Updated"
            },
            
            # 错误信息
            "init_error": {
                "zh_CN": "初始化错误",
                "en_US": "Initialization Error"
            },
            "system_init_failed": {
                "zh_CN": "系统初始化失败",
                "en_US": "System initialization failed"
            },
            "config_error": {
                "zh_CN": "配置错误",
                "en_US": "Configuration Error"
            },
            "runtime_error": {
                "zh_CN": "运行错误",
                "en_US": "Runtime Error"
            },
            "unknown_error": {
                "zh_CN": "未知错误",
                "en_US": "Unknown Error"
            },
            "camera_start_failed": {
                "zh_CN": "摄像头{}启动失败",
                "en_US": "Camera {} start failed"
            },
            
            # 系统启动相关
            "creating_fallback_audio": {
                "zh_CN": "创建备用音频文件",
                "en_US": "Creating fallback audio file"
            },
            "system_starting": {
                "zh_CN": "系统启动中...",
                "en_US": "System starting..."
            },
            "system_crash": {
                "zh_CN": "系统崩溃",
                "en_US": "System crash"
            },
            "fatal_error": {
                "zh_CN": "致命错误",
                "en_US": "Fatal Error"
            },
            "unrecoverable_error": {
                "zh_CN": "系统发生不可恢复错误",
                "en_US": "System encountered an unrecoverable error"
            },
            
            # 语言设置
            "language_settings": {
                "zh_CN": "语言设置",
                "en_US": "Language Settings"
            },
            "chinese": {
                "zh_CN": "中文",
                "en_US": "Chinese"
            },
            "english": {
                "zh_CN": "英文",
                "en_US": "English"
            },
            
            # 时间显示
            "current_time": {
                "zh_CN": "当前时间",
                "en_US": "Current Time"
            }
        }
    
    def get_text(self, key, *args):
        """获取指定键的当前语言文本
        
        Args:
            key: 文本键名
            *args: 格式化参数
            
        Returns:
            str: 当前语言的文本
        """
        if key not in self.translations:
            return key  # 如果找不到翻译，返回键名本身
        
        text = self.translations[key].get(self.current_language, key)
        if args:
            try:
                return text.format(*args)
            except Exception:
                return text
        return text
    
    def switch_language(self, language_code):
        """切换语言
        
        Args:
            language_code: 语言代码，如'zh_CN'或'en_US'
            
        Returns:
            bool: 切换是否成功
        """
        if language_code in self.languages:
            self.current_language = language_code
            # 保存语言偏好到配置
            CONFIG.save_language_preference(language_code)
            return True
        return False
    
    def get_current_language(self):
        """获取当前语言代码"""
        return self.current_language
    
    def get_language_name(self, language_code=None):
        """获取语言名称
        
        Args:
            language_code: 语言代码，默认为当前语言
            
        Returns:
            str: 语言名称
        """
        if language_code is None:
            language_code = self.current_language
        return self.language_names.get(language_code, language_code)

# 创建全局语言管理器实例
lang = LanguageManager()

# 便捷函数，用于获取文本
def get_text(key, *args):
    """获取指定键的当前语言文本的便捷函数"""
    return lang.get_text(key, *args)