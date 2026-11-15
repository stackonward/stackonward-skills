# 2. 网站与 App 配置

前置条件：[账号、工具和路径变量](01-accounts-and-tools.md) 已准备。网站、App 和商店资料都使用同一套真实品牌、支持渠道和数据处理说明。

## 2.1 最少准备哪些公开页面【人工内容 + 网站部署】

| 页面 | 应包含的内容 | 对应商店／App 配置 |
| --- | --- | --- |
| 支持／联系 | App 名称、有效支持渠道、常见问题或反馈方式 | `supportUrl` |
| 隐私政策 | 实际处理的数据、用途、第三方、保留与删除方式、联系方式 | `privacyPolicyUrl`；App 内可访问入口 |
| 服务条款 | 真实服务范围、使用条件、付费及权利约定 | App 内条款；适用的 EULA／订阅说明 |
| 产品首页 | 真实功能、适用设备、下载入口 | 可选 `marketingUrl` |
| 隐私选择／删除说明 | 实际可用的控制方式及联系路径 | 按需 `privacyChoicesUrl`；不能代替 App 内删号能力 |

页面路径由自己决定，例如 `/privacy`、`/legal/privacy` 或带语言路径都可以。不同语言的 URL 分别填入对应商店语言 JSON，不能把所有语言都指向未经确认的英文页面。

域名购买、DNS、HTTPS 证书、续期和支持邮箱由相应平台配置。对外页面应匿名可打开，避免要求审核员先注册、登录或绕过地区限制。隐私和条款正文依据真实产品准备，不把网站模板默认文案当成法律结论。

## 2.2 已有网站时

沿用现有网站，补齐页面和真实内容，确认生产 URL 后直接进入下一章。无需为了使用 Apple CLI 重建网站或迁移托管平台。

没有网站时，可用同版本 CLI 创建一个 Nuxt 网站：

```bash
npx --yes @stackonward/cli@1.10.0 init app-website \
  --template nuxt --yes --skip-git --skip-install
cd app-website
corepack pnpm install
pnpm dev
```

这里明确跳过自动 Git 初始化和首次提交，便于先审阅生成内容。Git 管理由项目负责人决定。生成目标应是新空目录。

修改站点名称、Logo、导航、支持页面、法律正文和下载地址，同时更新 `test/e2e/rendering.test.ts` 等页面测试中对应实际标题的预期。保留页面渲染和功能断言，不通过删除测试来跳过检查。模板不是已完成的产品官网；默认英文页面也不等于已经有完整多语言内容。

| 文件 | 需要编辑的内容 |
| --- | --- |
| `app/app.config.ts` | `siteShell.name/logoText/url`、实际导航／页脚、Cookie 与存储披露 |
| `app/pages/index.vue` | 真实首页内容、SEO 标题／描述、下载与支持入口 |
| `app/pages/legal/` | 对应法律正文和页面 SEO；另创建实际支持页 |
| `app/i18n/locales/` | 已启用语言的导航、站点描述、Cookie 与其他文案 |
| `.env.production` | 生产 origin、公开运行配置和确实启用的集成 |

`NUXT_PUBLIC_SITE_*` 不会自动覆盖模板的 `app.config.ts`：`useSiteShell()` 从 `siteShell` 读取名称和 URL，页面 canonical 也依赖它。因此两处应填写一致的真实值。未使用的博客、工作区、设计展示或价格入口，从实际导航／页面中移除；不要把失效的示例链接一起发布。

按自己的生产环境创建 `.env.production`，只放公开值：

```dotenv
NUXT_PUBLIC_SITE_URL=https://app.example.com
NUXT_PUBLIC_SITE_ENV=production
NUXT_PUBLIC_SITE_NAME="Your App"
NUXT_PUBLIC_SITE_DESCRIPTION="Your app's real purpose."
NUXT_PUBLIC_API_BASE_URL=
NUXT_PUBLIC_GTM_ID=
```

纯支持／法律站不必启用业务 API、GTM 或 OneX。需要这些服务时，按相应模块配置真实服务和用户授权。

静态部署还要明确生成所有公开页面。模板默认关闭链接爬取，只预渲染首页；仅运行 generate 不保证法律页已输出。先创建自己的支持页及其他实际页面，再在现有 `nuxt.config.ts` 的 `defineNuxtConfig` 对象内合并以下 `nitro` 属性，保留其他配置：

```ts
nitro: {
  prerender: {
    crawlLinks: false,
    failOnError: true,
    routes: ["/", "/support", "/legal/privacy", "/legal/terms", "/legal/cookies"],
  },
},
```

列表按自己的真实路径、语言和页面调整，没有 Cookie 页时不照抄该项；不要把私有账号页或 API 路由加入。动态内容依赖服务器时选择 SSR 部署，不能只复制静态目录。参见 [Nuxt 预渲染](https://nuxt.com/docs/4.x/getting-started/prerendering)。

```bash
pnpm format
pnpm check

# 纯静态站，产物为 .output/public
pnpm exec nuxt generate --dotenv .env.production

# 需要 Node SSR 服务时使用这一条，不把它当静态目录
pnpm exec nuxt build --dotenv .env.production
```

首次安装或修改页面后先格式化，再检查；生成的锁文件随网站代码保存，后续按锁定依赖安装。选择一种实际部署方式。模板没有 `pnpm generate` 脚本；直接 `pnpm build` 也不能被理解成会自动读取 `.env.production`。静态发布前，检查每个支持／法律／语言页面的 HTML 已生成，并修复构建日志中的无效链接。参见 [Nuxt generate](https://nuxt.com/docs/4.x/api/commands/generate) 与 [部署说明](https://nuxt.com/docs/4.x/getting-started/deployment)。

## 2.3 网站上线【任选适合自己的方式】

最短路线是将 `.output/public` 上传到已有的 HTTPS 静态托管；具体域名绑定和 TLS 按所用平台完成。不要只上传本机开发服务器地址。

已有 Linux、Nginx 和 SSH 主机时，也可使用 CLI 的 `static-files + ssh-directory + atomic-link`。在网站项目根目录执行：

```bash
stackonward deploy init \
  --profile static-files --target ssh-directory --rollout atomic-link
```

此命令物化部署资源，不会自动把 Nuxt 原来的 `deploy.config.json` 改成这套组合。将 [网站部署示例](../assets/website-deploy.json) 复制并编辑为网站的 `deploy.config.json`，替换站点名、服务器根目录和 HTTPS 健康 URL。

通过自己的私有环境提供 `DEPLOY_SSH_HOST`、`DEPLOY_SSH_PORT`、`DEPLOY_SSH_USER`、`DEPLOY_SSH_KEY`、`DEPLOY_SSH_KNOWN_HOSTS`。最后两项是私钥和 known_hosts 的**内容**，不是文件路径，不写进公开 JSON。预先核实主机指纹和远端目录权限。

网站代码经负责人提交后，用真实完整 Git SHA 构建：

```bash
export SOURCE_REVISION="$(git rev-parse HEAD)"

stackonward deploy validate --config deploy.config.json --environment production
stackonward deploy build --config deploy.config.json --environment production \
  --revision "$SOURCE_REVISION" --output website-build.json
stackonward deploy publish --config deploy.config.json --environment production \
  --artifact website-build.json --output website-published.json
stackonward deploy release --config deploy.config.json --environment production \
  --artifact website-published.json
```

从实际发布结果取得 release ID，设置为 `WEBSITE_RELEASE_ID`，再核对同一版本：

```bash
stackonward deploy verify --config deploy.config.json --environment production \
  --release "$WEBSITE_RELEASE_ID"
```

Nginx 站点启用、域名 DNS、TLS 和证书续期仍需配置。纯法律静态站应让不存在的路径返回正确 404，不能照用 SPA 回退让所有 URL 都返回首页 200。若通过 CLI 环境合并传递构建变量，将实际需要的公开变量列入 `source.build.env` 白名单。

例如在实际静态站 server 内使用 `location / { try_files $uri $uri/ =404; }`，根目录指向本次部署的 current 目录；保留自己的域名、TLS 和其他必需规则，检查 Nginx 配置后再生效。

不使用这条部署路线时，不执行这组写入命令。Nuxt 默认 `registry-only` 配置只能构建／推送镜像，不能作为网站已经上线的证明。

## 2.4 配置自己的 iOS 工程【人工开发 + 本地工具】

### 原生 Xcode

已有工程沿用现有结构。新项目在 Xcode 创建 iOS App，选择真实产品名称、组织标识和语言；完成实际产品功能后再准备上架，空白示例工程不是可发布产品。

在主 target 和各 extension 检查 Bundle ID、Team、Release scheme、支持设备、最低系统和横竖屏。记录实际 `.xcodeproj`／`.xcworkspace`、target、scheme、Info.plist、entitlements 和 AppIcon 资源路径，供后续 manifest 使用。

现代 Xcode 工程可能自动生成 Info.plist。CLI 1.10.0 的原生配置使用明确的 plist 文件路径；先在 Xcode 确认工程实际采用的 plist 和 build settings，不凭教程示例新建一份未被 target 使用的文件。

### Flutter

已有 Flutter 项目固定自己的 Flutter 版本。新项目可先创建 iOS 工程：

```bash
flutter --version
flutter create --platforms=ios --org com.yourcompany your_app
cd your_app
flutter pub get
flutter analyze
flutter test
```

打开 `ios/Runner.xcworkspace` 检查实际 Bundle ID、Team、scheme 和平台配置。`Runner` 是 Flutter 默认名称，改过名称的工程以实际值为准。

对需要编译配置的 App，服务 origin、OAuth 客户端标识和法律链接属于产品自己的配置合同。按代码实际读取的键填写公开配置；服务密钥、管理 API 私钥和签名密码不能进入 App 资源、`--dart-define` 或日志。

## 2.5 权限、隐私与真实功能【按功能适用】

只配置实际使用的系统能力。相机、麦克风、定位、照片访问等用途说明应表达用户为什么需要该权限，并覆盖 App 实际支持的原生语言。使用系统照片选择器不应被笼统解释成必须申请完整照片库权限。

在 `Info.plist`、各语言的 `InfoPlist.strings`、最终包和系统弹窗中核对同一项用途。隐私清单应包含实际使用的 Required Reason API、数据收集和 SDK 要求，不能复制一份通用答案。参见 [Apple 第三方 SDK 要求](https://developer.apple.com/support/third-party-SDK-requirements/)。

根据产品功能实际测试：

| 功能 | 要验收的行为 |
| --- | --- |
| 账号 | 注册、验证码／邮件、登录恢复、退出与失效处理；支持创建账号时可在 App 内发起删除 |
| 社交登录 | 适用的等价登录选项、真实回调、取消和失败；不要把所有 App 都理解成必须 Apple 登录 |
| 数字付费 | 商品、购买、恢复、重复回调、订阅到期、退款与权益处理 |
| 推送 | 用户许可、设备 token、服务端环境、签名和真实设备投递 |
| 外部 AI／SDK | 真实接收方、发送的数据和用途、适用的事先告知与许可 |
| 用户生成内容／社区 | 按适用规则落实过滤、举报、及时处理、屏蔽滥用用户和公开联系方式 |
| 多语言／辅助功能 | 长文本、大字号、VoiceOver、深浅色、操作反馈及所申报的支持能力 |

这些行为不能靠商店字段、一次 HTTP 200 或静态 Boolean 宣称通过。没有使用的能力不需要为了上架盲加。Apple 当前规则见 [登录服务](https://developer.apple.com/app-store/review/guidelines/#login-services)、[账号删除](https://developer.apple.com/help/app-review/guideline-reference/5-1-1-account-deletion) 和 [内购](https://developer.apple.com/app-store/review/guidelines/#in-app-purchase)。

面向儿童、健康医疗、金融、游戏或用户生成内容等产品，还需阅读 [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) 中对应条款，并完成该行业及发行地区的适用要求。

下一步：[商店建档与配置](03-store-configuration.md)。
