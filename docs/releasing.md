# 发布与维护

技能与模板通过 GitHub 仓库和 Release ZIP 分发。操作教程所用的 CLI 由 npm 的 `@stackonward/cli` 提供，两者各自维护版本。

## 建立公开仓库

发布目标为 `stackonward/stackonward-skills`。首次发布时在 StackOnward 组织下建空仓库，提交本目录并推送到 `main`。仓库描述可使用 `Agent Skills and templates for delivering iOS apps with StackOnward CLI`。Topics 可填写 `agent-skills`、`codex`、`ios`、`app-store-connect`。

开启 Issues，并检查 [Community Standards](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories) 是否识别 README、MIT 许可、贡献说明、行为准则和 Issue 表单。启用 [私密漏洞报告](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)，确认安全报告入口可用。

首次推送后查看 `Validate skills / Check and package` 的实际结果。可将通过该检查作为 `main` 的合并条件。需要由组织团队审阅时，先为实际团队授予写权限，再在 `CODEOWNERS` 中配置该团队。[GitHub Code Owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

## 准备一个版本

在 [CHANGELOG.md](../CHANGELOG.md) 将本次内容移入发布版本，把版本记录纳入要发布的提交。首个技能版本可使用 `v1.0.0`。在该提交上运行下列命令，也可使用同一提交的 Actions 构建产物。

```bash
python3 scripts/package_skills.py --verify-cli
(cd dist && shasum -a 256 -c SHA256SUMS)
```

用该提交的 Git tag 创建 GitHub Release 草稿。将 `ios-app-delivery.zip`、`stackonward-skills.zip` 和 `SHA256SUMS` 附到草稿，核对下载包与版本号后发布。Skill 版本和 CLI 版本分别记录。

## 核对公开安装

在一个空目录运行 README 的 GitHub 安装命令。需要复现固定版本时，在安装来源末尾加 `@` 和对应的 Git tag。

```bash
npx skills add stackonward/stackonward-skills --list
npx skills add stackonward/stackonward-skills --skill ios-app-delivery --agent codex
```

检查安装结果含 `SKILL.md`、`LICENSE`、`references/` 和 `assets/`。运行首次配置的离线命令验证模板。涉及 App Store Connect、签名构建或上线的验证各自使用实际项目和授权。[安装器命令](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)
