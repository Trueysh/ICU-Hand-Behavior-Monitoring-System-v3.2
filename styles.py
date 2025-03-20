# -*- coding: utf-8 -*-
# styles.py: UI样式定义模块

class UIStyles:
    """UI样式类，定义系统界面的颜色、字体和样式
    
    主要功能：
    - 提供统一的颜色方案
    - 定义不同主题（浅色/深色/蓝色）
    - 提供字体和按钮样式
    - 提供高级UI效果（渐变、阴影等）
    """
    
    # 主题定义
    THEMES = {
        "light": {
            "bg": "#f5f7fa",
            "fg": "#2c3e50",
            "accent": "#3498db",
            "success": "#2ecc71",
            "warning": "#f39c12",
            "error": "#e74c3c",
            "button_bg": "#ecf0f1",
            "button_fg": "#2c3e50",
            "button_active": "#3498db",
            "frame_bg": "#ffffff",
            "border": "#dfe6e9",
            "hover": "#d6eaf8",
            "gradient_start": "#3498db",
            "gradient_end": "#2980b9",
            "shadow": "#bdc3c7"
        },
        "dark": {
            "bg": "#2d3436",
            "fg": "#dfe6e9",
            "accent": "#74b9ff",
            "success": "#00b894",
            "warning": "#fdcb6e",
            "error": "#ff7675",
            "button_bg": "#353b48",
            "button_fg": "#dfe6e9",
            "button_active": "#74b9ff",
            "frame_bg": "#2d3436",
            "border": "#636e72",
            "hover": "#0984e3",
            "gradient_start": "#6c5ce7",
            "gradient_end": "#a29bfe",
            "shadow": "#1e272e"
        },
        "blue": {
            "bg": "#e3f2fd",
            "fg": "#0d47a1",
            "accent": "#1976d2",
            "success": "#43a047",
            "warning": "#ff9800",
            "error": "#e53935",
            "button_bg": "#bbdefb",
            "button_fg": "#0d47a1",
            "button_active": "#1976d2",
            "frame_bg": "#ffffff",
            "border": "#90caf9",
            "hover": "#64b5f6",
            "gradient_start": "#2196f3",
            "gradient_end": "#1976d2",
            "shadow": "#bbdefb"
        }
    }
    
    # 默认主题
    DEFAULT_THEME = "light"
    
    # 字体设置
    FONTS = {
        "title": ("Microsoft YaHei", 18, "bold"),
        "subtitle": ("Microsoft YaHei", 16, "bold"),
        "heading": ("Microsoft YaHei", 14, "bold"),
        "body": ("Microsoft YaHei", 12, "normal"),
        "small": ("Microsoft YaHei", 10, "normal"),
        "button": ("Microsoft YaHei", 12, "normal"),
        "monospace": ("Consolas", 12, "normal"),
        "status": ("Microsoft YaHei", 13, "bold")
    }
    
    # 按钮样式
    BUTTON_STYLES = {
        "normal": {
            "padding": (12, 6),
            "border_width": 1,
            "border_radius": 6,
            "shadow_depth": 2,
            "hover_effect": True,
            "transition_ms": 150
        },
        "small": {
            "padding": (8, 4),
            "border_width": 1,
            "border_radius": 4,
            "shadow_depth": 1,
            "hover_effect": True,
            "transition_ms": 100
        },
        "large": {
            "padding": (16, 10),
            "border_width": 1,
            "border_radius": 8,
            "shadow_depth": 3,
            "hover_effect": True,
            "transition_ms": 200
        },
        "pill": {
            "padding": (12, 6),
            "border_width": 1,
            "border_radius": 20,
            "shadow_depth": 2,
            "hover_effect": True,
            "transition_ms": 150
        },
        "flat": {
            "padding": (12, 6),
            "border_width": 0,
            "border_radius": 4,
            "shadow_depth": 0,
            "hover_effect": True,
            "transition_ms": 100
        },
        "icon": {
            "padding": (10, 10),
            "border_width": 0,
            "border_radius": 20,
            "shadow_depth": 1,
            "hover_effect": True,
            "transition_ms": 100
        }
    }
    
    # 状态颜色
    STATUS_COLORS = {
        "normal": "#43a047",  # 绿色
        "detecting": "#ff9800",  # 橙色
        "alarm": "#e53935",  # 红色
        "disabled": "#9e9e9e"  # 灰色
    }
    
    # 报警级别颜色
    ALARM_LEVEL_COLORS = {
        0: "#43a047",  # 绿色 - 无报警
        1: "#ffeb3b",  # 黄色 - 5秒报警
        2: "#ff9800",  # 橙色 - 10秒报警
        3: "#f44336",  # 红色 - 15秒报警
        4: "#d32f2f"   # 深红色 - 30秒报警
    }
    
    @classmethod
    def get_theme(cls, theme_name=None):
        """获取指定主题的颜色方案
        
        Args:
            theme_name: 主题名称，默认为None，使用默认主题
            
        Returns:
            dict: 主题颜色方案
        """
        if not theme_name:
            theme_name = cls.DEFAULT_THEME
        return cls.THEMES.get(theme_name, cls.THEMES[cls.DEFAULT_THEME])
    
    @classmethod
    def get_status_color(cls, status, theme_name=None):
        """获取状态对应的颜色
        
        Args:
            status: 状态名称
            theme_name: 主题名称
            
        Returns:
            str: 颜色代码
        """
        theme = cls.get_theme(theme_name)
        if status == "normal":
            return cls.STATUS_COLORS["normal"]
        elif status == "detecting":
            return cls.STATUS_COLORS["detecting"]
        elif status == "alarm":
            return cls.STATUS_COLORS["alarm"]
        else:
            return cls.STATUS_COLORS["disabled"]
    
    # UI效果设置
    UI_EFFECTS = {
        "shadows": {
            "light": {
                "color": "#00000022",
                "offset_x": 2,
                "offset_y": 2,
                "blur_radius": 5
            },
            "medium": {
                "color": "#00000033",
                "offset_x": 4,
                "offset_y": 4,
                "blur_radius": 8
            },
            "heavy": {
                "color": "#00000044",
                "offset_x": 6,
                "offset_y": 6,
                "blur_radius": 12
            }
        },
        "animations": {
            "fast": 150,  # 毫秒
            "normal": 300,
            "slow": 500
        },
        "gradients": {
            "blue": ("#3498db", "#2980b9"),
            "green": ("#2ecc71", "#27ae60"),
            "red": ("#e74c3c", "#c0392b"),
            "purple": ("#9b59b6", "#8e44ad"),
            "orange": ("#f39c12", "#d35400"),
            "gray": ("#95a5a6", "#7f8c8d")
        },
        "card": {
            "padding": 15,
            "border_radius": 8,
            "shadow_depth": "medium",
            "border_width": 1
        },
        "panel": {
            "padding": 20,
            "border_radius": 10,
            "shadow_depth": "light",
            "border_width": 1
        }
    }
    
    @classmethod
    def get_alarm_level_color(cls, level):
        """获取报警级别对应的颜色
        
        Args:
            level: 报警级别
            
        Returns:
            str: 颜色代码
        """
        return cls.ALARM_LEVEL_COLORS.get(level, cls.ALARM_LEVEL_COLORS[0])
        
    @classmethod
    def get_shadow(cls, depth="medium"):
        """获取阴影效果设置
        
        Args:
            depth: 阴影深度，可选值为light、medium、heavy
            
        Returns:
            dict: 阴影效果设置
        """
        return cls.UI_EFFECTS["shadows"].get(depth, cls.UI_EFFECTS["shadows"]["medium"])
    
    @classmethod
    def get_animation_duration(cls, speed="normal"):
        """获取动画持续时间
        
        Args:
            speed: 动画速度，可选值为fast、normal、slow
            
        Returns:
            int: 动画持续时间（毫秒）
        """
        return cls.UI_EFFECTS["animations"].get(speed, cls.UI_EFFECTS["animations"]["normal"])
    
    @classmethod
    def get_gradient(cls, color="blue"):
        """获取渐变色
        
        Args:
            color: 渐变色名称
            
        Returns:
            tuple: 渐变起始和结束颜色
        """
        return cls.UI_EFFECTS["gradients"].get(color, cls.UI_EFFECTS["gradients"]["blue"])
    
    @classmethod
    def get_card_style(cls):
        """获取卡片样式
        
        Returns:
            dict: 卡片样式设置
        """
        return cls.UI_EFFECTS["card"]
    
    @classmethod
    def get_panel_style(cls):
        """获取面板样式
        
        Returns:
            dict: 面板样式设置
        """
        return cls.UI_EFFECTS["panel"]