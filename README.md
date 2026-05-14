# Claude Usage Meter — SwiftBar Plugin

Real-time Claude.ai Pro usage in your macOS menu bar. Reads browser cookies automatically — zero configuration.

[中文文档](README.zh.md)

## Preview

```
███░░░░░░░ 29%          ← menu bar (green / orange / red)
─────────────────
Session (5h)  ██░░░░░░  29%
  Resets in 2h 10m
Weekly  (7d)  ███░░░░░  36%
  Resets in 2h 20m
─────────────────
Updated 10:39
Refresh
```

## Prerequisites

**macOS 13+** and the following tools:

### 1. Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After installation, follow the prompt to add Homebrew to your PATH (Apple Silicon Macs require one extra step shown at the end of the installer).

### 2. Python 3

```bash
brew install python3
```

### 3. Log in to Claude.ai

Log in to [claude.ai](https://claude.ai) in **Chrome or Safari** and stay logged in. The script reads your browser's auth cookies automatically — no manual steps needed.

---

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/lx02918/claude-usage-meter/main/install.sh | bash
```

The menu bar item appears immediately after installation and refreshes every 5 minutes.

---

## Color thresholds

| Usage | Color |
|---|---|
| 0–69% | Green |
| 70–89% | Orange |
| ≥90% | Red |

## How it works

1. Reads all `claude.ai` cookies from Chrome/Safari via `browser_cookie3`
2. Makes an authenticated request to `claude.ai/api/organizations/{uuid}/usage` (all cookies required — Cloudflare blocks requests with only `sessionKey`)
3. Renders `five_hour.utilization` as the menu bar primary display

## Troubleshooting

| Issue | Fix |
|---|---|
| `⚠ Claude 403` in menu bar | Re-login to claude.ai in Chrome |
| org_id errors | `rm ~/.config/claudemeter/org_id.txt` then refresh |
| Menu bar shows plain text "claude" | Python path issue — re-run the install script |
