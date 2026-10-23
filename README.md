# AdCopilot for Meta Ads (Facebook & Instagram Ads)

Meta Ads, Facebook Ads and Instagram Ads help in your AI client, through AdCopilot. It works through AdCopilot's Google connection, so it covers what shows up in your Google products and in your own planning.

What it does today:

- **Checks your Meta Pixel in Google Tag Manager.** It finds the base code, its trigger and the event tags such as Lead or Purchase (`gtm_list_tags`, `gtm_list_triggers`, `gtm_list_version_headers`), and says what that proves and what it does not.
- **Stages a missing pixel or event tag** in a workspace named AdCopilot in your own Tag Manager container (`gtm_create_tag`, `gtm_create_trigger`), after your yes. You review and publish it yourself.
- **Reports Facebook and Instagram traffic and key events in Google Analytics (GA4)** by source, medium and campaign, paid social against organic social (`ga4_run_report`, `ga4_list_conversion_events`).
- **Finds UTM mistakes** such as split spellings, campaigns that are (not set), and paid clicks landing as referral, and writes a UTM tag set for each campaign.
- **Guides conversion setup**, plans campaigns, drafts ad copy and creative briefs, and does the budget pacing math. These are Claude's own work from what you tell it. AdCopilot reads no Meta data for them.

Today AdCopilot works through its Google connection: it checks your Meta Pixel in Google Tag Manager, reports Facebook and Instagram traffic and key events in Google Analytics (GA4), finds UTM mistakes, guides conversion setup, plans campaigns, drafts ad copy and does budget pacing math. It does not read your Meta ad account yet: direct access comes when Meta approves AdCopilot's API access, and no date is promised. When that access arrives, it is planned to come as an update to this plugin, with its own sign-in for Meta.

Made by Atromx Intelligence (https://adcopilot.cloud). Not affiliated with or endorsed by Meta Platforms, Inc. Meta, Facebook and Instagram are trademarks of Meta Platforms, Inc. AdCopilot is not related to other products named AdCopilot.

The plugin is free (MIT). The AdCopilot connector is a hosted service: Free plan available; paid plans on https://adcopilot.cloud/pricing

## Install

Two steps on every surface: add the plugin, then sign in to the connector it brings with it.

### Claude on the web, Cowork and the desktop app

1. Open **Customize**, then **Plugins**, search for AdCopilot for Meta Ads, and click **Add**.
2. Open the plugin's **Connectors** tab, click **Connect** beside `adcopilot`, and sign in.

The plugin already registers the connector, so there is no need for "Add custom connector". If you added AdCopilot by hand earlier, Claude links a connector by its address, so it is the same connector.

### Claude Code

```
/plugin marketplace add AtromxIntelligence/adcopilot-meta-ads-plugin
/plugin install adcopilot-meta-ads@adcopilot-meta-ads-plugin
/mcp
```

The last step opens the connector list. Choose `adcopilot` and sign in. There is no `claude mcp add` step: the plugin registers the connector for you.

### Connect your Google products once

Tag Manager and Analytics are connected inside AdCopilot at https://app.adcopilot.cloud, not in your AI client. Run `/adcopilot-meta-ads:setup` (or ask "set me up") and it tells you which are missing and where to connect them. The campaign plan and the budget math need no connected product.

## Already use another AdCopilot plugin?

There is one connector and one sign-in, whichever AdCopilot plugins you add. In Claude Code, `/mcp` shows the connector once, under whichever AdCopilot plugin loaded first. On Claude on the web, Cowork and the desktop app, the connector is matched by its address, so your account holds one. If Claude asks you to sign in again after you remove an AdCopilot plugin, run `/mcp` and sign in once.

## What you get

Commands, used as `/adcopilot-meta-ads:<name>` in Claude Code:

- `setup` checks the connector and says what Tag Manager and Analytics unlock.
- `check` runs the pixel check, then the traffic check.
- `plan` plans a campaign and drafts ad copy, and checks the budget pace if you give figures.

Skills, which Claude uses when you ask in your own words:

- `meta-ads-tracking` checks the Meta Pixel in Tag Manager and stages a missing tag. It uses `get_org_context`, `gtm_list_accounts`, `gtm_list_containers`, `gtm_list_workspaces`, `gtm_list_tags`, `gtm_list_triggers`, `gtm_list_version_headers`, `gtm_list_built_in_variables`, `gtm_enable_built_in_variable`, `gtm_create_trigger` and `gtm_create_tag`.
- `meta-ads-traffic` reads Facebook and Instagram traffic in GA4 and finds UTM mistakes. It uses `get_org_context`, `ga4_list_account_summaries`, `ga4_get_metadata`, `ga4_run_report` and `ga4_list_conversion_events`.
- `meta-ads-plan` writes the plan and the copy. It uses `get_org_context` for your saved business profile only.
- `meta-ads-budget` does the pacing arithmetic from your figures. It uses no tool.

## What it will not do

- Read your Meta ad account: no campaigns, ad sets, ads, spend, results, pixel events or Events Manager data. It has no access to Meta, and it gives no Meta figure from memory. Meta publishes a connector of its own for Meta ads, and AdCopilot's guide shows it beside AdCopilot: https://adcopilot.cloud/docs/guides/meta-ads-alongside-adcopilot/
- Create or change anything in Meta.
- Publish Tag Manager. Every tag it stages waits in the AdCopilot workspace until you publish it.
- Delete anything.
- Change anything without your explicit yes in the conversation. Every change is proposed first, with what it changes and how to undo it.

## Data

The plugin is instructions only: it runs no code and sends nothing anywhere itself. The AdCopilot connector at mcp.adcopilot.cloud reads and, on your yes, writes your Google products through Google's APIs with your Google sign-in. When you ask it to stage a Meta Pixel tag, the code you pasted travels in that Tag Manager request through the connector. Links in the plugin to Meta's pages and to adcopilot.cloud are for you to open; the plugin fetches none of them. Privacy policy: https://adcopilot.cloud/privacy. Terms: https://adcopilot.cloud/terms.

## Support

Open an issue at https://github.com/AtromxIntelligence/adcopilot-meta-ads-plugin/issues or write to support@adcopilot.cloud.

## Version

**0.1.0 (2026-10-23, written against AdCopilot v2.44.0, live since 2026-10-22)** First release. Meta Pixel check and staged tags in Google Tag Manager, Facebook and Instagram traffic and key events in Google Analytics, UTM checks, conversion setup guidance, campaign plans, ad copy drafts and budget pacing math. Reading the Meta ad account is not included and has no date.

## Licence

MIT, see the LICENSE file. Copyright (c) 2026 Atromx Intelligence Private Limited.

## What CI runs

Every push to main and every pull request runs the structural tests (manifests, the connector file, front matter, tool names, size limits and hygiene rules, in stdlib Python), `claude plugin validate` in strict mode on a pinned Claude Code release, and gitleaks over every commit. None of it reads a credential or runs a model.
