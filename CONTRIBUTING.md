# 贡献指南

感谢您对ICU手部行为监测系统的关注！我们欢迎任何形式的贡献，包括但不限于功能改进、bug修复、文档完善等。

## 贡献流程

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 代码规范

### Python 代码风格
- 遵循 PEP 8 规范
- 使用 4 个空格进行缩进
- 每行最大长度为 120 字符
- 使用类型提示（Type Hints）
- 为所有函数和类添加文档字符串

### 提交规范
提交信息应遵循以下格式：
```
<type>(<scope>): <subject>

<body>

<footer>
```

类型（type）包括：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

### 示例
```
feat(camera): 添加多摄像头支持

- 实现多摄像头并行处理
- 添加摄像头切换功能
- 优化资源占用

Closes #123
```

## 开发环境设置

1. 安装依赖
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 开发依赖
```

2. 运行测试
```bash
python -m pytest tests/
```

## 注意事项

- 在提交 PR 前，请确保所有测试都已通过
- 新功能请添加相应的单元测试
- 保持代码简洁，遵循 DRY（Don't Repeat Yourself）原则
- 及时更新文档

## 行为准则

请保持友善和专业，尊重所有社区成员。我们致力于维护一个开放、包容的社区环境。

## 许可证

通过贡献代码，您同意您的贡献将在MIT许可证下发布。

## 联系我们

如有任何问题，请通过 Issues 与我们联系。