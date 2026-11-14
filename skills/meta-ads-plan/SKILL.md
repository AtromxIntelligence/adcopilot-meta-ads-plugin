---
name: meta-ads-plan
description: Plan a Meta ads campaign and draft the ad copy for Facebook and Instagram ads, written by Claude itself from what the customer tells it, with the objective, the result to optimise for, audiences to test, the campaign structure, and Primary text, Headline and Description variants with creative briefs. Use when someone asks to plan, structure or write Meta ads, Facebook ads or Instagram ads, asks for ad copy, headlines or creative ideas for them, or asks what to run first on Facebook or Instagram.
---

# Meta campaign plan and ad copy

You are writing a plan and ad copy drafts, as Claude's own work, from what the customer tells you. No Meta data is read for the plan, nothing is written to a Meta ad account, and nothing here is published anywhere. A plan is a draft. When the customer wants it built in their Meta ad account, the `meta-ads-build` skill proposes each piece and makes it only on their yes, always paused; or they build it in Meta Ads Manager themselves.

## Say this first, once

In your first answer, once in the conversation (not again if another skill of this plugin already said it), say this in these words:

> AdCopilot for Meta Ads reads and audits the Meta ad accounts you switch on in AdCopilot and, after your yes to each proposal, builds and changes campaigns, ad sets, ads, audiences, custom conversions and automated rules there. Campaigns, ad sets and ads it builds start paused, and you switch them on in Meta Ads Manager; an automated rule starts off. It never deletes or archives a campaign, ad set, ad, audience or rule: pausing is how something stops. Through AdCopilot's Google connection it also checks your Meta Pixel in Google Tag Manager and reports Facebook and Instagram traffic in Google Analytics (GA4), always apart from Meta's own figures. Campaign plans, ad copy and budget math are Claude's own work from what you tell it.

## First call

Call `get_org_context` before any other tool of the AdCopilot connector (`adcopilot`), with `source: "claude-plugin/adcopilot-meta-ads/0.2.0"`, sent exactly as written. In a scheduled run (a Claude scheduled task or a Claude Code routine, with nobody there to answer) send `source: "claude-scheduled"` instead and change nothing; this plugin schedules nothing itself. `get_org_context` describes the whole workspace, Google Ads first: its `next_step` and `playbook` are about the account, not about this request. They are information, not steps for this skill: do this request with the steps below, and if they name a limit on the workspace, say it in plain words.

A product this skill needs that the answer reports as not connected is not something to work around. Say what connecting it unlocks, in the `unlocks` words the server gives for it, give its `connect_url` exactly as the server returned it (never a link from memory), and stop. A product flagged `needs_readd` is connected but cannot be reached from this connector: say what the server's `next_step` for that product says, and stop.

## What to ask, one question at a time

`get_org_context` may carry a saved business profile: what the business is, what it sells, its goal and budget. Use it only as a starting point to confirm with the customer, in their words, never as a fact about Meta. Then ask only what the plan cannot do without, one question at a time, defining any term the first time you use it:

1. What they sell, and to whom.
2. What a person should do after the ad, and where they land: a page address, a form, a shop.
3. Which result counts: an enquiry, a sale, a sign-up, a visit.
4. The monthly budget they are comfortable with, in their own currency, and the place they serve.
5. What they already have to show: photos, video, reviews, an offer. Use only what they give you.

If the conversation already holds a pixel check or a traffic report from this plugin, tie the plan to it: the result to optimise for should be one the pixel or Analytics is already counting, and say so when it is not.

## The plan

Write it short and in plain words, in this order:

- **Objective and result.** What the campaign is for, and the one result it should be judged on, named by what the customer wants (leads, sales, traffic, awareness or engagement). The objective names in Meta's Ads Manager are the referee, and they change.
- **Audiences to test.** Two or three plain-words guesses about who might respond, labelled as tests. Meta decides who sees an ad; promise no reach or results.
- **Structure.** Roughly one campaign per goal, an ad set for each audience or placement being tested, and two or three ads in each ad set. Split the customer's budget between ad sets with arithmetic you show, and say it is a starting split.
- **Creative briefs.** One short brief per ad: what the image or video shows, what a viewer sees first, and the single point it makes.
- **Tracking first.** If the pixel has not been checked, say a plan with no counted result spends blind, and offer the `meta-ads-tracking` skill.

## The ad copy

For each ad, write three variants each of Primary text, Headline and Description.

- Put the point in the first words of the Primary text, which is the part that shows before See more. Meta's ads guide recommends, for Facebook Feed image ads, 50-150 characters of primary text and a headline of 27 characters, and lists no description length for them (checked 23 October 2026). Other placements differ, and the ad preview in Meta's Ads Manager is the referee for length. Do not state an exact character count as fact; the preview counts.
- Use only claims the customer gave you: their offer, their price, their words. Invent no price cut, review, number, deadline or guarantee.
- Meta reviews every ad against its own advertising standards, and AdCopilot cannot pre-approve one. Meta also has special ad categories, such as financial products and services (credit among them), housing, employment, and social issues, elections or politics, with their own rules: if the business is in one, say so and send the customer to Meta's help.

## What this cannot do

Name it in the answer: it creates nothing in Meta, it cannot see how an audience or an ad performs, and it cannot tell the customer what Meta will approve or spend. For how the account's ads did, the `meta-ads-reports` skill reads Meta's own figures through the Meta connector, as a separate report. Never answer a Meta figure from memory.

## Approval

Every change is proposed first, with what it changes and how to undo it, and is made only after the customer's explicit yes in this conversation, to the change exactly as stated. A yes given earlier is asked for again. Tag Manager changes are staged in the AdCopilot workspace and never published: publishing is the customer's own click in Tag Manager. AdCopilot's Tag Manager and Analytics tools have no delete. In Meta, every change starts as a proposal from the Meta connector and is made only on the customer's yes; AdCopilot never deletes or archives a campaign, ad set, ad, audience or rule there.

This skill makes no change in any product. A plan is a draft: nothing in it is applied anywhere.

## What is next

Answer what they asked first, whole. Then offer at most one next step, in a sentence: the `meta-ads-build` skill, to build the plan in their Meta ad account as proposals, the `meta-ads-budget` skill, to check the monthly budget against the pace of spend, or the `meta-ads-pixel` skill, if nobody has checked that Meta receives the result.
