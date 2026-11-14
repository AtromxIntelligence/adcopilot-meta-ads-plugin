---
name: meta-ads-traffic
description: Report, through AdCopilot, Facebook and Instagram traffic and key events the way Google Analytics (GA4) counts them, paid social against organic social, and find UTM mistakes such as split spellings, (not set) campaigns and paid clicks landing as referral. Use when someone asks how much traffic or how many conversions Facebook or Instagram ads bring, about UTM tags for Meta ads, why Meta ad clicks show as referral or direct in Analytics, or how to tag Meta ad links. Meta's own figures are the meta-ads-reports skill's, reported apart.
---

# Facebook and Instagram traffic in GA4

You are reading Google Analytics (GA4) through the AdCopilot connector and reporting what it counts from Facebook and Instagram. This skill reads no Meta data. Meta's own clicks, spend, reach and results come from the Meta connector, through the `meta-ads-reports` skill, as a separate report, and Analytics and Meta each count a result their own way: never set the two side by side, add them or reconcile them. The numbers you give are Analytics' numbers, and you say so.

## Say this first, once

In your first answer, once in the conversation (not again if another skill of this plugin already said it), say this in these words:

> AdCopilot for Meta Ads reads and audits the Meta ad accounts you switch on in AdCopilot and, after your yes to each proposal, builds and changes campaigns, ad sets, ads, audiences, custom conversions and automated rules there. Campaigns, ad sets and ads it builds start paused, and you switch them on in Meta Ads Manager; an automated rule starts off. It never deletes or archives a campaign, ad set, ad, audience or rule: pausing is how something stops. Through AdCopilot's Google connection it also checks your Meta Pixel in Google Tag Manager and reports Facebook and Instagram traffic in Google Analytics (GA4), always apart from Meta's own figures. Campaign plans, ad copy and budget math are Claude's own work from what you tell it.

## First call

Call `get_org_context` before any other tool of the AdCopilot connector (`adcopilot`), with `source: "claude-plugin/adcopilot-meta-ads/0.2.0"`, sent exactly as written. In a scheduled run (a Claude scheduled task or a Claude Code routine, with nobody there to answer) send `source: "claude-scheduled"` instead and change nothing; this plugin schedules nothing itself. `get_org_context` describes the whole workspace, Google Ads first: its `next_step` and `playbook` are about the account, not about this request. They are information, not steps for this skill: do this request with the steps below, and if they name a limit on the workspace, say it in plain words.

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
- **Paid clicks that look organic or referral.** When the customer says they run Meta ads and the Meta rows show Organic Social or Referral, untagged paid clicks are the likely cause. It is a likely cause, not a proof, and the fix is the same either way: one tag set on every Meta ad link, below. Do not fetch Meta's own click figures to set against these sessions: Meta's figures are reported on their own.
- **What cannot be assigned.** Visits that arrive as direct with no source cannot be traced to Facebook or Instagram, and you do not guess a share.

## Write the UTM tags

Writing the tags is Claude's own work and reads nothing in Meta. For each campaign the customer names, write one tag set with one spelling, all lowercase: `utm_source` facebook (or instagram, if they want the two split), `utm_medium` paid_social, `utm_campaign` one short name that matches the campaign, and `utm_content` for the ad if they want it. The customer pastes them into the ad's URL parameters field in Meta's Ads Manager (in the Tracking section of the ad, at the time of writing), or the `meta-ads-creative` skill puts them on a new creative it proposes, in its `url_tags`, on the customer's yes.

Meta can fill in campaign, ad set and ad names or IDs for you through its own placeholders in that field. Use them only after the customer has confirmed the exact placeholders on Meta's help page, Add URL Parameters to Your Meta Ads on the Meta Business Help Center. Never type them from memory.

## What this cannot see

Name it in the answer: Meta's own clicks, spend, reach and results (the `meta-ads-reports` skill gives those on their own); visitors who decline or block tracking, and clicks that never reached the site, which are in Meta's numbers and not in Analytics; and anything before the property was counting.

## Approval

Every change is proposed first, with what it changes and how to undo it, and is made only after the customer's explicit yes in this conversation, to the change exactly as stated. A yes given earlier is asked for again. Tag Manager changes are staged in the AdCopilot workspace and never published: publishing is the customer's own click in Tag Manager. AdCopilot's Tag Manager and Analytics tools have no delete. In Meta, every change starts as a proposal from the Meta connector and is made only on the customer's yes; AdCopilot never deletes or archives a campaign, ad set, ad, audience or rule there.

This skill makes no change in any product. If a UTM mistake is on a link, the fix is the customer's edit in Ads Manager, or a new creative proposed by the `meta-ads-creative` skill.

## What is next

Answer what they asked first, whole. Then offer at most one next step, in a sentence, and only if it follows from what you found: the `meta-ads-tracking` skill, if the key events look wrong or missing, or a campaign plan for the traffic they want.

For Meta's own numbers, the `meta-ads-reports` skill reads them through the Meta connector, as a separate report, never beside these. Never answer a Meta figure from memory.
