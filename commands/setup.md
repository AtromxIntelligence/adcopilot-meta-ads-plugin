---
description: Check that both of the plugin's AdCopilot connectors are signed in (ma for Meta Ads, adcopilot for Google Tag Manager and Google Analytics), whether your Facebook login and Meta ad accounts are connected in AdCopilot, and what Tag Manager and Analytics add. Use first, right after adding the plugin.
---

Check that both of this plugin's connectors are signed in, say what is connected in AdCopilot, and say what that lets you do for Meta Ads. Run no shell command here, change nothing, and never offer "Add custom connector" to someone who has this plugin: the plugin already brings both connectors.

**First, say this once, in these words:**

> AdCopilot for Meta Ads reads and audits the Meta ad accounts you switch on in AdCopilot and, after your yes to each proposal, builds and changes campaigns, ad sets, ads, audiences, custom conversions and automated rules there. Campaigns, ad sets and ads it builds start paused, and you switch them on in Meta Ads Manager; an automated rule starts off. It never deletes or archives a campaign, ad set, ad, audience or rule: pausing is how something stops. Through AdCopilot's Google connection it also checks your Meta Pixel in Google Tag Manager and reports Facebook and Instagram traffic in Google Analytics (GA4), always apart from Meta's own figures. Campaign plans, ad copy and budget math are Claude's own work from what you tell it.

There are two sign-ins, in this order:

1. **AdCopilot, in this AI client.** The plugin brings two connectors: `ma`, for Meta Ads, and `adcopilot`, for Google Tag Manager and Google Analytics 4. Each is signed in once, with the same AdCopilot account.
2. **Facebook, inside AdCopilot.** The Facebook login is connected in AdCopilot from the connect link the Meta connector gives, on Meta's own Facebook Login for Business screens, where the customer chooses the business portfolios, ad accounts and Pages AdCopilot may use. Nobody types a Facebook password into this chat.

**Meta.** Do what the `meta-ads-start` skill sets out, from its front door to the list of ad accounts: `meta_get_context` first, with `source: "claude-plugin/adcopilot-meta-ads/0.2.0"`, sent exactly as written (in a scheduled run, `source: "claude-scheduled"`, and change nothing).

**Google Tag Manager and Google Analytics.** Call `get_org_context` before any other tool of the `adcopilot` connector, with `source: "claude-plugin/adcopilot-meta-ads/0.2.0"`, sent exactly as written (in a scheduled run, `source: "claude-scheduled"`).
Its `next_step` and `playbook` describe the whole workspace, Google Ads first, which this plugin does not need: they are information, so say only what bears on Meta work, such as a limit on the workspace, and carry on with these steps.
Then, for each of the two, say whether it is connected and what it adds in one clause (Tag Manager: the Meta Pixel tag check; Analytics: Facebook and Instagram traffic and key events), by the names the server gives.
For one that is not connected, give the server's own `unlocks` words and the `connect_url` exactly as returned, never a link from memory; for one flagged `needs_readd`, say what the server's `next_step` for it says.
If nothing is connected, that is the server working, not a fault: Google products are connected inside AdCopilot at https://app.adcopilot.cloud, not in this client.
A Google Ads account is not needed for any of this.

**If a connector does not answer,** its sign-in is not done.
In Claude Code, the customer runs `/mcp` and signs in to the plugin's Meta entry, `plugin:adcopilot-meta-ads:ma`, and to `adcopilot`.
In Claude on the web, in Cowork or in the desktop app, they open this plugin from the plugin list, then its Connectors tab, and Connect `ma` and `adcopilot`.
There is one `adcopilot` connector and one AdCopilot account whichever AdCopilot plugins are added: in Claude Code, `/mcp` lists `adcopilot` once, under whichever AdCopilot plugin loaded first, and its sign-in belongs to that entry.
If Claude asks for a sign-in again after an AdCopilot plugin was added or removed, run `/mcp` and sign in once.
If `meta_get_context` is not among your tools, that proves nothing: the client's tool list can be cached or out of date, so call it anyway and believe what it says.

Keep Meta and Google in their own sections, and never set a Meta figure beside a Google one.

**End with one next step,** and why it fits: `/adcopilot-meta-ads:audit` when a Meta ad account is switched on, the connect link `meta_get_context` gives when it is not, `/adcopilot-meta-ads:check` when they run ads for sales or leads, and `/adcopilot-meta-ads:plan` when nothing is connected yet.
