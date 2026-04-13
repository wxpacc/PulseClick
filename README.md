# PulseClick

轻量级、跨平台的鼠标自动化连点器软件

## 项目概述

PulseClick 是一款轻量级、跨平台的鼠标自动化连点器软件，设计理念为"简约而不简单"。它提供了直观的用户界面和丰富的功能，适用于游戏辅助、办公自动化、软件测试等场景。

- **轻量**：最小依赖，快速启动，运行时内存占用 < 50MB
- **简约**：卡片式布局，零学习成本，所有核心操作一目了然
- **跨平台**：支持 Windows、Linux 和 macOS
- **可靠**：毫秒级计时精度，长时间运行稳定不崩溃
- **安全**：开源透明，无广告无后门，配置本地存储

## 功能特性

### 核心功能

- **高精度点击引擎**：支持左键/右键/中键，单击/双击，毫秒级间隔控制
- **灵活的点击模式**：无限循环或指定次数，跟随光标或固定坐标
- **坐标拾取**：一键获取当前鼠标屏幕坐标
- **全局热键**：支持自定义热键（默认 F6 启停）
- **系统托盘**：最小化到系统托盘，后台运行
- **配置持久化**：自动保存和恢复设置
- **配置档案**：保存多组配置，快速切换不同场景
- **随机延迟**：防检测，模拟人类点击节奏
- **实时状态显示**：CPS（每秒点击次数）、已点击计数、运行时长

### 技术特性

- **现代化界面**：基于 PySide6 的深色主题，美观直观
- **跨平台兼容**：Windows、Linux、macOS 全支持
- **免安装便携**：PyInstaller 打包为单文件可执行
- **开源透明**：MIT 许可证，代码完全开放

## 系统要求

- **操作系统**：Windows 7+ / Linux (Ubuntu 18.04+) / macOS 10.14+
- **Python**：3.10+（仅开发环境）
- **依赖**：PySide6、pynput（仅开发环境）

## 安装方法

### Windows 版本

1. **从发布版安装**：
   - 访问 [GitHub Releases](https://github.com/wxpacc/PulseClick/releases) 页面
   - 下载 `PulseClick.exe` 文件
   - 双击运行即可，无需安装

2. **从源码构建**：
   ```bash
   git clone https://github.com/wxpacc/PulseClick.git
   cd PulseClick
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python src/main.py
   # 打包
   python build.py
   # 运行打包后的程序
   dist\PulseClick.exe
   ```

### macOS 版本

1. **从发布版安装**：
   - 访问 [GitHub Releases](https://github.com/wxpacc/PulseClick/releases) 页面
   - 下载 `PulseClick.app` 文件
   - 双击运行即可，无需安装

2. **从源码构建**：
   ```bash
   git clone https://github.com/wxpacc/PulseClick.git
   cd PulseClick
   python3 -m venv venv
   source venv/bin/activate
   pip3 install -r requirements.txt
   python3 src/main.py
   # 打包
   python3 build.py
   # 运行打包后的程序
   open dist/PulseClick.app
   ```

### Linux 版本

1. **从发布版安装**：
   - 访问 [GitHub Releases](https://github.com/wxpacc/PulseClick/releases) 页面
   - 下载 `PulseClick` 可执行文件
   - 赋予执行权限并运行：
     ```bash
     chmod +x PulseClick
     ./PulseClick
     ```

2. **从源码构建**：
   ```bash
   git clone https://github.com/wxpacc/PulseClick.git
   cd PulseClick
   python3 -m venv venv
   source venv/bin/activate
   pip3 install -r requirements.txt
   python3 src/main.py
   # 打包
   python3 build.py
   # 运行打包后的程序
   ./dist/PulseClick
   ```

## 使用说明

### 基本操作

1. **点击设置**：选择鼠标按钮（左键/右键/中键）、点击类型（单击/双击）、点击间隔和重复次数
2. **位置设置**：选择跟随光标或固定坐标，使用"拾取坐标"按钮获取屏幕坐标
3. **高级设置**：启用随机延迟，设置最小/最大间隔
4. **热键设置**：配置全局启停热键
5. **启动/停止**：点击界面按钮或使用热键控制

### 配置档案

1. **保存档案**：在设置完成后，点击"保存档案"按钮并输入名称
2. **加载档案**：从档案列表中选择已保存的配置
3. **管理档案**：重命名或删除已保存的档案

### 系统托盘

- 点击托盘图标：显示/隐藏主窗口
- 右键托盘图标：快速访问开始/停止/退出功能
- 托盘图标状态：绿色表示运行中，灰色表示空闲

## 开发指南

### 项目结构

```
PulseClick/
├── src/             # 源代码
│   ├── main.py      # 应用入口
│   ├── app.py       # 应用主类
│   ├── ui/          # 界面相关
│   ├── core/        # 核心逻辑
│   └── utils/       # 工具类
├── resources/       # 资源文件
├── config/          # 配置模板
├── tests/           # 测试文件
├── requirements.txt # 依赖项
├── build.py         # 打包脚本
└── README.md        # 本文档
```

### 开发规范

- **代码风格**：遵循 PEP 8，使用类型注解
- **命名约定**：模块（snake_case）、类（PascalCase）、函数（snake_case）
- **日志**：使用 Python 标准 logging 模块
- **测试**：使用 pytest，核心模块覆盖率 > 80%

### 构建与发布

- **打包命令**：`python build.py`
- **目标平台**：Windows (.exe)、Linux (AppImage)、macOS (.app)
- **打包大小**：Windows < 20MB，Linux < 25MB，macOS < 30MB

## 竞品对比

| 特性 | PulseClick | OP Auto Clicker | MouseClickTool | clicker.rs | rusty-autoclicker |
|------|-----------|----------------|---------------|-----------|-------------------|
| 跨平台 | ✅ Win/Mac/Linux | ❌ Win Only | ❌ Win Only | ✅ | ✅ |
| 轻量级 | ✅ <50MB | ✅ 1.13MB | ✅ 16KB | ✅ ~3MB | ✅ ~5MB |
| 现代UI | ✅ PySide6 | ✅ | ✅ | ✅ Iced | ✅ Iced |
| 全局热键 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 坐标拾取 | ✅ | ❌ | ❌ | ❌ | ✅ |
| 随机延迟 | ✅ | ❌ | ✅ | ✅ | ✅ |
| 配置档案 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 系统托盘 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 开源 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 免安装 | ✅ | ✅ | ✅ | ✅ | ✅ |

## 版本规划

### v1.0 - 核心版
- 点击引擎（按钮/模式/间隔/重复/位置）
- 全局热键
- 系统托盘
- 配置持久化
- 配置档案
- 随机延迟
- 实时状态显示
- 打包发布

### v2.0 - 增强版
- 键盘按键自动化
- 宏录制与回放
- 多显示器支持
- 浅色主题
- 命令行参数支持

### v3.0 - 专业版
- 颜色检测触发
- 图像识别触发
- 脚本编辑器
- 插件系统

## 贡献指南

1. **Fork 仓库**：在 GitHub 上 fork 项目仓库
2. **创建分支**：`git checkout -b feature/your-feature`
3. **提交更改**：`git commit -m "Add your feature"`
4. **推送分支**：`git push origin feature/your-feature`
5. **创建 PR**：在 GitHub 上提交 Pull Request

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 联系方式

- **GitHub**：[github.com/wxpacc/PulseClick](https://github.com/wxpacc/PulseClick)
- **Issues**：[提交问题](https://github.com/wxpacc/PulseClick/issues)
- **Email**：vkcew.r@gmail.com

---

**注意**：本工具仅用于合法用途，如游戏辅助、办公自动化、软件测试等。使用时请遵守相关平台的服务条款。