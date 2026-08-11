# TASKS — reference build → shippable

Read `WEBSITE.md` first. Read `css/site.css`, `index.html`, `kcal/index.html`,
and `apps.json` before writing anything, and match what is there. Do not
redesign, do not introduce a new font, spacing token, radius, or shadow. If a
task seems to require changing the design system, stop and say so.

Work through these in order. The build is close; these are corrections and two
new pages.

---

## A. Fixes to the existing build

**A1 — Store link from data, not HTML.** `kcal/index.html` hardcodes
`https://apps.apple.com/app/id6786282885` with no campaign token. Read
`appStoreUrl` from `apps.json` and set the badge `href` from it. Update
`apps.json` so the value carries `?ct=web_kcal&mt=8`. Handle `status: "pending"`
now, not later: pending renders a non-interactive "Coming soon" element in the
badge's place, with the same footprint so the layout doesn't jump.

**A2 — Kill the price-line string slicing.** `priceLine.slice(app.price.length)`
breaks silently if `priceLine` doesn't begin with `price`. Replace with two
fields, `price` and `priceRest`, concatenated — `price` in the accent, the rest
plain. Update `apps.json`.

**A3 — Open Graph and meta.** Neither page has any. Add to both, per page:
`og:title`, `og:description`, `og:url`, `og:image` (absolute URL, 1200×630),
`og:type`, and `twitter:card=summary_large_image`. Also add
`<meta name="color-scheme" content="light dark">` so scrollbars and controls
follow dark mode. Generate the OG images from the app's accent and wordmark in
the existing `.tile` visual language — one for the home page, one per app.

**A4 — Neutral home header.** `index.html` hardcodes Kcal's orange onto the
header via inline `--accent-l`/`--accent-d`. Remove it. The home page belongs to
the portfolio, not one app, and this drifts the moment a second app exists.
Either drop the accent dot or give the shell a neutral one from the root tokens.

**A5 — Fetch failure is a blank page.** Both pages render entirely from
`fetch('apps.json')` with no `.catch`. If the file 404s or the JSON is malformed,
the visitor gets an empty page and no signal. Add a catch that renders a plain
readable fallback (the tagline and a direct App Store link at minimum) and logs
the error. Consider whether the hero and feature copy — which is static in the
HTML already — should survive a fetch failure; it should.

**A6 — Screenshot rail: four slots, not five.** The rail has five figures,
two of them the same Home screen in light and dark. A light/dark pair of one
screen is one slot; the rail swaps sets with `prefers-color-scheme`. Rebuild as
four slots — Home, log sheet, AI photo review, calendar — sourced from
`assets/shots/kcal/light-N.webp` / `dark-N.webp` with `shots: 4` in `apps.json`.
Every `<img>` needs explicit `width` and `height`. Remove the placeholder
`figcaption`s; if real captures aren't present yet, keep the striped placeholder
background but leave no caption text that could ship.

**A7 — Focus states.** No `:focus-visible` rules exist. Add visible focus to
cards, the badge, more-apps links, and footer links, using the accent and an
offset that reads correctly on the rounded card shapes.

---

## B. New pages

Build `kcal/privacy/index.html` and `kcal/support/index.html` in the existing
shell — same header, same footer, same tokens. Source every factual claim from
`kcal-status.md` and publish nothing from that file's never-publish list.

**B1 — Privacy.** Plain language, no boilerplate generator text. Cover: data is
stored on the device and stays there; there is no account and no sign-up; what
leaves the device for each network feature and to whom; camera use (barcode
scanning and meal photos) and that photos are sent for estimation; notification
use; purchases go through Apple and no payment details are seen; how to delete
data (uninstalling removes it); the support email; a last-updated date. Include
any attribution the status file requires. Accurate and short beats long and
generic — a reviewer reads this.

**B2 — Support.** Contact email, a realistic response window, and four or five
real answers drawn from what actually confuses users: restoring a purchase,
what the free trial covers and when it ends, why barcode scanning needs a real
device, the daily cap on AI estimates, and how to delete data. Link back to the
app page.

**B3 — Wire them up.** Replace the `#` Privacy placeholder and the `mailto:`
Support link in `kcal/index.html` with the real page URLs. Keep the support
email reachable somewhere, but the App Store Connect support field needs a URL,
so the page is what matters.

---

## C. Verify before you report back

- Nothing from the never-publish list appears in any HTML, including comments
  and `alt` text
- No app name appears anywhere except the one in `apps.json`
- Accent hexes still match `kcal-status.md` exactly
- `apps.json` is the only place any app appears twice
- Both new pages render correctly at 390px and at 320px, light and dark
- Disabling JavaScript still leaves a readable page with a working store link
- No dead links, no placeholder text, no lorem
- `WEBSITE.md` still describes what the build actually does; if a task above
  changed the schema, update the schema section to match

---

## Blocked — do not invent

The domain is **simpleappsdev.com**. Use it for every absolute URL —
`og:url`, `og:image`, canonical links.

Everything else in `apps.json` is the owner's to fill via the GitHub web
interface. See §6 of `WEBSITE.md`: write `TODO:<fieldname>` placeholders, never
values, and make every renderer degrade honestly when a value is absent. Create
the `assets/icons/`, `assets/shots/<app>/` and `assets/og/` folders with
committed `.gitkeep` files so uploads have somewhere to land.

Report the placeholders you left as a checklist the owner can work through —
field name, which file, and what the page shows until it's filled.

---

## D. Phase 2 — Dose and Lapse (only after A–C are approved)

Do not start these until the Kcal pages have been reviewed and accepted. Kcal is
the reference; building three apps against an unapproved shell means fixing the
same mistake three times.

For each app, read its `<app>-status.md` and follow §3 of `WEBSITE.md`: an app
page, a privacy page, and a support page, plus its `apps.json` entry, its icon
at `assets/icons/<app>.png`, and its captures under `assets/shots/<app>/`.

Both are **pending**: a "Coming soon" element in place of the badge, and no
`appStoreUrl` in `apps.json` at all.

- **Dose** — mint accent, dark-only. `"theme": "dark"`, `"schemes": ["dark"]`.
  The app page renders dark regardless of system setting. There are no light
  captures and none should be invented.
- **Lapse** — cobalt accent, `auto` theme, both schemes. It has an App Store ID
  from test uploads but was never publicly released, so nothing links to it.

Adding each app means updating the More apps strip on every existing app page,
in both directions. After both are in, verify that all three pages list the
other two.

Do not touch `css/site.css`. If either app appears to need a new style, stop and
say so — a change to the system applies to all three at once or not at all.
