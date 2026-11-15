# 参与贡献

欢迎修正步骤、补充可验证的示例，或贡献新的项目交付技能。请先查阅现有 Issues。跨度较大的变更可以先说明要解决的用户问题和验证方式。

## 修改技能

1. 将技能放在 `skills/技能名/`，`SKILL.md` 使用 YAML frontmatter 和 Markdown，`name` 与目录名一致。每个可单独安装的技能包含 [MIT 许可证](LICENSE) 的副本。[Agent Skills 规范](https://agentskills.io/specification)
2. 入口写任务范围、关键步骤和资源索引。长教程放在 `references/`，可复制的配置放在 `assets/`。技能内部链接应随技能目录一起安装。
3. 使用通用身份、公开示例域名和空白私有字段。填写后的账号文件、密钥、日志、执行回执和项目素材留在自己的环境。CLI 命令以技能声明的版本为准，涉及真实发布的操作要写明前置条件。

## 本地验证

在仓库根目录运行，准备 Python 3.10+、Node.js 22.20+ 及 npm。

```bash
python3 scripts/package_skills.py --verify-cli
npx --yes skills@1.8.1 add . --list
```

第一条检查分发文件、许可证、相对链接和 JSON，并用发布版 CLI 执行 iOS 示例的离线检查，将 ZIP 和校验和写到 `dist/`。第二条检查安装器能否发现技能。更改 CLI 命令时，在 PR 说明使用了哪个已发布版本和验证了哪个阶段。涉及账户、签名或真机的结果分别列明。

## 提交 PR

请描述用户遇到的问题、实际改动和验证结果。附可复现的最小配置，清除账号信息、密钥、测试密码和签名 URL。新增或修改分发内容使用本仓库的 MIT 许可。参与讨论请遵守 [社区行为准则](CODE_OF_CONDUCT.md)。
