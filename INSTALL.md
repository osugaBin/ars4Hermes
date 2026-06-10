# ARS4Hermes 安装指南

## 概述

ARS4Hermes (Academic Research Skills for Hermes Agent) 是将 Imbad0202/academic-research-skills（原 Claude Code 版）的核心工作流移植为 Hermes Agent SKILL.md 格式的技能包。包含 4 个技能：deep-research、academic-paper、academic-paper-reviewer、academic-pipeline。

## 前提条件

- **Hermes Agent** 已安装并配置可用（任何模型均可，当前已验证 DeepSeek-V4-Flash / SiliconFlow）
- 无需安装 Claude Code、Codex 或其他外部 CLI
- 无需注册任何外部服务

## 安装方法

### 方法一：从 GitHub 克隆（推荐）

```bash
git clone https://github.com/osugaBin/ars4Hermes.git
cd ars4Hermes
bash install.sh
```

安装脚本会自动将 4 个技能复制到 `~/.hermes/skills/research/` 下。

### 方法二：解压安装包

拿到 `ars4hermes_package_v1.0.tar.gz` 后：

```bash
tar xzf ars4hermes_package_v1.0.tar.gz
cd ars4hermes_full
bash install.sh
```

## 验证安装

安装后，在 Hermes 对话中测试触发词：

```
你: 开始深度研究 量子计算在教育中的应用

Hermes 应自动加载 deep-research 技能并开始检索...
```

如果 Hermes 正确进入研究流程，说明安装成功。

## 目录结构

```
ars4hermes_full/
├── install.sh                          ← 一键安装脚本
├── docs/
│   ├── README.md                       ← 项目概览
│   ├── MANUAL.md                       ← 详细使用指南
│   └── WORKFLOW.md                     ← 工作流快速参考
├── skills/research/
│   ├── deep-research/                  ← Stage 1: 学术深度研究
│   │   ├── SKILL.md                    （主定义）
│   │   ├── references/                 （参考文档：证据分级、协议等）
│   │   └── templates/                  （输出模板）
│   ├── academic-paper/                 ← Stage 3: 学术论文写作
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── templates/
│   ├── academic-paper-reviewer/        ← Stage 5: 多视角同行评审
│   │   ├── SKILL.md
│   │   └── references/
│   └── academic-pipeline/              ← 全流程编排器
│       └── SKILL.md
└── example_output/
    └── (eg1 全流程示例产出)
```

## 触发词速查

| 技能 | 触发词 |
|------|--------|
| deep-research | `开始深度研究 [主题]`、`快速调研 [主题]`、`系统综述 [主题]`、`引导我研究 [主题]`、`事实核查 [主张]`、`文献综述 [主题]` |
| academic-paper | `写学术论文 [主题]`、`写综述 [主题]`、`修改论文`、`生成大纲 [主题]`、`写摘要 [主题]` |
| academic-paper-reviewer | `评审论文 [文件路径]`、`快速评估 [文件路径]`、`引导改进 [文件路径]` |
| academic-pipeline | `启动学术全流程 [选题]`、`从零开始写论文 [选题]` |

## 运行示例

完整的 pipeline 运行示例可查看 `example_output/` 目录：

```
启动学术全流程 人工智能对统计学本科教学质量保障的影响
```

产出 9 个文件覆盖 6 个阶段：研究 → 完整性门控 → 写作 → 引用审计 → 评审 → 终稿。

## 卸载

```bash
rm -rf ~/.hermes/skills/research/deep-research
rm -rf ~/.hermes/skills/research/academic-paper
rm -rf ~/.hermes/skills/research/academic-paper-reviewer
rm -rf ~/.hermes/skills/research/academic-pipeline
```

## 注意

- 所有技能基于 Hermes Agent 的工具集（web_search、web_extract、browser、delegate_task 等），无需外部 CLI
- 参考文献的真实性标注说明：`[需人工确认]` = API 未验证，`[MATERIAL GAP]` = 材料缺失
- 当前模型使用 DeepSeek-V4-Flash（SiliconFlow 提供商），其他模型应兼容
