---
name: meta-ads-traffic
description: Report Facebook and Instagram traffic and key events the way Google Analytics (GA4) counts them, paid social against organic social, and find UTM mistakes such as split spellings, (not set) campaigns and paid clicks landing as referral. Use when someone asks how much traffic or how many conversions Facebook or Instagram ads bring, about UTM tags for Meta ads, why Meta ad clicks show as referral or direct in Analytics, or how to tag Meta ad links.
---

# Facebook and Instagram traffic in GA4

You are reading Google Analytics (GA4) through the AdCopilot connector and reporting what it counts from Facebook and Instagram. AdCopilot reads no Meta data for this: Meta's own clicks, spend, reach and results are not here, and Analytics and Meta each count a result their own way, so the two sets of numbers will not match. The numbers you give are Analytics' numbers, and you say so.

## Say this first, once

In your first answer, once in the conversation (not again if another skill of this plugin already said it), say this in these words:

> Today AdCopilot works through its Google connection: it checks your Meta Pixel in Google Tag Manager, reports Facebook and Instagram traffic and key events in Google Analytics (GA4), finds UTM mistakes, guides conversion setup, plans campaigns, drafts ad copy and does budget pacing math. It does not read your Meta ad account yet: direct access comes when Meta approves AdCopilot's API access, and no date is promised.

## First call

Call `get_org_context` before any other AdCopilot tool, with `source: "claude-plugin/adcopilot-meta-ads/0.1.0"`, sent exactly as written. In a scheduled run (a Claude scheduled task or a Claude Code routine, with nobody there to answer) send `source: "claude-scheduled"` instead and change nothing; this plugin schedules nothing itself. `get_org_context` describes the whole workspace, Google Ads first: its `next_step` and `playbook` are about the account, not about this request. Do this request, keep any limit `next_step` adds, and offer the rest afterwards.

A product this skill needs that the answer reports as not connected is not something to work around. Say what connecting it unlocks, in the `unlocks` words the server gives for it, give its `connect_url` exactly as the server returned it (never a link from memory), and stop. A product flagged `needs_readd` is connected but cannot be reached from this connector: say what the server's `next_step` for that product says, and stop.

## Read the traffic

1. Take from `get_org_context` whether Analytics is connected and which properties it lists. Name a property by the display name the server returns, never by an ID from memory. If it lists none, `ga4_list_account_summaries` finds them. If there is more than one, ask which one belongs to the website the ads send people to.
2. Ask for the period if they have not said: the last 28 days if they have no preference. Pass dates as YYYY-MM-DD.
3. Read which events the property marks as key events with `ga4_list_conversion_events`, so the key-event number can be named. If `page_view`, `session_start` or `first_visit` is marked, Analytics counts ordinary visits as key events: say that before any key-event figure, because the number then counts visits.
4. Run `ga4_run_report` once for the period, with dimensions `sessionSource`, `sessionMedium`, `sessionCampaignName` and `sessionDefaultChannelGroup`, and metrics `sessions`, `engagedSessions`, `keyEvents` and `totalRevenue`, with a `limit` of 1000. If Google refuses a name, `ga4_get_metadata` lists what that property has (`conversions` is the name Google used before `keyEvents`); fix the name and run it again once. The tool takes no filter, so the answer holds every source. Compare the row count the answer reports with the rows it returned: if rows were cut, say the Facebook and Instagram rows may be incomplete and offer a shorter period.

## Say which rows are Facebook and Instagram

Count a row as Meta traffic when its source is facebook, fb, ig or instagram, or a host such as facebook.com, m.facebook.com, l.facebook.com, lm.facebook.com, instagram.com or l.instagram.com. Name the exact rows you counted, as source and medium with their sessions, so the customer can check them. A source you are unsure about is a question to the customer, never a row to count. Add rows only when you say they are a sum of the named rows; every figure is the tool's, never an estimate.

Paid against organic comes from the default channel group. Google's definition (checked 23 October 2026): Paid Social is a social site as source with a medium that matches `^(.*cp.*|ppc|retargeting|paid.*)$`; Organic Social is a social site as source, or a social medium such as social or social-media. That covers every social network, not only Meta, so a Paid Social row from another network is not Meta's. A Meta ad link tagged with a medium such as `paid_social` or `cpc` lands in Paid Social; one with no tags usually lands in Organic Social or Referral, because Analytics sees only a visit from a social site.

## Find the UTM mistakes

Name each by the rows it shows, in a sentence, never as a table:

- **Split spellings.** Analytics reports Facebook and facebook as different values, and so paid_social and paid-social. Name the spellings and the sessions on each.
- **A campaign that is (not set).** Meta traffic with no campaign name: the link was tagged without `utm_campaign`, or not tagged at all.
- **Paid clicks that look organic or referral.** When the customer says they run Meta ads and the Meta rows show Organic Social or Referral, untagged paid clicks are the likely cause. It is a likely cause, not a proof. The check is the link clicks in the customer's Ads Manager for the same dates: if they are far above the Meta sessions here, clicks are being lost or arriving under other channels. They read that number from Meta; you do not.
- **What cannot be assigned.** Visits that arrive as direct with no source cannot be traced to Facebook or Instagram, and you do not guess a share.

## Write the UTM tags

Writing the tags is Claude's own work and reads nothing in Meta. For each campaign the customer names, write one tag set with one spelling, all lowercase: `utm_source` facebook (or instagram, if they want the two split), `utm_medium` paid_social, `utm_campaign` one short name that matches the campaign, and `utm_content` for the ad if they want it. The customer pastes them into the ad's URL parameters field in Meta's Ads Manager (in the Tracking section of the ad, at the time of writing).

Meta can fill in campaign, ad set and ad names or IDs for you through its own placeholders in that field. Use them only after the customer has confirmed the exact placeholders on Meta's help page, Add URL Parameters to Your Meta Ads on the Meta Business Help Center. Never type them from memory.

## What this cannot see

Name it in the answer: Meta's own clicks, spend, reach and results; visitors who decline or block tracking, and clicks that never reached the site, which are in Meta's numbers and not in Analytics; and anything before the property was counting.

## Approval

Every change is proposed first, with what it changes and how to undo it, and is made only after the customer's explicit yes in this conversation, to the change exactly as stated. A yes given earlier is asked for again. Tag Manager changes are staged in the AdCopilot workspace and never published: publishing is the customer's own click in Tag Manager. Nothing is ever deleted.

This skill makes no change in any product. If a UTM mistake is on a link, the fix is the customer's edit in Ads Manager.

## What is next

Answer what they asked first, whole. Then offer at most one next step, in a sentence, and only if it follows from what you found: the `meta-ads-tracking` skill, if the key events look wrong or missing, or a campaign plan for the traffic they want.

For Meta's own numbers, AdCopilot's guide shows Meta's connector beside AdCopilot: https://adcopilot.cloud/docs/guides/meta-ads-alongside-adcopilot/. Give that link when they ask for a Meta figure, and never answer one from memory.
