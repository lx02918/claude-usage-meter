#!/bin/bash
set -e

PLUGIN_DIR="$HOME/.config/claudemeter/plugins"
SCRIPT_URL="https://raw.githubusercontent.com/lx02918/claude-usage-meter/main/claude_usage.5m.py"

echo "→ Claude Usage Meter 安装中..."

# Homebrew
if ! command -v brew &>/dev/null; then
  echo "✗ 需要先安装 Homebrew: https://brew.sh"
  exit 1
fi

# SwiftBar
if [ ! -d "/Applications/SwiftBar.app" ]; then
  echo "→ 安装 SwiftBar..."
  brew install --cask swiftbar
fi

# browser-cookie3
echo "→ 安装 Python 依赖..."
python3 -m pip install browser-cookie3 --break-system-packages -q 2>/dev/null \
  || pip3 install browser-cookie3 --break-system-packages -q

# 插件目录
mkdir -p "$PLUGIN_DIR"

# 下载脚本
echo "→ 下载插件脚本..."
curl -fsSL "$SCRIPT_URL" -o "$PLUGIN_DIR/claude_usage.5m.py"
chmod +x "$PLUGIN_DIR/claude_usage.5m.py"

# 修正 python3 路径（兼容 Homebrew Intel/Apple Silicon）
PYTHON_PATH=$(which python3)
sed -i '' "1s|.*|#!$PYTHON_PATH|" "$PLUGIN_DIR/claude_usage.5m.py"

# 配置 SwiftBar 插件目录
defaults write com.ameba.SwiftBar PluginDirectory "$PLUGIN_DIR"

# 启动 SwiftBar
killall SwiftBar 2>/dev/null || true
sleep 1
open /Applications/SwiftBar.app

echo ""
echo "✓ 安装完成！"
echo "  保持 Chrome 或 Safari 登录 claude.ai 即可，无需任何手动配置。"
echo "  菜单栏会出现用量显示，每 5 分钟自动刷新。"
