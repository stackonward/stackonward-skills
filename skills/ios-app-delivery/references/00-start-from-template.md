# 新项目从交付模板开始

模板提供 `delivery/apple/` 的起始配置、文案、声明与素材目录。它包含 CLI 1.10.0 生成的 [主配置 schema](../assets/starter/delivery/apple/manifest.schema.json) 和同版本 Ruby 依赖锁。发布命令使用该版本 npm 包内的执行脚本。

## 1. 复制交付目录

在新 App 项目的根目录执行。技能放在其他位置时，把 `IOS_SKILL_DIR` 改成实际路径。`mkdir delivery/apple` 会在目标已存在时停止复制。已有项目按需合并字段。

```bash
export IOS_SKILL_DIR="$HOME/.agents/skills/ios-app-delivery"
(
  set -e
  mkdir -p delivery
  mkdir delivery/apple
  cp -R "$IOS_SKILL_DIR/assets/starter/delivery/apple/." delivery/apple/
  mkdir -p delivery/apple/artwork delivery/apple/screenshots delivery/apple/previews
)
```

用实际 Bundle ID、App 名称、SKU、主语言、目标版本和构建号替换 [app.json](../assets/starter/delivery/apple/app.json) 中的示例值。ASC 建档后填写该 App 的数字 `app.appId`。官网、支持页、隐私政策和商店文案使用各自项目的真实内容。

示例的英语文案位于 [metadata/en-US.json](../assets/starter/delivery/apple/metadata/en-US.json)。需要空白表时用 [单语言全字段模板](../assets/starter/delivery/apple/examples/metadata.full.example.json)，包含名称、副标题、描述、关键词、宣传文本、更新说明和四种链接。每种语言保存一份文件并登记到 `metadata.localizations`。只填要设置的字段，空白链接或不适用的可选项从正式文件省略。首版省略 `whatsNew`，后续更新时填写。参见 [商店资料配置](03-store-configuration.md)。

先检查本地配置和引用文件。

```bash
npx --yes @stackonward/cli@1.10.0 apple preflight \
  --manifest delivery/apple/app.json --scope metadata --offline --json
```

## 2. 按功能合并示例

从 `examples/` 选择需要的键，合并到 `app.json` 中对应的对象。保留已填写的 App 身份与语言列表。素材和声明路径相对 `delivery/apple/`，填写并保存实际文件后再加入配置。

| 要配置的内容 | 示例及填写位置 |
| --- | --- |
| 原生构建与签名 | [Xcode](../assets/starter/delivery/apple/examples/app.xcode.json) 或 [Flutter](../assets/starter/delivery/apple/examples/app.flutter.json)，复制其中 `build`、`signing`，改为真实工程与签名仓库。Flutter 的 [公开构建参数](../assets/starter/delivery/apple/examples/public.release.json) 按项目实际键名放入 `build.publicDefinesFile` 指向的位置 |
| 分类、版权、年龄分级、EULA、内容权利、服务端通知 | [商店设置](../assets/starter/delivery/apple/examples/store-settings.example.json)。如要管理年龄或自定义 EULA，填写 [年龄问卷](../assets/starter/delivery/apple/declarations/age-rating.example.json) 或 [EULA](../assets/starter/delivery/apple/declarations/license-agreement.example.json)，分别保存为 `declarations/age-rating.json` 和 `declarations/license-agreement.json`。年龄表的 `null` 表示尚未选择，保留在正式 JSON 的字段须填实际值。是否申报及其内容按 App 和适用地区判断 |
| 图标、截图、预览视频和创意图 | [商店素材](../assets/starter/delivery/apple/examples/store-assets.example.json)。把真实图片或视频放到对应目录，按需要填写类型、语言和顺序。视频设备类型代码可查 [Apple Preview Sets](https://developer.apple.com/documentation/appstoreconnectapi/get-v1-appstoreversionlocalizations-_id_-apppreviewsets) |
| 登录、推送与内购能力 | [Apple 能力及 APNs](../assets/starter/delivery/apple/examples/capabilities.example.json)。启用实际使用的能力，推送选对应签名与服务器环境 |
| 地区、下载价格、内购和订阅 | [商品与售价](../assets/starter/delivery/apple/examples/commerce.example.json)。免费无内购的项目可只取 `availability`、`appPricing`，价格与地区由负责人填写。有试用、推广优惠或优惠码时，从 [订阅优惠示例](../assets/starter/delivery/apple/examples/subscription-offers.example.json) 选择对应项，填写真实条件后加入该订阅的 `offers`。其他商品类型和价格规则见 [可选功能](06-optional-capabilities.md) 和 schema |
| 审核联系、说明、声明和隐私标签 | [审核与隐私](../assets/starter/delivery/apple/examples/review-and-privacy.example.json)。按实际流程填写 [审核说明](../assets/starter/delivery/apple/review/notes.example.txt) 和 [提交声明](../assets/starter/delivery/apple/declarations/submission.example.md)，保存为 `review/notes.txt` 和 `declarations/submission.md`。采集数据的 [隐私答案表](../assets/starter/delivery/apple/declarations/privacy.example.json) 按实际类别、用途和是否关联填完整，或先用 `privacy-download` 获取现有结果。经核实确实不收集数据时才用 [不收集示例](../assets/starter/delivery/apple/declarations/privacy-no-data.example.json)。把正式答案保存为 `declarations/privacy.json` |
| TestFlight 测试 | [测试资料与组](../assets/starter/delivery/apple/examples/testflight.example.json)。填写 ASC 已有测试组 ID，核对组类型和通知选择，发邀请时才配置 `invitationsRef` |
| 辅助功能 | [辅助功能声明](../assets/starter/delivery/apple/examples/accessibility.example.json)。按实际支持的设备分组，每组九项均以实测结果填写 |
| 安装包检查 | [包检查要求](../assets/starter/delivery/apple/examples/package-checks.example.json)。按真实的权限用途、App 内语言、最低系统、设备和隐私清单配置 |
| 版本与发布 | 初次手动发布使用起始 `release`。需要定时或分阶段更新时参照 [发布策略](../assets/starter/delivery/apple/examples/release-policy.example.json)，使用实际 UTC 时间和版本。审核批次及构建 ID 根据 [提审流程](05-review-and-release.md) 回读填写 |
| 可选的静态官网部署 | [网站部署 JSON](../assets/website-deploy.json) 放到网站根目录的 `deploy.config.json`，按 [官网说明](02-website-and-app.md) 配置自己的主机与域名 |

## 3. 私有 JSON 放在项目之外

从 `assets/private-examples/` 选需要的文件，复制到自己的私有目录，删除文件名中的 `.example`，填写实际值。按 [账号与工具](01-accounts-and-tools.md) 设置路径和权限。仅执行离线检查时可以先跳过这一步。

| 示例 | 什么时候使用 |
| --- | --- |
| [account.example.json](../assets/private-examples/account.example.json) | 用 `--account` 读取或修改 ASC。填 Team ID、Key ID、Issuer ID 和真实 `.p8` 文件路径。涉及签名时才保留 `signingSecretsFile` |
| [signing-secrets.example.json](../assets/private-examples/signing-secrets.example.json) | 初始化或同步签名。填写 match 密码，Git 需要 HTTP Basic 认证时另填 `gitBasicAuthorization`，不使用该字段时将其省略 |
| [review-credentials.example.json](../assets/private-examples/review-credentials.example.json) | `review.credentialsRef` 引用。填写审核联系人，按真实登录要求决定 `demoAccountRequired` |
| [testers.example.json](../assets/private-examples/testers.example.json) | `testflight.invitationsRef` 引用。填写本次要邀请的真实人员 |
| [portal-account.example.json](../assets/private-examples/portal-account.example.json) | 用 `--portal-account` 登录 Developer Portal 后配置 APNs |
| [privacy-account.example.json](../assets/private-examples/privacy-account.example.json) | 用 `--privacy-account` 读写 App 隐私标签。填写数字 ASC `providerId` |

私有目录使用 `0700`，私有文件使用 `0600`。登录会话由相应登录命令生成，`.p8` 从 Apple 下载。计划、回执、远端导出和归档摘要由各自 CLI 命令生成。继续按 [提审教程](01-accounts-and-tools.md) 的阶段使用相应命令。
