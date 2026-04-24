# PulseClick

PulseClick 是一款 Windows 10/11 专用的轻量级便携连点器。它不需要安装，下载后解压即可使用；配置、档案和日志都保存在软件目录内，删除整个目录即可完整卸载。

## 当前状态

- 产品形态：Windows 便携软件
- 最终产物：`dist\PulseClick.exe`
- 输入后端：Windows `SendInput`
- 全局热键：Windows `RegisterHotKey`
- 配置存储：软件同级目录下的 `data\`
- 默认热键：`F6`

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

## 直接使用

当前已构建好的可执行文件位于：

```text
dist\PulseClick.exe
```

双击 `PulseClick.exe` 即可启动。第一次运行后，会在 exe 同级目录自动生成：

```text
dist\data\config.json
dist\data\profiles\
dist\data\logs\pulseclick.log
```

要作为便携软件分发，可以把 `dist` 文件夹改名为 `PulseClick`：

```text
PulseClick\
├── PulseClick.exe
└── data\              # 首次运行后自动生成
```

卸载时先从托盘退出程序，然后删除整个 `PulseClick` 文件夹即可。

## 开发运行

如果需要从源码运行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

源码运行时，配置和日志会写入项目根目录：

```text
data\config.json
data\profiles\
data\logs\pulseclick.log
```

## 测试

```powershell
pytest
```

测试覆盖配置读写、热键解析、点击引擎状态机和便携路径逻辑。测试不会直接触发真实鼠标点击。

## 重新打包

```powershell
python build.py
```

打包成功后会生成：

```text
dist\PulseClick.exe
```

`build\` 和 `PulseClick.spec` 是打包临时文件，可以删除。`dist\data\` 是运行时数据，也可以在发布前删除。

## 注意事项

- 仅支持 Windows 10/11。
- 如果 `F6` 已被其他软件占用，请在界面里改成其他组合键。
- 鼠标点击使用 Windows `SendInput`，部分游戏、反作弊或安全软件可能限制模拟输入。
- 请只在合法、合规、被允许的场景使用自动点击功能。

