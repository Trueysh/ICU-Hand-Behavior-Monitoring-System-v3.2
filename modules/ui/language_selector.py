# -*- coding: utf-8 -*-
# modules/ui/language_selector.py
# 语言选择器组件，用于在UI界面中提供语言切换功能

import tkinter as tk
from tkinter import ttk
import logging
from modules.language import lang

class LanguageSelector:
    """语言选择器组件
    
    提供语言切换功能的UI组件，允许用户在界面上切换系统语言。
    """
    def __init__(self, parent, callback=None):
        """初始化语言选择器
        
        Args:
            parent: 父级窗口组件
            callback: 语言切换后的回调函数
        """
        self.frame = ttk.LabelFrame(parent, text=lang.get_text("language_settings"), padding=5)
        self.language_var = tk.StringVar(value=lang.get_current_language())
        self.callback = callback
        
        # 创建语言选择单选按钮
        self.chinese_radio = ttk.Radiobutton(
            self.frame, 
            text=lang.get_text("chinese"), 
            value="zh_CN", 
            variable=self.language_var, 
            command=self._on_language_change
        )
        self.chinese_radio.pack(side=tk.LEFT, padx=5)
        
        self.english_radio = ttk.Radiobutton(
            self.frame, 
            text=lang.get_text("english"), 
            value="en_US", 
            variable=self.language_var, 
            command=self._on_language_change
        )
        self.english_radio.pack(side=tk.LEFT, padx=5)
    
    def _on_language_change(self):
        """语言变更处理"""
        new_language = self.language_var.get()
        if lang.switch_language(new_language):
            logging.info(f"已切换语言到: {lang.get_language_name()}")
            if self.callback:
                self.callback()
    
    def pack(self, **kwargs):
        """打包组件"""
        self.frame.pack(**kwargs)
    
    def update_text(self):
        """更新组件文本"""
        self.frame.config(text=lang.get_text("language_settings"))
        self.chinese_radio.config(text=lang.get_text("chinese"))
        self.english_radio.config(text=lang.get_text("english"))