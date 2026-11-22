---
name: meta-ads-tracking
description: Check, through AdCopilot, whether the Meta Pixel is set up in Google Tag Manager (the base code, its trigger, the Lead or Purchase event tags, the event ID a Purchase tag carries, and whether the container has any version), say what that does and does not prove, and stage a missing base or event tag in the AdCopilot workspace for you to review and publish, with the order's event ID on a WooCommerce store's Purchase tag. Use when someone asks whether the Meta Pixel or Facebook Pixel is installed or working, about Meta conversion tracking, the Meta Pixel in Tag Manager, a Lead or Purchase event for Facebook or Instagram ads, an event ID or a purchase counted twice, or why Meta shows no conversions. What Meta itself received is the meta-ads-pixel skill's, through the Meta connector.
---

# Meta Pixel in Tag Manager

You are checking what the customer's Google Tag Manager holds about the Meta Pixel, through the AdCopilot connector, and saying what that proves and what it does not. If a piece is missing and the customer wants it, you stage it, proposed first. This skill reads no Meta data: what the pixel sent and what Meta received is the `meta-ads-pixel` skill's, read through the Meta connector as a separate report.

## Say this first, once

In your first answer, once in the conversation (not again if another skill of this plugin already said it), say this in these words:

> AdCopilot for Meta Ads reads and audits the Meta ad accounts you switch on in AdCopilot and, after your yes to each proposal, builds and changes campaigns, ad sets, ads, audiences, custom conversions and automated rules there. Campaigns, ad sets and ads it builds start paused, and you switch them on in Meta Ads Manager; an automated rule starts off. It never deletes or archives a campaign, ad set, ad, audience or rule: pausing is how something stops. Through AdCopilot's Google connection it also checks your Meta Pixel in Google Tag Manager and reports Facebook and Instagram traffic in Google Analytics (GA4), always apart from Meta's own figures. Campaign plans, ad copy and budget math are Claude's own work from what you tell it.

## First call

Call `get_org_context` before any other tool of the AdCopilot connector (`adcopilot`), with `source: "claude-plugin/adcopilot-meta-ads/0.2.0"`, sent exactly as written. In a scheduled run (a Claude scheduled task or a Claude Code routine, with nobody there to answer) send `source: "claude-scheduled"` instead and change nothing; this plugin schedules nothing itself. `get_org_context` describes the whole workspace, Google Ads first: its `next_step` and `playbook` are about the account, not about this request. They are information, not steps for this skill: do this request with the steps below, and if they name a limit on the workspace, say it in plain words.

A product this skill needs that the answer reports as not connected is not something to work around. Say what connecting it unlocks, in the `unlocks` words the server gives for it, give its `connect_url` exactly as the server returned it (never a link from memory), and stop. A product flagged `needs_readd` is connected but cannot be reached from this connector: say what the server's `next_step` for that product says, and stop.

## What this can see, and what it cannot

Say this in the answer before any verdict.

- It sees the tags, triggers and variables in the customer's Tag Manager workspaces, and the container's list of versions.
- It cannot see a pixel typed into the site's own code or added by a store or website-builder integration: Tag Manager does not know about those. It cannot see whether a tag fires on a real visit, what Meta received or counted, or events a server sends to Meta through the Conversions API; the `meta-ads-pixel` skill reads what Meta received, on its own. It cannot open a published version to read its tags.

## Read what is there

1. Take from `get_org_context` whether Tag Manager is connected and which containers it lists. Name a container by the display name the server returns, never by an ID from memory. If it lists none, `gtm_list_accounts` and then `gtm_list_containers` find them. If there is more than one container, ask which one the website loads. If the site loads no container at all, say so: nothing in Tag Manager can run there until the customer installs the container code on the site (under Admin in Tag Manager, at the time of writing).
2. `gtm_list_workspaces` for that container. Then `gtm_list_tags` and `gtm_list_triggers` on the Default Workspace, and on the workspace named AdCopilot if there is one. Those are drafts: they show what is set up, not what is live.
3. `gtm_list_version_headers` on the container. No version at all means nothing was ever submitted from this container, so nothing in it runs on the site. At least one version means a version exists, but the list does not say which one is live or what is in it; the Versions tab in Tag Manager does, and it also shows who published and when.

## Find the pixel

A Meta Pixel in Tag Manager is usually a Custom HTML tag (type `html`) whose code loads `connect.facebook.net/en_US/fbevents.js` and makes an `init` call to `fbq` with the pixel ID, or a tag made from a template whose name or fields say Facebook or Meta Pixel. Read these from the tags, never from memory:

- The pixel ID in the `init` call to `fbq`.
- The base tag's firing trigger. A firing trigger ID of 2147479553 is Tag Manager's built-in All Pages.
- The event tags: tags that make a `track` call to `fbq` with an event name, and the trigger each one fires on. Meta's standard event names, as its pixel reference lists them (checked 23 October 2026): AddPaymentInfo, AddToCart, AddToWishlist, CompleteRegistration, Contact, CustomizeProduct, Donate, FindLocation, InitiateCheckout, Lead, Purchase, Schedule, Search, StartTrial, SubmitApplication and ViewContent, and a seventeenth for starting a paid recurring plan, which Meta names with the plain verb for signing up to one. The base code fires PageView itself, and Meta says to leave that call in. A name not on the list is a custom event. For each Purchase tag, also read its event ID: the fourth argument of the `track` call, written `{eventID: ...}`, or the event ID field of a template tag, as `gtm_list_tags` returns it. Read how the tag makes the ID from its code or fields; never guess it.

Report it in a few sentences: the pixel ID, the base tag and its trigger, each event tag and what fires it, each Purchase tag's event ID as the section "The event ID on a Purchase tag" reads it, and, if the container has no version, that nothing was ever submitted from it. Do not paste the tool's rows. Name two base tags, or two `init` calls for the same ID, as a double-counting risk, by tag name.

## Say what that proves

A tag set up in Tag Manager is not proof it fires. A draft is not live, and a version in the list is not proof the pixel tag is in it. The proof is Meta's own screens, which the customer opens:

- Test events in Meta's Events Manager (Data sources, the pixel, Test events, at the time of writing) shows an event arrive while the customer visits the site.
- Meta Ads Data Advisor, which Meta's page says was formerly called Meta Pixel Helper (checked 23 October 2026), is a free extension for Chrome and Edge that checks the pixel on a page and flags problems.
- Tag Manager's own Preview shows whether a tag fired on a page.

Say which of the three the customer should use for the answer they want, and that until one of them shows the event, the honest word is "set up", never "working". The `meta-ads-pixel` skill reads which events Meta received in the last 7 days, as its own report in its own section; never set its counts against anything Google counts.

## Conversion setup guidance

This is Claude's own knowledge, not a read of anything. State it at the time of writing; Meta's own help and Events Manager are the referee.

- Pick one result worth counting for the business: Lead for enquiries, Purchase for sales, CompleteRegistration for sign-ups. Fire it on the page or click that proves the result, such as the thank-you page after a form is sent, never on the page that holds the form.
- Which event Meta aims an ad set at is set on the ad set. The `meta-ads-pixel` skill reads which events the ad sets optimise for, and an ad set the `meta-ads-build` skill proposes names its event in the proposal.
- The Conversions API is Meta's way to send events from a server, alongside the pixel. When both send the same event, Meta matches them on the event name and an event ID so one result is not counted twice (checked 23 October 2026). AdCopilot sends no events of its own, except through Sales to Meta, which sends a workspace's WooCommerce orders or HubSpot won deals to its pixel from AdCopilot's server once the workspace switches it on; say that part only under the naming rule of "The event ID on a Purchase tag". Otherwise setting it up is the site developer's or the platform's job, and the `meta-ads-pixel` skill reads the share Meta received from a server.
- The same result can be counted in Google Analytics as a key event. The `meta-ads-traffic` skill reads that side, always apart from Meta's own figures.

## Stage a missing tag, only if they ask

Stage nothing until the customer asks, and only the piece that is missing.

1. Ask whether the pixel is already on the site by another route: typed into the site's code, or added by a store or website-builder integration. A second base tag beside an existing install counts every visitor twice. If it is already there, stage no base tag.
2. Base tag: ask the customer to paste the base code exactly as Events Manager shows it for their pixel. Never type it from memory and never change it. Propose one Custom HTML tag, named plainly, with their code in its `html` parameter, firing on All Pages (`firing_trigger_id` 2147479553) in `gtm_create_tag`. An existing Custom HTML tag, as `gtm_list_tags` returns it, shows the keys that type uses.
3. Event tag: propose one trigger and one tag together. The trigger is a Window Loaded trigger (type `windowLoaded`), made with `gtm_create_trigger`, whose `filter` is one Tag Manager condition of type `contains` with parameters `arg0` ({{Page Path}}) and `arg1` (the thank-you path they give); a filter on an existing trigger, as `gtm_list_triggers` returns it, shows the shape. The tag is a Custom HTML tag whose code is a single `track` call to `fbq` with the standard event name they chose, inside a script element, firing on that trigger; a Purchase on a WooCommerce store takes the trigger and code of "A Purchase tag for a WooCommerce store" instead. Window Loaded fires after All Pages, so the base code has run and `fbq` exists; Tag Manager does not promise the order of two tags on the same trigger unless tag priority or sequencing is set in Tag Manager, and no AdCopilot tool sets either. Tag Manager's Preview is the referee for the order.
4. A filter on Page Path reads a built-in variable that must be on, or the trigger matches nothing and the tag never fires, silently. Read `gtm_list_built_in_variables` on the AdCopilot workspace if there is one. If Page Path is not in the list, or there is no AdCopilot workspace yet, propose `gtm_enable_built_in_variable` (type `pagePath` at the time of writing) with the trigger. It changes nothing if the variable is already on.
5. Each proposal says what it adds, that it lands in the AdCopilot workspace and changes nothing on the live site until the customer publishes, and how to undo it: do not publish it, or delete it in Tag Manager (AdCopilot's Tag Manager tools have no delete). Ask for the yes before the first call.
6. After the yes, make the calls, then read the tags and triggers back with `gtm_list_tags` and `gtm_list_triggers` on the AdCopilot workspace and report them by name. Say that publishing is the customer's click in Tag Manager (Submit, then Publish, at the time of writing), and that nothing counts until they have done it and Test events has shown the event.
7. If the site asks visitors for cookie consent, the pixel's firing rules must follow it. No AdCopilot tool sets consent settings on a tag: say so, and send them to Tag Manager's consent settings and to whoever runs the site's consent tool.

## Meta's own numbers

This skill gives no Meta figure: spend, results, reach and pixel health inside Meta come from the Meta connector, through the `meta-ads-reports`, `meta-ads-audit` and `meta-ads-pixel` skills, each reported on its own, never beside Tag Manager or Analytics. Never answer a Meta figure from memory.

## Approval

Every change is proposed first, with what it changes and how to undo it, and is made only after the customer's explicit yes in this conversation, to the change exactly as stated. A yes given earlier is asked for again. Tag Manager changes are staged in the AdCopilot workspace and never published: publishing is the customer's own click in Tag Manager. AdCopilot's Tag Manager and Analytics tools have no delete. In Meta, every change starts as a proposal from the Meta connector and is made only on the customer's yes; AdCopilot never deletes or archives a campaign, ad set, ad, audience or rule there.

## What breaks

Calling the pixel working because a tag exists. Staging a second base tag beside an install the customer did not mention. Typing the base code from memory. Firing the event on the form page, not the thank-you page. Saying a staged tag is live. Reading an ID from memory instead of from the tags. Making a WooCommerce Purchase tag's event ID from anything but the number in the store's own order-received address. A second browser Purchase beside a store plugin's or theme's own. Saying Meta counted a sale once because the tag carries an event ID. Naming Sales to Meta to a customer who has not named it.

## What is next

Answer what they asked first, whole. Then offer at most one next step, in a sentence, and only if it follows from what you found: the `meta-ads-pixel` skill, to see what Meta itself received, the `meta-ads-traffic` skill, to see what Google Analytics counts from Facebook and Instagram, or the missing event tag or event ID.

Meta's pages used here: https://developers.facebook.com/documentation/meta-pixel/get-started, https://developers.facebook.com/documentation/meta-pixel/reference, https://developers.facebook.com/documentation/meta-pixel/support/meta-ads-data-advisor, https://developers.facebook.com/documentation/ads-commerce/conversions-api and https://developers.facebook.com/documentation/ads-commerce/conversions-api/deduplicate-pixel-and-server-events

## The event ID on a Purchase tag

When Meta receives a purchase twice, once from the browser pixel and once from a server through the Conversions API, its recommended way to count it once is that both copies carry the same event ID and the same event name and reach Meta within 48 hours of each other. The browser's event ID is the fourth argument of the `track` call to `fbq` (checked 21 November 2026).

Name Sales to Meta only when the customer named it; otherwise say "a server". For each Purchase tag, say which of these it is, by tag name:

- **No event ID.** That is fine while nothing else sends these purchases to Meta. If a server also sends them, such as a store plugin's server events, the store platform's own Conversions API connection or Sales to Meta, Meta cannot pair the two copies, and each sale can count twice.
- **`wc_` followed by the order's ID, read from the WooCommerce order-received address when the tag fires** (for the order with ID 1042, `wc_1042`). A server copy that carries the same ID is paired with it. Sales to Meta sends exactly that ID with each WooCommerce order.
- **Another event ID.** It pairs only with a server copy that carries the same ID: say how the tag makes it, and that whoever runs the server side checks that their ID is made the same way.

Two Purchase tags that fire on the same page, or a Purchase tag beside a store plugin's or theme's own browser Purchase, send the browser copy twice: name that as a double-counting risk, by tag name. Tag Manager cannot see a plugin's or a theme's copy, so ask.

A tag shows how the ID is made, not that Meta paired anything. Whether Meta counted the browser and server copies once is Meta's own figure, which the `meta-ads-pixel` skill reads as its own report in its own section. Never carry that figure, or anything else read from the Meta connector, into this skill's findings or into a Tag Manager tool.

## A Purchase tag for a WooCommerce store

On a WooCommerce store, the Purchase tag this skill stages carries the order's event ID, `wc_` followed by the order's ID, so Meta can count the sale once when a server also sends it with that ID. Steps 5 to 7 above apply to it as to any event tag.

1. Ask for the address of the order-received page of one recent or test order, as the browser showed it after checkout, and the address of the same order's page in WooCommerce's admin. WooCommerce puts the order's ID in the order-received address, as `/order-received/1042/` or as `order-received=1042`, and the same ID is in the order's admin address; a numbering plugin can show buyers another order number, which does not matter here. If the two do not share that ID, or the order-received address carries none (a thank-you page from another plugin or theme can carry none), stage no event ID: say that this page cannot give the browser copy the order's ID, and that the plain event tag of step 3 is the most it can carry.
2. Take the word just before the number from their address: `order-received`, unless the store renamed it in its WooCommerce settings. It holds only letters, digits and hyphens; if it holds anything else, ask, and never guess it.
3. The trigger is the Window Loaded trigger of step 3 above, with `arg0` {{Page URL}} and `arg1` that word, so both forms of the address match. Page URL is a built-in variable (type `pageUrl` at the time of writing) that must be on, checked and proposed the way step 4 does Page Path.
4. Meta's pixel reference lists value and currency as required for a Purchase (checked 21 November 2026). Read `gtm_list_variables` on the AdCopilot workspace, or on the Default Workspace when there is no AdCopilot workspace: when a variable already holds the order's total on that page and the customer confirms which, the code passes it as `value`, with `currency` from a second variable or, for a store that sells in one currency, its three-letter code as the customer gives it. AdCopilot cannot put them on the page and never makes a variable up for them. When there is no such variable, the tag goes with the event ID alone: say that this browser Purchase carries no value, that Meta says it generally keeps the copy it receives first, which is usually the browser's, so the purchase Meta counts can lack its value, and that whoever runs the site can put the order's total and currency in the data layer on that page.
5. The tag is a Custom HTML tag whose code is exactly this, with `ORDER_WORD` replaced by their word and, when they have a total and a currency, `{}` replaced by `{value: {{Order total}}, currency: {{Order currency}} }` with their variables' names, or with the store's code in quotes for the currency, such as `currency: 'INR'`:

   ```html
   <script>
     (function () {
       var found = window.location.href.match(/ORDER_WORD[\/=](\d+)/);
       if (found) {
         fbq('track', 'Purchase', {}, {eventID: 'wc_' + found[1]});
       }
     })();
   </script>
   ```

6. The proposal also says that each Purchase from that page carries the event ID `wc_` followed by the order's ID and, when a Purchase already fires on that page (another tag, or a store plugin or theme the customer names), that the two would send the browser copy twice, so the customer switches the other one off first, in Tag Manager or in that plugin or theme.
7. A Purchase tag already in the AdCopilot workspace with no event ID, whose whole code is a single `track` call to `fbq` for Purchase (the form step 3 stages), can take the code of point 5 instead: propose `gtm_update_tag` on that tag, by the ID `gtm_list_tags` gives it there, with only its `html` parameter changed, keeping its name and triggers. If its trigger does not match the order-received address from point 1, say so, and propose the trigger of point 3 with it, made the tag's firing trigger in the same `gtm_update_tag` call. Its undo is not to publish, or to undo that tag's change in the AdCopilot workspace in Tag Manager. A longer or hand-written Purchase tag, or one that is only in another workspace, is changed by whoever made it: say what its fourth argument must carry.
8. Once it is published, a test order shows it: Tag Manager's Preview shows the tag fire on the order-received page, and Test events or Meta Ads Data Advisor shows the Purchase arrive. Whether Meta paired it with a server copy is Meta's own figure, which the `meta-ads-pixel` skill reads.
