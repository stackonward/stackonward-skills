# 5. 提审、发布与更新

前置条件：网站可公开访问；资料、截图、年龄问卷和适用声明已完成；本次 `release.version/buildNumber` 对应的构建已上传、处理为 `VALID` 且未过期；真实设备测试已完成。继续使用第 1 章的路径变量。

## 5.1 完成人工声明【负责人操作】

在 ASC 逐项确认以下事实，不把“CLI 无报错”当成负责人确认：

| 事项 | 实际完成内容 |
| --- | --- |
| 隐私 | 标签与 App、服务端及 SDK 一致，并已发布；隐私政策可访问 |
| 加密 | 当前构建的答案准确；需要的声明已获批并关联正确 App |
| 内容权利 | 自有及第三方内容具有相应使用权，后台声明与事实一致 |
| 地区 | 发行地区、经营身份、许可、备案及适用 DSA 等要求已处理 |
| 账号与审核入口 | 联系人可联系；演示账号可登录并能访问完整审核功能 |
| 商业协议 | 免费、付费、内购各自适用的协议已生效；需要时完成税务和银行资料 |

`declarations` 用于记录负责人已经核实的事项，不替代后台操作或法律判断。支持的常用代码为 `privacy`、`encryption`、`contentRights`、`regionalCompliance`。例如在 `delivery/apple/declarations/privacy.md` 写清本次核实的数据行为、后台页面及结论，再在 manifest 引用：

```json
{
  "declarations": [
    {
      "code": "privacy",
      "file": "declarations/privacy.md",
      "confirmed": false,
      "evidence": "operator-attestation",
      "consoleUrl": "https://appstoreconnect.apple.com/"
    }
  ]
}
```

先填写自己的核实记录，负责人确实完成后才把对应 `confirmed` 改为 `true`；其余代码按实际需要增加，不能复制后统一确认。文件须存在且位于 manifest 目录内。`remote-readback` 不是要求 CLI 去自动证明文件内容，未由对应 adapter 核实的声明仍会要求人工处理。

已配置 `release.encryption` 和 `metadata.contentRightsDeclaration` 时，review 会核对对应远端值；内容权利先通过 metadata 同步。隐私保存与发布见第 3 章。首次内购或订阅的联提条件见第 6 章。

## 5.2 选择发布方式【CLI，提审前配置】

在版本仍可编辑时设置 `release.mode`。三种方式任选一种：

| 值 | 审核通过后的行为 |
| --- | --- |
| `MANUAL` | 等负责人手动发布 |
| `AFTER_APPROVAL` | Apple 批准后自动发布 |
| `SCHEDULED` | 批准后不早于指定时间自动发布 |

定时方式另填 `release.earliestReleaseDate`，使用真实未来时间的 ISO 8601 **UTC `Z`** 字符串，例如格式 `YYYY-MM-DDTHH:mm:ssZ`。不要把本地北京时间直接加 `Z`；审批未完成时不会因时间已到而自动通过。参见 [Apple 发布方式](https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/select-an-app-store-version-release-option/)。

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope release --intent configure --state "$IOS_STATE" --out "$IOS_STATE/release-policy.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope release --intent configure --state "$IOS_STATE" \
  --plan "$IOS_STATE/release-policy.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope release --intent configure --state "$IOS_STATE" --json
```

`configure` 保存策略，不会立即发布 App。

## 5.3 准备审核批次【CLI】

确认 `release.reviewItems` 只包含本次实际提交的内容。仅提交 App 时为 `includeApp: true`、`productIds: []`、`groupKeys: []`。商品及订阅组不能用名称猜远端身份。

```bash
stackonward apple preflight --manifest "$IOS_MANIFEST" --scope review --intent prepare --offline --json
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope review --intent prepare --state "$IOS_STATE" --out "$IOS_STATE/review-prepare.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope review --intent prepare --state "$IOS_STATE" \
  --plan "$IOS_STATE/review-prepare.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope review --intent prepare --state "$IOS_STATE" --json
```

prepare 会核对精确版本／构建、按需关联构建、建立或复用审核草稿并加入选定项目，**不提交审核**。首次不需要先在网页手动选择构建。

它也可能完成部分写入后因人工事项返回退出码 6。检查 `receipt.completed`、`manualRequirements` 和实际 ASC 草稿，不能把非零退出码理解为未执行。

取得这次草稿的准确 ID：

- 新建草稿时，从 apply 的 `receipt.completed` 中找到 `type` 为 `reviewSubmissions` 的资源。
- 复用草稿时，查看上述 prepare verify 的 `resources`，找到本次选定的 `reviewSubmissions`。

核对其所属 App、iOS 平台及本次审核项，填入 manifest 的 `release.reviewSubmissionId`。`status` 可能包含多个历史批次，不能取列表第一项。CLI 1.10.0 没有 `--review-submission-id` 或 `--build-id` 参数；这些值放在 manifest。

## 5.4 正式提交审核【CLI 或适用的网页联提】

先完成 prepare 中列出的人工事项，再基于已填写的审核批次 ID **重新 plan**：

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope review --intent submit --state "$IOS_STATE" --out "$IOS_STATE/review-submit.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope review --intent submit --state "$IOS_STATE" \
  --plan "$IOS_STATE/review-submit.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope review --intent submit --state "$IOS_STATE" --json
```

submit 会核对审核项精确匹配、构建和声明已准备，防止把其他内容一起送审。首次相应类型内购／首次订阅需要网页联提时，按 [Apple 提交流程](https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-app/) 在同一版本选择相关项目并确认正式提交；不要删掉商品或首次类型标识来绕过限制。

```bash
stackonward apple status --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --state "$IOS_STATE" --json
```

`WAITING_FOR_REVIEW` 表示已排队，`IN_REVIEW` 表示审核中，不是批准。留意 ASC 的消息与 Resolution Center；收到问题后按具体条款修复、回复或重新提交，不重复发送已有审核请求。

确实需要撤回时，核对 `release.reviewSubmissionId`，并只在 Apple 允许的当前状态执行：

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope review --intent withdraw --state "$IOS_STATE" --out "$IOS_STATE/review-withdraw.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope review --intent withdraw --state "$IOS_STATE" \
  --plan "$IOS_STATE/review-withdraw.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope review --intent withdraw --state "$IOS_STATE" --json
```

## 5.5 发布到商店【CLI + 真实商店核对】

`MANUAL` 方式在本次版本达到 `PENDING_DEVELOPER_RELEASE` 后才执行：

```bash
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope release --intent publish --state "$IOS_STATE" --out "$IOS_STATE/release-publish.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope release --intent publish --state "$IOS_STATE" \
  --plan "$IOS_STATE/release-publish.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope release --intent publish --state "$IOS_STATE" --json
```

`AFTER_APPROVAL` 和 `SCHEDULED` 按已保存的策略等待，不把手动 publish 当成必做步骤。返回 `release_processing_pending` 时先查看远端实际状态和回执；接受发布请求与所有地区已可下载是两回事。

发布后在计划发行的地区打开 App Store 页面，核对名称、截图、隐私、价格和版本，使用正式渠道安装并走通关键功能。检查购买与恢复、服务端通知、推送、账号删除等适用场景；TestFlight 成功不能代替正式商店验证。

## 5.6 后续版本与分阶段更新

已有 App 保持原有 Bundle ID、App ID、SKU、Team 及商品身份。新商店版本更新 `release.version`；重新上传构建使用新的 `buildNumber`。更新说明、截图、隐私、年龄问卷及地区事项只按实际变更调整，但每次都确认其仍然准确。

清除 manifest 中上一批次的 `reviewSubmissionId`，重新 prepare 并绑定本次 ID；不要删除执行状态或已有商品绑定。源代码／公开配置改变后重新归档，不复用旧 `artifact.json`。

需要对更新使用 Apple 的 [分阶段发布](https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/) 时，在可编辑阶段设置 `release.phasedRelease: true`，执行本章 configure。它控制自动更新的分阶段分发，不阻止用户手动下载。

后续控制先确认该版本的实际 phased release 资源，可用 `release.phasedReleaseId` 固定身份。以下只选择一个真实需要的动作：`pause`（ACTIVE → PAUSED）、`resume`（PAUSED → ACTIVE）、`complete`（ACTIVE／PAUSED → COMPLETE）。

```bash
export IOS_RELEASE_ACTION="pause"
stackonward apple plan --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope release --intent "$IOS_RELEASE_ACTION" --state "$IOS_STATE" \
  --out "$IOS_STATE/phased-$IOS_RELEASE_ACTION.plan.json"
stackonward apple apply --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope release --intent "$IOS_RELEASE_ACTION" --state "$IOS_STATE" \
  --plan "$IOS_STATE/phased-$IOS_RELEASE_ACTION.plan.json" --yes --json
stackonward apple verify --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --scope release --intent "$IOS_RELEASE_ACTION" --state "$IOS_STATE" --json
```

已有 phased release 时，把 `phasedRelease` 改为 `false` 不会自动删除；需要移除按 ASC 支持的操作处理。

检查与异常处理见 [第 7 章](07-errors-and-verification.md)。
