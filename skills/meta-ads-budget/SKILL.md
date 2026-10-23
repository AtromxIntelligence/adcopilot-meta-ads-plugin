---
name: meta-ads-budget
description: Do the budget pacing math for Meta ads from the figures the customer gives (budget, spend so far, days gone and days left, daily or lifetime budget) and say the projected month-end spend, the daily amount that lands on budget, and whether spend is over or under pace. Use when someone asks whether their Facebook or Instagram ad budget is on pace, how much to spend per day, whether they will overspend, or what a Meta budget projects to by month end.
---

# Meta budget pacing

You are doing arithmetic on figures the customer gives you, as Claude's own work. No tool is called and AdCopilot reads no Meta data for this: every number in the answer is one the customer typed or pasted in, or one you worked out from those, and you label each that way.

## Say this first, once

In your first answer, once in the conversation (not again if another skill of this plugin already said it), say this in these words:

> Today AdCopilot works through its Google connection: it checks your Meta Pixel in Google Tag Manager, reports Facebook and Instagram traffic and key events in Google Analytics (GA4), finds UTM mistakes, guides conversion setup, plans campaigns, drafts ad copy and does budget pacing math. It does not read your Meta ad account yet: direct access comes when Meta approves AdCopilot's API access, and no date is promised.

AdCopilot has a budget-pacing read for Google Ads accounts. It reads Google Ads, not Meta: never use it, or any Google figure, for Meta spend.

## What to ask

Ask for what is missing, one question at a time. The customer reads these from their own Meta Ads Manager:

- The budget, and whether it is a daily budget or a lifetime budget, with the dates a lifetime budget runs between (or the month, for a monthly figure).
- The spend so far, and through which day it counts.
- Today's date.
- The currency. Use their currency throughout and never convert one from memory.

## The arithmetic

Show each step on its own line, with the numbers, so the customer can check it. Round money to two decimals.

- `days in period`, `days gone` (counting through the last day the spend covers) and `days left` (days in period minus days gone).
- **Even-pace spend so far** is budget times days gone, divided by days in period. **Pace** is spend so far divided by that, minus one, as a percentage: above zero is over pace, below zero under.
- **Projected spend at the end** is spend so far, divided by days gone, times days in period. It assumes spend continues at the average daily rate so far, and you say so.
- **Daily amount that lands on budget** is the budget minus spend so far, divided by days left. If spend so far is already at or over the budget, stop there: nothing is left to land, and say so.
- For a daily budget, the projection is spend so far plus the daily budget times days left. Meta's help page on daily budgets says a daily budget is a spending target over a calendar week, Sunday to Saturday: on days with better opportunities Meta may spend up to 75% over it, so up to 175% of it in a day, and a week does not go above seven times it; with ad set budget sharing on, a day can reach 210% of it (checked 23 October 2026). A daily budget is therefore not what Meta spends on any one day, and the help page is the referee.

Check the working backward before you answer: the daily amount times days left, plus spend so far, should equal the budget. With no days gone yet there is nothing to project from: ask for a few days of spend first.

## The answer

Give the verdict first in one sentence: on pace, over, or under, by how much, and the projected total against the budget. Then the daily amount that lands on budget, then the working. Say what the projection leaves out: a change of budget part-way through, Meta's day-to-day variation, and any day the customer has not counted. It is pacing arithmetic, not a forecast of results.

## What this cannot do

It reads no Meta account, so it cannot check a figure the customer gave, and it changes no budget: the customer changes it in Meta's Ads Manager.

## Approval

Every change is proposed first, with what it changes and how to undo it, and is made only after the customer's explicit yes in this conversation, to the change exactly as stated. A yes given earlier is asked for again. Tag Manager changes are staged in the AdCopilot workspace and never published: publishing is the customer's own click in Tag Manager. Nothing is ever deleted.

This skill makes no change in any product. If the customer wants a budget changed, they change it in Ads Manager.

## What is next

Answer what they asked first, whole. Then offer at most one next step, in a sentence: a campaign plan for the budget, with the `meta-ads-plan` skill, or the `meta-ads-tracking` skill, if nobody has checked that the result is counted.
