# iOS 交付目录

[app.json](app.json) 管理 App 身份、商店语言、发布版本和本次使用的功能。替换示例 Bundle ID、名称、SKU、版本与生产链接。首次建档后补 `app.appId`。字段定义见 [CLI 1.10.0 Schema](manifest.schema.json)。

- 文案维护在 `metadata/`，每种语言一份 JSON。可从 [全字段空表](examples/metadata.full.example.json) 起草，只将已填写且适用的字段纳入正式文案。
- 按需从 `examples/` 合并工程、签名、App Store 设置、内购或 TestFlight 字段。实际素材放在 `artwork/`、`screenshots/`、`previews/`。
- 确认审核说明及声明后，将准备好的文件放入 `review/` 和 `declarations/`。账号、审核密码、会话和私钥保存在项目外的私有目录。

在 App 项目根目录运行本地检查。

```bash
npx --yes @stackonward/cli@1.10.0 apple preflight \
  --manifest delivery/apple/app.json --scope metadata --offline --json
```

在 Codex 中调用 `$ios-app-delivery` 可查阅后续阶段的操作命令。
