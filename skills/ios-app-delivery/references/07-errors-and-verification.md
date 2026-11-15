# 7. 完整性检查与失败恢复

`check` 列出交付资料和证据缺口，不修改项目或账号；`verify` 回读某个 scope 的已配置目标。两者不能证明产品功能、Apple 审批或全部地区已经可下载。

## 7.1 按现有证据检查【只读】

在 App 项目根目录，使用第 1 章的路径变量：

```bash
# 本地配置与资料
stackonward apple check --manifest "$IOS_MANIFEST" --json

# 增加公开网站检查
stackonward apple check --manifest "$IOS_MANIFEST" --website --json

# 增加 ASC 远端读取
stackonward apple check --manifest "$IOS_MANIFEST" --remote --account "$IOS_ACCOUNT" --json

# 已有正式归档产物时，合并网站、包、符号与远端检查
stackonward apple check --manifest "$IOS_MANIFEST" --website \
  --remote --account "$IOS_ACCOUNT" --ipa "$IOS_IPA" --dsym "$IOS_DSYM" --json
```

没有包时先做前三项，不传空路径。检查本地 `.app` 时用 `--app /absolute/path/Actual.app` 替代 `--ipa`，二者互斥；dSYM 必须同时提供对应包。包检查需要 macOS 的 codesign、plutil、dwarfdump 和 unzip，不会自动构建、安装或操作 App。

报告分为 `manifest/website/package/remote/runtime`，逐项读取 `code/status/severity/field`：

| 状态 | 含义与处理 |
| --- | --- |
| `verified` | 本次指定证据的检查已通过 |
| `missing` | 已检查的必需项缺失，补齐对应配置或资料 |
| `failed` | 读取或核对失败，按具体 code 排查 |
| `not-checked` | 未提供证据，或需要人工／真实设备验证 |
| `not-applicable` | 已明确不适用 |

`outcome: verified` 只表示本次自动检查没有错误级别的 missing/failed；`runtimeVerified` 始终为 `false`。阅读 not-checked 项并完成实际验收，不把它转写成“所有功能全部通过”。

网站检查从每种商店语言的 `supportUrl/privacyPolicyUrl/marketingUrl/privacyChoicesUrl` 取 URL。支持自己的域名、子域名、路径与查询参数，无固定业务路径。它匿名访问、最多跟随五次 HTTPS 跳转，不发送账号或 Cookie；检查 HTTP、HTML、语言、标题、服务端正文和 canonical。质量提示不是全部 Apple 硬性字段，页面内容和交互仍须人工核对。

离线 preflight 只检查本地结构和引用材料，不证明工程可编译、凭据可用、设备组被当前 Apple 接受或功能可用。例如：

```bash
stackonward apple preflight --manifest "$IOS_MANIFEST" --scope metadata --offline --json
```

## 7.2 保存当前远端状态与交接资料【只读】

```bash
stackonward apple status --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --state "$IOS_STATE" --json
stackonward apple export --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --state "$IOS_STATE" --out "$IOS_PRIVATE/asc-export.json" --json
stackonward apple handoff --manifest "$IOS_MANIFEST" --account "$IOS_ACCOUNT" \
  --state "$IOS_STATE" --out "$IOS_PRIVATE/runtime-handoff.json" --json
```

输出文件使用尚不存在的路径；第二次导出换新文件名。export 是读取结果，不覆盖 manifest 或替代完整账号备份。handoff 给出产品标识和运行时配置需求，identity/notifications/commerce 的 verified 保持 false，直到相应服务独立验收。

## 7.3 看懂退出码

| 退出码 | 常见含义 | 下一步 |
| --- | --- | --- |
| `0` | 当前命令成功 | 仍按结果字段判断成功范围 |
| `2` | 输入、路径、字段或命令组合不合法 | 修正输入，查 `apple schema` 和该命令 `--help` |
| `3` | Portal／Privacy 登录或 session 问题 | 在自己的终端重新交互登录，不在聊天中提交凭据 |
| `4` | 计划／身份／状态冲突，或 verify 仍有待执行项 | 读取具体 code，确认远端状态后生成新 plan |
| `5` | API、工具、构建或回读失败 | 阅读 code、HTTP 状态和私有进度／回执 |
| `6` | 检查被缺项阻塞或存在人工事项 | 看 completed 和 manualRequirements，完成人工操作再重新 plan |
| `7` | 写入结果 unknown，需要核实 | 保留执行状态，先查实际资源与恢复信息 |
| `130` | 取消 | 判断取消发生在写入前还是写入后，再恢复 |

不要将整份教程拼成遇到失败就自动重放的脚本。一次命令非零退出，不代表没有创建或修改任何资源。

## 7.4 常见问题与恢复

| 情况 | 处理方式 |
| --- | --- |
| 首次 setup 返回 `app_record_required` | 查看已完成的 Bundle/capability；人工创建 ASC App，填 appId，再生成新 setup plan |
| 修改 manifest 后旧计划不能 apply | 重新 plan，检查新差异，不手改旧 plan 的操作或摘要 |
| `account_configuration_required`／凭据 scope 冲突 | API、Portal、Privacy 三套账号按章节分开传；APNs／Privacy 不附加 `--account` |
| 网站 200 但显示空白、登录页或错误正文 | 确认真实页面、服务端正文、语言、链接和匿名访问；不要只改检查结果 |
| signing verify 始终有 sync pending | 1.10.0 已知行为；查看成功 apply，再用 archive 的真实签名检查，不重复 initialize |
| 构建版本／Bundle／Team／profile 不一致 | 修正真实工程、配置或签名资源，重新归档；不编辑 artifact.json 绕过 |
| 构建仍在 processing 或不可选 | 查 Apple 处理与错误；按 manifest 的精确版本／构建读取，不改成“最新构建” |
| review prepare 返回 6 | 可能已关联构建并建草稿；确认回执和具体人工事项，保留本次准确审核批次 |
| `first_purchase_requires_console` | 在 ASC 按首次商品／订阅联提规则处理；不删除标记绕过 |
| 审核提交包含不受管理的项目 | 在 ASC 和 manifest 核对准确批次与所有审核项，移除确实不属于本次的内容后重新准备 |
| 图片处理中断 | 保留绑定和 state，修复实际素材错误；在结果已知、adapter 支持恢复时重新 plan/apply，复用已处理素材 |
| `previous_write_requires_reconciliation` | 先核实实际 Apple 资源和私有日志；CLI 没有通用“强制成功”或清 journal 命令 |
| APNs 一次性下载中断 | 保留 `.p8` 旁的私有恢复文件与原 state；无法回读的私钥不能通过更换 state 找回 |
| 隐私替换写入后超时或 unknown | 对照 ASC 的实际答案和本地记录核实，不把原文件再盲目上传一遍 |
| 发布请求接受但商店尚不可见 | 查看本次版本状态、地区／价格／协议与商店实际页面，不能自动当作上架成功 |

执行结果中的 `progressPath`、`receiptPath` 指向私有进度和回执。对外求助时只分享脱敏的 code、资源身份和必要状态；私钥、session、演示账号和包含私钥的下载恢复文件不贴进聊天或公开 issue。

`plan --out` 可以更新同一个私有计划文件；需要保留旧计划时另取文件名。重新 plan 指重新生成并阅读内容，不是必须不断更换文件名。export、handoff 和 privacy-download 的输出则要求使用新文件路径。

## 7.5 最后由人完成的验收

| 范围 | 检查内容 |
| --- | --- |
| 账号 | 正确主体、有效会员、人员权限及适用协议；需要时核对税务和银行 |
| 网站 | HTTPS、域名及链接正确；支持入口有人处理；政策与服务事实一致；各声明语言可读 |
| App | 冷启动、核心流程、断网／超时、权限拒绝与恢复、前后台、真实设备和适用屏幕 |
| 账号功能 | 登录／退出、真实邮件和验证码、第三方登录及取消；App 内删号和数据处理 |
| 付费功能 | 真实商品／币种／周期、购买、恢复、续费、退款／撤销、账号归属、服务端通知及权益 |
| 推送 | 最终签名环境、真实设备 token、服务端发送、前后台接收及退出／删除后的处理 |
| 隐私 | SDK 数据行为、ATT 适用性、权限用途、隐私清单、标签与实际政策一致 |
| 商店 | 正确版本与构建、真实截图和说明、年龄／内容／加密、发行地区和适用资质 |
| 审核 | 有效联系人、可用测试账号、完整入口说明；审核问题有实际修复及回复 |
| 发布 | 已获批的本次版本、实际商店可下载、正式安装后核心服务仍正常 |

未使用的能力标明不适用。人工验收记录保存在产品自己的发布资料中；本技能包不收集任何 App 的账号或业务数据。
