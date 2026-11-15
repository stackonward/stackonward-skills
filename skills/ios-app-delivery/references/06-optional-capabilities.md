# 6. 登录、推送、内购及辅助功能

只配置 App 实际具备的能力。没有这些功能时不创建对应密钥、商品或服务。以下继续使用第 1 章的路径变量；金额、地区、商品、地址和声明答案均替换为自己的事实。

## 6.1 Sign in with Apple【平台配置 + 产品实现】

需要时在 manifest 设置 `capabilities.signInWithApple: true`，依次执行第 3 章 setup、第 4 章 native、signing 和 build。capabilities 只接受启用的 `true`；省略表示不管理，不是关闭远端能力。

CLI 不创建登录业务代码或验证登录结果。人工完成：

- 原生授权入口、服务端令牌校验、用户绑定与取消流程；检查实际 Bundle／Team／client ID。
- 有网站登录时，在 Apple Developer 配置对应 Services ID、域名和 Return URL；服务端 client secret 的密钥与生成逻辑由认证服务管理。
- 使用 Hide My Email 时配置邮件来源和投递，验证真实收件。
- 提供账号创建时，实现 App 内发起删除，处理相应数据及适用的 Apple 授权撤销；删除账号与取消订阅分别告知。

第三方／社交登录是否需要等效的隐私保护登录选项，按 [4.8 Login Services](https://developer.apple.com/app-store/review/guidelines/#login-services) 的适用条件和例外判断；不是所有 App 都必须增加社交登录。账号删除要求见 [Apple 说明](https://developer.apple.com/help/app-review/guideline-reference/5-1-1-account-deletion)。

## 6.2 APNs Key【独立 Portal 身份】

推送需要四部分：Bundle Push capability、签名 entitlements/profile、服务端 APNs 凭据、真实设备 token 和发送链路。创建 Key 只完成其中一部分。

在 manifest 中按实际环境设置，例如正式分发：

```json
{
  "capabilities": { "pushNotifications": true },
  "apns": {
    "name": "Your App Production Push",
    "environment": "production",
    "scope": "team"
  }
}
```

`environment` 必须明确为 `development` 或 `production`。1.10.0 只支持 team scope，授权范围不等于单个 App；需要 topic-specific Key 时使用 Apple 支持的人工方式，不伪造 CLI 字段。两种环境使用各自名字和私钥输出路径。

在私有目录创建 Portal account JSON，使用真实 Apple ID 和 Team：

```json
{
  "username": "operator@example.com",
  "teamId": "YOURTEAMID",
  "sessionFile": "portal-session.yml"
}
```

```bash
export IOS_PORTAL_ACCOUNT="$IOS_PRIVATE/portal-account.json"
export IOS_APNS_KEY="$IOS_PRIVATE/apns-production.p8"
chmod 600 "$IOS_PORTAL_ACCOUNT"

stackonward apple portal-login --portal-account "$IOS_PORTAL_ACCOUNT"
stackonward apple preflight --manifest "$IOS_MANIFEST" --key-output "$IOS_APNS_KEY" \
  --scope apns --intent provision --offline --json
stackonward apple plan --manifest "$IOS_MANIFEST" --portal-account "$IOS_PORTAL_ACCOUNT" \
  --key-output "$IOS_APNS_KEY" --scope apns --intent provision \
  --state "$IOS_STATE" --out "$IOS_STATE/apns.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --portal-account "$IOS_PORTAL_ACCOUNT" \
  --key-output "$IOS_APNS_KEY" --scope apns --intent provision --state "$IOS_STATE" \
  --plan "$IOS_STATE/apns.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --portal-account "$IOS_PORTAL_ACCOUNT" \
  --key-output "$IOS_APNS_KEY" --scope apns --intent provision --state "$IOS_STATE" --json
```

登录按终端提示完成密码／2FA，不把密码写入账号 JSON。该阶段使用锁定 Fastlane/Spaceship 的 Developer Portal 自动化，**不是公开 APNs Key 管理 API**，也不使用 ASC API Key。[Apple 私钥管理](https://developer.apple.com/help/account/keys/create-a-private-key/)

输出必须是绝对 `.p8` 路径，目录私有且目标文件不存在。此例成功后的 `apns-production.p8` 与 `apns-production.p8.receipt.json` 分开保管；恢复文件 `apns-production.p8.download.json` 也含秘密。一次性下载中断、状态 unknown 时保留原 state 和恢复文件，不改 state 重建第二把 Key。Apple 已消耗下载且没有本地恢复内容时，CLI 不能找回私钥。

接着完成 setup/native/signing/build，并把私钥、Key ID、Team ID、Bundle topic 和环境配置到自己的推送服务；经 Firebase 等服务转发时按其后台接入。CLI 不上传 Firebase 配置或发送测试消息。原生 lane 写入的开发 entitlements 与最终 App Store 导出包不同，应检查最终签名的 `aps-environment`，再验证正式设备链路。

## 6.3 内购与自动续费订阅【有数字付费功能时】

先由有权限的负责人完成 [付费协议、税务和银行资料](https://developer.apple.com/help/app-store-connect/manage-agreements/sign-and-update-agreements)。免费且无内购的 App 不因此需要套用同一银行流程。数字内容／功能解锁按 [3.1 内购规则](https://developer.apple.com/app-store/review/guidelines/#in-app-purchase) 及地区适用条款处理；实物等场景分别判断。

| `kind` | 用途与必要配置 |
| --- | --- |
| `CONSUMABLE` | 消耗型商品，稳定 Product ID |
| `NON_CONSUMABLE` | 非消耗型，产品实现相应恢复购买 |
| `NON_RENEWING_SUBSCRIPTION` | 非续期订阅，产品负责期限与权益 |
| `subscription` | 自动续费订阅，另有 `groupKey`、`duration`、`level`、`offers` |

仅在适用时启用 `capabilities.inAppPurchase: true` 并运行 setup/native。`catalog` 放商品身份与当地化，`pricing` 管价格、销售地区、优惠和宽限期，`assets` 管商品图片。顺序为 catalog → assets → pricing。

下面是一个自动续费商品的结构示例，**不是默认收费方案**：

```json
{
  "catalog": {
    "groups": [
      {
        "key": "membership",
        "name": "Membership",
        "localizations": [{ "locale": "en-US", "name": "Membership" }]
      }
    ],
    "items": [
      {
        "kind": "subscription",
        "productId": "com.yourcompany.yourapp.membership.monthly",
        "name": "Monthly Membership",
        "groupKey": "membership",
        "duration": "ONE_MONTH",
        "level": 1,
        "offers": [],
        "localizations": [
          { "locale": "en-US", "name": "Monthly Membership", "description": "Describe the actual membership." }
        ],
        "reviewScreenshot": "artwork/purchase-review.png",
        "prices": [
          { "territory": "USA", "customerPrice": "3.99", "currency": "USD", "preserveCurrentPrice": true }
        ],
        "availability": { "territories": ["USA"], "availableInNewTerritories": false }
      }
    ]
  }
}
```

替换成真实商品方案和审核截图。`preserveCurrentPrice` 必须按是否保留现有订阅用户价格明确选择，不能把示例 `true` 当成通用策略。已有订阅组填写准确的 `remoteId` 或沿用工具已有私有绑定；同名不会自动认领。

普通内购使用自己的 `kind`，去掉订阅专属的 `groupKey/duration/level/offers`，按需指定 `baseTerritory`。价格为十进制字符串，地区为 Apple 三字代码、币种为 ISO 代码；无法唯一选择 Apple 价格点时指定准确 `pricePointId`。

```bash
stackonward apple preflight --manifest "$IOS_MANIFEST" --scope catalog --offline --json
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope catalog --intent reconcile --state "$IOS_STATE" --out "$IOS_STATE/catalog.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope catalog --intent reconcile --state "$IOS_STATE" \
  --plan "$IOS_STATE/catalog.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope catalog --intent reconcile --state "$IOS_STATE" --json
```

商品审核截图、推广图配置后执行第 3 章 assets；其后运行：

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope pricing --intent reconcile --state "$IOS_STATE" --out "$IOS_STATE/pricing.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope pricing --intent reconcile --state "$IOS_STATE" \
  --plan "$IOS_STATE/pricing.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope pricing --intent reconcile --state "$IOS_STATE" --json
```

价格变更前阅读计划中的金额、地区、生效日期和保价策略。App／普通内购可设 `startDate/endDate`，日期区间不能重叠。自动续费价格有自己的 `startDate/preserveCurrentPrice` 合同。

有活动时，`offers` 支持 `introductory`、`promotional` 和 `code`；按 `stackonward apple schema` 的实际字段填写周期、模式、价格点及适用用户，不默认赠送试用。实际优惠码批次在 ASC 管理。`catalog.gracePeriod` 另包含 `optIn/sandboxOptIn/duration/renewalType`，按自己的续费策略配置，仍由 pricing 同步。

### App 下载价格和销售地区

不是购买商品价格。在 manifest 顶层使用 `availability` 管 App 的发行地区，用 `appPricing` 管 App 下载价格；同样执行 pricing。免费 App 也应在 ASC 确认下载价格和地区。

```json
{
  "availability": { "territories": ["USA"], "availableInNewTerritories": false },
  "appPricing": {
    "baseTerritory": "USA",
    "prices": [{ "territory": "USA", "customerPrice": "0.00", "currency": "USD" }]
  }
}
```

这只是一个免费、单地区示例；不自动代表“全球销售”。后台实际支持的价格点、税务分类和地区资质另核对。

### 交易服务与首次联提

产品实现真实 StoreKit 购买、恢复、交易校验、账号归属、退款／撤销、续费与权益同步；提供实际价格、周期、自动续订说明及有效的隐私政策／条款链接。CLI 创建商品不实现这些逻辑。

已实现并公开可访问的 App Store Server Notifications V2 地址，可通过 metadata 同步：

```json
{
  "metadata": {
    "serverNotifications": {
      "production": { "url": "https://api.example.com/apple/notifications", "version": "V2" },
      "sandbox": { "url": "https://sandbox-api.example.com/apple/notifications", "version": "V2" }
    }
  }
}
```

配置后执行第 3 章 metadata。省略字段表示不管理，`null` 表示显式清空；不能随意复制 `null`。Sandbox 未单独配置时，生产地址可能接收两种环境，服务端必须校验签名及通知环境。

首次相应内购类型／首次订阅按 [Apple 内购联提](https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-in-app-purchase/) 和 [订阅审核](https://developer.apple.com/documentation/appstoreconnectapi/submitting-subscriptions-and-subscription-groups-for-app-review) 随新 App 版本在网页提交。`release.reviewItems.productIds/groupKeys` 选择真实项目；适用时将类型列入 `release.firstPurchaseTypes`。首次边界不靠删除此配置绕过，常规后续版本也不应无条件复制首次标识。

## 6.4 辅助功能声明【实测后填写】

按设备测试后再填 `accessibility.declarations`。每条需有 `deviceFamily` 和完整九项布尔答案：

`supportsVoiceover`、`supportsVoiceControl`、`supportsLargerText`、`supportsSufficientContrast`、`supportsDarkInterface`、`supportsDifferentiateWithoutColorAlone`、`supportsReducedMotion`、`supportsCaptions`、`supportsAudioDescriptions`。

设备取实际支持的 `IPHONE/IPAD/APPLE_TV/APPLE_WATCH/MAC/VISION`。不能为了通过配置验证统一填写 `true` 或 `false`；例如更大字体须满足 [Apple 评估标准](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/larger-text-evaluation-criteria)，仅稍微放大文字不够。

首次上架前可保存草稿：

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope accessibility --intent reconcile --state "$IOS_STATE" --out "$IOS_STATE/accessibility-save.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope accessibility --intent reconcile --state "$IOS_STATE" \
  --plan "$IOS_STATE/accessibility-save.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope accessibility --intent reconcile --state "$IOS_STATE" --json
```

满足 Apple 对已有上架版本及设备的 [发布条件](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/manage-accessibility-nutrition-labels) 后，单独发布：

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope accessibility --intent publish --state "$IOS_STATE" --out "$IOS_STATE/accessibility-publish.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope accessibility --intent publish --state "$IOS_STATE" \
  --plan "$IOS_STATE/accessibility-publish.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope accessibility --intent publish --state "$IOS_STATE" --json
```

发布辅助功能资料与发布 App 版本是独立操作；实际无障碍体验仍需测试。
