# PulseClick - 轻量级连点器

## 项目概述

PulseClick 是一款轻量级、跨平台的鼠标自动化连点器软件。设计理念为"简约而不简单"——界面清爽、操作直觉、功能充足、资源占用极低。适用于游戏辅助、办公自动化、软件测试等场景。

## 设计哲学

| 原则 | 说明 |
|------|------|
| **轻量** | 最小依赖，快速启动，运行时内存占用 < 50MB |
| **简约** | 卡片式布局，零学习成本，所有核心操作一目了然 |
| **跨平台** | Windows / Linux 全支持 |
| **可靠** | 毫秒级计时精度，长时间运行稳定不崩溃 |
| **安全** | 开源透明，无广告无后门，配置本地存储 |

## 技术选型

| 技术 | 用途 | 选择理由 |
|------|------|----------|
| Python 3.10+ | 主语言 | 跨平台、生态丰富、开发效率高 |
| PySide6 | GUI框架 | 原生 Qt 渲染、精美现代UI、跨平台一致体验、QSS样式支持 |
| pynput | 鼠标/键盘控制 | 跨平台全局热键+事件模拟、API简洁 |
| PyInstaller | 打包工具 | 单文件可执行、免安装便携 |
| JSON | 配置持久化 | 人类可读、Python原生支持、轻量 |

## 功能规格

### 核心功能（v1.0 MVP）

#### 1. 点击引擎
- 鼠标按钮选择：左键 / 右键 / 中键
- 点击模式：单击 / 双击
- 点击间隔：1ms ~ 3600000ms（1小时），支持毫秒级精度
- 重复模式：无限循环 / 指定次数（1 ~ 999999）
- 位置模式：跟随光标 / 固定坐标
- 坐标拾取：一键获取当前鼠标屏幕坐标

#### 2. 全局热键
- 开始/停止热键（默认 F6）
- 支持组合键（Ctrl+Alt+X 等）
- 热键自定义，冲突检测

#### 3. 系统托盘
- 最小化到系统托盘
- 托盘右键菜单：显示主窗口 / 开始 / 停止 / 退出
- 托盘图标状态指示（运行中/空闲）

#### 4. 配置持久化
- 自动保存当前所有设置
- 启动时自动恢复上次配置
- JSON 格式存储，便于手动编辑/备份
- 配置文件路径：`~/.pulseclick/config.json`

#### 5. 配置档案
- 保存多组配置档案
- 快速切换不同场景配置
- 档案重命名与删除

#### 6. 随机延迟（防检测）
- 启用/禁用随机延迟
- 最小/最大间隔设置
- 模拟人类点击节奏

#### 7. 实时状态显示
- 运行状态指示（绿色运行/灰色空闲）
- 实时 CPS（每秒点击次数）
- 已完成点击计数
- 运行时长计时

## 界面设计

### 布局方案

```
┌───────────────────────────────────────────┐
│  PulseClick                           ─ □ ✕ │
├───────────────────────────────────────────┤
│                                           │
│  ┌─────────────────────────────────────┐  │
│  │  核心设置                           │  │
│  ├─────────────────────────────────────┤  │
│  │  鼠标按钮: 左 ○ 右 ○ 中 ○           │  │
│  │  点击类型: 单击 ○ 双击 ○            │  │
│  │  点击间隔: [100] ms                 │  │
│  │  重复模式: 无限 ○ 次数 ○ [100]       │  │
│  └─────────────────────────────────────┘  │
│                                           │
│  ┌─────────────────────────────────────┐  │
│  │  位置设置                           │  │
│  ├─────────────────────────────────────┤  │
│  │  位置模式: 跟随 ○ 固定 ○            │  │
│  │  固定坐标: X: [640]  Y: [480]       │  │
│  │  [拾取坐标]                          │  │
│  └─────────────────────────────────────┘  │
│                                           │
│  ┌─────────────────────────────────────┐  │
│  │  高级设置                           │  │
│  ├─────────────────────────────────────┤  │
│  │  [x] 启用随机延迟                   │  │
│  │  延迟范围: [80] ms - [120] ms       │  │
│  │  配置档案: [默认] [保存] [加载]      │  │
│  └─────────────────────────────────────┘  │
│                                           │
│  ┌─────────────────────────────────────┐  │
│  │  热键设置                           │  │
│  ├─────────────────────────────────────┤  │
│  │  启停热键: [F6] [修改]              │  │
│  └─────────────────────────────────────┘  │
│                                           │
│  ┌─────────────────────────────────────┐  │
│  │  状态面板                           │  │
│  ├─────────────────────────────────────┤  │
│  │  ● 空闲  │ CPS: 0.0  │ 点击: 0      │  │
│  └─────────────────────────────────────┘  │
│                                           │
│              [ ▶ 启动 ]                  │
│                                           │
└───────────────────────────────────────────┘
```

### 视觉规范
- 主题：深色主题（默认）
- 主色调：#1a1a2e（背景）、#16213e（卡片）、#0f3460（强调）、#e94560（高亮/运行状态）
- 字体：系统默认无衬线字体，12px 正文 / 14px 标题
- 圆角：8px（卡片）、6px（按钮）、4px（输入框）
- 间距：10px 基准网格，组内间距 12px
- 窗口尺寸：380×600px
- 控件高度：24px 基准，按钮高度 28px
- 输入框宽度：90px（数值输入），120px（下拉选择）
- 按钮宽度：50-60px（小按钮），120px（主按钮）

## 项目结构

```
PulseClick/
├── src/
│   ├── __init__.py
│   ├── main.py                 # 应用入口
│   ├── app.py                  # 应用主类（生命周期管理）
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py      # 主窗口
│   │   ├── widgets.py          # 自定义组件
│   │   ├── styles.py           # QSS 样式定义
│   │   └── dialogs.py          # 对话框（坐标拾取、档案管理）
│   ├── core/
│   │   ├── __init__.py
│   │   ├── clicker.py          # 点击引擎（核心逻辑）
│   │   ├── hotkey.py           # 全局热键管理
│   │   └── recorder.py         # 坐标拾取器
│   └── utils/
│       ├── __init__.py
│       ├── config.py           # 配置读写与档案管理
│       ├── tray.py             # 系统托盘
│       └── logger.py           # 日志工具
├── resources/
│   ├── icon.png                # 应用图标
│   ├── tray.png                # 托盘图标
│   └── styles.qss              # 样式文件
├── config/
│   └── default.json            # 默认配置模板
├── tests/
│   ├── __init__.py
│   ├── test_clicker.py
│   ├── test_hotkey.py
│   ├── test_config.py
│   └── test_integration.py
├── requirements.txt
├── setup.py
├── build.py                    # PyInstaller 打包脚本
├── agents.md
└── .ignore
```

## 核心模块设计

### clicker.py - 点击引擎

```python
class ClickEngine:
    """核心点击引擎，运行在独立线程中"""

    def __init__(self, config: ClickConfig):
        self.config = config
        self._running = False
        self._thread: threading.Thread | None = None
        self._click_count = 0
        self._start_time: float | None = None

    def start(self) -> None: ...
    def stop(self) -> None: ...
    def _click_loop(self) -> None: ...
    def _perform_click(self, x: int, y: int) -> None: ...
    def get_cps(self) -> float: ...
    def get_click_count(self) -> int: ...
    def get_elapsed(self) -> float: ...

@dataclass
class ClickConfig:
    button: str = "left"           # left / right / middle
    click_type: str = "single"     # single / double
    interval_ms: int = 100
    repeat_mode: str = "infinite"  # infinite / count
    repeat_count: int = 1000
    position_mode: str = "follow"  # follow / fixed
    fixed_x: int = 0
    fixed_y: int = 0
    random_enabled: bool = False
    random_min: int = 80
    random_max: int = 120
```

### hotkey.py - 全局热键

```python
class HotkeyManager:
    """全局热键管理，基于 pynput"""

    def __init__(self):
        self._hotkeys: dict[str, Callable] = {}
        self._listener: keyboard.Listener | None = None

    def register(self, key_combo: str, callback: Callable) -> None: ...
    def unregister(self, key_combo: str) -> None: ...
    def start_listening(self) -> None: ...
    def stop_listening(self) -> None: ...
    def parse_combo(self, combo_str: str) -> tuple: ...
```

### config.py - 配置管理

```python
class ConfigManager:
    """JSON 配置文件读写与档案管理"""

    CONFIG_DIR = Path.home() / ".pulseclick"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    PROFILES_DIR = CONFIG_DIR / "profiles"

    def load(self) -> dict: ...
    def save(self, config: dict) -> None: ...
    def get_default(self) -> dict: ...
    def save_profile(self, name: str, config: dict) -> None: ...
    def load_profile(self, name: str) -> dict: ...
    def list_profiles(self) -> list[str]: ...
    def delete_profile(self, name: str) -> None: ...
```

## 开发规范

### 代码风格
- 遵循 PEP 8
- 类型注解必须（Python 3.10+ 语法，使用 `X | Y` 而非 `Union`）
- 使用 dataclass 而非 dict 传递结构化数据
- 异步操作使用 threading，不使用 asyncio（GUI 线程安全）

### 命名约定
- 模块：snake_case
- 类：PascalCase
- 函数/方法：snake_case
- 常量：UPPER_SNAKE_CASE
- 私有成员：_前缀

### 日志规范
- 使用 Python 标准 logging 模块
- 级别：DEBUG（开发）/ INFO（关键操作）/ WARNING（异常但可恢复）/ ERROR（严重错误）
- 日志文件：`~/.pulseclick/pulseclick.log`
- 日志轮转：最大 5MB，保留 3 个备份

### 测试规范
- 使用 pytest
- 核心模块单元测试覆盖率 > 80%
- 集成测试覆盖主流程
- 不测试 GUI 渲染，只测试逻辑

### 打包规范
- 使用 PyInstaller 打包为单文件可执行
- 打包命令：`python build.py` 或 `pyinstaller PulseClick.spec`
- 目标平台：Windows (.exe)、Linux (可执行文件)、macOS (.app)
- 打包后大小：Windows < 20MB，Linux < 25MB，macOS < 30MB

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
- 多显示器支持

### v3.0 - 专业版
（暂未规划）
