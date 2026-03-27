# xyf-competition-mvp

> 主 README 在这里：[README.md](README.md)

这份手册的目标只有一个：

让第一次接手项目的人，在新的 Windows 电脑上，把正式版 `real` 模式跑起来。

## 先记住正式启动命令

```powershell
.\scripts\start-real.ps1
```

启动成功后，你应该能打开：

- 前端：`http://localhost:8501`
- 后端：`http://127.0.0.1:8000`
- 文档：`http://127.0.0.1:8000/docs`

## 正式版依赖什么

你至少要准备好这些东西：

- Git
- Python 3.12+
- uv
- 项目代码
- `.env`
- Codex CLI
- ODPS 配置

## 从零开始操作

### 1. 安装 Git

打开：

`https://git-scm.com/download/win`

安装完成后，在 PowerShell 输入：

```powershell
git --version
```

### 2. 安装 Python 3.12+

打开：

`https://www.python.org/downloads/windows/`

安装时一定勾选：

`Add python.exe to PATH`

安装完成后，在 PowerShell 输入：

```powershell
python --version
```

### 3. 安装 uv

在 PowerShell 输入：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

然后关闭 PowerShell，再重新打开，输入：

```powershell
uv --version
```

### 4. 获取代码

如果你有仓库地址，输入：

```powershell
git clone <仓库地址>
cd xyf-competition-mvp
```

### 5. 如果脚本不能运行

在 PowerShell 输入：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

如果系统提示确认，输入 `Y`。

### 6. 创建 `.env`

进入项目根目录后，输入：

```powershell
Copy-Item .env.example .env
```

### 7. 填写 `.env`

至少填写这些：

```env
APP_MODE=real
API_BASE_URL=http://127.0.0.1:8000
CODEX_CLI_COMMAND=
CODEX_BINARY=
CODEX_MODEL=
CODEX_REASONING_EFFORT=
ODPS_ACCESS_KEY_ID=
ODPS_ACCESS_KEY_SECRET=
ODPS_PROJECT=
ODPS_ENDPOINT=
```

如果你不知道这些值是什么，就去问项目负责人或环境交接人。

### 8. 检查正式环境

在 PowerShell 输入：

```powershell
uv run python scripts/preflight.py --mode real
```

只有这一步执行成功，并且输出里明确看到：

```text
APP_MODE: real
```

才说明正式环境真的基本配好了。

如果这一步报错，先修报错，不要直接启动。

### 9. 正式启动

在 PowerShell 输入：

```powershell
.\scripts\start-real.ps1
```

## 如果失败怎么办

### 找不到 Python

重新安装 Python，并勾选：

`Add python.exe to PATH`

### 找不到 uv

重新安装 `uv`，然后重新打开 PowerShell。

### 找不到 `.env`

执行：

```powershell
Copy-Item .env.example .env
```

### `preflight` 失败

说明 Codex 或 ODPS 配置还没好。

先修 `.env`，再执行：

```powershell
uv run python scripts/preflight.py --mode real
```

并确认输出里是：

```text
APP_MODE: real
```

### PowerShell 不允许执行脚本

执行：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 页面打不开

先看启动时弹出来的 PowerShell 窗口，错误通常在那里。

### 端口被占用

关闭占用 `8000` 或 `8501` 的旧程序，再重新启动。

## Demo 只用于排障

`demo` 不是正式入口。

只有你怀疑是本机环境问题时，才临时执行：

```powershell
.\scripts\start-demo.ps1
```

正式交付、正式验收、正式演示，都以 `real` 模式为准。

## 最后记住这几个命令

```powershell
python --version
uv --version
Copy-Item .env.example .env
uv run python scripts/preflight.py --mode real
.\scripts\start-real.ps1
```
