# ARS4Hermes — Academic Research Skills for Hermes Agent

将 Imbad0202/academic-research-skills（原 Claude Code 版）的学术研究工作流移植为 **Hermes Agent 原生技能**。用 Hermes 自身的工具直接执行，不依赖 Claude Code、Codex 或任何外部 CLI。

> **朋友，收到这个仓库后，两步就能用：**
> ```bash
> git clone https://github.com/osugaBin/ars4Hermes.git
> cd ars4Hermes && bash install.sh
> ```
> 然后在 Hermes 对话中输入 `启动学术全流程 [选题]` 即可。

---

## 安装

```bash
git clone https://github.com/osugaBin/ars4Hermes.git
cd ars4Hermes
bash install.sh
```

安装脚本将 4 个技能复制到 `~/.hermes/skills/research/` 下，Hermes Agent 下次对话自动发现。

> **卸载：** `rm -rf ~/.hermes/skills/research/deep-research ~/.hermes/skills/research/academic-paper ~/.hermes/skills/research/academic-paper-reviewer ~/.hermes/skills/research/academic-pipeline`

---

## 快速开始

安装后在 Hermes 对话中输入以下触发词：

| 你说 | 技能 | 行为 |
|------|------|------|
| `启动学术全流程 人工智能对教育的影响` | academic-pipeline | 研究 → 完整性门控 → 写作 → 引用审计 → 评审 → 终稿 |
| `开始深度研究 量子计算在教育中的应用` | deep-research | 检索 10-15 个来源，交叉验证，完整报告 |
| `写学术论文 区块链在高等教育中的应用` | academic-paper | 先确认论文类型，逐章写作，中英双语摘要 |
| `评审论文 ~/paper.md` | academic-paper-reviewer | 7 维度加权评分，引用核查，反奉承机制 |
| `快速调研 元宇宙教育` | deep-research (quick) | 5-6 个核心来源，500-1500 字简报 |
| `系统综述 AI辅助评估` | deep-research (SR) | PRISMA 流程：PICOS → 检索 → 筛选 → 偏倚评估 |
| `引导我研究 教育公平` | deep-research (socratic) | 5 层苏格拉底对话，帮你厘清研究问题 |
| `事实核查 中国大学数量在下降` | deep-research (fact-check) | 3-5 个来源交叉验证，输出裁决 |

---

## 包含的 4 个技能

| 技能 | 对应原版 | 作用 |
|------|---------|------|
| **deep-research** | deep-research v2.9.4 | 学术深度研究：检索、交叉验证、完整性门控、结构化报告 |
| **academic-paper** | academic-paper v3.2.0 | 论文写作：规划、逐章撰写、Anti-Leakage 协议、中英双语摘要 |
| **academic-paper-reviewer** | academic-paper-reviewer v1.10.0 | 同行评审：7 维度加权评分、反奉承机制、引用完整性核查 |
| **academic-pipeline** | academic-pipeline v3.12.0 | 全流程编排：研究 → 写作 → 评审 → 修订 → 终稿 |

**一个完整的 pipeline 流程：**

```
用户触发「启动学术全流程 X」
         │
Stage 1: 深度研究 (deep-research)      产出: stage1_research.md
         │ [用户确认]
Stage 2.5: 完整性门控 [强制]           产出: stage25_integrity.md
         │ [PASS / 修复重检 × 3 轮]
Stage 3: 论文写作 (academic-paper)     产出: stage3_draft.md
         │ [用户确认]
Stage 4.5: 引用审计 [强制]             产出: stage45_citation_audit.md
         │ [PASS / 修复重检 × 3 轮]
Stage 5: 同行评审 (academic-paper-reviewer) 产出: stage5_review.md
         │ [Accept / Minor / Major / Reject]
Stage 6: 最终输出 + 流程总结            产出: final_paper.md + process_summary.md
```

---

## 项目结构

```
ars4Hermes/
├── install.sh                     ← 一键安装脚本
├── README.md                      ← 本文件
├── INSTALL.md                     ← 详细安装指南
├── MANUAL.md                      ← 各技能详细使用指南
├── WORKFLOW.md                    ← pipeline 工作流快速参考
├── skills/research/
│   ├── deep-research/             ← 学术深度研究技能
│   │   ├── SKILL.md               （主定义，含 6 种模式）
│   │   ├── references/            （证据分级、API 协议、故障处理等）
│   │   └── templates/             （简报模板）
│   ├── academic-paper/            ← 学术论文写作技能
│   │   ├── SKILL.md               （4 种模式 + Anti-Leakage 协议）
│   │   ├── references/            （论文结构、引用格式等）
│   │   └── templates/             （双语摘要、修订跟踪）
│   ├── academic-paper-reviewer/   ← 多视角同行评审技能
│   │   ├── SKILL.md               （7 维度评分 + 反奉承机制）
│   │   └── references/            （评分标准、决策矩阵）
│   └── academic-pipeline/         ← 全流程编排技能
│       └── SKILL.md               （6 阶段编排定义）

---

## 与 Claude Code 原版的差异

| 维度 | 原版 (Claude Code) | ARS4Hermes |
|------|-------------------|------------|
| 执行引擎 | Claude Code CLI + 内部 agent 系统 | Hermes Agent 自身 |
| 子 agent | 14-18 个独立 agent prompt | 单 agent + delegate_task 并行 |
| 工具链 | Claude 内部工具（Read, Edit, Bash） | Hermes 工具（web_search, web_extract, browser） |
| 协议 | 复杂的 agent 间 handoff 协议 | 内联在工作流步骤中 |
| 依赖 | npm install + Anthropic API key | 无需安装任何东西 |
| 模型 | 仅 Claude | 当前 Hermes 配置的任意模型 |

---

## 许可证

基于 Imbad0202/academic-research-skills（CC-BY-NC 4.0）改编。
