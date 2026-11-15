# StackOnward Skills

可安装的项目交付技能、操作指南和配置模板。`ios-app-delivery` 支持原生 Xcode 与 Flutter 项目，配合 `@stackonward/cli@1.10.0` 使用。

## 技能

| 技能 | 用途 | CLI 版本 |
| --- | --- | --- |
| [ios-app-delivery](skills/ios-app-delivery/SKILL.md) | 从开发者账号、网站和 App 配置，到商店资料、检查、打包、提审与发布 | 1.10.0 |

## 安装到 Codex

使用 Node.js 22.20+。全局安装后，可在多个 Codex 项目中使用。

```bash
npx skills add stackonward/stackonward-skills --skill ios-app-delivery --agent codex --global
```

仅在当前项目使用时，可在项目根目录执行项目级安装。

```bash
npx skills add stackonward/stackonward-skills --skill ios-app-delivery --agent codex
```

已有本地仓库副本时，在仓库根目录运行 `npx skills add . --skill ios-app-delivery --agent codex`。

首次通过 ZIP 安装时，将 `ios-app-delivery` 目录解压到 Codex 的用户技能目录。

```bash
mkdir -p "$HOME/.agents/skills"
unzip ios-app-delivery.zip -d "$HOME/.agents/skills"
```

目标目录已有同名技能时，先比较文件并保留自己的修改。在 Codex 对话中输入以下内容开始使用。

```text
使用 $ios-app-delivery，带我检查这个项目目前距离首次 iOS 上架还缺什么，先完成本地准备。
```

运行教程里的 CLI 命令时，使用以下版本。

```bash
npm install --global @stackonward/cli@1.10.0
stackonward --version
```

也可以用 `npx --yes @stackonward/cli@1.10.0` 直接调用这一版本。

## 从这里开始

准备上架或更新版本时，按 [187 项 iOS App 上架检查清单](skills/ios-app-delivery/references/ios-app-delivery-checklist.md) 核对适用条件和通过标准。

新项目可先复制完整的 `delivery/apple/` 交付目录，再填写自己的配置与文案。[模板和 JSON 示例](skills/ios-app-delivery/references/00-start-from-template.md)

1. [开发者账号、工具和私有凭据](skills/ios-app-delivery/references/01-accounts-and-tools.md)
2. [网站与 App 配置](skills/ios-app-delivery/references/02-website-and-app.md)
3. [App Store Connect、资料、隐私与素材](skills/ios-app-delivery/references/03-store-configuration.md)
4. [签名、打包、上传与 TestFlight](skills/ios-app-delivery/references/04-build-and-test.md)
5. [提审、发布与更新](skills/ios-app-delivery/references/05-review-and-release.md)
6. [登录、推送、内购及辅助功能](skills/ios-app-delivery/references/06-optional-capabilities.md)
7. [完整性检查与失败恢复](skills/ios-app-delivery/references/07-errors-and-verification.md)

没有账号、内购或推送的 App，按各章节的适用条件跳过相应功能。所有域名、路径、账号和商品均由自己的项目配置。

## 支持和贡献

[使用支持](SUPPORT.md) · [贡献指南](CONTRIBUTING.md) · [安全报告](SECURITY.md) · [更新日志](CHANGELOG.md) · [MIT 许可](LICENSE)
