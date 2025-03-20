# 文档目录

此目录包含ICU手部行为监测系统的详细文档。

## 文档目录结构

- `user_guide/` - 用户指南
  - `installation.md` - 安装指南
  - `configuration.md` - 配置说明
  - `usage.md` - 使用说明
- `developer_guide/` - 开发者指南
  - `architecture.md` - 系统架构
  - `api_reference.md` - API参考
  - `contributing.md` - 贡献指南

## 项目目录结构

- `config.py` - 系统配置文件
- `main.py` - 系统主程序入口
- `modules/` - 系统核心模块
  - `camera_manager.py` - 摄像头管理模块
  - `fps_counter.py` - 帧率计数器
  - `language.py` - 语言支持模块
  - `video_processor.py` - 视频处理模块
  - `ui/` - 用户界面组件
    - `components.py` - UI基础组件
    - `control_panel.py` - 控制面板
    - `language_selector.py` - 语言选择器
- `sounds/` - 音频和字体资源
  - `5S报警音.wav` - 5秒报警音效
  - `10S报警音.wav` - 10秒报警音效
  - `15S报警音.wav` - 15秒报警音效
  - `alarm.WAV` - 30秒紧急报警音效
  - `fallback_beep.wav` - 备用报警音效
  - `simhei.ttf` - 黑体字体文件（用于界面显示）
- `data/` - 数据和资源文件
  - `UI.png` - 系统界面预览图
- `logs/` - 日志文件目录
  - `system.log` - 系统运行日志