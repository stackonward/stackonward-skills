# 3. App Store Connect、资料、隐私与素材

前置条件：已设置 `IOS_PROJECT`、`IOS_MANIFEST`、`IOS_ACCOUNT`、`IOS_STATE`；网站生产 URL 和产品标识已确定。每次只操作当前 App，不把示例值直接用于正式账号。

## 3.1 注册 Bundle ID【CLI】

先在 `app.json` 中确认 Bundle ID、名称、SKU 和主语言；只启用实际需要的能力。执行只读准备和计划：

```bash
cd "$IOS_PROJECT"
stackonward apple preflight --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope setup --intent reconcile --json
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope setup --intent reconcile --state "$IOS_STATE" --out "$IOS_STATE/setup.plan.json"
```

阅读计划，确认是自己的 Team、Bundle ID 和 capability，再执行：

```bash
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope setup --intent reconcile --state "$IOS_STATE" \
  --plan "$IOS_STATE/setup.plan.json" --yes --json
```

**首次退出码可能为 6。** 查看 `receipt.completed` 与 `manualRequirements`：Bundle ID 和 capability 可能已经创建，剩下的是 `app_record_required`。这不代表什么都没执行，不要因此重复建一个新标识。

## 3.2 首次创建 ASC App【人工】

在 [App Store Connect](https://appstoreconnect.apple.com/) 按 [Add a new app](https://developer.apple.com/help/app-store-connect/create-an-app-record/add-a-new-app/) 创建 App：选择 iOS、名称、主语言、刚注册的 Bundle ID、SKU 和实际访问范围。先由 Account Holder 接受适用的最新协议。

CLI 1.10.0 不创建首次 ASC App 记录。创建后取得数字 App ID，填入 `app.appId`。它与 Bundle ID、Team ID 不同。

远端状态已经改变，应重新生成计划，不能重放建档前的旧计划：

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope setup --intent reconcile --state "$IOS_STATE" --out "$IOS_STATE/setup-bound.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope setup --intent reconcile --state "$IOS_STATE" \
  --plan "$IOS_STATE/setup-bound.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope setup --intent reconcile --state "$IOS_STATE" --json
```

## 3.3 配置商店资料【填写事实，CLI 同步】

按 [原生配置示例](../assets/starter/delivery/apple/examples/app.xcode.json) 或 [Flutter 配置示例](../assets/starter/delivery/apple/examples/app.flutter.json) 合并自己需要的字段，不覆盖现有业务配置。示例中的项目名、分类、版本、工具链、路径和签名地址都应替换为真实值。

在 `delivery/apple/metadata/en-US.json` 等文件维护对应语言文案，可复制 [首版英语示例](../assets/starter/delivery/apple/metadata/en-US.json) 或 [单语言全字段表](../assets/starter/delivery/apple/examples/metadata.full.example.json) 后填写。

在 manifest 中引用对应文件：

```json
{
  "metadata": {
    "localizations": [{ "locale": "en-US", "file": "metadata/en-US.json" }],
    "primaryCategory": "UTILITIES",
    "copyright": "2026 Your Company"
  },
  "release": {
    "version": "1.0",
    "buildNumber": "1",
    "mode": "MANUAL",
    "reviewItems": { "includeApp": true, "productIds": [], "groupKeys": [] }
  }
}
```

这是字段示例，不是通用分类或功能承诺。首次版本通常不需要更新说明；更新时按实际变更填写 `whatsNew`。支持与隐私 URL 使用各自实际语言；网站语言不必与原生权限文案的 locale 文件名一模一样。

```bash
stackonward apple preflight --manifest "$IOS_MANIFEST" --scope metadata --offline --json
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope metadata --intent reconcile --state "$IOS_STATE" --out "$IOS_STATE/metadata.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope metadata --intent reconcile --state "$IOS_STATE" \
  --plan "$IOS_STATE/metadata.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope metadata --intent reconcile --state "$IOS_STATE" --json
```

未知字段会被拒绝；省略可选字段表示不管理该字段，不会自动清空远端值。已发布／审核中的资源按 Apple 的编辑状态限制处理，不强改状态来绕过限制。

## 3.4 联系人、审核账号和说明【人工填写 + CLI】

创建私有审核 JSON，放在 `IOS_PRIVATE` 中，权限设为 `0600`。包含真实 `contactFirstName`、`contactLastName`、`contactEmail`、`contactPhone`、`demoAccountRequired`；需要账号时另填可用的 `demoAccountName`、`demoAccountPassword`。不要创建公开示例密码或把账号设成审核时必须再收一次无法取得的验证码。

将 `review.credentialsRef` 设为该文件的实际绝对路径；JSON 不会替你展开 `$HOME`。将非秘密说明写入 `delivery/apple/review/notes.txt`，用 `review.notesFile` 引用，说明审核员如何进入功能、测试付费及使用特殊硬件／依赖。

联系人／账号／说明通过 metadata 同步；附件通过 assets 同步。省略或空的 demo 名称、密码不会被发送，也不会清空 Apple 旧值；不要把“保存成功”当成审核员已能登录。

## 3.5 年龄、内容权利、地区与加密【负责人判断】

- **年龄问卷**：按 App 真实功能、可见内容、频率和控制措施在 ASC 完成。不能统一填 4+。如使用 `metadata.ageRatingFile` 自动录入，文件必须使用当前 Apple 年龄声明属性，CLI 只更新明确配置的值；先对照 [当前年龄问卷](https://developer.apple.com/help/app-store-connect/manage-app-information/set-an-app-age-rating/)，不套旧问卷答案。
- **内容权利**：`metadata.contentRightsDeclaration` 支持 `DOES_NOT_USE_THIRD_PARTY_CONTENT`、`USES_THIRD_PARTY_CONTENT`。只有负责人已确认权利事实后才配置；copyright 不是同一声明。
- **加密**：按 App 和第三方库实际情况判断，见 [出口合规](https://developer.apple.com/help/app-store-connect/manage-app-information/determine-and-upload-app-encryption-documentation/)。不要为了关闭提示盲填“豁免”。确认后用 `release.encryption.usesNonExemptEncryption`；需要非豁免材料时提供对应 `appEncryptionDeclarationId`，CLI 会核对所属 App 和批准状态。构建关联在 review prepare 执行。
- **地区**：只选择计划发行且具备条件的地区，完成适用的 [DSA 状态](https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements/)、中国大陆备案／内容许可及其他 [地区信息](https://developer.apple.com/help/app-store-connect/reference/app-information/app-information/)。中国开发者同时核对 [810 号令相关资料](https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-information-for-state-council-decree-no-810/)。CLI 不替负责人作法律身份结论或签协议。

App Store Connect 的设备兼容发行开关，例如是否向兼容 Mac／Vision 设备提供 iOS App，按真实测试在后台核对；CLI 1.10.0 没有把这些正式商店开关作为可写字段。

## 3.6 隐私标签【先核实事实，再保存和发布】

阅读 [App Privacy](https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy/)，把 App、服务端和第三方 SDK 实际处理的数据逐项核对：是否收集、用途、是否关联用户、是否用于跟踪。需要跟踪时另按规则处理 ATT；“不跟踪”不能当作“不收集”。

首次填写可以直接在 ASC 完成。CLI 可以下载、保存和发布答案，不能猜答案。还没有任何回答时，下载的空数组不是可直接用来清空声明的问卷。

CLI 隐私使用独立 Apple ID session，不使用 ASC API Key。账号文件格式：

```json
{
  "username": "operator@example.com",
  "providerId": "12345678",
  "sessionFile": "privacy-session.yml"
}
```

`providerId` 是数字 ASC Provider/Team ID，不能填 Developer Team ID 或 App ID。需要查找时，在已安装锁定 Ruby 依赖的交付目录，用自己的 Apple ID 交互登录并只列团队：

```bash
cd "$IOS_PROJECT/delivery/apple"
export APPLE_ID_EMAIL="operator@example.com"
BUNDLE_PATH="$HOME/.cache/stackonward/apple-gems" bundle exec ruby -rspaceship -rjson \
  -e 'Spaceship::Tunes.login(ARGV.fetch(0)); puts JSON.pretty_generate(Spaceship::Tunes.client.teams.map { |team| {providerId: team.fetch("providerId").to_s, name: team.fetch("name")} })' \
  "$APPLE_ID_EMAIL"
cd "$IOS_PROJECT"
```

按自己团队的 ID 填文件；无法取得合法身份时，使用 ASC 网页完成隐私表单，不猜 ID、不改用 API Key。此查询会有真实登录提示；普通 privacy plan/apply 不自动登录。

设置私有账号路径并登录，按提示完成认证：

```bash
export IOS_PRIVACY_ACCOUNT="$IOS_PRIVATE/privacy-account.json"
chmod 600 "$IOS_PRIVACY_ACCOUNT"
stackonward apple privacy-login --privacy-account "$IOS_PRIVACY_ACCOUNT"
stackonward apple privacy-download --manifest "$IOS_MANIFEST" \
  --privacy-account "$IOS_PRIVACY_ACCOUNT" --out "$IOS_PRIVATE/privacy-current.json" --json
```

下载目标必须是新文件。审核下载的 [Fastlane 原生答案格式](https://docs.fastlane.tools/actions/upload_app_privacy_details_to_app_store/)，把需要管理的完整答案保存到 `delivery/apple/declarations/privacy.json`，并在 manifest 添加 `"privacy": {"file":"declarations/privacy.json"}`。`DATA_NOT_COLLECTED` 只适用于事实符合的 App。

先保存，不发布：

```bash
stackonward apple preflight --manifest "$IOS_MANIFEST" --scope privacy --offline --json
stackonward apple plan --manifest "$IOS_MANIFEST" --privacy-account "$IOS_PRIVACY_ACCOUNT" \
  --scope privacy --intent reconcile --state "$IOS_STATE" --out "$IOS_STATE/privacy-save.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --privacy-account "$IOS_PRIVACY_ACCOUNT" \
  --scope privacy --intent reconcile --state "$IOS_STATE" \
  --plan "$IOS_STATE/privacy-save.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --privacy-account "$IOS_PRIVACY_ACCOUNT" \
  --scope privacy --intent reconcile --state "$IOS_STATE" --json
```

负责人确认整份答案后，独立发布标签：

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --privacy-account "$IOS_PRIVACY_ACCOUNT" \
  --scope privacy --intent publish --state "$IOS_STATE" --out "$IOS_STATE/privacy-publish.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --privacy-account "$IOS_PRIVACY_ACCOUNT" \
  --scope privacy --intent publish --state "$IOS_STATE" \
  --plan "$IOS_STATE/privacy-publish.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --privacy-account "$IOS_PRIVACY_ACCOUNT" \
  --scope privacy --intent publish --state "$IOS_STATE" --json
```

答案替换不是原子操作。写入已派发后超时、取消或回读不明时保留 unknown，不盲重放。隐私标签发布不提交或发布 App 版本。

## 3.7 图标、截图、预览和附件【人工制作 + CLI】

图标准备为 1024×1024、不透明 PNG，用 `assets.icon` 引用，native 阶段写入声明的图标资源。截图来自实际 App，不能让模板图或错误语言承诺不存在的功能。

提交当天核对 [Apple 截图规格](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/) 和 ASC 必需设备组；当前要求、回退规则会随设备更新，不把固定旧尺寸当成永远适用。支持 iPad 的产品另准备实际需要的 iPad 组。预览视频和创意位置按需配置。

将真实素材放入空的交付素材目录，可先显式导入：

```bash
stackonward apple import-assets delivery/apple/artwork \
  /absolute/path/icon.png /absolute/path/iphone-screen.png
```

然后在 `assets.screenshots` 逐张填入 `file`、`locale`、Apple 的 `displayType` 和 `order`，在 `assets.icon` 填实际图标文件。displayType 是 Apple 设备组代码，不是任意“iPhone”文字；使用当前后台要求的组，代码查 [Screenshot Sets 的枚举](https://developer.apple.com/documentation/appstoreconnectapi/get-v1-appstoreversionlocalizations-_id_-appscreenshotsets)。需要非秘密审核附件时设置 `review.attachments`。

```bash
stackonward apple preflight --manifest "$IOS_MANIFEST" --scope assets --offline --json
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope assets --intent reconcile --state "$IOS_STATE" --out "$IOS_STATE/assets.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope assets --intent reconcile --state "$IOS_STATE" \
  --plan "$IOS_STATE/assets.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope assets --intent reconcile --state "$IOS_STATE" --json
```

追加、替换和删除不同。已有完成素材会复用；处理中资源按绑定继续。删除只使用显式的 `remove-owned-assets` 与工具持有所有权的 ID，不通过清空配置删除所有远端图片。

需要删除工具曾创建的指定截图／预览时，在 `assets.removeOwnedIds` 列出准确的 `{ "type": "appScreenshots", "id": "实际资源ID" }` 或 `appPreviews` 资源。检查计划确认所属 App、语言和父级后才执行：

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope assets --intent remove-owned-assets --state "$IOS_STATE" --out "$IOS_STATE/assets-remove.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope assets --intent remove-owned-assets --state "$IOS_STATE" \
  --plan "$IOS_STATE/assets-remove.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope assets --intent remove-owned-assets --state "$IOS_STATE" --json
```

删除后移除对应本地截图／预览配置，避免下次 reconcile 重新创建；保留已有执行状态作为资源归属依据。

下一步：[签名、构建与测试](04-build-and-test.md)。
