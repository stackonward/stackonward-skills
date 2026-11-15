# 1. 开发者账号、工具和私有凭据

本教程使用已发布的 `@stackonward/cli@1.10.0`，适用于原生 Xcode 和 Flutter iOS 项目。先完成这一章，再进入网站与 App 配置。

## 1.1 选择真实的开发者主体【人工】

在 [Apple Developer Program](https://developer.apple.com/programs/enroll/) 注册或加入团队。

| 主体 | 需要准备 | 商店展示与注意事项 |
| --- | --- | --- |
| 个人 | 开启双重认证的 Apple Account、法定身份、达到当地成年年龄 | 个人法定姓名通常作为卖方名称 |
| 组织 | 法人实体、签约授权人、企业域名邮箱、有效官网、适用的 D‑U‑N‑S | 组织名称应与真实法人信息一致 |

组织通常需要 [D‑U‑N‑S](https://developer.apple.com/help/account/membership/D-U-N-S/)，政府实体存在例外；个人注册不需要为此申请企业号码。Apple 当前标价为每会员年 99 美元，实际金额按注册地区显示；符合条件的机构可申请减免。不要按固定人民币金额或承诺审批天数准备预算。

CLI 不注册主体、不签协议、不付款、不替人完成身份验证。先确认会员有效，再邀请实际参与开发、资料管理和发布的人。

## 1.2 准备开发环境【本机】

- 可运行当前稳定 Xcode 的 Mac；原生打包、签名和包检查需要 macOS。
- CLI 需要 Node.js 20+。本教程的网站模板需要 Node.js 22.22.1+、pnpm 9+，因此统一使用满足后者要求的 Node.js。
- Flutter 项目额外准备项目固定的 Flutter SDK。
- Apple Ruby 操作使用 CLI 分发的 Gemfile.lock；1.10.0 锁定 fastlane 2.240.1、Bundler 4.0.16，使用兼容该锁的 Ruby。

```bash
node --version
npm --version
xcode-select -p
xcodebuild -version
ruby --version
bundle --version

npm install --global @stackonward/cli@1.10.0
stackonward --version
stackonward apple --help
```

`stackonward --version` 应显示 `1.10.0`。如不希望改变已有全局 CLI，可将后续命令的 `stackonward` 替换为 `npx --yes @stackonward/cli@1.10.0`。

缺少所需 Bundler 时，先准备符合 [Bundler 兼容要求](https://bundler.io/compatibility.html) 的 Ruby，再安装锁定版本：

```bash
gem install bundler --version 4.0.16
bundle _4.0.16_ --version
```

首次使用 Xcode 时，先在 Xcode 中安装所需平台组件并完成许可确认。Apple 会更新提交门槛；在实际提审当天阅读 [Upcoming Requirements](https://developer.apple.com/news/upcoming-requirements/)，区分构建使用的 SDK、App 支持的最低 iOS 版本和测试设备系统版本。

## 1.3 确定产品标识【人工】

准备自己的值，不直接使用示例身份操作正式账号：

| 值 | 含义 | 后续是否可随意更换 |
| --- | --- | --- |
| Bundle ID | 如 `com.yourcompany.yourapp`，对应 App、证书及平台登记 | 上架后不应更换为另一个 App 身份 |
| Developer Team ID | 开发者团队标识，常见为 10 位字母数字 | 必须与签名团队一致 |
| App ID | ASC 创建 App 后分配的数字 ID | 不是 Bundle ID，也不是 Team ID |
| SKU | ASC 首次建档使用的内部库存标识 | 由产品稳定管理 |
| 主语言 | 商店资料的主语言 | 对应真实维护的商店语言 |
| 版本与构建号 | 如营销版本 `1.0.0`、构建号 `1` | 每个上传构建使用合适的新构建号 |

商品 Product ID、API Key ID、Issuer ID、隐私会话数字 providerId 都是不同标识，不能互相代填。

## 1.4 创建 ASC Team API Key【人工】

按 [App Store Connect API](https://developer.apple.com/help/app-store-connect/get-started/app-store-connect-api) 的说明操作：Account Holder 申请 API access；具备相应权限的 Account Holder 或 Admin 生成 Team API Key，并为实际工作选择角色。

本教程的 CLI 账号合同包含 `issuerId`，按 Team Key 路线准备。个人开发者主体也应分清 Team Key 与 Individual API Key；两者不是“公司账号／个人账号”的同义词。Individual Key 不支持 Provisioning 等操作，不能未经核对就替代这套凭据。

记录 Team ID、Issuer ID、Key ID，将只能下载一次的 `.p8` 放入自己的私有目录。Team Key 不能按单个 App 限定权限；按参与者和实际任务管理权限，不把密钥交给客户端或公开技能包。

## 1.5 创建交付目录和私有目录【CLI + 本机】

新项目可先按 [交付模板](00-start-from-template.md) 复制目录，然后继续设置终端路径。需要从 CLI 创建空白交付目录时，在自己的 App 项目根目录执行，并替换 Bundle ID 和名称。

```bash
stackonward apple init delivery/apple \
  --bundle-id com.yourcompany.yourapp \
  --name "Your App"
```

生成的 `delivery/apple/app.json` 是公开产品配置，`manifest.schema.json` 描述 CLI 字段。目标目录必须为空；已有交付目录应直接检查和编辑，不重复 init 覆盖。

然后保持终端位于项目根目录，设置本教程后续命令使用的路径：

```bash
export IOS_PROJECT="$PWD"
export IOS_MANIFEST="$IOS_PROJECT/delivery/apple/app.json"
export IOS_PRIVATE="$HOME/.config/stackonward/apple/your-app"
export IOS_STATE="$HOME/.local/state/stackonward/apple/your-app"
export IOS_ACCOUNT="$IOS_PRIVATE/account.json"

mkdir -p "$IOS_PRIVATE" "$IOS_STATE"
chmod 700 "$IOS_PRIVATE" "$IOS_STATE"
```

把真实 API 私钥复制到私有目录，例如 `AuthKey.p8`。新建 `$IOS_ACCOUNT`，填入自己的值：

```json
{
  "teamId": "YOURTEAMID",
  "keyId": "KEYID12345",
  "issuerId": "00000000-0000-4000-8000-000000000000",
  "privateKeyPath": "AuthKey.p8"
}
```

上面的标识只用于说明格式。`.p8` 路径相对账号 JSON 解析，私有文件权限必须正确：

```bash
chmod 600 "$IOS_ACCOUNT" "$IOS_PRIVATE/AuthKey.p8"
```

准备 Ruby 依赖和本地配置检查：

```bash
cd delivery/apple
BUNDLE_PATH="$HOME/.cache/stackonward/apple-gems" bundle install
cd ../..

stackonward apple preflight --manifest "$IOS_MANIFEST" --scope setup --offline --json
```

离线通过只说明本地输入有效；它没有验证 Apple 权限、真实服务或 App 功能。私钥、审核密码、签名仓库密码、Portal/隐私会话与执行状态都不提交到产品或技能仓库。

下一步：[网站与 App 配置](02-website-and-app.md)。
