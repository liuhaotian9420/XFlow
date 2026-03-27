# xyf-competition-mvp

这是主 README。

这份文档只解决一件事：让一个第一次接手项目的人，在新的 Windows 电脑上，把正式版 `real` 模式成功跑起来。

如果你完全不熟悉 Python、PowerShell、uv，也没关系，按顺序照着做就行。

## 最终成功标准

启动成功后，你应该能打开这 3 个地址：

- 前端页面：`http://localhost:8501`
- 后端接口：`http://127.0.0.1:8000`
- 接口文档：`http://127.0.0.1:8000/docs`

正式启动命令是：

```powershell
.\scripts\start-real.ps1
```

## 先理解一件事

对外发布用的是 `real` 模式。

所以新人接手项目时，重点不是 `mock`，而是把下面这些东西配好：

- Python
- uv
- 项目代码
- `.env`
- Codex CLI
- ODPS 配置

`mock` 只适合开发排障，不是正式发布入口。

## 从零开始操作

下面的步骤不要跳。

### 第 1 步：安装 Git

1. 打开：`https://git-scm.com/download/win`
2. 下载并安装 Git
3. 安装完成后，重新打开 PowerShell
4. 输入：

```powershell
git --version
```

如果能看到版本号，说明 Git 安装成功。

### 第 2 步：安装 Python

1. 打开：`https://www.python.org/downloads/windows/`
2. 下载 Python `3.12` 或更高版本
3. 安装时，一定勾选 `Add python.exe to PATH`
4. 安装完成后，重新打开 PowerShell
5. 输入：

```powershell
python --version
```

如果能看到 `Python 3.12.x` 或更高版本，说明 Python 安装成功。

### 第 3 步：安装 uv

在 PowerShell 输入：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安装完成后，关闭 PowerShell，再重新打开一个新的 PowerShell，输入：

```powershell
uv --version
```

如果能看到版本号，说明 `uv` 安装成功。

### 第 4 步：把代码放到本地

如果你有仓库地址，输入：

```powershell
git clone <仓库地址>
cd xyf-competition-mvp
```

如果你是直接拿到压缩包并解压，也可以。总之最后要进入项目根目录。

项目根目录里应该能看到这些文件：

- `README.md`
- `.env.example`
- `pyproject.toml`
- `scripts\start-real.ps1`

### 第 5 步：允许 PowerShell 运行脚本

如果你第一次运行 `.ps1` 脚本时报权限错误，就输入：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

如果系统询问是否继续，输入 `Y`。

### 第 6 步：创建 `.env`

在项目根目录输入：

```powershell
Copy-Item .env.example .env
```

执行完成后，你会在项目根目录看到一个新的 `.env` 文件。

### 第 7 步：填写 `.env`

用记事本、VS Code 或任何文本编辑器打开 `.env`。

至少要填写这些项：

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

你可以先这样理解：

- `APP_MODE=real`
  - 表示正式模式
- `CODEX_CLI_COMMAND` 或 `CODEX_BINARY`
  - 告诉程序去哪里找 Codex CLI
- `ODPS_ACCESS_KEY_ID`
- `ODPS_ACCESS_KEY_SECRET`
- `ODPS_PROJECT`
- `ODPS_ENDPOINT`
  - 这些是访问真实数据需要的配置

如果你不知道这些值该填什么，就去找项目负责人、平台同学或者给你交接环境的人要。

### 第 8 步：检查 Codex CLI

你需要先确认这台电脑上的 Codex CLI 本身是可用的。

如果你们团队有固定安装方式，按团队方式安装。

装好后，确保 `.env` 里的 `CODEX_CLI_COMMAND` 或 `CODEX_BINARY` 指向正确位置。

### 第 9 步：先做启动前检查

在项目根目录输入：

```powershell
uv run python scripts/preflight.py --mode real
```

只有这条命令执行成功，并且输出里明确看到：

```text
APP_MODE: real
```

才说明当前机器的正式模式配置基本齐了。

如果这里报错，不要直接启动，先修报错。

常见报错大致就是两类：

- Codex 没配置好
- ODPS 没配置好

### 第 10 步：正式启动

在项目根目录输入：

```powershell
.\scripts\start-real.ps1
```

这个脚本会自动做这些事：

- 检查 `python`
- 检查 `uv`
- 检查 `.env` 是否存在
- 执行 `uv sync`
- 执行正式模式预检查
- 通过后再启动前后端

## 如果失败，先看哪里

### 情况 1：提示 `python is not installed or not on PATH`

说明 Python 没装好，或者没有加到系统路径里。

处理方法：

1. 重新安装 Python
2. 勾选 `Add python.exe to PATH`
3. 重新打开 PowerShell
4. 再执行：

```powershell
python --version
```

### 情况 2：提示 `uv is not installed or not on PATH`

说明 `uv` 没装好，或者安装后没有重新打开 PowerShell。

处理方法：

1. 重新安装 `uv`
2. 关闭当前 PowerShell
3. 打开新的 PowerShell
4. 再执行：

```powershell
uv --version
```

### 情况 3：提示 `.env not found`

说明你还没有创建 `.env`。

执行：

```powershell
Copy-Item .env.example .env
```

然后把 `.env` 填好，再重试。

### 情况 4：`preflight` 检查失败

这是最关键的一类错误。

处理方法：

1. 先看报错里写的是 `Codex` 没准备好，还是 `ODPS` 没准备好
2. 回到 `.env` 检查对应配置
3. 修完后再执行：

```powershell
uv run python scripts/preflight.py --mode real
```

并确认输出里是：

```text
APP_MODE: real
```

只有这里通过了，再去执行：

```powershell
.\scripts\start-real.ps1
```

### 情况 5：PowerShell 不让你运行脚本

执行：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

然后重试。

### 情况 6：页面打不开

先看启动后弹出来的两个 PowerShell 窗口。

真正的错误信息通常都在那里，不在浏览器里。

### 情况 7：端口被占用

如果 `8000` 或 `8501` 已经被别的程序占用了，应用可能起不来。

先关闭旧程序，再重新启动。

## 只在排障时才用 Demo

`demo` 不是正式发布入口。

只有在下面这种场景，才建议临时使用：

- 你怀疑不是账号配置问题，而是本机 Python 或依赖环境有问题
- 你只是想快速确认前后端壳子能不能起来

临时启动命令：

```powershell
.\scripts\start-demo.ps1
```

但正常交付、正常验收、正常对外演示，都应该以 `real` 模式为准。

## 你真正要记住的命令

```powershell
python --version
uv --version
Copy-Item .env.example .env
uv run python scripts/preflight.py --mode real
.\scripts\start-real.ps1
```

## 补充

- 主 README 是中文。
- [README.zh-CN.md](C:/Users/haotian.liu/Documents/GitHub/xyf-competition-mvp/README.zh-CN.md) 也保留了一份中文手册。
