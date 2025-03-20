# 配置说明

本文档提供ICU手部行为监测系统的详细配置指南。

## 配置文件概述

系统的主要配置文件是`config.py`，它包含了所有可自定义的系统参数。配置文件采用Python类的形式组织，主要包括以下几个部分：

- 摄像头配置
- 界面设置
- 语言设置
- 手势检测参数
- 报警设置
- 日志设置
- 性能优化参数

## 摄像头配置

```python
self.cameras: List[CameraConfig] = [
    CameraConfig(
        source=0,
        roi={"x": 200, "y": 100, "w": 800, "h": 600},
        min_confidence=0.8,
        resolution=(1280, 720)
    ),
    # 更多摄像头配置...
]
```

### 参数说明

- `source`: 视频源（摄像头ID或视频文件路径）
- `roi`: 感兴趣区域，格式为 {"x": int, "y": int, "w": int, "h": int}
- `min_confidence`: 手势检测的最小置信度阈值（0-1之间）
- `resolution`: 视频分辨率，格式为 (width, height)
- `enabled`: 是否启用该摄像头（默认为True）
- `buffer_size`: 视频缓冲区大小（帧数）
- `auto_reconnect`: 断开连接后是否自动重连（默认为True）
- `reconnect_delay`: 重连等待时间（秒）

## 界面设置

```python
# 界面设置
self.font_path: str = "sounds/simhei.ttf"
self.font_size: int = 24
self.show_fps: bool = True
self.show_roi: bool = True
self.window_title: str = "ICU手部行为监测系统 v3.2"
self.status_update_interval: float = 1.0  # 状态更新间隔（秒）
```

### 参数说明

- `font_path`: 字体文件路径（默认为sounds/simhei.ttf，黑体字体文件位于sounds目录下）
- `font_size`: 字体大小
- `show_fps`: 是否显示帧率
- `show_roi`: 是否显示ROI区域
- `window_title`: 窗口标题
- `status_update_interval`: 状态更新间隔（秒）

## 语言设置

```python
# 语言设置
self.language_preference: str = "zh_CN"  # 默认使用中文
```

### 参数说明

- `language_preference`: 语言偏好，可选值为"zh_CN"（中文）或"en_US"（英文）

## 手势检测参数

```python
# 手势检测参数
self.gesture_threshold: float = 0.8
self.detection_interval: float = 0.1  # 检测间隔（秒）
self.smooth_factor: float = 0.3  # 平滑因子（0-1）
```

### 参数说明

- `gesture_threshold`: 手势检测阈值（0-1之间）
- `detection_interval`: 检测间隔（秒）
- `smooth_factor`: 平滑因子（0-1之间），用于平滑手部轨迹

## 报警设置

```python
# 报警设置
self.alarm_triggers: List[int] = [5, 10, 15, 30]
self.alarm_sounds: Dict[int, str] = {
    t: f"sounds/{t}S报警音.wav" if t < 30 else "sounds/alarm.wav"
    for t in self.alarm_triggers
}
self.fallback_sound: str = "sounds/fallback_beep.wav"
self.alarm_volume: float = 1.0  # 音量（0-1）
```

### 参数说明

- `alarm_triggers`: 报警触发时间列表（秒）
- `alarm_sounds`: 报警声音文件映射
- `fallback_sound`: 备用报警声音文件
- `alarm_volume`: 报警音量（0-1之间）

## 日志设置

```python
# 日志设置
self.log_file: str = os.path.join("logs", "system.log")
self.log_max_size: int = 10 * 1024 * 1024  # 10MB
self.log_backup_count: int = 5
self.log_level: int = logging.INFO
```

### 参数说明

- `log_file`: 日志文件路径
- `log_max_size`: 日志文件最大大小（字节）
- `log_backup_count`: 日志文件备份数量
- `log_level`: 日志级别

## 性能优化参数

```python
# 性能优化参数
self.thread_pool_size: int = 6  # 线程池大小
self.frame_buffer_size: int = 3
self.max_fps: Optional[int] = 30  # 限制帧率以优化性能
```

### 参数说明

- `thread_pool_size`: 线程池大小，用于并行处理多个摄像头
- `frame_buffer_size`: 帧缓冲区大小
- `max_fps`: 最大帧率限制，用于优化性能

## 配置验证

系统在启动时会自动验证所有配置参数的有效性，包括：

- ROI区域是否在有效范围内
- 音频文件是否存在
- 字体文件是否可用
- 其他参数的合理性

如果发现无效的配置，系统会记录警告日志或抛出异常。

## 配置示例

以下是一个完整的配置示例：

```python
# 创建自定义配置
config = SystemConfig()

# 修改摄像头配置
config.cameras[0].roi = {"x": 100, "y": 50, "w": 1000, "h": 700}
config.cameras[0].min_confidence = 0.7

# 修改界面设置
config.show_fps = False
config.window_title = "ICU监控系统 - 病房A"

# 修改语言设置
config.language_preference = "en_US"

# 修改报警设置
config.alarm_triggers = [3, 8, 12, 20]  # 自定义报警时间
config.alarm_volume = 0.8  # 降低音量

# 验证配置
config.validate()
```

## 常见问题

### 如何永久保存配置？

当前版本的系统不支持自动保存配置到文件。如需永久修改配置，请直接编辑`config.py`文件。

### 如何为不同环境创建不同配置？

您可以创建多个配置文件（如`config_dev.py`、`config_prod.py`），并在启动系统时指定要使用的配置文件。

### 配置文件格式是否会在未来版本中更改？

我们计划在未来版本中引入基于JSON或YAML的配置文件格式，以便更容易地进行配置管理。