# ARS4Hermes — Academic Research Skills for Hermes Agent

将 Imbad0202/academic-research-skills（Claude Code 版）的核心工作流移植为 Hermes Agent SKILL.md 格式，用 Hermes 自身的工具（web_search, web_extract, browser, delegate_task）直接执行，无需依赖 Claude Code 或任何外部 CLI。

## 项目结构

```
ars4Hermes/
├── README.md           ← 本文件：项目概览
├── MANUAL.md           ← 使用指南：各技能详细操作方法
└── skills/             ← 生成的 Hermes 技能文件（安装在 ~/.hermes/skills/ 下）
    └── research/
        ├── deep-research/          ✓ Step 1 完成
        ├── academic-paper/         — Step 2
        ├── academic-paper-reviewer/— Step 3
        └── academic-pipeline/      — Step 4
```

## 四步计划

| Step | 技能 | 原仓库对应 | 说明 | 状态 |
|------|------|-----------|------|------|
| **1** | `deep-research` | deep-research v2.9.4 | 学术深度研究 | ✅ 完成 |
| **2** | `academic-paper` | academic-paper v3.2.0 | 学术论文写作 | ✅ 完成 |
| **3** | `academic-paper-reviewer` | academic-paper-reviewer v1.10.0 | 多视角同行评审 | ✅ 完成 |
| **4** | `academic-pipeline` | academic-pipeline v3.12.0 | 全流程编排器 | ✅ 完成 |

## 技能安装位置

所有技能安装在 `~/.hermes/skills/research/` 下，Hermes Agent 自动发现。每个技能包含：

- `SKILL.md` — 主定义文件（YAML 前置元数据 + Markdown 工作流）
- `references/` — 参考文档（证据分级、协议、故障处理等）
- `templates/` — 输出模板

## 触发方式

在对话中说出触发词，Hermes 自动加载对应技能：

```
# deep-research
开始深度研究 [主题]
快速调研 [主题]
系统综述 [主题]
引导我研究 [主题]
事实核查 [主张]
文献综述 [主题]

# academic-paper
写学术论文 [主题]
写综述 [主题]
修改论文 (附上草稿+审稿意见)
生成大纲 [主题]
写摘要 [主题]

# academic-paper-reviewer
评审论文 (附上论文文本或文件路径)
审稿 [文件路径]
快速评估 [文件路径]
引导改进 [文件路径]

# academic-pipeline
完整学术流水线 [主题]
从研究到发表 [主题]
```

## 与原版的差异

| 维度 | 原版 (Claude Code) | ARS4Hermes |
|------|-------------------|------------|
| 执行引擎 | Claude Code CLI + 内部 agent 系统 | Hermes Agent 自身 |
| 子 agent | 14-18 个独立 agent prompt | 单 agent + delegate_task 并行 |
| 工具链 | Claude 内部工具（Read, Edit, Bash） | Hermes 工具（web_search, web_extract, browser） |
| 协议 | 复杂的 agent 间 handoff 协议 | 内联在工作流步骤中 |
| 依赖 | npm install + Anthropic API key | 无需安装任何东西 |
| 模型 | 仅 Claude | 当前 Hermes 配置的任意模型（当前 DeepSeek-V4-Flash） |

## 许可证

基于 Imbad0202/academic-research-skills（CC-BY-NC 4.0）改编。
