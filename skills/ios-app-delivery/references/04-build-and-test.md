# 4. 签名、打包、上传与 TestFlight

前置条件：已有可运行的真实 App、准确的 App/Bundle/Team、ASC App 记录和发布版本；[商店配置](03-store-configuration.md) 已按适用事项准备。回到 App 项目根目录，保持第 1 章的路径变量。

## 4.1 写入实际工程路径【本地配置】

参照 [Xcode](../assets/starter/delivery/apple/examples/app.xcode.json) 或 [Flutter](../assets/starter/delivery/apple/examples/app.flutter.json) 的字段结构，把 `build` 和 `signing` 合并到现有 manifest。

- `build.projectRoot` 相对 manifest 所在目录解析。交付文件在 `项目/delivery/apple/app.json` 时，`../..` 指向项目根。
- `projectPath`、`workspace`、Info.plist、entitlements、AppIcon 和单个 `publicDefinesFile` 再相对该项目根解析。
- scheme、target 和额外 target 只填写实际存在且要管理的目标；不要猜测试或 extension 名称。
- `xcodeVersion`、`flutterVersion` 使用本机已选择、已验证且满足 Apple 当前要求的实际版本。示例版本只说明结构，不是 SDK 推荐。
- Flutter 示例引用项目的 `config/public.release.json`，可复制 [公开参数示例](../assets/starter/delivery/apple/examples/public.release.json) 到该路径。按 App 实际读取的键维护公开参数，不能照搬示例 `API_BASE_URL` 作为所有项目通用的键。

先用本地工具核对工程，再进行原生配置：

```bash
cd "$IOS_PROJECT"
xcodebuild -version

# 原生项目按实际文件使用 -project 或 -workspace
xcodebuild -list -project Example.xcodeproj

# Flutter 项目
flutter --version
flutter pub get
flutter analyze
flutter test
```

上述两个工程分支按实际项目选择。`native` 会改工程配置、声明的 plist/entitlements 及可选图标，先检查计划和当前文件：

```bash
stackonward apple preflight --manifest "$IOS_MANIFEST" --scope native --offline --json
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope native --intent configure --state "$IOS_STATE" --out "$IOS_STATE/native.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope native --intent configure --state "$IOS_STATE" \
  --plan "$IOS_STATE/native.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope native --intent configure --state "$IOS_STATE" --json
```

App 的真实功能、服务端 origin、登录回调和 SDK 初始化逻辑仍在产品代码中实现。服务交接可以读取：

```bash
stackonward apple handoff --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --out "$IOS_STATE/runtime-handoff.json" --json
```

交接文件列出标识和所需配置键，不证明登录、推送或交易服务已经接通。

## 4.2 准备签名仓库和密码【人工 + CLI】

`signing.storageUrl` 是自己的专用私有 HTTPS Git 仓库；`signing.bundleIds` 包含本次真实签名目标，`profileType` 为 `appstore`。它不是主项目代码仓库，更不是公开素材目录。

在 `IOS_PRIVATE` 创建 `signing-secrets.json`，放真实的 match 加密 `password`，必要时增加 `gitBasicAuthorization`（Git 用户名与 token 的 Base64 表示，仍然是秘密）。在 API 账号 JSON 中添加 `"signingSecretsFile":"signing-secrets.json"`，相对账号文件解析。

```bash
chmod 600 "$IOS_PRIVATE/signing-secrets.json"
```

首次确实需要创建签名资源时，将 manifest 的 `signing.readonly` 设为 `false`，明确使用 initialize：

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope signing --intent initialize --state "$IOS_STATE" --out "$IOS_STATE/signing-init.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope signing --intent initialize --state "$IOS_STATE" \
  --plan "$IOS_STATE/signing-init.plan.json" --yes --json
```

已有签名资源时不重复初始化。常规构建将 `signing.readonly` 设回 `true`，同步已有资源：

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope signing --intent sync --state "$IOS_STATE" --out "$IOS_STATE/signing-sync.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope signing --intent sync --state "$IOS_STATE" \
  --plan "$IOS_STATE/signing-sync.plan.json" --yes --json
```

**1.10.0 的限制**：signing planner 每次都安排同步，因此 standalone signing verify 会保留 pending 操作，不能靠反复 initialize 等它变绿。检查 apply 成功结果；下一步 archive 会对真实 profile、证书、entitlements 和签名执行检查。

## 4.3 归档正式包【CLI，消耗本机构建时间】

确认 `release.version` 和 `release.buildNumber` 是本次要上传的值；不要拿旧版本的构建号、旧源码摘要或另一套 Team 混用。

工程须位于真实 Git 工作区，供 CLI 计算源码指纹；首次 Git 初始化、审阅和提交由项目负责人完成。先按项目自身流程解析依赖并保留锁文件。Flutter 先完成 `flutter pub get`；使用 CocoaPods 的项目在 `ios` 目录按项目锁定版本执行 `pod install`。使用 Swift Package Manager 时先在 Xcode 解析并核对实际锁定版本。CLI 的归档不替你自动升级依赖，Flutter 配置阶段使用 `--no-pub`。

```bash
stackonward apple preflight --manifest "$IOS_MANIFEST" --scope build --offline --json
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope build --intent archive --state "$IOS_STATE" --out "$IOS_STATE/archive.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope build --intent archive --state "$IOS_STATE" \
  --plan "$IOS_STATE/archive.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope build --intent archive --state "$IOS_STATE" --json
```

保存实际输出中的 IPA、dSYM 和 `artifact.json`。CLI 检查源码／公开参数摘要、版本、Team、主 App 与 appex 的签名、profile、证书及授权边界。不要编辑摘要文件来冒充另一个构建。

## 4.4 核对最终包和网站【只读】

将实际产物路径赋值，而不是猜固定文件名：

```bash
export IOS_IPA="/absolute/path/to/actual.ipa"
export IOS_DSYM="/absolute/path/to/actual.dSYM.zip"

stackonward apple check --manifest "$IOS_MANIFEST" \
  --ipa "$IOS_IPA" --dsym "$IOS_DSYM" --website --json
```

也可用 `--app /absolute/Actual.app` 替代 `--ipa`，二者不能同时传。dSYM 支持目录或 ZIP，必须和包一起提供，比较主可执行文件的 UUID 与架构。

仅将实际需要的用途文案和原生语言加入 `checks.package`。例如：

```json
{
  "checks": {
    "package": {
      "requiredPurposeStrings": ["NSCameraUsageDescription"],
      "locales": ["en", "zh-Hans"],
      "deviceFamilies": [1, 2]
    }
  }
}
```

这个例子只适用于确实使用相机、这些原生语言且支持相应设备的 App。最低系统和根隐私清单要求按实际项目设置。检查清单结构、签名完整性与实际 SDK 数据行为分别确认。

## 4.5 上传并等待 Apple 处理【CLI】

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope upload --intent upload --state "$IOS_STATE" --out "$IOS_STATE/upload.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope upload --intent upload --state "$IOS_STATE" \
  --plan "$IOS_STATE/upload.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope upload --intent upload --state "$IOS_STATE" --json
```

上传使用构建产物和摘要。传输接受、构建处理完成、可被版本选择是不同状态。处理尚未完成时先查看 Apple 的实际状态与错误，不因为暂时不可用就盲目再传同一构建。新构建使用新的构建号并重新归档。

```bash
stackonward apple status --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" --json
stackonward apple check --manifest "$IOS_MANIFEST" \
  --remote --account "$IOS_ACCOUNT" --website --json
```

## 4.6 TestFlight【推荐测试渠道，可按需使用】

按 [TestFlight 概览](https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/) 在 ASC 创建测试组，取得该组的准确 ID。CLI 1.10.0 不创建测试组；组名不是 `groupIds`，组类型须与 `external` 一致。若网页地址没有给出明确 ID，使用 Apple 的 [App 测试组 ID 读取接口](https://developer.apple.com/documentation/appstoreconnectapi/get-v1-apps-_id_-relationships-betagroups) 或由有权限的管理员提供，不猜测 ID。

外测前在 ASC 的 TestFlight 页面补齐 Beta App Review 联系人、需要的测试账号、审核说明等资料；它们与正式商店审核资料分别维护。CLI 1.10.0 的 testflight 配置不提供这些审核凭据字段。

在 `testflight` 填真实 `groupIds`、`betaDescription`、`feedbackEmail`、`whatsNew`、`locale`、`external` 和 `notifyTesters`。prepare 保存资料，不等于分发或发邀请：

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope testflight --intent prepare --state "$IOS_STATE" --out "$IOS_STATE/beta-prepare.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope testflight --intent prepare --state "$IOS_STATE" \
  --plan "$IOS_STATE/beta-prepare.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope testflight --intent prepare --state "$IOS_STATE" --json
```

外测才执行 Beta App Review；不要对内测组运行这一段：

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope testflight --intent review --state "$IOS_STATE" --out "$IOS_STATE/beta-review.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope testflight --intent review --state "$IOS_STATE" \
  --plan "$IOS_STATE/beta-review.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope testflight --intent review --state "$IOS_STATE" --json
```

审核达到相应要求后，向准确的组分发：

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope testflight --intent distribute --state "$IOS_STATE" --out "$IOS_STATE/beta-distribute.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope testflight --intent distribute --state "$IOS_STATE" \
  --plan "$IOS_STATE/beta-distribute.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope testflight --intent distribute --state "$IOS_STATE" --json
```

发邀请是另一项外部动作。需要时在私有 `invitationsRef` 文件放实际测试员数组，每项有 `email`、`firstName`、`lastName`，文件权限 `0600`：

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope testflight --intent invite --state "$IOS_STATE" --out "$IOS_STATE/beta-invite.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope testflight --intent invite --state "$IOS_STATE" \
  --plan "$IOS_STATE/beta-invite.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope testflight --intent invite --state "$IOS_STATE" --json
```

用 TestFlight 实际安装构建，完成登录、删号、关键功能、网络异常和适用的购买／恢复／推送等测试。TestFlight 的 StoreKit 测试和 APNs 环境分别核对；不能因为 StoreKit 是 Sandbox 就把推送一律配成 Sandbox。外测审核通过不等于正式商店审核通过。

下一步：[提审与发布](05-review-and-release.md)。
