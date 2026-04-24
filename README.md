# PulseClick

PulseClick 是一款 Windows 10/11 专用的轻量级鼠标连点器。它使用 PySide6 构建界面，鼠标点击和全局热键走 Windows 原生 API，适合办公自动化、软件测试和允许自动化的本地场景。

## 功能

- 左键、右键、中键点击
- 单击、双击、三击
- 1ms 到 1 小时点击间隔
- 无限循环或指定次数
- 跟随光标或固定坐标
- 屏幕覆盖层拾取坐标
- 默认 F6 全局启停热键，支持组合键
- 系统托盘后台运行
- 随机延迟
- 配置档案
- 实时 CPS、点击计数和运行时长

## Windows 开发运行

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

配置、档案和日志默认保存在项目文件夹内的 `data` 目录，不写入 Windows 用户目录：

```text
PulseClick\data\config.json
PulseClick\data\profiles\
PulseClick\data\logs\pulseclick.log
```

## 测试

```powershell
pytest
```

测试覆盖配置读写、热键解析和点击引擎状态机。测试不会直接触发真实鼠标点击。

## 打包

```powershell
python build.py
```

打包产物位于：

```text
dist\PulseClick.exe
```

## 注意事项

- 本项目仅支持 Windows 10/11。
- 全局热键依赖 Windows `RegisterHotKey`，如果组合键已被其他软件占用，需要更换热键。
- 鼠标点击使用 Windows `SendInput`；部分游戏、反作弊或安全软件可能限制模拟输入。
- 请只在合法、合规、被允许的场景使用自动点击功能。
