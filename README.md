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

## 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/lx02918/claude-usage-meter/main/install.sh | bash
```

保持 Chrome 或 Safari 登录 claude.ai 即可，无需任何手动配置。

**前提**：macOS + [Homebrew](https://brew.sh) + Python 3

## 文件结构

```
ClaudeMeter-SwiftBar/
└── claude_usage.5m.py    # 主脚本，SwiftBar 每 5 分钟自动执行
```

运行时缓存：
```
~/.config/claudemeter/org_id.txt    # organization UUID 缓存
```

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
| 脚本不执行 | 确认 shebang 第一行是 `/opt/homebrew/bin/python3` |
