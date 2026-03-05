# OpenClaw 迁移备份清单

## 📦 已备份文件

### 核心配置
- ✅ `openclaw-config.sanitized.json` - 主配置（已脱敏）
- ✅ `channels.config.json` - 频道配置（钉钉等）
- ✅ `cron-jobs.config.json` - 定时任务配置

### 工作空间文件
- ✅ `SOUL.md` - 人格设定
- ✅ `USER.md` - 用户信息
- ✅ `IDENTITY.md` - 身份定义
- ✅ `AGENTS.md` - Agent 指南
- ✅ `TOOLS.md` - 工具笔记
- ✅ `MEMORY.md` - 长期记忆
- ✅ `HEARTBEAT.md` - 心跳任务

### 自定义技能
- ✅ `skills/searxng/` - SearXNG 搜索技能

### 其他
- ✅ `.env.example` - 环境变量模板
- ✅ `.gitignore` - Git 忽略规则

---

## 🔐 需要手动保存的敏感信息

**⚠️ 以下信息未备份到 GitHub，请单独保存！**

### 1. API Keys
- [ ] DashScope API Key (当前：`sk-sp-9202cbe48a4f4cb8b1d42b4a34b9d34e`)
- [ ] 其他模型 API Key

### 2. 钉钉配置
- [ ] Client Secret: `8hL7jyzvJanLIocRdOnpTYlwWrS4H9JZ-NWAWczYfNwBv5DliYyVkZRlIu_E3nK8`

### 3. Gateway Token
- [ ] Gateway Auth Token: `07053cee1e09490e1b4516472b530c51`

### 4. GitHub Token
- [ ] 已创建新 Token（旧 token 已泄露需撤销）

---

## 📋 迁移步骤

### 1. 在新镜像上恢复配置

```bash
# 克隆备份仓库
git clone https://github.com/liangzai-66/backup.git /path/to/new/workspace

# 复制配置文件
cp channels.config.json /new/openclaw/workspace/
cp cron-jobs.config.json /new/openclaw/workspace/
cp openclaw-config.sanitized.json /new/openclaw/workspace/

# 复制工作空间文件
cp SOUL.md USER.md IDENTITY.md AGENTS.md TOOLS.md MEMORY.md /new/openclaw/workspace/
cp -r skills/ /new/openclaw/workspace/
```

### 2. 恢复敏感配置

```bash
# 编辑 openclaw.json，填入真实的 API Key 和 Token
# 或者使用环境变量
export DASHSCOPE_API_KEY="your-key-here"
export DINGTALK_CLIENT_SECRET="your-secret-here"
export GATEWAY_TOKEN="your-token-here"
```

### 3. 恢复定时任务

```bash
# 将 cron-jobs.config.json 导入到新实例
# （具体命令取决于 OpenClaw 版本的 cron 管理方式）
```

### 4. 验证

- [ ] 测试钉钉消息发送
- [ ] 验证定时任务是否正常运行
- [ ] 检查模型调用是否正常

---

## 📊 当前配置摘要

### 频道
| 频道 | 状态 | 群组 |
|------|------|------|
| 钉钉 | ✅ 启用 | 小龙虾群 |
| QQ Bot | ✅ 启用 | - |
| 企业微信 | ✅ 启用 | - |

### 定时任务
| 任务 | 时间 | 状态 |
|------|------|------|
| 热点推送 - 早间 | 08:00 每天 | ✅ |
| 热点推送 - 午间 | 12:00 每天 | ✅ |
| 热点推送 - 晚间 | 18:00 每天 | ✅ |
| 美股分析推送 | 21:00 周一至周五 | ✅ |

### 模型
| 提供商 | 模型 | 状态 |
|--------|------|------|
| DashScope | qwen3.5-plus | ✅ |
| DashScope-US | qwen3-max-2025-09-23 | ✅ |
| DashScope-Coding | MiniMax-M2.5 | ✅ |

---

**备份时间**: 2026-03-05 23:45
**备份仓库**: https://github.com/liangzai-66/backup.git
**最后提交**: f8f5080
