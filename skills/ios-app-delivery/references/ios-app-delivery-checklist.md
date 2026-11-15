# 187 项 iOS App 上架检查清单

适用于通过 App Store 发行的原生 iOS 或 Flutter iOS App，覆盖首次提交、版本更新和发布后的验收。每项包含通过标准、验证方式和适用条件，可按编号记录结果。

- **通用**适用于常规上架流程。
- **按需**取决于 App 能力、目标地区、账号资格或实际出现的表单。
- **增强**用于营销、分析或运营，可按发行目标选用。

标注 `CLI` 的条目可以用 StackOnward CLI 1.10.0 辅助对应步骤。命令和适用条件见各章指南。查看自动报告中实际执行的项目，再按清单中的验证方式完成协议处理、声明核实和真机验收。 [检查结果说明](07-errors-and-verification.md)

## 目录

| 主题 | 检查项 |
| --- | ---: |
| [1. 账号、标识与密钥](#1-账号标识与密钥) | 12 |
| [2. 官网、支持与法律页面](#2-官网支持与法律页面) | 24 |
| [3. App Store Connect 商店资料](#3-app-store-connect-商店资料) | 27 |
| [4. 数据、同意与隐私](#4-数据同意与隐私) | 16 |
| [5. 年龄、版权、出口与地区](#5-年龄版权出口与地区) | 14 |
| [6. 内购、订阅与价格](#6-内购订阅与价格) | 16 |
| [7. 原生工程、权限与 SDK](#7-原生工程权限与-sdk) | 15 |
| [8. 登录、删除账号与内容治理](#8-登录删除账号与内容治理) | 10 |
| [9. 服务、推送与环境](#9-服务推送与环境) | 14 |
| [10. 签名、归档、IPA 与上传](#10-签名归档ipa-与上传) | 15 |
| [11. TestFlight 与审核](#11-testflight-与审核) | 12 |
| [12. 真机、发布与维护](#12-真机发布与维护) | 12 |
| **合计** | **187** |

## 1. 账号、标识与密钥

[Apple Developer 注册](https://developer.apple.com/programs/enroll/) · [创建 App 记录](https://developer.apple.com/help/app-store-connect/create-an-app-record/add-a-new-app/) · [团队角色](https://developer.apple.com/help/app-store-connect/manage-your-team/overview-of-accounts-and-roles/) · [CLI 账号配置](01-accounts-and-tools.md)

| 编号 | 检查项与通过标准 | 验证方式 | 适用范围与变更位置 |
| --- | --- | --- | --- |
| A01 | 核实账号主体、公开卖方名称和联系方式。组织按注册条件准备法人资格、D-U-N-S 编号、域名邮箱和官网 | Developer Program · 人工 | 通用 · 账号 |
| A02 | 确认会员资格有效、账户持有人可处理续费和协议，Xcode 使用实际发行团队 | Developer 账号、Xcode Accounts · 人工 | 通用 · 账号 |
| A03 | 为 Apple Account 启用双重认证，并为团队成员分配独立账号 | 账号与 Users and Access · 人工 | 通用 · 账号 |
| A04 | 核对操作者的角色、App 访问范围和证书与标识访问权限。分别检查网页账号及 API Key 的权限 | Users and Access、Integrations · 人工/API | 通用 · 账号 |
| A05 | 核对 Bundle ID、Team ID、ASC 数字 App ID 和 App SKU 的引用关系。使用内购时同时核对商品与订阅组标识 | manifest、Developer、ASC · `CLI:setup` | 通用 · 部分标识不可随意变更 |
| A06 | 在 App Store Connect 选择正确平台、名称、主语言、SKU 和 Bundle ID 建档。取得数字 App ID 后绑定到交付清单 | ASC 新建 App 网页 · `CLI:setup` 回读 | 通用 · 首次建档需网页 |
| A07 | 按实际功能启用 Sign in with Apple、推送、内购等适用能力，逐项核对与 App ID 和签名相关的配置 | Certificates, Identifiers & Profiles · `CLI:setup` | 按需 · 工程和 profile 可能重建 |
| A08 | 核对 App Store Connect Team API Key 的 Key ID、Issuer ID、私钥与团队。私钥保存在受保护的位置，并准备撤销和人员交接流程 | API Key 管理、外部私有配置 | 使用 API 时 · 账号 |
| A09 | 按用途确认 App Store Connect、APNs、Apple 登录和内购服务所用密钥的授权范围、持有人及存储位置 | Developer/ASC/服务端秘密配置 | 按需 · 服务与账号 |
| A10 | 在受控位置存储与备份私钥、证书、签名密码、Portal 会话和审核凭据。检查文件权限、Git、App 资源、日志及截图中的凭据隔离 | 私有文件、秘密管理 · 源码检查 | 通用 · 账号与工具 |
| A11 | 核对实际使用的 Node、Xcode、Flutter、Ruby、Bundler、Fastlane 和锁文件。确认安装的 CLI 版本提供教程中的命令 | 版本输出、锁文件、`apple --help` | 使用 CLI 时 · 本机工具 |
| A12 | 在空目录初始化交付模板。已有项目升级时比较配置差异，保留已有商店资料、素材和私有状态 | `apple init`、schema、版本差异 | 使用 CLI 时 · 本地文件 |

## 2. 官网、支持与法律页面

支持页和隐私政策是 App Store 发行资料的一部分。营销页、博客、搜索优化和分享按发行需求选择。

[商店网址字段](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/) · [App 隐私管理](https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy/) · [Associated Domains](https://developer.apple.com/documentation/xcode/supporting-associated-domains) · [多语言网站](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites) · [Google Consent Mode](https://developers.google.com/tag-platform/security/concepts/consent-mode) · [网站配置指南](02-website-and-app.md)

| 编号 | 检查项与通过标准 | 验证方式 | 适用范围与变更位置 |
| --- | --- | --- | --- |
| W01 | 公开域名正确指向正式站，HTTPS 证书有效、证书链完整，审核期间可访问 | DNS、TLS、HTTP · `dig`、`curl`、浏览器 | 通用支持/政策站 · 网站部署 |
| W02 | Support URL 提供有效支持入口。通过真实的邮件或表单往返验证有人接收和处理 | 支持页、真实邮件往返 | 通用 · 网站及商店字段 |
| W03 | 用户无需登录即可在手机上阅读隐私政策。分别从商店和 App 内打开正确的政策正文 | ASC、App、浏览器 | 通用 · 网站及商店字段 |
| W04 | 政策与联系页准确标识运营者、开发者和相关数据处理服务商，联系渠道与发行主体和实际业务相符 | 政策、联系页、账号 · 人工审读 | 通用 · 网站 |
| W05 | 政策准确说明收集的数据、处理目的、接收方、留存和删除、用户权利与联系渠道。涉及跨境处理时核对实际地域与适用要求 | 政策、数据流、服务配置 | 通用 · 网站，相关商店标签同步 |
| W06 | 核对 App SDK、后端、存储及第三方 AI 等数据接收方的实际用途，按适用要求维护供应商信息与政策链接 | 政策、SDK 依赖、供应商配置 | 按需 · 网站及 App 告知 |
| W07 | 按合同、供应商政策和实际配置确认留存期限、模型训练用途及数据处理地域，再写入对用户的承诺 | 合同、供应商政策、实际绑定 | 按需 · 网站及告知 |
| W08 | 核对服务、付款、退款、内容权利和责任条款。隐私政策、服务条款和适用的 EULA 各自说明对应事项 | 条款页、购买页、ASC 描述 | 按需 · 网站/metadata |
| W09 | 支持创建账号时，从 App 内验证可发起删除。增设网站说明时，确保指引与实际处理方式一致 | App、删除说明页、服务端 | 按需 · App/网站/服务 |
| W10 | 核对删除完成时间、依法需保留的数据及理由、订单或订阅影响。发起测试删除后核实实际结果 | 删除说明与真实删除结果 | 按需 · App/网站/服务 |
| W11 | 数据访问、更正、导出和撤回的说明与适用要求及实际处理流程一致 | 政策、设置、支持处理流程 | 按需 · 网站/服务/App |
| W12 | 填写 Privacy Choices URL 时，页面清楚说明用户如何管理隐私选择。可使用提供这些说明的隐私政策页 | ASC 字段、网站 | 可选字段 · metadata |
| W13 | 逐语言核对 URL、正文、标题及其与商店语言的对应关系，同时打开公开网页和 App 内入口 | 路由、locale 内容、浏览器 | 多语言时 · 网站/metadata |
| W14 | 在 App 内嵌网页中验证可阅读、滚动和返回，政策正文与联系入口完整可见 | App 内嵌浏览器、真机 | 使用内嵌页时 · 网站/App |
| W15 | 下载按钮和二维码指向同一个实际可用的 App 入口。从目标商店地区打开并核对 App ID | 下载页、二维码解码、商店 | 增强 · 网站/商店地区 |
| W16 | 官网、下载页、FAQ 和截图展示的能力与发行版 App 一致，承诺可在对应版本验证 | 页面内容、发行包 · 人工核对 | 营销站 · 网站 |
| W17 | 按支持场景实测窄屏、大字号、键盘、焦点、从右到左的排版、按钮、图片和错误页，确认法律正文始终可阅读 | 浏览器与设备 | 网站存在时 · 网站 |
| W18 | 核对 canonical、hreflang、语言切换和旧地址跳转。验证公开页面返回可读取的正文，错误地址返回正确的 HTTP 状态 | HTML、HTTP、现有站点检查 | SEO 增强 · 网站 |
| W19 | 按页面用途核对 robots、sitemap 和 noindex。确认正式页面可以被预期地收录，需要移除的页面已按搜索引擎规则处理 | HTTP、HTML、搜索工具 | SEO 增强 · 网站 |
| W20 | 核对搜索标题、描述、分享图和结构化数据，并按实际商店地区展示下载状态 | HTML、分享预览、商店 | SEO 增强 · 网站 |
| W21 | 核对网站 Cookie 或分析的默认行为、拒绝、撤回、重访和实际网络请求。分别验证网站与 App 中的选择 | 浏览器存储和网络日志、真机 | 按需 · 网站/标签发布 |
| W22 | 验证支持邮箱收发。发送验证或通知邮件时，再核对实际投递、退信和 SPF、DKIM、DMARC 等发信配置 | 邮箱、DNS、服务商配置 | 使用域名邮件时 · DNS/服务 |
| W23 | 在启用 Universal Links 时核对站点 AASA 与 App Associated Domains，并验证 AASA 可通过 HTTPS 直接获取且无重定向，再在真机上打开链接 | AASA、entitlement、设备点击 | 按需 · 网站和 App |
| W24 | 核对 Smart App Banner、活动链接、二维码及下载归因。分别衡量商店点击、安装和首次打开 | 网页元标签、分析、商店报告 | 增强 · 网站/分析 |

## 3. App Store Connect 商店资料

[App 信息](https://developer.apple.com/help/app-store-connect/reference/app-information/app-information/) · [版本资料](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/) · [截图规格](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/) · [Apple 芯片 Mac 分发](https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/manage-availability-of-iphone-and-ipad-apps-on-macs-with-apple-silicon/) · [Apple Vision Pro 分发](https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/manage-availability-of-iphone-and-ipad-apps-on-apple-vision-pro/) · [商店资料配置](03-store-configuration.md)

| 编号 | 检查项与通过标准 | 验证方式 | 适用范围与变更位置 |
| --- | --- | --- | --- |
| M01 | 核对主语言、App 名称、SKU、Bundle ID 与数字 App ID 是否对应同一个 App 和开发者团队 | App Information、`app.*` · `CLI:setup` | 通用 · 商店身份 |
| M02 | 逐语言核对名称、副标题、商标和产品承诺。App 名称为 2 至 30 个字符，副标题最多 30 个字符 | 名称及副标题字段 · `CLI:metadata` | 名称通用、副标题可选 · 商店版本 |
| M03 | 逐语言核对描述中的用途、主要能力、价格和订阅说明。使用纯文本，最多 4,000 个字符 | locale JSON · `CLI:metadata` | 通用 · 商店版本 |
| M04 | 为适用语言填写相关关键词，核对词条分隔和品牌权利，按 Apple 当前要求最多提供 100 字节 | 商店各语言关键词 · `CLI:metadata` | 提交商店版本时 · 商店资料 |
| M05 | 按需填写推广文本，最多 170 个字符。提交更新时按 Apple 字段要求填写相应语言的更新说明，写明本版本实际改动 | `promotionalText/whatsNew` | 按版本 · 字段的生效方式不同 |
| M06 | 主分类及填写的次分类应与 App 的真实用途相符 | metadata 分类 · `CLI:metadata` | 通用 · 商店 |
| M07 | 按适用字段分别核对支持、营销、隐私政策和隐私选择网址的用途、语种与可访问性 | locale JSON · `CLI:metadata` | 通用及可选字段 · 商店 |
| M08 | 核对版权署名，并按 App 实际使用的内容分别处理 Content Rights 声明 | copyright、Content Rights | 通用 · metadata/人工声明 |
| M09 | 对照 App Store Connect、网站及原生工程的语言标识，确认各端映射到正确语言 | 语言映射、工程设置和商店资料 | 多语言时 · 多端 |
| M10 | 分别核对商店文字、截图文案、原生资源和 App 实际支持的界面语言 | 商店、截图、设备语言 | 多语言时 · 素材/App |
| M11 | 按 Apple 当期截图规格提供所需设备组，检查各组语言、尺寸和方向 | ASC、图片尺寸 · `CLI:assets` | 通用 · 商店素材 |
| M12 | 使用真实发行功能的截图，核对可读性、顺序、主题和素材中个人信息及测试数据的清理 | 原始截图、商店预览 | 通用 · 商店素材 |
| M13 | 逐张核对文件尺寸、格式、透明通道、显示组、语言和排序是否匹配 | 素材/manifest · `CLI:assets` | 通用 · 商店素材 |
| M14 | 普通截图、内购审核截图、推广素材和产品页素材各按所属位置配置。通过归档检查 App 图标 | assets、catalog、AppIcon | 按需 · 素材或 App |
| M15 | 提供 App 预览时，按当期规格核对内容、设备组、时长、音频和封面帧 | `assets.previews` · `CLI:assets` | 增强 · 商店素材 |
| M16 | 变更素材前核对追加、替换或删除的精确目标。遇到处理中断时，先回读远端和执行回执，再恢复对应操作 | plan/回执/ASC · `CLI:assets` | 自动上传时 · 商店素材 |
| M17 | 上传后逐语言和设备组核对素材处理结果、关联顺序及实际预览，再确认版本审核与公开状态 | CLI 回读与 ASC 预览 | 使用素材时 · 商店 |
| M18 | 在 App Store Connect 确认 Apple 芯片 Mac 上的兼容分发设置。发布前实测最低系统、输入和适用的购买功能 | Pricing and Availability、Mac 测试 | 兼容分发时 · 商店/App |
| M19 | 在 App Store Connect 确认 Apple Vision Pro 的兼容分发设置。在对应运行方式下验证交互、硬件和核心功能 | Pricing and Availability、兼容测试 | 兼容分发时 · 商店/App |

### 3.1 可选的商店运营

[自定义产品页](https://developer.apple.com/app-store/custom-product-pages/) · [产品页优化](https://developer.apple.com/app-store/product-page-optimization/) · [App 内活动](https://developer.apple.com/app-store/in-app-events/) · [推荐提名](https://developer.apple.com/documentation/appstoreconnectapi/featuring-nominations) · [Analytics Reports API](https://developer.apple.com/help/app-store-connect-analytics/overview/analytics-reports-api) · [评论回复](https://developer.apple.com/help/app-store-connect/monitor-ratings-and-reviews/respond-to-reviews/) · [内测反馈](https://developer.apple.com/help/app-store-connect/test-a-beta-version/view-tester-feedback/)

| 编号 | 检查项与通过标准 | 验证方式 | 适用范围与变更位置 |
| --- | --- | --- | --- |
| G01 | 核对自定义产品页的语言、截图、预览、推广文本、审核状态和渠道 URL | Custom Product Pages · 网页/官方 API | 增强 · 商店 |
| G02 | 核对产品页优化实验的素材变体、地区、流量分配和审核状态，按样本及指标解释结果 | Product Page Optimization · 网页/API | 增强 · 商店 |
| G03 | 核对 App 内活动资格、起止时间、地区、文案和深度链接，并实测打开目标活动 | In-App Events · 网页/API/设备 | 增强 · 商店与 App |
| G04 | 推荐提名提交准确的发布计划、重要更新和素材。在 App Store Connect 核对提名状态 | Featuring Nominations · 网页/API | 增强 · 商店运营 |
| G05 | 按同一口径核对曝光、产品页、转化、来源与使用指标，区分观测值、缺失值和隐私阈值导致的隐藏值 | App Analytics、Analytics Reports API | 增强 · 数据权限与分析 |
| G06 | 分别核对销售、下载、订阅、税费、净收益和结算周期，以对应的报告确认各项数据 | 销售/财务报表、官方 API | 收费运营时 · 报表 |
| G07 | 按平台和地区查看评分与评论。公开回复使用有权限的账号，保护评论者的个人信息 | Ratings and Reviews · 网页/API | 增强 · 公开回复 |
| G08 | 确认 TestFlight 反馈关联正确文本、截图、设备、系统版本、构建及崩溃数据，反馈事件按独立用途处理 | TestFlight Feedback、API/webhook | 内测运营时 · 反馈处理 |

## 4. 数据、同意与隐私

按实际数据处理分别核对网站政策、App 告知与控制、二进制内的 `PrivacyInfo.xcprivacy` 和 App Store Connect 隐私标签。

[App 隐私数据定义](https://developer.apple.com/app-store/app-privacy-details/) · [跟踪与隐私](https://developer.apple.com/app-store/user-privacy-and-data-use/) · [隐私清单](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files) · [Required Reason API](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api) · [第三方 SDK 要求](https://developer.apple.com/support/third-party-SDK-requirements/) · [数据使用与共享](https://developer.apple.com/app-store/review/guidelines/#data-use-and-sharing)

| 编号 | 检查项与通过标准 | 验证方式 | 适用范围与变更位置 |
| --- | --- | --- | --- |
| P01 | 盘点 App、后端、SDK、网关、存储、客服和分析的数据流，记录收集者、用途、身份关联、传输、留存和删除方式 | 源码、供应商合同、运行配置 | 通用 · 文案/服务/App |
| P02 | 分别确认姓名、邮箱、电话、照片或视频、其他用户内容及客服内容是否符合 Apple 对收集的定义 | 数据流与 SDK 声明 | 按实际数据 · ASC/政策 |
| P03 | 核对用户和设备标识、购买记录、产品交互、其他使用数据和粗略位置的实际处理 | API、分析、推送、IP 日志 | 按实际数据 · ASC/政策 |
| P04 | 分别核对崩溃、性能和其他诊断数据，以及是否与账号或设备关联。按 Apple 定义判断可选采集 | Crash/诊断 SDK、服务日志 | 按需 · ASC/政策/App |
| P05 | 按 Apple 定义确认搜索词、浏览记录、精确位置、音频、通讯录、支付和健康等数据是否实际收集。支付数据以 App 及服务商实际接触的数据为准 | 实际请求与持久化 | 按需 · ASC/政策 |
| P06 | 逐类数据填写实际用途、是否关联用户及是否用于跟踪，并对照 App 与第三方服务的真实行为 | App Store Connect · 网页或 `CLI:privacy` | 通用问卷 · 保存/发布 |
| P07 | 按 Apple 对跟踪的定义判断 ATT 的适用性。涉及跟踪时，在开始跟踪前取得所需系统授权并检查拒绝路径 | SDK、广告/归因、设备 | 按需 · App 与服务 |
| P08 | 分别核对首次告知、系统权限、向第三方发送数据时的许可与适用的内容权利声明，并验证请求发生顺序 | 启动/上传流程、网络顺序 | 按需 · App |
| P09 | 验证默认值、原生 SDK 启动、后台启动及已保存偏好的读取，实测撤回后的请求和重启行为 | 原生配置、运行网络、存储 | 有分析/诊断时 · App |
| P10 | 使用支持持久化采集开关的 SDK 时，分别验证静态默认值、保存的运行时偏好和重启后的实际网络行为 | SDK API、设备重启与网络 | 按需 · App/服务 |
| P11 | 向第三方 AI 服务共享个人数据前，向用户明确披露接收方、数据和用途并取得明确许可。接收方或用途变化时重新核对许可范围 | App 告知、实际供应商绑定 | 有第三方 AI 时 · App/网站/服务 |
| P12 | 撤回可选分析或诊断后，验证其余可用功能。换账号时确认账号级偏好与同意独立保存 | App 账户作用域与设备 | 按需 · App |
| P13 | 检查最终归档中的 App 和 SDK 隐私清单。由对应的代码或 SDK 维护方提供适用的收集及 API 使用原因声明 | 最终 Archive 的隐私报告/文件 | 按 API/SDK 要求 · 重新打包 |
| P14 | 对照 Required Reason API 的真实调用用途检查类别和理由，核对 Apple 对使用的第三方 SDK 所要求的清单与签名 | 依赖、Xcode 报告、Archive | 按需 · 依赖/App |
| P15 | 核实本地问卷与 App Store Connect 中的实际答案，分别核对草稿、公开标签和版本提交。数据处理变化时同步相关说明 | App Store Connect 实际答案 · 网页或 `CLI:privacy` | 通用 · 商店声明 |
| P16 | 对照官网、App、商店标签及 SDK 清单中各自适用的政策链接、供应商、用途、默认开关和权利控制 | 多端对照 · 人工+静态检查 | 通用 · 按变更 owner 生效 |

## 5. 年龄、版权、出口与地区

按 App 实际内容、数据处理、分发地区和付款方式填写当期表单。由负责该 App 的主体核实适用的申报及协议。

[年龄分级](https://developer.apple.com/help/app-store-connect/manage-app-information/set-an-app-age-rating/) · [年龄分级定义](https://developer.apple.com/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions) · [出口合规](https://developer.apple.com/help/app-store-connect/manage-app-information/determine-and-upload-app-encryption-documentation/) · [欧盟经营者要求](https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements/) · [数字商品和服务问卷](https://developer.apple.com/help/app-store-connect/manage-app-information/complete-the-digital-goods-and-services-questionnaire/)

| 编号 | 检查项与通过标准 | 验证方式 | 适用范围与变更位置 |
| --- | --- | --- | --- |
| R01 | 根据用户在实际 App 中可以访问的内容和功能填写当前年龄问卷 | ASC 年龄问卷 · `CLI:metadata` | 通用 · 商店 |
| R02 | 按实际功能判断广告、家长控制、年龄验证、无限制网页访问、用户生成内容及 App 内消息和聊天 | 问卷、实际 App | 通用问卷 · 商店 |
| R03 | 核对健康和医疗主题、粗俗幽默、恐怖、成人暗示及性内容与裸露的实际内容和频率 | 问卷与内容库 | 通用问卷 · 商店 |
| R04 | 核对酒烟毒品、武器、各类暴力、赌博和模拟赌博、竞赛与开箱等适用类别 | 问卷与内容/玩法 | 通用问卷 · 商店 |
| R05 | 按实际适用地区处理额外分级、提高年龄和儿童类别。填写 Apple 当期问卷所要求的字段 | ASC、声明 JSON | 按需 · 商店 |
| R06 | 核实图像、字体、音频、商标、示例人物及截图素材的使用授权，并按实际使用声明第三方内容 | 权利资料、Content Rights | 通用 · 素材/商店声明 |
| R07 | 按 App 和依赖实际使用的加密与适用豁免，核对出口合规问卷及对应的 App 配置 | App/依赖、ASC 出口问卷 | 通用核对 · 可能需 App/文件 |
| R08 | 按 Apple 要求提供适用的出口文件或批准信息，将其关联到准确构建，并回读实际状态 | ASC 构建和加密资料 | 需要文件时 · 商店 |
| R09 | 核对目标销售地区、各地区的发行条件、App Store Connect 中的可售范围及真实商店状态 | App 可用性、商店页面 · `CLI:pricing` 回读 | 通用 · 商店 |
| R10 | 面向中国大陆发行时，按 Apple 当前表单与业务类型核对适用的 ICP 备案号、实际备案信息和内容许可等资料 | App Store Connect 地区信息、实际备案与许可材料 | 面向大陆时 · 地区资格 |
| R11 | 在 App Store Connect 声明实际经营者状态。面向欧盟发行的经营者按 Apple 流程核对公开联系方式及验证状态 | Business 与 App Information | 通用申报 · 欧盟核验视身份和发行地区 |
| R12 | 对照目标市场的实际表单处理附加分级、主体、付款或内容要求 | 当期地区表单 | 按地区 · 人工/API 视字段 |
| R13 | 出现数字商品和服务问卷时，由负责人按地区与实际付款方式填写，并在提交前核对生效范围和锁定期 | App Information → Digital Goods and Services | 表单出现时 · 人工决策 |
| R14 | 分别核对开发者协议、发行及付费协议，以及适用的银行、税务和收款状态。由有权限的账户持有人处理协议 | Developer 与 ASC Business | 按业务 · 人工 |

## 6. 内购、订阅与价格

[内购配置](https://developer.apple.com/help/app-store-connect/configure-in-app-purchase-settings/overview-for-configuring-in-app-purchases) · [提交内购审核](https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-in-app-purchase/) · [订阅](https://developer.apple.com/app-store/subscriptions/) · [内购审核规则](https://developer.apple.com/app-store/review/guidelines/#in-app-purchase) · [服务器通知 URL](https://developer.apple.com/help/app-store-connect/configure-in-app-purchase-settings/enter-server-urls-for-app-store-server-notifications/) · [CLI 商品与定价](06-optional-capabilities.md)

| 编号 | 检查项与通过标准 | 验证方式 | 适用范围与变更位置 |
| --- | --- | --- | --- |
| I01 | 核对内购商品类型、Product ID 和 App 及服务端的商品映射，确保交易归属到正确的商品类型 | catalog、StoreKit、服务端 · `CLI:catalog` | 有 IAP 时 · 多端 |
| I02 | 按业务核对订阅组、组本地化、周期、等级与家庭共享。验证用户可在同一服务的正确组选项中升级或降级 | catalog、ASC | 自动续订时 · 商店 |
| I03 | 逐商品核对名称、描述、本地化、审核说明、实际购买截图和适用的推广素材 | catalog/assets · CLI | 有 IAP 时 · 商店 |
| I04 | 分别核对 App 下载、内购、订阅的价格及税务分类。有付费项目时，确认对应协议与收款配置 | Pricing、Business | 按收费形态 · 商店 |
| I05 | 核对基准地区、Apple 价格点、币种、手动覆盖价格、自动换算区和销售地区 | `appPricing`、商品 prices/availability · `CLI:pricing` | 收费时 · 商店 |
| I06 | 核对改价生效时间、时区、结束时间、订阅者保价与相应的价格同意要求 | 价格计划、保价策略 | 改价时 · 商业决策 |
| I07 | 按实际业务核对试用、介绍优惠、推广优惠、优惠码和宽限期适用的商品、期限与资格 | offers/gracePeriod · `CLI:pricing` | 使用优惠时 · 商店/服务 |
| I08 | 实机核对 StoreKit 当前地区的价格、币种、扣款金额及适用的恢复路径。使用订阅时，同时核对计费周期、自动续费、管理和条款入口 | 真实购买页与 StoreKit | 有 IAP 时 · App |
| I09 | 按 Apple 的要求将首个内购、订阅或适用的新商品类型与新 App 版本联提，并核对实际商品审核状态 | Review submission | 首次销售时 · 网页/CLI 条件处理 |
| I10 | 按验签结果识别沙盒和正式交易，核对各环境的商品映射、数据和账本 | 验单、映射、交易账本 | 有 IAP 时 · 服务 |
| I11 | 核对 App Store Server Notifications V2 的正式及沙盒 URL、产品、Bundle ID、签名与环境隔离。通过测试通知确认投递和处理 | ASC 与服务端 | 有服务器通知时 · 商店/服务 |
| I12 | 分别验证 App 主动验单和通知履约。核对取消、待处理、断网、重启、重复通知与恢复，确保每笔交易按规则履约后正确结束 | StoreKit、服务端、真实测试 | 有 IAP 时 · App/服务 |
| I13 | 按 `appAccountToken` 和原始交易链核对归属。切换账号后区分历史交易和新购买，同一交易只交付给正确账号 | App、归属查询、账本 | 有账号购买时 · App/服务 |
| I14 | 实测消耗品余额、订阅有效期、取消续费、续订、退款和撤销。核对通过内购购买的积分或游戏内货币持续有效 | 权益规则与真实交易 | 有相关权益时 · 服务/App |
| I15 | 分别在本地 StoreKit、Apple 沙盒和正式渠道验证适用的交易、恢复和履约行为，包含 TestFlight 或 App Review 使用的实际测试环境 | StoreKit 本地/沙盒/正式 | 有 IAP 时 · 分别验证 |
| I16 | 报表按交易环境区分沙盒与正式数据。退款沿原交易和环境处理，保留必要的交易记录 | 订单、报表、退款链路 | 有报表时 · 服务 |

## 7. 原生工程、权限与 SDK

[权限用途说明](https://developer.apple.com/help/app-review/guideline-reference/5-1-1-purpose-strings) · [SDK 要求](https://developer.apple.com/support/third-party-SDK-requirements/) · [辅助功能标签](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/manage-accessibility-nutrition-labels) · [提交要求](https://developer.apple.com/news/upcoming-requirements/)

| 编号 | 检查项与通过标准 | 验证方式 | 适用范围与变更位置 |
| --- | --- | --- | --- |
| N01 | 核对应用标识、显示名称、Team 及主目标、测试目标和扩展的归属，按声明的目标修改工程 | Xcode、manifest · `CLI:native` | 通用 · 重新构建 |
| N02 | 确认最低系统、支持设备、方向、设备能力和后台模式与实际工程和发行范围一致 | build settings、Info.plist | 通用 · 重新构建 |
| N03 | 按提审时的 Apple 要求核对 Xcode 与构建 SDK，并独立验证 App 的最低部署版本 | Xcode、SDK、最终包 | 通用 · 重新构建 |
| N04 | 按实际功能为相机、照片读取和照片写入提供用途文案。验证选择器和权限申请路径 | Info.plist、Photos/Camera 调用 | 使用能力时 · 重新构建 |
| N05 | 按实际调用核对麦克风、定位、蓝牙、联系人、本地网络、运动等用途声明和权限请求 | Info.plist、原生插件、调用路径 | 按需 · 重新构建 |
| N06 | 检查最终包中各支持语言的权限用途文案。使用 `InfoPlist.strings` 的本地化在对应系统语言下真机核对 | Xcode 资源与最终包 | 多语言权限时 · 重新构建 |
| N07 | 在相关操作触发时实测权限申请，并验证允许、拒绝、受限、系统设置返回和有限照片库等路径 | 真机、系统设置 | 使用权限时 · App |
| N08 | 核对构建中使用的 App 图标来源、各声明变体、尺寸和透明通道，按当期 Apple 规格检查最终归档 | Assets.xcassets、Archive | 通用 · 重新构建 |
| N09 | 启动画面、显示名称、原生语言和冷启动界面符合发行版内容，清除模板和调试标记 | 原生资源与冷启动 | 通用 · 重新构建 |
| N10 | 按实际需要配置 URL Scheme、第三方登录回调、Associated Domains、Keychain Group 及 App Group，并核对平台登记 | Info.plist、entitlements、平台 | 按需 · App/平台 |
| N11 | 核对实际使用的公开系统 API、依赖许可证、插件资源、隐私清单与 SDK 签名。评估依赖升级对归档和申报的影响 | 依赖、归档、上传校验 | 通用 · 依赖/重新构建 |
| N12 | 按设备实测 VoiceOver、Voice Control、较大文字、对比度、颜色辨识、深色界面、减少动态效果、字幕和音频描述等适用能力，再填写支持声明 | App 设备与 `accessibility.declarations` | 标签为可选增强 · App/商店 |
| N13 | 按设备填写辅助功能支持情况。保存草稿与公开发布分别核对，发布时验证 Apple 当期资格及已实测的能力 | ASC、`CLI:accessibility` | 使用标签时 · 商店 |
| N14 | 分别验证系统大字号与 App 内字体偏好。声明较大文字时，按 Apple 当前标签条件检查主要界面 | 设备设置、所有主要界面 | 声明更大字体时 · App |
| N15 | 使用第三方 SDK 时，分别核对原生初始化开关、随包配置、框架层显式初始化和构建时上传符号所需的配置。查看最终包和实际运行结果 | 原生工程、最终包、SDK 配置与运行日志 | 使用第三方 SDK 时 · 重新构建 |

## 8. 登录、删除账号与内容治理

[登录服务规则](https://developer.apple.com/app-store/review/guidelines/#login-services) · [App 内账号删除](https://developer.apple.com/help/app-review/guideline-reference/5-1-1-account-deletion) · [用户生成内容](https://developer.apple.com/app-store/review/guidelines/#user-generated-content) · [数据共享](https://developer.apple.com/app-store/review/guidelines/#data-use-and-sharing)

| 编号 | 检查项与通过标准 | 验证方式 | 适用范围与变更位置 |
| --- | --- | --- | --- |
| U01 | 使用第三方或社交登录建立主要账号时，按 Apple 的登录规则核对等效选项的要求及适用例外 | 登录方式与当期规则 | 按需 · App/平台 |
| U02 | 核对 Apple 登录的受众、客户端标识、授权码校验和服务端凭据。实测取消后保持未登录状态 | 原生、服务端、Portal | 使用 Apple 登录时 · 多端 |
| U03 | 真机验证首次登录、重复登录、隐藏邮箱、撤销授权、重新授权、退出及换账号。审核账号能按说明进入目标功能 | 真机与真实登录 | 有登录时 · App/服务 |
| U04 | 支持创建账号的 App 可从 App 内发起完整删除。验证普通用户在适用的身份验证与确认之后可完成删除 | App 设置与删除服务 | 有账号时 · App/服务 |
| U05 | 按 Sign in with Apple 的删除要求验证令牌撤销及失败恢复。处理既有账号缺少授权记录的情形，并核对删除后的数据和会话 | 真实 Apple/删除回执 | 使用 Apple 登录时 · 服务/App |
| U06 | 删除账号时告知用户商店订阅及续费的影响，提供管理订阅入口，并保留可独立完成的账号删除流程 | 删除页、StoreKit 管理入口 | 有自动续订时 · App |
| U07 | 按内容类型和 Apple 审核规则测试适用的过滤、举报、及时处置、屏蔽及联系渠道。生成式功能按实际场景验证内容安全 | 服务策略、举报、工单、运营 | 有相关内容时 · App/服务 |
| U08 | 验证举报指向正确对象且提交者有相应权限。回执对应实际处理记录，重复提交保持一致，原内容状态按明确的处置规则更新 | 举报接口、处理记录和真机操作 | 有举报时 · 多端 |
| U09 | 核对内容安全服务、实际启用的策略和用户告知。用符合预期的输入验证请求、判定结果与后续处置 | 内容策略、真实请求、处理结果与告知 | 使用内容审核时 · 服务/告知 |
| U10 | 核实审核员可访问的支持入口和负责内容处置的人员，从收到请求到完成响应逐步验证 | 支持系统与响应流程 | 有相关内容时 · 运营 |

## 9. 服务、推送与环境

通过 TestFlight 测试时，APNs 使用正式推送环境，内购使用沙盒。分别用最终签名、实际服务地址和验签后的交易确认环境。

[APNs 注册](https://developer.apple.com/documentation/usernotifications/registering-your-app-with-apns) · [APNs 密钥](https://developer.apple.com/help/account/keys/create-a-private-key/) · [APNs entitlement](https://developer.apple.com/documentation/bundleresources/entitlements/aps-environment) · [Firebase iOS 消息配置](https://firebase.google.com/docs/cloud-messaging/ios/get-started) · [TestFlight 内购](https://developer.apple.com/help/app-store-connect/test-a-beta-version/testing-subscriptions-and-in-app-purchases-in-testflight/)

| 编号 | 检查项与通过标准 | 验证方式 | 适用范围与变更位置 |
| --- | --- | --- | --- |
| S01 | 在发行包中核对实际 HTTPS API、认证、官网和法律地址，清理本地、测试和管理端配置 | 公开编译参数、最终 App | 联网 App · 重新打包 |
| S02 | 将允许公开的客户端标识与服务秘密分开管理，并确认各标识已在对应平台登记和授权 | 客户端配置、服务密钥和平台登记 | 按需 · App/服务 |
| S03 | 使用分层服务或多客户端时，核对产品、客户端和服务身份的绑定。按实际调用验证访问权限及拒绝路径 | 角色或服务权限、实际 API 请求 | 使用分层服务或多客户端时 · 服务 |
| S04 | 核对发布所需的迁移、配置、任务和存储，实测回调及适用的签名链接。私有资源由服务校验访问权限 | 发布流程、服务实际请求与存储授权 | 联网 App · 服务 |
| S05 | 分别核对版本和构建号、App API 环境、APNs 环境、StoreKit 交易环境及分发渠道 | App、证书、交易与服务配置 | 按需 · 多端 |
| S06 | 对照 App ID 能力、描述文件、最终 `aps-environment`、topic、Key ID、Team 和服务端 endpoint，确认字段对应真实推送环境 | Developer、Archive、推送服务 | 有推送时 · App/服务 |
| S07 | 核对 APNs Key 的用途、适用环境和授权范围。一次性下载后存入受保护的位置并备份 | Developer Portal · `CLI:apns` | 有推送时 · 账号/服务 |
| S08 | 使用 FCM 等推送服务时，确认平台上的 iOS App、Bundle ID 与 APNs 配置对应，并验证真实设备投递 | Firebase Console、服务与设备 | 使用 FCM 时 · 服务 |
| S09 | 分别测试允许、拒绝、系统关闭、退出换账号与设备令牌更新后的注册和解绑。按适用要求单独处理营销同意 | 系统通知与设备登记 | 有推送时 · App/服务 |
| S10 | 确认通知可投递并打开对应页面。拒绝推送时，实测购买等无关功能及适用的站内替代入口 | TestFlight/正式设备 | 有推送时 · 设备 |
| S11 | 逐一核对支持页、隐私选择页、App API、App Store Server Notifications 和使用的 App Store Connect webhook 入口 | 多端 URL 清单 | 按需 · 网站/平台/服务 |
| S12 | 检查 App、服务与遥测日志的敏感数据过滤和脱敏，并用不含凭据的请求关联标识完成诊断 | App 和服务日志、分析与崩溃平台 | 使用日志时 · 多端 |
| S13 | 核对付费、账号和数据处理方式与发行地区及已审核行为的一致性。远程配置变更按适用的审核要求处理 | 平台配置、实际发行能力 | 联网 App · 服务/审核 |
| S14 | 明确正式配置的维护人，分别回读 App Store Connect 配置和各服务实际生效的配置，再在设备上核对关键行为 | `apple handoff`、服务配置回读与实测 | 使用自动化时 · 服务 |

## 10. 签名、归档、IPA 与上传

每次提交时查看 Apple 当期的 Xcode 和 SDK 要求。记录本次归档及上传使用的真实产物。

[上传构建](https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds/) · [Apple 提交要求](https://developer.apple.com/news/upcoming-requirements/) · [Flutter iOS 分发](https://docs.flutter.dev/deployment/ios) · [Build Upload API](https://developer.apple.com/videos/play/wwdc2025/324/) · [签名与打包指南](04-build-and-test.md)

| 编号 | 检查项与通过标准 | 验证方式 | 适用范围与变更位置 |
| --- | --- | --- | --- |
| B01 | 固定待发布源码、依赖锁和资源，核对本次产物来自对应的版本记录并包含实际发行内容 | Git、锁文件、构建记录 | 通用 · 构建 |
| B02 | 核对选定的工程或工作区、Scheme、目标、Release 配置、Xcode 及适用的 Flutter SDK | manifest/build settings · `CLI:build` | 通用 · 构建 |
| B03 | 分别核对版本号与构建号。重新上传时按 Apple 要求选择可用构建号，并验证各扩展的版本关系 | manifest、Info.plist、ASC 构建 | 通用 · 重新构建 |
| B04 | 确保证书和描述文件有效，Team、Bundle ID、分发类型及能力授权和本次归档匹配 | Certificates/Profiles · `CLI:signing` | 通用 · 签名/重新构建 |
| B05 | 从最终 IPA 和签名信息确认 Development、Ad Hoc 或 App Store 分发类型，按该分发类型选择安装或上传路径 | 最终 IPA/profile/entitlements | 通用 · 重新导出/构建 |
| B06 | 对照描述文件核对 `get-task-allow`、应用和团队标识，以及 Keychain、APNs 等实际 entitlement | `codesign`、`security cms` · `CLI:build` | 通用 · 重新签名/构建 |
| B07 | 逐个验证主 App 与扩展的签名、证书有效期、描述文件及标识 | 最终包 · `CLI:build/upload` | 有 extension 时 · 重新构建 |
| B08 | 解包核对 Bundle ID、版本、构建号、最低系统、SDK、设备组与架构 | 解包后的 Info.plist | 通用 · 构建 |
| B09 | 从最终归档检查所需图标、权限本地化、隐私清单、语言、字体以及其他资源。使用 Git LFS 时确认实际文件完整 | Archive/IPA · 包检查 | 通用 · 构建 |
| B10 | 检查发行产物的秘密与调试文件过滤，确认保留的公开配置指向真实发行目标 | IPA 内容和构建配置 | 通用 · 重新构建 |
| B11 | 用 UUID 对照 dSYM 和发行二进制，并核对符号上传。使用 Dart 混淆时保留同一构建对应的符号文件 | Archive、符号服务 | 有崩溃诊断/混淆时 · 构建/服务 |
| B12 | 保留已验证的 IPA、归档及相关恢复信息。上传前用构建号、路径或产物校验信息核对所选文件 | 构建产物、artifact 记录 | 通用 · 本地交付 |
| B13 | 选择实际可用的上传方式，按 Xcode、Transporter、Fastlane 或 App Store Connect Build Upload API 的要求完成认证和上传验证 | 实际上传工具或 API、上传结果 | 通用 · 上传 |
| B14 | 分别核对上传结果、Apple 处理状态以及构建是否可被版本选择。处理报错时查看对应构建的详细反馈 | ASC、CLI/Transporter 状态 | 通用 · 商店 |
| B15 | 用准确版本和构建号绑定提交，检查该构建的出口合规、处理告警及 SDK 或隐私提示 | ASC、`CLI:review` | 通用 · 商店 |

## 11. TestFlight 与审核

[审核资料](https://developer.apple.com/help/app-review/before-submitting-for-review/complete-review) · [提交 App](https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-app/) · [TestFlight](https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/)

| 编号 | 检查项与通过标准 | 验证方式 | 适用范围与变更位置 |
| --- | --- | --- | --- |
| T01 | 核对 TestFlight 的已处理构建、测试说明、反馈邮箱、语言及适用的审核联系人 | ASC TestFlight · `CLI:testflight prepare` | 使用 TestFlight 时 · 商店 |
| T02 | 核对内外测组、测试员访问、外部测试审核及通知。分别验证分发范围和发送邀请的对象 | groups/testers · CLI/网页 | 使用 TestFlight 时 · 真实通知 |
| T03 | 从 TestFlight 安装指定构建，在真实设备上检查启动、网络、权限、推送和 StoreKit 等适用功能 | 真实设备 | 使用 TestFlight 时 · 设备 |
| T04 | 审核联系人可联系，电话包含实际国家码。审核账号凭据通过私有配置或 App Store Connect 提供 | Review Information · `CLI:metadata` | 通用 · 商店 |
| T05 | 提供持续有效、权限合适的审核账号。按给审核员的说明实测登录、验证码或多因素认证及可访问功能 | 专用审核账号、真实设备 | 有登录时 · 账号/服务 |
| T06 | 用审核账号验证核心功能和购买流程，确保既有订阅或余额状态允许完成对应测试。分别准备 App 登录和适用的 Apple 测试账号 | 审核准备、沙盒测试 | 有 IAP 时 · 账号 |
| T07 | 在审核说明中写明功能入口、特殊权限、AI、付费和外部依赖。附所需演示或附件，并清理服务凭据 | notes、attachments · CLI | 按需 · 商店 |
| T08 | 对照当前构建和服务行为，在 App Store Connect 核对隐私、内容权利、出口、地区和年龄声明 | App Store Connect 表单和当前构建 | 通用 · 人工/商店 |
| T09 | 绑定准确的 App 版本、构建、内购商品和订阅组，核对审核批次及适用的首次内购联提要求，再提交 | Review Submission · CLI/网页 | 通用 · 商店 |
| T10 | 按需分别准备、提交或撤回审核，并从 App Store Connect 回读真实审核状态 | `CLI:review`、ASC | 通用 · 商店 |
| T11 | 确保审核期间服务、测试账号、支持页和必要供应商可用，说明地理、硬件或付款前提并提供可复现方式 | 服务监测与审核沟通 | 按需 · 运营 |
| T12 | 按拒审条款和复现步骤修正问题，判断适合更新资料还是需上传新构建，再按实际结果重新提交 | Resolution Center、版本资料 | 拒审时 · 按修改类型 |

## 12. 真机、发布与维护

[分阶段发布](https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/) · [提审和发布指南](05-review-and-release.md)

| 编号 | 检查项与通过标准 | 验证方式 | 适用范围与变更位置 |
| --- | --- | --- | --- |
| D01 | 在发行候选包验证首次安装、覆盖升级、冷启动、断网和前后台切换。核对 SDK 在授权前的请求与重启后已保存的偏好 | 实机与运行网络 | 通用 · App |
| D02 | 在支持的 iPhone 和 iPad 设备及方向上验证键盘、安全区、长文和大字号，按实际设备实测声明的辅助功能 | 支持范围内设备 | 通用 · App |
| D03 | 验证系统权限提示的语言和用途，拒绝后提供相关恢复路径，并确认无关功能可继续 | 实机系统权限 | 按需 · App |
| D04 | 分别用真实服务和设备完成登录、删除账号、第三方授权撤销、推送、购买恢复和退款等适用验证 | 真实服务与设备 | 按能力 · 多端 |
| D05 | 实测分析、诊断和营销选择的默认值、保存、撤回与换号行为，对照政策及商店隐私标签 | 设备和服务遥测 | 按需 · App/服务 |
| D06 | 从网页、商店和 App 内打开实际语言的法律和支持页面。确认从 App 内页面返回后保留必要状态 | 设备/浏览器/ASC | 通用 · 多端 |
| D07 | 明确手动、审核通过后自动或定时发布策略，核对定时设置与时区。分别回读审核结果和发布状态 | 发布设置 · `CLI:release` | 通用 · 商店 |
| D08 | 使用分阶段发布时，核对适用版本及暂停、恢复、完成的状态，并按实际更新分发情况验证结果 | phased release、版本状态 | 使用分阶段发布时 · 商店 |
| D09 | 按目标商店地区核对公开 App ID、版本、价格和下载，并实测适用的内购可用性 | 真实 storefront | 通用 · 商店 |
| D10 | 官网页面、下载二维码和活动入口指向可用的真实链接，分别记录网站点击、商店下载、首次打开和付费 | 官网、ASC、App 分析 | 增强 · 多端 |
| D11 | 为会员、证书与描述文件、密钥、域名与 TLS、客服邮箱和服务依赖指定维护人，按适用要求维护有效性和监控 | 账号和运营资产 | 按需 · 运营 |
| D12 | 更新时复核 SDK、数据接收方、权限、商品、地区和政策变化。按实际改动决定需要重验的项、发布的代码和同步的配置 | 源码/配置 diff | 更新时 · 对应 owner |
