---
name: ios-app-delivery
description: Prepare and guide iOS App Store delivery with StackOnward CLI 1.10.0, from developer enrollment and website configuration through checks, signing, TestFlight, review and release. Use for first submissions and updates.
license: MIT
---

# iOS App Delivery

Guide the user through the required parts of one real iOS release. The Chinese references also serve as a beginner tutorial.

## Start with the actual project

- MUST identify the current stage, project root, native Xcode or Flutter build, Bundle ID, selected version/build, developer team, intended regions and optional services before constructing live commands.
- MUST inspect existing configuration and preserve unrelated work. Ask only for missing facts that affect the selected stage.
- MUST use the published CLI `1.10.0` contract. Check `stackonward --version`; use `npx --yes @stackonward/cli@1.10.0` when a different installed version would change the documented commands. NEVER silently replace a user's toolchain.
- MUST obtain product names, URLs, identifiers, prices, territories, privacy answers and permission purposes from the project or its owner. NEVER apply the example identities or legal answers to a live account.

## Read only the relevant chapter

| Task | Reference |
| --- | --- |
| Copy a starter `delivery/apple` directory and choose JSON examples | [Start from the template](references/00-start-from-template.md) |
| Enrollment, prerequisites, private credentials and working directories | [Accounts and tools](references/01-accounts-and-tools.md) |
| Website, native/Flutter configuration, permissions and product acceptance | [Website and app](references/02-website-and-app.md) |
| First Bundle/App record, metadata, screenshots, privacy and declarations | [Store configuration](references/03-store-configuration.md) |
| Native configuration, signing, package checks, upload and TestFlight | [Build and test](references/04-build-and-test.md) |
| Review preparation, exact submission, release and subsequent updates | [Review and release](references/05-review-and-release.md) |
| Sign in with Apple, APNs, IAP/subscriptions, pricing and accessibility | [Conditional capabilities](references/06-optional-capabilities.md) |
| Completeness reports, errors, partial effects and recovery | [Errors and verification](references/07-errors-and-verification.md) |

MUST read the stage's prerequisites and relevant conditional section before its commands. The assets contain editable example configuration; they are not evidence that a real product meets the declarations.

## Execute the selected stage

1. MUST separate local preparation, read-only inspection and external changes. A request to learn or check does not authorize changing an account, submitting a build, inviting testers or publishing a version.
2. MUST reuse the existing `preflight → plan → apply → verify` workflow and the exact scope/intent. Build, upload, TestFlight review, invitation, App Review submission and public release remain separate actions. Existing explicit authorization for the selected action remains valid.
3. MUST inspect the concrete saved plan before apply. NEVER edit its operations, reuse an expired/drifted plan, or treat `--yes` as general release authorization.
4. MUST distinguish API credentials, Developer Portal sessions and App Privacy sessions. Keep private files outside product source; NEVER ask for a password, session, private key or token in chat or place it in client build values.
5. MUST verify the exact version and build rather than select the latest. After review preparation, obtain the exact `reviewSubmissions` ID from the result before preparing submit.
6. MUST treat Apple website steps as manual where CLI 1.10.0 has no adapter. NEVER invent a command or silently replace a failed authenticated read with an assumed empty account.

In CLI 1.10.0, standalone signing verify always retains a sync operation. MUST use the successful signing apply result and subsequent archive's real signing/profile/certificate checks; NEVER repeat signing initialization merely to make that verify converge.

## Preserve the important boundaries

- MUST inspect `receipt.completed`, `pending` and manual requirements even on a nonzero exit. First `setup apply` can create Bundle ID/capabilities and still return exit 6 because the owner must create the ASC App record.
- MUST preserve private execution state after partial or unknown writes. NEVER blindly repeat an unknown write, clear its journal, replace state to bypass it, or repeat an APNs one-time download as if it were idempotent.
- MUST distinguish configured fields, successful provider readback, package signatures, real-device behavior, approval and storefront availability. `check` may retain `not-checked` items when its automatic outcome is verified.
- MUST keep legal/privacy/content/trader facts, actual account deletion and live purchase/push/login behavior under their real owners. NEVER infer compliance from a generic template or a static Boolean.
- MUST recheck Apple's current SDK deadlines, required screenshot groups, questionnaires and regional rules before an actual submission. CLI version pinning does not freeze Apple policy.

## Handoff

MUST explain what changed, what was actually checked, the real Apple state, unresolved manual steps and the next exact command or website action. Keep private data out of the handoff. MUST NOT claim the App is approved or available from upload, a green local check, or an accepted release request alone.
