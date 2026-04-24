# PulseClick - Windows 专用轻量级连点器

## 项目定位

PulseClick 是一款面向 Windows 10/11 的轻量级鼠标自动化连点器。产品目标是启动快、界面清爽、设置直觉、后台热键稳定、配置本地保存，并尽量减少第三方依赖。

## 设计原则

| 原则 | 说明 |
|------|------|
| Windows 专用 | 不承诺 Linux/macOS；输入、热键、配置路径、打包流程均以 Windows 原生体验为准 |
| 轻量 | 依赖最少化，优先标准库和 Win32 API，运行时内存目标 < 50MB |
| 简约 | 单窗口卡片式布局，核心设置一屏可见，零学习成本 |
| 可靠 | 点击线程可停止、热键可注销、退出时清理后台资源 |
| 本地安全 | 无联网、无广告、无后门；配置、档案和日志只写入项目内 `data/` |

## 技术选型

| 技术 | 用途 | 规则 |
|------|------|------|
| Python 3.10+ | 主语言 | 使用类型注解和 dataclass |
| PySide6 | GUI | 保留 Qt 原生渲染和 QSS 深色主题 |
| ctypes + Win32 API | 输入和热键 | 鼠标点击使用 `SendInput`，全局热键使用 `RegisterHotKey` |
| PyInstaller | 打包 | 仅生成 Windows 单文件 `PulseClick.exe` |
| JSON | 配置持久化 | 人类可读，便于备份和迁移 |

禁止重新引入跨平台输入库作为默认后端，例如 `pynput`。只有在明确做兼容实验时，才能放入隔离模块且不得改变 Windows 默认路径。

## v1 功能范围

- 鼠标按钮：左键、右键、中键
- 点击类型：单击、双击、三击
- 点击间隔：1ms 到 3600000ms
- 重复模式：无限循环或指定次数
- 位置模式：跟随光标或固定坐标
- 坐标拾取：覆盖层点击拾取屏幕坐标
- 全局热键：默认 F6，支持 Ctrl/Alt/Shift/Win 组合键
- 系统托盘：显示主窗口、开始、停止、退出
- 配置持久化：`data\config.json`
- 配置档案：`data\profiles\`
- 日志文件：`data\logs\pulseclick.log`
- 随机延迟：可设置最小/最大间隔
- 实时状态：运行状态、CPS、点击计数、运行时长

## 项目结构

```text
PulseClick/
├── main.py
├── build.py
├── requirements.txt
├── config/default.json
├── resources/
│   ├── icon.svg
│   └── styles.qss
├── src/
│   ├── app.py
│   ├── main.py
│   ├── core/
│   │   ├── clicker.py
│   │   ├── config.py
│   │   ├── hotkey.py
│   │   └── recorder.py
│   ├── platform/windows/
│   │   ├── input.py
│   │   └── paths.py
│   ├── ui/
│   │   ├── dialogs.py
│   │   ├── main_window.py
│   │   └── styles.py
│   └── utils/
│       ├── config.py
│       ├── logger.py
│       └── tray.py
└── tests/
```

## 开发规范

- 遵循 PEP 8，使用 Python 3.10+ 类型语法。
- 结构化设置使用 dataclass，不用散乱 dict 传递。
- 核心逻辑必须可注入 fake 后端测试，避免单元测试直接触发真实鼠标或全局热键。
- GUI 线程只更新界面；后台线程通过 Qt Signal 或线程安全回调回到 UI。
- 文件写入必须限制在项目根目录的 `data/` 或仓库工作区。
- 不测试 GUI 渲染；测试配置、热键解析、点击引擎状态机和 Windows 路径逻辑。

## 打包规范

- 打包命令：`python build.py`
- 目标产物：`dist\PulseClick.exe`
- 只支持 Windows 10/11。
- 打包脚本不得添加 Linux/macOS 分支。
- 发布说明必须提示：自动点击工具可能被部分游戏、反作弊或安全软件限制，用户应遵守相关平台规则。
