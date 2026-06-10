#!/bin/bash
# ARS4Hermes - Academic Research Skills for Hermes Agent
# Install from cloned repo: bash install.sh

set -e

SKILLS_DIR="${HERMES_HOME:-$HOME/.hermes}/skills/research"

echo "========================================"
echo " ARS4Hermes 安装脚本"
echo " 将 4 个学术研究技能安装到 Hermes Agent"
echo "========================================"
echo ""

# 检查技能目录是否存在
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$SCRIPT_DIR/skills/research"

if [ ! -d "$SKILL_SRC" ]; then
    echo "❌ 错误: 未找到 skills/research/ 目录"
    echo "   请确认你在仓库根目录运行此脚本"
    exit 1
fi

# 创建目标目录
mkdir -p "$SKILLS_DIR"

# 复制技能
echo "📦 正在安装技能..."

declare -A SKILL_NAMES
SKILL_NAMES[deep-research]="学术深度研究"
SKILL_NAMES[academic-paper]="学术论文写作"
SKILL_NAMES[academic-paper-reviewer]="多视角同行评审"
SKILL_NAMES[academic-pipeline]="全流程编排器"

for skill in deep-research academic-paper academic-paper-reviewer academic-pipeline; do
    if [ -d "$SKILL_SRC/$skill" ]; then
        cp -r "$SKILL_SRC/$skill" "$SKILLS_DIR/"
        echo "  ✅ ${SKILL_NAMES[$skill]} → $SKILLS_DIR/$skill/"
    else
        echo "  ⚠️  未找到: $skill"
    fi
done

echo ""
echo "========================================"
echo " ✅ 安装完成！"
echo "========================================"
echo ""
echo "技能已安装至: $SKILLS_DIR/"
echo ""
echo "🚀 快速开始 (在 Hermes 对话中输入):"
echo ""
echo "  ┌─────────────────────────────────────────────┐"
echo "  │ 启动学术全流程 你的选题                      │"
echo "  │ 开始深度研究 你的主题                        │"
echo "  │ 写学术论文 你的主题                          │"
echo "  │ 评审论文 你的论文路径                        │"
echo "  └─────────────────────────────────────────────┘"
echo ""
echo "📖 查看文档: docs/"
echo "📂 查看示例: example_output/"
