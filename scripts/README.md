# OpenClaw 自动备份到 GitHub

## 概述

每天凌晨 2 点自动备份 OpenClaw 配置到 GitHub 仓库。

## 备份内容

- ✅ `~/.openclaw/openclaw.json` - 主配置（频道、插件等）
- ✅ `~/.openclaw/cron/jobs.json` - 定时任务配置
- ✅ `~/.openclaw/workspace/skills/` - 所有技能文件
- ✅ `~/.openclaw/workspace/memory/` - 记忆文件
- ✅ `~/.openclaw/workspace/*.md` - 配置文件（SOUL.md, USER.md, MEMORY.md 等）

## 首次配置

### 1. 创建 GitHub 仓库

在 GitHub 上创建一个私有仓库（推荐）或公有仓库：
```
https://github.com/your-username/openclaw-backup
```

### 2. 初始化 Git 仓库

```bash
cd /home/admin/.openclaw/workspace
git init
git remote add origin https://github.com/your-username/openclaw-backup.git
```

### 3. 配置 Git 用户信息

```bash
git config user.name "Your Name"
git config user.email "your-email@example.com"
```

### 4. 配置 Git 认证（推荐方式）

**方式 A: 使用 SSH（推荐）**
```bash
# 生成 SSH key（如果没有）
ssh-keygen -t ed25519 -C "your-email@example.com"

# 将公钥添加到 GitHub
cat ~/.ssh/id_ed25519.pub
# 复制输出内容，添加到 GitHub Settings > SSH and GPG keys

# 更改 remote 为 SSH 方式
git remote set-url origin git@github.com:your-username/openclaw-backup.git
```

**方式 B: 使用 Personal Access Token**
```bash
# 在 GitHub 生成 token: Settings > Developer settings > Personal access tokens
# 权限：repo (Full control of private repositories)

# 使用 token 克隆
git remote set-url origin https://your-token@github.com/your-username/openclaw-backup.git
```

**方式 C: 使用 Git Credential Manager**
```bash
# 首次 push 时会弹出浏览器进行认证
git push -u origin main
```

### 5. 手动测试备份

```bash
/home/admin/.openclaw/workspace/scripts/backup-to-github.sh
```

### 6. 验证

检查 GitHub 仓库是否收到提交。

## 自动执行

已配置 cron 任务，每天凌晨 2 点自动执行：
- 任务 ID: `backup-to-github-0200`
- 执行时间：每天 02:00 (Asia/Shanghai)

## 手动触发

```bash
# 通过 CLI 运行 cron 任务
openclaw cron run backup-to-github-0200

# 或直接运行脚本
/home/admin/.openclaw/workspace/scripts/backup-to-github.sh
```

## 查看备份历史

```bash
# 查看 cron 任务执行历史
openclaw cron runs --id backup-to-github-0200

# 查看 Git 提交历史
cd /home/admin/.openclaw/workspace
git log --oneline

# 查看 GitHub 仓库
https://github.com/your-username/openclaw-backup/commits/main
```

## 注意事项

### ⚠️ 敏感信息

`openclaw.json` 可能包含敏感信息：
- API Keys
- Client Secrets
- Tokens

**建议：**
1. 使用私有仓库
2. 定期轮换密钥
3. 考虑使用环境变量存储敏感信息

### 📦 文件大小

技能文件可能包含 `node_modules`，备份前请确保：
- 技能目录包含 `.gitignore`
- 排除 `node_modules` 等大型目录

### 🔄 冲突处理

如果多设备同时备份可能产生冲突：
- 备份前自动 pull 最新代码
- 如有冲突，手动解决后重新推送

## 故障排除

### 推送失败

```bash
# 检查网络连接
ping github.com

# 检查 Git 配置
git remote -v
git config --list

# 手动测试推送
cd /home/admin/.openclaw/workspace
git push origin main
```

### 认证失败

```bash
# 清除缓存的凭证
git credential-cache exit

# 重新认证
git push
```

### 仓库不存在

确保已在 GitHub 创建仓库，并且 remote URL 正确。

## 恢复配置

如需从备份恢复：

```bash
# 克隆备份仓库
git clone https://github.com/your-username/openclaw-backup.git /tmp/openclaw-restore

# 恢复配置文件
cp /tmp/openclaw-restore/.backup-configs/openclaw.json ~/.openclaw/
cp -r /tmp/openclaw-restore/.backup-configs/skills/* ~/.openclaw/workspace/skills/
cp -r /tmp/openclaw-restore/.backup-configs/memory/* ~/.openclaw/workspace/memory/

# 重启 OpenClaw
openclaw gateway restart
```

## 版本历史

- v1.0 (2026-03-10) - 初始版本
