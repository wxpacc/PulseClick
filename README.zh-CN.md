# PulseClick

[English](README.md)

**最新版本：** [PulseClick v1.0.0](https://github.com/wxpacc/PulseClick/releases/tag/v1.0.0)  
**直接下载：** [PulseClick.exe](https://github.com/wxpacc/PulseClick/releases/download/v1.0.0/PulseClick.exe)

PulseClick 是一款 Windows 10/11 专用的轻量级便携连点器。它不需要安装，下载后双击即可使用；配置、档案和日志都保存在软件目录内，删除整个目录即可完整卸载。

## 下载使用

推荐从 GitHub Release 下载稳定版：

- 最新发布页：[PulseClick v1.0.0](https://github.com/wxpacc/PulseClick/releases/tag/v1.0.0)
- 直接下载：[PulseClick.exe](https://github.com/wxpacc/PulseClick/releases/download/v1.0.0/PulseClick.exe)
- SHA256：`8046fddbe5eff47343677f7e170bc4619712a1b6c699ac4c5ef362b69b0cf0c9`

下载后双击 `PulseClick.exe` 即可启动。首次运行后，程序会在 exe 同级目录自动生成：

```text
data\config.json
data\profiles\
data\logs\pulseclick.log
```

卸载时先从托盘退出程序，然后删除整个 `PulseClick` 文件夹即可。

## 功能

- 左键、右键、中键点击
- 单击、双击、三击
- 1ms 到 1 小时点击间隔
- 无限循环或指定次数
- 跟随光标或固定坐标
- 屏幕覆盖层拾取坐标
- 默认 F6 全局启停热键，支持 Ctrl/Alt/Shift/Win 组合键
- 系统托盘后台运行
- 随机延迟
- 配置档案
- 实时 CPS、点击计数和运行时长

## 当前状态

- 产品形态：Windows 便携软件
- 发布产物：`PulseClick.exe`
- 输入后端：Windows `SendInput`
- 全局热键：Windows `RegisterHotKey`
- 配置存储：软件同级目录下的 `data\`
- 默认热键：`F6`

## 从源码运行

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

`build\` 和 `PulseClick.spec` 是打包临时文件，可以删除。`dist\data\` 是运行时数据，发布前不要打包给用户。

## 注意事项

- 仅支持 Windows 10/11。
- 如果 `F6` 已被其他软件占用，请在界面里改成其他组合键。
- 鼠标点击使用 Windows `SendInput`，部分游戏、反作弊或安全软件可能限制模拟输入。
- 请只在合法、合规、被允许的场景使用自动点击功能。
