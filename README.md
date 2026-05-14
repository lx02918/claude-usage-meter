# Claude Usage Meter — SwiftBar Plugin

macOS 菜单栏实时显示 Claude.ai Pro 用量。自动从浏览器读取认证，零配置。

## 效果

```
███░░░░░░░ 29%          ← 菜单栏（绿/橙/红随用量变色）
─────────────────
Session (5h)  ██░░░░░░  29%
  Resets in 2h 10m
Weekly  (7d)  ███░░░░░  36%
  Resets in 2h 20m
─────────────────
Updated 10:39
Refresh
```

## 前提条件

**macOS 13+** 和以下工具（按顺序装）：

### 1. Homebrew

Homebrew 是 macOS 的包管理器，用来安装后续工具。

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

安装完后按提示把 Homebrew 加入 PATH（Apple Silicon Mac 需要额外一步，安装结束时会有提示）。

### 2. Python 3

macOS 自带的 Python 版本过旧，用 Homebrew 装一个：

```bash
brew install python3
```

### 3. 登录 Claude.ai

在 **Chrome 或 Safari** 中登录 [claude.ai](https://claude.ai)，保持登录状态。脚本会自动读取浏览器的认证 Cookie，无需手动操作。

---

## 一键安装

前提条件满足后，运行：

```bash
curl -fsSL https://raw.githubusercontent.com/lx02918/claude-usage-meter/main/install.sh | bash
```

完成后菜单栏会出现用量显示，每 5 分钟自动刷新。

---

## 颜色阈值

| 用量 | 颜色 |
|---|---|
| 0–69% | 绿色 |
| 70–89% | 橙色 |
| ≥90% | 红色 |

## 工作原理

1. 用 `browser_cookie3` 从 Chrome/Safari 读取全部 `claude.ai` cookies
2. 携带 cookies（含 Cloudflare clearance）请求 `claude.ai/api/organizations/{uuid}/usage`
3. 解析 `five_hour.utilization` 和 `seven_day.utilization` 渲染菜单栏

> 只带 `sessionKey` 单个 cookie 会被 Cloudflare 以 403 拦截，必须带全部 cookies。

## 故障排查

| 问题 | 解决 |
|---|---|
| 菜单栏显示 `⚠ Claude 403` | 在 Chrome 重新登录 claude.ai |
| org_id 相关报错 | `rm ~/.config/claudemeter/org_id.txt` 再刷新 |
| 菜单栏只显示文字「claude」| Homebrew python3 路径问题，重新跑一遍安装脚本 |
