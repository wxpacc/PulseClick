# PulseClick - Windows 专用便携连点器

## 项目定位

PulseClick 是一款面向 Windows 10/11 的轻量级便携鼠标连点器。最终用户应能下载、解压、双击运行；删除整个软件目录即可卸载，不在 Windows 用户目录、注册表或系统目录留下配置、档案或日志。

## 设计原则

| 原则 | 说明 |
|------|------|
| Windows 专用 | 不承诺 Linux/macOS；输入、热键、打包流程均以 Windows 原生体验为准 |
| 便携优先 | 所有运行时数据写入程序目录下的 `data/` |
| 轻量 | 依赖最少化，优先标准库和 Win32 API |
| 简约 | 单窗口卡片式布局，核心设置一屏可见 |
| 可靠 | 点击线程可停止，热键可注销，退出时清理后台资源 |
| 本地安全 | 无联网、无广告、无后门 |

## 技术选型

| 技术 | 用途 | 规则 |
|------|------|------|
| Python 3.10+ | 主语言 | 使用类型注解和 dataclass |
| PySide6 | GUI | 保留 Qt 原生渲染和 QSS 深色主题 |
| ctypes + Win32 API | 输入和热键 | 鼠标点击使用 `SendInput`，全局热键使用 `RegisterHotKey` |
| PyInstaller | 打包 | 生成 Windows 单文件 `PulseClick.exe` |
| JSON | 配置持久化 | 人类可读，便于备份和迁移 |

禁止把 `pynput` 或其他跨平台输入库重新作为默认后端。后续功能必须保持 Windows 原生和便携存储这两个核心约束。

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
├── data/.gitkeep
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
├── tests/
└── dist/PulseClick.exe
```

`dist/` 是发布产物目录，默认被 Git 忽略。交付用户时只需要 `PulseClick.exe`；`data/` 会在首次运行后自动生成。

## 开发规范

- 遵循 PEP 8，使用 Python 3.10+ 类型语法。
- 结构化设置使用 dataclass，不用散乱 dict 传递。
- 核心逻辑必须可注入 fake 后端测试，避免单元测试直接触发真实鼠标或全局热键。
- GUI 线程只更新界面；后台线程通过 Qt Signal 或线程安全回调回到 UI。
- 文件写入必须限制在程序根目录的 `data/` 或仓库工作区。
- 不测试 GUI 渲染；测试配置、热键解析、点击引擎状态机和便携路径逻辑。

## 打包与发布

- 开发环境安装依赖：`pip install -r requirements.txt`
- 打包命令：`python build.py`
- 目标产物：`dist\PulseClick.exe`
- 只支持 Windows 10/11。
- `build\`、`PulseClick.spec`、`dist\data\` 都是可清理文件。
- 发布前确认 `dist\PulseClick.exe` 能启动，并删除 `dist\data\`。
- 发布说明必须提示：自动点击工具可能被部分游戏、反作弊或安全软件限制，用户应遵守相关平台规则。

