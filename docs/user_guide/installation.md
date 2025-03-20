# 安装指南

本文档提供ICU手部行为监测系统的详细安装步骤。

## 系统要求

### 操作系统
- Windows 10/11
- Ubuntu 20.04+
- macOS 10.15+

### 硬件要求
- CPU: Intel Core i5或同等性能（多摄像头设置推荐i7）
- 内存: 8GB RAM（推荐16GB以获得最佳性能）
- 摄像头: 720p或更高分辨率USB摄像头（最多支持3个摄像头）
- 存储: 500MB可用空间
- 显卡: 集成显卡足够（独立GPU可提升性能）

## 安装步骤

### 1. 克隆仓库
```bash
git clone https://github.com/yourusername/ICU_Mediapipe.git
cd ICU_Mediapipe
```

### 2. 创建虚拟环境
```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 验证安装
运行以下命令启动系统：
```bash
python main.py
```

如果系统成功启动并显示主界面，则表示安装成功。

## 常见问题

### 依赖安装失败
如果在安装依赖时遇到问题，请尝试以下解决方案：

1. 确保您的Python版本为3.9或更高
2. 更新pip到最新版本：`pip install --upgrade pip`
3. 对于Windows用户，某些依赖可能需要安装Visual C++ Build Tools

### 摄像头检测问题
如果系统无法检测到摄像头：

1. 确保摄像头已正确连接并被操作系统识别
2. 检查是否有其他应用程序正在使用摄像头
3. 尝试在`config.py`中手动设置摄像头ID

## 更多帮助

如需更多帮助，请参考以下资源：

- [配置说明](configuration.md)
- [使用说明](usage.md)
- [GitHub Issues](https://github.com/yourusername/ICU_Mediapipe/issues)