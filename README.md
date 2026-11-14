# AdCopilot for Meta Ads (Facebook & Instagram Ads)

Meta Ads, Facebook Ads and Instagram Ads in your AI client, through AdCopilot. The plugin brings two AdCopilot connectors: `ma`, which works the Meta ad accounts you connect directly, and `adcopilot`, AdCopilot's Google connection, for your Meta Pixel in Google Tag Manager and your Facebook and Instagram traffic in Google Analytics (GA4).

What it does:

- **Reads and audits your Meta ad accounts.** Campaigns, ad sets, ads, creatives, audiences, automated rules, results and pixel health, with a score out of 100 and what to fix first. The score and its checks are AdCopilot's; Meta's rankings and recommendations are Meta's.
- **Finds wasted spend and reports results.** Spend with no result by ad set, ad, placement, age and hour; results by level, breakdown and period; two periods compared; what changed in the account and who changed it.
- **Builds and changes, after your yes to each proposal.** Campaigns, ad sets and ads (always created paused, for you to switch on in Meta Ads Manager), creatives from images and videos you link, copies, budgets, bids, targeting, placements and schedules, audiences and customer lists, custom conversions, automated rules (created off), A/B tests, Meta's own recommendations and the account's spending limit. A pause or a resume is said first and made on your yes too.
- **Checks your Meta Pixel** in Meta (events received, match quality, the Conversions API share) and in Google Tag Manager, where it can stage a missing tag for you to publish.
- **Reports Facebook and Instagram traffic and key events in Google Analytics (GA4)**, finds UTM mistakes and writes UTM tags.
- **Plans campaigns, drafts ad copy and does the budget pacing math.** That is Claude's own work, from what you tell it.

Meta's figures are always reported on their own: never added to, compared with or mixed with Google Ads, Google Analytics or Search Console figures, and never used to plan another platform's campaigns.

Made by Atromx Intelligence (https://adcopilot.cloud). Not affiliated with or endorsed by Meta Platforms, Inc. Meta, Facebook and Instagram are trademarks of Meta Platforms, Inc. AdCopilot is not related to other products named AdCopilot.

The plugin is MIT licensed. The AdCopilot connectors it brings are a hosted service, so you need an AdCopilot account to use them. Whether your workspace's plan includes Meta Ads is in the Meta connector's first answer, and `/adcopilot-meta-ads:setup` shows it.

## Install

Three steps on every surface: add the plugin, sign in to its two connectors, then connect your Facebook login in AdCopilot.

### Claude on the web, Cowork and the desktop app

1. Open **Customize**, then **Plugins**, search for AdCopilot for Meta Ads, and click **Add**.
2. Open the plugin's **Connectors** tab and click **Connect** beside `ma`, then beside `adcopilot`, signing in to each.

The plugin already registers both connectors, so there is no need for "Add custom connector".

### Claude Code

```
/plugin marketplace add AtromxIntelligence/adcopilot-meta-ads-plugin
/plugin install adcopilot-meta-ads@adcopilot-meta-ads-plugin
/mcp
```

The last step opens the connector list. Choose `plugin:adcopilot-meta-ads:ma` and sign in, then `adcopilot`. If you had 0.1.x, `ma` is new in 0.2.0 and needs its own sign-in once. If you added AdCopilot to Claude Code by hand before, Claude Code uses that copy instead of the plugin's `adcopilot`, and AdCopilot's docs show how to remove it: https://adcopilot.cloud/docs/connect/claude-code-plugin#already-added-the-connector-by-hand

### Connect your Facebook login and Google products once

Your Facebook login, Tag Manager and Analytics are connected inside AdCopilot at https://app.adcopilot.cloud, not in your AI client.
Run `/adcopilot-meta-ads:setup` (or ask "start AdCopilot for Meta") and it gives the connect link.
Meta's own Facebook Login for Business screens ask which business portfolios, ad accounts and Pages AdCopilot may use; only ad accounts switched on in AdCopilot are read. Nobody types a Facebook password into the chat.

## Already use another AdCopilot plugin?

There is one `adcopilot` connector and one AdCopilot account, whichever AdCopilot plugins you add.
Every AdCopilot plugin points `adcopilot` at the same address, so your AI client treats it as one connector; in Claude Code, `/mcp` shows it once, under whichever AdCopilot plugin loaded first, and the sign-in belongs to that entry.
The Meta connector, `ma`, has its own address and its own sign-in.
If Claude asks you to sign in again after you add or remove an AdCopilot plugin, run `/mcp` and sign in once.

## What it will not do

- Switch on a campaign, ad set or ad it built. You switch it on in Meta Ads Manager, and Meta reviews each ad before it runs.
- Delete or archive a campaign, ad set, ad, audience or rule in Meta. It pauses instead. A customer list uploaded in replace mode leaves only that upload's people in the list, and it says so before your yes.
- Change anything without your explicit yes in the conversation, or in a scheduled task.
- Read the people in your audiences, or repeat back a customer list you upload: it gives counts.
- Make political or gambling ads. Those are made in Meta Ads Manager.
- Publish Tag Manager. Every tag it stages waits in the AdCopilot workspace until you publish it.
- Put Meta's figures beside Google's, or use them to plan Google Ads or another platform's campaigns.

## Data

The plugin is instructions only: it runs no code and sends nothing anywhere itself.
Both connectors are at mcp.adcopilot.cloud.
The Meta connector (https://mcp.adcopilot.cloud/meta/mcp) reads and, on your yes, changes the Meta ad accounts you switch on, through Meta's Marketing API with the Facebook login you connect in AdCopilot.
The Google connector (https://mcp.adcopilot.cloud/mcp) reads and, on your yes, writes your Google products through Google's APIs with your Google sign-in.
A customer list you give passes through your AI conversation to AdCopilot, which hashes every value but your own customer IDs at once and never stores or logs the list.
An image you ask it to upload is fetched by AdCopilot from the link you give, and a video by Meta.
A Meta Pixel tag you paste travels in that Tag Manager request through the Google connector.
Links in the plugin to Meta's pages (developers.facebook.com) and to adcopilot.cloud are for you to open; the plugin fetches none of them.
Privacy policy: https://adcopilot.cloud/privacy.
Terms: https://adcopilot.cloud/terms.

## What you get

Commands, used as `/adcopilot-meta-ads:<name>` in Claude Code:

- `setup` checks both connectors and what is connected in AdCopilot: the Facebook login, the Meta ad accounts switched on, Tag Manager and Analytics.
- `audit` scores the Meta ad account and says what to fix first.
- `waste` finds spend with no results and proposes what to pause or change.
- `report` reports how the ads did, Meta's figures on their own.
- `build` builds or changes a campaign, ad set or ad, one proposal at a time.
- `creative` shows which ads work and which are tired, and proposes a fresh creative.
- `check` checks the pixel in Meta and in Tag Manager, then the traffic in Analytics.
- `plan` plans a campaign and drafts ad copy, and checks the budget pace if you give figures.

Skills, which Claude uses when you ask in your own words:

- `meta-ads-start` gets the Meta connector working: sign-in, the Facebook login, the ad accounts switched on.
- `meta-ads-audit` runs the scored audit and the closer looks it points to (learning, overlap, pacing, delivery, tracking, Meta's recommendations).
- `meta-ads-waste` finds spend with no results by ad set, ad, placement, age and hour.
- `meta-ads-reports` reads results by level, breakdown and period, compares periods and lists what changed.
- `meta-ads-build` builds and changes campaigns, ad sets and ads, pauses and resumes, and applies Meta's recommendations, A/B tests and the spending limit.
- `meta-ads-creative` compares ads and creatives, finds fatigue, uploads images and videos and makes creatives and ads.
- `meta-ads-audiences` reads and makes custom and lookalike audiences and uploads hashed customer lists.
- `meta-ads-rules` reads and makes automated rules, created off.
- `meta-ads-pixel` checks the pixel and conversions inside Meta and makes custom conversions.
- `meta-ads-tracking` checks the Meta Pixel in Google Tag Manager and stages a missing tag.
- `meta-ads-traffic` reads Facebook and Instagram traffic in GA4 and finds UTM mistakes.
- `meta-ads-plan` writes the plan and the copy.
- `meta-ads-budget` does the pacing arithmetic from your figures.

## Example prompts

After you sign in, ask in your own words. For example:

- "Start AdCopilot for Meta and run a full audit of my Meta ad account."
- "Where is my Meta ad spend bringing no results in the last 30 days, and what should I pause?"
- "How did my Facebook and Instagram ads do this month against last month, by placement?"
- "Build a paused sales campaign for my new product with a 30 a day budget, and show me each step before you make it."
- "Which of my Meta ads are tired, and can you make a fresh creative from this image link?"
- "Does Meta receive my purchases, and is my Meta Pixel set up in Google Tag Manager?"

## Support

If a tool fails or a connector will not sign in, AdCopilot's troubleshooting page is https://adcopilot.cloud/docs/troubleshooting. Open an issue at https://github.com/AtromxIntelligence/adcopilot-meta-ads-plugin/issues, write to support@adcopilot.cloud, or see https://adcopilot.cloud/contact.

To report a security problem, write to support@adcopilot.cloud.

## Version

**0.2.0** Works your Meta ad account directly through AdCopilot's Meta connector, `ma`, beside the Google connector: start, audit, wasted spend, reports, build and change, creatives, audiences, automated rules and the pixel and conversions in Meta, each change proposed first and made only on your yes. New commands: audit, waste, report, build and creative; check and setup now cover Meta too.

**0.1.1 (2026-11-05)** Changes nothing you use. The plugin folder now holds only the files Claude loads.

**0.1.0 (2026-10-23)** First release. Meta Pixel check and staged tags in Google Tag Manager, Facebook and Instagram traffic and key events in Google Analytics, UTM checks, conversion setup guidance, campaign plans, ad copy drafts and budget pacing math.

## Licence

MIT, see the LICENSE file. Copyright (c) 2026 Atromx Intelligence Private Limited.
