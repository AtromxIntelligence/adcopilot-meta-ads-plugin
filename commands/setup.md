---
name: setup
description: Check that the AdCopilot connector is connected and signed in for Meta Ads work, and say what Tag Manager and Google Analytics unlock. Use first, right after adding the plugin.
---

Run no shell command here, and never offer "Add custom connector" to someone who has this plugin: the plugin already brings the connector.

**First, say this once, in these words:**

> Today AdCopilot works through its Google connection: it checks your Meta Pixel in Google Tag Manager, reports Facebook and Instagram traffic and key events in Google Analytics (GA4), finds UTM mistakes, guides conversion setup, plans campaigns, drafts ad copy and does budget pacing math. It does not read your Meta ad account yet: direct access comes when Meta approves AdCopilot's API access, and no date is promised.

Then call `get_org_context` with `source: "claude-plugin/adcopilot-meta-ads/0.1.0"`, sent exactly as written. In a scheduled run send `source: "claude-scheduled"` instead and change nothing. Its `next_step` and `playbook` describe the whole workspace, Google Ads first, which these skills do not need: keep any limit `next_step` adds, and say only what bears on Meta work.

**If the call fails or asks for a sign-in,** the connector is not signed in yet. In Claude on the web, Cowork and the desktop app, open this plugin from the plugin list, then its Connectors tab, and Connect `adcopilot`. In Claude Code, run `/mcp`, choose `adcopilot` and sign in. If they have another AdCopilot plugin installed, or added or removed one: there is one connector and one AdCopilot account whichever AdCopilot plugins are added. In Claude Code, `/mcp` lists it once, under whichever AdCopilot plugin loaded first, and the sign-in belongs to that entry. If Claude asks for a sign-in again after an AdCopilot plugin was added or removed, run `/mcp` and sign in once. Stop there until it works.

**If it answers,** say in plain words what is ready for Meta Ads work:

- Google Tag Manager, for the Meta Pixel check: connected or not, and the containers it lists, by the names the server gives.
- Google Analytics (GA4), for Facebook and Instagram traffic: connected or not, and the properties it lists, by the names the server gives.
- For a product that is not connected, say what connecting it unlocks in the server's own `unlocks` words, and give the `connect_url` exactly as the server returned it, never a link from memory. For one flagged `needs_readd`, say what the server's `next_step` for it says.
- A Google Ads account is not needed for any of this. The campaign plan and the budget math need no connected product at all.

If nothing is connected, that is the server working, not a fault: Google products are connected inside AdCopilot at https://app.adcopilot.cloud, not in this client. Send them there.

**End with one next step,** and why it fits: `/adcopilot-meta-ads:check` if Tag Manager or Analytics is connected, `/adcopilot-meta-ads:plan` if neither is.
