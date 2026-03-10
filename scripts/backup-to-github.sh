#!/bin/bash

# OpenClaw 配置备份脚本
# 备份到 GitHub 仓库
# 用法：./backup-to-github.sh

set -e

# 配置
BACKUP_ROOT="$HOME/.openclaw"
WORKSPACE="$BACKUP_ROOT/workspace"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
COMMIT_MSG="Backup: $TIMESTAMP"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 创建临时备份目录
BACKUP_DIR=$(mktemp -d)
log_info "创建临时备份目录：$BACKUP_DIR"

# 复制需要备份的文件
log_info "开始备份配置文件..."

# 1. openclaw.json (主配置)
if [ -f "$BACKUP_ROOT/openclaw.json" ]; then
    cp "$BACKUP_ROOT/openclaw.json" "$BACKUP_DIR/"
    log_info "✓ openclaw.json"
fi

# 2. cron/jobs.json (定时任务)
if [ -f "$BACKUP_ROOT/cron/jobs.json" ]; then
    mkdir -p "$BACKUP_DIR/cron"
    cp "$BACKUP_ROOT/cron/jobs.json" "$BACKUP_DIR/cron/"
    log_info "✓ cron/jobs.json"
fi

# 3. workspace/skills/ (技能)
if [ -d "$WORKSPACE/skills" ]; then
    cp -r "$WORKSPACE/skills" "$BACKUP_DIR/"
    log_info "✓ workspace/skills/"
fi

# 4. workspace/memory/ (记忆)
if [ -d "$WORKSPACE/memory" ]; then
    cp -r "$WORKSPACE/memory" "$BACKUP_DIR/"
    log_info "✓ workspace/memory/"
fi

# 5. workspace/*.md (其他配置文件)
for file in SOUL.md USER.md MEMORY.md IDENTITY.md TOOLS.md AGENTS.md HEARTBEAT.md; do
    if [ -f "$WORKSPACE/$file" ]; then
        cp "$WORKSPACE/$file" "$BACKUP_DIR/"
        log_info "✓ workspace/$file"
    fi
done

# 6. 持仓清单
if [ -f "$WORKSPACE/memory/stock-portfolio.md" ]; then
    log_info "✓ stock-portfolio.md"
fi

# 检查 Git 配置
log_info "检查 Git 配置..."

cd "$WORKSPACE"

if [ ! -d ".git" ]; then
    log_error "workspace 目录没有初始化 Git 仓库"
    log_info "请先执行以下命令初始化："
    echo "  cd $WORKSPACE"
    echo "  git init"
    echo "  git remote add origin <your-github-repo-url>"
    exit 1
fi

# 检查 remote
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [ -z "$REMOTE_URL" ]; then
    log_error "未配置 Git remote"
    log_info "请执行：git remote add origin <your-github-repo-url>"
    exit 1
fi

log_info "Git remote: $REMOTE_URL"

# 复制备份文件到 workspace 临时目录
BACKUP_IN_WORKSPACE="$WORKSPACE/.backup-configs"
mkdir -p "$BACKUP_IN_WORKSPACE"
cp -r "$BACKUP_DIR/"* "$BACKUP_IN_WORKSPACE/"

# Git 操作
log_info "执行 Git 操作..."

cd "$WORKSPACE"

# 添加备份文件
git add .backup-configs/

# 检查是否有变更
if git diff --cached --quiet; then
    log_info "没有检测到配置变更，跳过提交"
    rm -rf "$BACKUP_IN_WORKSPACE"
    rm -rf "$BACKUP_DIR"
    exit 0
fi

# 提交
git commit -m "$COMMIT_MSG"
log_info "✓ 提交成功"

# 推送到 GitHub
log_info "推送到 GitHub..."
if git push origin main 2>/dev/null || git push origin master 2>/dev/null; then
    log_info "✓ 推送成功"
else
    log_warn "推送失败，可能是网络问题或需要认证"
    log_info "请检查 Git 配置和网络连接"
fi

# 清理备份目录（保留在 git 中，但删除临时文件）
rm -rf "$BACKUP_IN_WORKSPACE"
rm -rf "$BACKUP_DIR"

# 提交清理变更
git add .backup-configs/ 2>/dev/null || true
if ! git diff --cached --quiet; then
    git commit -m "Cleanup backup temp files"
    git push origin main 2>/dev/null || git push origin master 2>/dev/null || true
fi

log_info "================================"
log_info "备份完成！"
log_info "时间：$TIMESTAMP"
log_info "仓库：$REMOTE_URL"
log_info "================================"
