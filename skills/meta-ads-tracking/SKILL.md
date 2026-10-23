---
name: meta-ads-tracking
description: Check whether the Meta Pixel is set up in Google Tag Manager (the base code, its trigger, the Lead or Purchase event tags, and whether the container has any version), say what that does and does not prove, and stage a missing base or event tag in the AdCopilot workspace for you to review and publish. Use when someone asks whether the Meta Pixel or Facebook Pixel is installed or working, about Meta conversion tracking, the pixel in Tag Manager, a Lead or Purchase event for Facebook or Instagram ads, or why Meta shows no conversions.
---

# Meta Pixel in Tag Manager

You are checking what the customer's Google Tag Manager holds about the Meta Pixel, through the AdCopilot connector, and saying what that proves and what it does not. If a piece is missing and the customer wants it, you stage it, proposed first. AdCopilot reads no Meta data for this: not the pixel's events, not Events Manager, not the ad account.

## Say this first, once

In your first answer, once in the conversation (not again if another skill of this plugin already said it), say this in these words:

> Today AdCopilot works through its Google connection: it checks your Meta Pixel in Google Tag Manager, reports Facebook and Instagram traffic and key events in Google Analytics (GA4), finds UTM mistakes, guides conversion setup, plans campaigns, drafts ad copy and does budget pacing math. It does not read your Meta ad account yet: direct access comes when Meta approves AdCopilot's API access, and no date is promised.

## First call

Call `get_org_context` before any other AdCopilot tool, with `source: "claude-plugin/adcopilot-meta-ads/0.1.0"`, sent exactly as written. In a scheduled run (a Claude scheduled task or a Claude Code routine, with nobody there to answer) send `source: "claude-scheduled"` instead and change nothing; this plugin schedules nothing itself. `get_org_context` describes the whole workspace, Google Ads first: its `next_step` and `playbook` are about the account, not about this request. Do this request, keep any limit `next_step` adds, and offer the rest afterwards.

A product this skill needs that the answer reports as not connected is not something to work around. Say what connecting it unlocks, in the `unlocks` words the server gives for it, give its `connect_url` exactly as the server returned it (never a link from memory), and stop. A product flagged `needs_readd` is connected but cannot be reached from this connector: say what the server's `next_step` for that product says, and stop.

## What this can see, and what it cannot

Say this in the answer before any verdict.

- It sees the tags, triggers and variables in the customer's Tag Manager workspaces, and the container's list of versions.
- It cannot see a pixel typed into the site's own code or added by a store or website-builder integration: Tag Manager does not know about those. It cannot see whether a tag fires on a real visit, what Meta received or counted, or events a server sends to Meta through the Conversions API. It cannot open a published version to read its tags.

## Read what is there

1. Take from `get_org_context` whether Tag Manager is connected and which containers it lists. Name a container by the display name the server returns, never by an ID from memory. If it lists none, `gtm_list_accounts` and then `gtm_list_containers` find them. If there is more than one container, ask which one the website loads. If the site loads no container at all, say so: nothing in Tag Manager can run there until the customer installs the container code on the site (under Admin in Tag Manager, at the time of writing).
2. `gtm_list_workspaces` for that container. Then `gtm_list_tags` and `gtm_list_triggers` on the Default Workspace, and on the workspace named AdCopilot if there is one. Those are drafts: they show what is set up, not what is live.
3. `gtm_list_version_headers` on the container. No version at all means nothing was ever submitted from this container, so nothing in it runs on the site. At least one version means a version exists, but the list does not say which one is live or what is in it; the Versions tab in Tag Manager does, and it also shows who published and when.

## Find the pixel

A Meta Pixel in Tag Manager is usually a Custom HTML tag (type `html`) whose code loads `connect.facebook.net/en_US/fbevents.js` and calls `fbq('init', '<pixel ID>')`, or a tag made from a template whose name or fields say Facebook or Meta Pixel. Read these from the tags, never from memory:

- The pixel ID in the `fbq('init', ...)` call.
- The base tag's firing trigger. A firing trigger ID of 2147479553 is Tag Manager's built-in All Pages.
- The event tags: tags that call `fbq('track', '<Event>')`, and the trigger each one fires on. Meta's standard event names, as its pixel reference lists them (checked 23 October 2026): AddPaymentInfo, AddToCart, AddToWishlist, CompleteRegistration, Contact, CustomizeProduct, Donate, FindLocation, InitiateCheckout, Lead, Purchase, Schedule, Search, StartTrial, SubmitApplication, Subscribe and ViewContent. The base code fires PageView itself, and Meta says to leave that call in. A name not on the list is a custom event.

Report it in a few sentences: the pixel ID, the base tag and its trigger, each event tag and what fires it, and, if the container has no version, that nothing was ever submitted from it. Do not paste the tool's rows. Name two base tags, or two `init` calls for the same ID, as a double-counting risk, by tag name.

## Say what that proves

A tag set up in Tag Manager is not proof it fires. A draft is not live, and a version in the list is not proof the pixel tag is in it. The proof is Meta's own screens, which the customer opens:

- Test events in Meta's Events Manager (Data sources, the pixel, Test events, at the time of writing) shows an event arrive while the customer visits the site.
- Meta Ads Data Advisor, which Meta's page says was formerly called Meta Pixel Helper (checked 23 October 2026), is a free extension for Chrome and Edge that checks the pixel on a page and flags problems.
- Tag Manager's own Preview shows whether a tag fired on a page.

Say which of the three the customer should use for the answer they want, and that until one of them shows the event, the honest word is "set up", never "working".

## Conversion setup guidance

This is Claude's own knowledge, not a read of anything. State it at the time of writing; Meta's own help and Events Manager are the referee.

- Pick one result worth counting for the business: Lead for enquiries, Purchase for sales, CompleteRegistration for sign-ups. Fire it on the page or click that proves the result, such as the thank-you page after a form is sent, never on the page that holds the form.
- Which event Meta aims an ad set at is chosen in Meta's Ads Manager when the ad set is made. AdCopilot cannot see or set it.
- The Conversions API is Meta's way to send events from a server, alongside the pixel. When both send the same event, Meta matches them on the event name and an event ID so one result is not counted twice (checked 23 October 2026). AdCopilot has no tool for it: it is the site developer's or the platform's job.
- The same result can be counted in Google Analytics as a key event. The `meta-ads-traffic` skill reads that side.

## Stage a missing tag, only if they ask

Stage nothing until the customer asks, and only the piece that is missing.

1. Ask whether the pixel is already on the site by another route: typed into the site's code, or added by a store or website-builder integration. A second base tag beside an existing install counts every visitor twice. If it is already there, stage no base tag.
2. Base tag: ask the customer to paste the base code exactly as Events Manager shows it for their pixel. Never type it from memory and never change it. Propose one Custom HTML tag, named plainly, with their code in its `html` parameter, firing on All Pages (`firing_trigger_id` 2147479553) in `gtm_create_tag`. An existing Custom HTML tag, as `gtm_list_tags` returns it, shows the keys that type uses.
3. Event tag: propose one trigger and one tag together. The trigger is a Window Loaded trigger (type `windowLoaded`), made with `gtm_create_trigger`, whose `filter` is one Tag Manager condition of type `contains` with parameters `arg0` ({{Page Path}}) and `arg1` (the thank-you path they give); a filter on an existing trigger, as `gtm_list_triggers` returns it, shows the shape. The tag is a Custom HTML tag whose code is a single `fbq('track', '<Event>')` call inside a script element, using the standard event name they chose, firing on that trigger. Window Loaded fires after All Pages, so the base code has run and `fbq` exists; Tag Manager does not promise the order of two tags on the same trigger unless tag priority or sequencing is set in Tag Manager, and no AdCopilot tool sets either. Tag Manager's Preview is the referee for the order.
4. A filter on Page Path reads a built-in variable that must be on, or the trigger matches nothing and the tag never fires, silently. Read `gtm_list_built_in_variables` on the AdCopilot workspace if there is one. If Page Path is not in the list, or there is no AdCopilot workspace yet, propose `gtm_enable_built_in_variable` (type `pagePath` at the time of writing) with the trigger. It changes nothing if the variable is already on.
5. Each proposal says what it adds, that it lands in the AdCopilot workspace and changes nothing on the live site until the customer publishes, and how to undo it: do not publish it, or delete it in Tag Manager (AdCopilot never deletes). Ask for the yes before the first call.
6. After the yes, make the calls, then read the tags and triggers back with `gtm_list_tags` and `gtm_list_triggers` on the AdCopilot workspace and report them by name. Say that publishing is the customer's click in Tag Manager (Submit, then Publish, at the time of writing), and that nothing counts until they have done it and Test events has shown the event.
7. If the site asks visitors for cookie consent, the pixel's firing rules must follow it. No AdCopilot tool sets consent settings on a tag: say so, and send them to Tag Manager's consent settings and to whoever runs the site's consent tool.

## Meta's own numbers

AdCopilot cannot give Meta's own figures: spend, results, reach, or pixel health inside Meta. Meta publishes a connector of its own for Meta ads, and AdCopilot's guide shows how it sits beside AdCopilot: https://adcopilot.cloud/docs/guides/meta-ads-alongside-adcopilot/. Give that link when they ask for a Meta number, and never answer one from memory.

## Approval

Every change is proposed first, with what it changes and how to undo it, and is made only after the customer's explicit yes in this conversation, to the change exactly as stated. A yes given earlier is asked for again. Tag Manager changes are staged in the AdCopilot workspace and never published: publishing is the customer's own click in Tag Manager. Nothing is ever deleted.

## What breaks

Calling the pixel working because a tag exists. Staging a second base tag beside an install the customer did not mention. Typing the base code from memory. Firing the event on the form page, not the thank-you page. Saying a staged tag is live. Reading an ID from memory instead of from the tags.

## What is next

Answer what they asked first, whole. Then offer at most one next step, in a sentence, and only if it follows from what you found: the `meta-ads-traffic` skill, to see what Google Analytics counts from Facebook and Instagram, or the missing event tag.

Meta's pages used here: https://developers.facebook.com/documentation/meta-pixel/get-started, https://developers.facebook.com/documentation/meta-pixel/support/meta-ads-data-advisor and https://developers.facebook.com/documentation/ads-commerce/conversions-api
