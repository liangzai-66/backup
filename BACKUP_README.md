# OpenClaw 配置备份

此仓库用于备份 OpenClaw 的配置和重要文件。

## 备份内容

- **openclaw.json** - 主配置文件（频道、网关、模型等）
- **cron/jobs.json** - 定时任务配置
- **skills/** - 自定义技能
- **memory/** - 记忆文件
- **workspace/*.md** - 配置文件（SOUL.md, USER.md, MEMORY.md 等）

## 自动备份

配置了每天凌晨 2:00 (Asia/Shanghai) 自动备份到 GitHub。

Cron 任务 ID: `backup-to-github-0200`

## 手动备份

```bash
cd /home/admin/.openclaw/workspace
git add -A
git commit -m "Manual backup: YYYY-MM-DD HH:mm:ss"
git push
```

## 恢复配置

```bash
# 克隆备份仓库
git clone <your-repo-url> /tmp/openclaw-backup

# 恢复配置文件
cp /tmp/openclaw-backup/openclaw.json ~/.openclaw/
cp -r /tmp/openclaw-backup/skills ~/.openclaw/workspace/
cp -r /tmp/openclaw-backup/memory ~/.openclaw/workspace/
# ... 其他文件

# 重启 Gateway
openclaw gateway restart
```

## 注意事项

⚠️ **敏感信息**: 提交前请检查 `openclaw.json` 中是否包含 API key、token 等敏感信息。建议使用环境变量或在使用前手动替换。

## 首次设置

```bash
cd /home/admin/.openclaw/workspace

# 配置 GitHub remote
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 或 SSH 方式
git remote add origin git@github.com:你的用户名/你的仓库名.git

# 初次推送
git branch -M main
git push -u origin main
```

## 备份历史

查看备份历史：
```bash
git log --oneline
```

恢复到特定版本：
```bash
git checkout <commit-hash>
```
