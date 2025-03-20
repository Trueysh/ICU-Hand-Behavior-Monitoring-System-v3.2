# -*- coding: utf-8 -*-
# tests/test_video_processor.py
# 视频处理器测试模块

import unittest
import numpy as np
import cv2
import os
import sys
from unittest.mock import MagicMock, patch
from threading import Event

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.video_processor import VideoProcessor

class TestVideoProcessor(unittest.TestCase):
    """视频处理器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.stop_event = Event()
        # 模拟配置
        with patch('modules.video_processor.CONFIG') as mock_config:
            mock_config.cameras = [MagicMock()]
            mock_config.cameras[0].source = 0
            mock_config.cameras[0].resolution = (640, 480)
            mock_config.cameras[0].roi = {"x": 0, "y": 0, "w": 640, "h": 480}
            mock_config.cameras[0].min_confidence = 0.7
            mock_config.cameras[0].buffer_size = 3
            mock_config.fallback_sound = "test_sound.wav"
            
            # 创建测试对象
            self.processor = VideoProcessor(0, self.stop_event)
    
    def tearDown(self):
        """测试后清理"""
        self.stop_event.set()
        if hasattr(self, 'processor'):
            self.processor.release_resources()
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.processor.camera_id, 0)
        self.assertFalse(self.processor.alarm_active)
        self.assertEqual(self.processor.played_sounds, set())
    
    def test_process_frame_empty(self):
        """测试处理空帧"""
        # 模拟空帧
        empty_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # 模拟MediaPipe处理结果
        self.processor.mp_hands = MagicMock()
        self.processor.hands = MagicMock()
        self.processor.hands.process.return_value = MagicMock(multi_hand_landmarks=None)
        
        # 调用测试方法
        result_frame = self.processor.process_frame(empty_frame)
        
        # 验证结果
        self.assertIsNotNone(result_frame)
        self.assertEqual(result_frame.shape, empty_frame.shape)

if __name__ == '__main__':
    unittest.main()