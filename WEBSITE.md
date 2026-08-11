# WEBSITE.md — portfolio site generator

Project instructions for building and maintaining the marketing site for the
`simpleappsdev` app portfolio. Lives at `IOSAPPS/WEBSITE.md`, next to
`BLUEPRINT.md`.

**Your job:** given an app's `<app>-status.md`, produce that app's pages so they
are indistinguishable in structure and quality from every other app's pages.
Consistency is the product. Never redesign; extend.

The Sous app is **not** part of this site. Different brand, different audience,
different price tier. If asked to add it, stop and confirm.

---

## 1. Stack and structure

Static HTML + CSS. No build step, no framework, no JS beyond a theme toggle and
a screenshot scroller. Hosted on GitHub Pages behind a custom domain.

```
site/
├── index.html              # portfolio home
├── apps.json               # SINGLE SOURCE OF TRUTH for the app list
├── css/site.css            # shared shell — identical for every app
├── assets/
│   ├── icons/<app>.png     # 512px app icon, rounded by CSS not baked in
│   └── shots/<app>/        # screenshots, light-N.webp / dark-N.webp
└── <app>/
    ├── index.html          # app page
    ├── privacy/index.html  # required by App Store Connect
    └── support/index.html  # required by App Store Connect
```

Adding an app = one `apps.json` entry + one `<app>/` folder + assets. You never
touch `index.html` or another app's folder. If a change would require editing
more than one existing app's files, it belongs in `css/site.css` or `apps.json`
instead.

### apps.json schema

Top level:

```json
{
  "handle": "simpleappsdev",
  "line": "Small apps that do one thing each.",
  "instagram": "https://instagram.com/simpleappsdev",
  "supportEmail": "support@simpleappsdev.com",
  "responseTime": "I usually reply within two days.",
  "apps": [ … ]
}
```

`responseTime` is one plain sentence appended after the support address. It is a
promise the owner makes, so an unset value simply omits the sentence — the
support page never invents a reply window.

Each app:

```json
{
  "id": "kcal",
  "name": "Kcal",
  "tagline": "Calories and macros. Nothing else.",
  "price": "$0.99",
  "priceRest": " one-time, after a 7-day free trial. No subscription.",
  "accentLight": "#FF7A00",
  "accentDark": "#FF8F2A",
  "url": "kcal/",
  "appStoreUrl": "https://apps.apple.com/app/id6786282885?ct=web_kcal&mt=8",
  "requires": "Requires an iPhone running iOS 17 or later.",
  "theme": "auto",
  "schemes": ["light", "dark"],
  "shots": 4,
  "status": "live",
  "icon": "assets/icons/kcal.png"
}
```

`price` and `priceRest` are separate strings that concatenate — `price` renders
in the accent, `priceRest` plain. Never derive one from the other by slicing.

`icon` is optional; without it the CSS `.tile` renders a gradient wordmark from
the app's accent, which is a legitimate permanent state, not a placeholder.

### theme and schemes

`theme` is `auto` (default — follows `prefers-color-scheme`) or `dark` (the app
page renders dark regardless of the visitor's system setting). Use `dark` only
when the app itself is dark-only; the page should show what the product is.

`schemes` lists which screenshot sets exist. A dark-only app has
`["dark"]` and no light captures — the rail must not try to swap sets or look
for files that were never exported. Never fabricate a light screenshot by
inverting a dark one.

As of now: **Dose is dark-only** — it enforces dark at the window level and has
no appearance setting, so `"theme": "dark"`, `"schemes": ["dark"]`. Kcal and
Lapse are `auto` with both sets.

### status

`live` or `pending`.

A `pending` app renders a non-interactive "Coming soon" element where the badge
would go, with the same footprint so the layout doesn't shift. It still gets
privacy and support pages — App Review reads those before approval.

**A pending app must never link to the App Store, even if an ID exists.** Lapse
has an App Store ID from test uploads but has never been publicly released; that
link would lead nowhere. For pending apps, omit `appStoreUrl` from `apps.json`
entirely rather than storing a URL the renderer is trusted not to use. Add it
only when the app is actually on sale, at which point `status` flips to `live`
in the same edit.

**Paths are root-relative-by-convention, not absolute.** `url` and `icon` are
written as they appear from the site root (`kcal/`, `assets/icons/kcal.png`);
app pages prefix `../`. Keep that convention when adding apps.

---

## 2. Extraction contract — status file → web copy

Status files are internal engineering documents. They contain material that
must never reach the public site. Read the whole file, then pull only from the
mapped sections.

### Pull from

| Status section | Produces |
|---|---|
| `## Concept` | tagline, headline, the "what it doesn't do" line, price/trial |
| `## Features` | the three feature blocks (see §3) |
| `## Design decisions` → Accent | `accent.light` / `accent.dark` — **copy the hex exactly, never invent one** |
| `## Design decisions` → Type / Motion | tone cues for that app's page only |
| `## Design decisions` → iPhone-only, project deployment target | `requires` |
| App Store ID (search `appStoreID`, `apps.apple.com/app/id…`) | store links |
| API clients + camera/notification usage | privacy page facts |
| Attribution requirements (e.g. "Powered by FatSecret") | privacy page footer |
| Health/medical disclaimers | app page footnote **verbatim** |

### Never publish

- File structure, class names, model schemas, `Secrets.swift`, bundle IDs,
  build numbers, team IDs, UDIDs, `xcodebuild` commands
- `## Known issues / deliberate deviations` — every line of it
- `## Debug tools`, `--seed-demo`, any DEBUG affordance
- Anything about lost source code, rebuilds, App Review rejections, or
  Guideline numbers
- Named third-party services **except** where attribution is contractually
  required, or where the privacy page must disclose data leaving the device
- Model names, quotas expressed as internals, rate limits

### Judgement calls

A feature is publishable if a user would notice it. "Live search-as-you-type"
is a benefit; "keystrokes debounce ~350 ms with a generation stamp" is
implementation. Where a status file describes a limit the user hits, publish
the limit in user terms — an AI daily cap is worth stating plainly on the page,
because someone who buys expecting unlimited use and finds a cap leaves a
one-star review.

If a fact is not in the status file, do not write it. No invented download
counts, no invented review quotes, no "trusted by thousands", no roadmap
promises. Missing information is a question for the user, not a gap to fill.

**App names are `apps.json`-only.** Status files mention other app names in
passing — inside the never-publish sections. Those are not products. An app
exists on this site when it has an `apps.json` entry and its own status file,
and never otherwise: no placeholder cards, no "coming soon" for an app absent
from `apps.json`, no mention in comments or alt text.

---

## 3. Page contracts

Mobile-first and mobile-real: effectively all traffic arrives from an Instagram
link on a phone. Design at 390px and let desktop be the adaptation. Anything
below the first screen is a bonus, not a plan.

### Home (`index.html`)

1. One line stating what this is. No About section, no bio, no blog.
2. App grid from `apps.json` — icon, name, tagline, price. **Cards link to the
   app page, never straight to the App Store.** The app page is where you get
   to convince; the store listing is where you can only lose.
3. Footer: Instagram, support email.

The home page holds no per-app copy of its own. Everything it shows comes from
`apps.json`, so it can never drift out of sync with an app page.

### App page (`<app>/index.html`)

In this order, because on a phone only the first screen is guaranteed:

1. Icon, name, one-line pitch, **App Store badge above the fold**
2. Price and trial in one plain sentence. State it clearly — anyone who balks
   at a dollar was never going to pay
3. Screenshots, horizontally scrolled, light or dark set matched to the
   active theme
4. Exactly **three** feature blocks. Not a feature list — the three things
   that make someone tap. Short heading, one or two sentences
5. The positioning line: what the app deliberately does not do. This is the
   portfolio's whole thesis and every app page must carry its version of it
6. Any required disclaimer, verbatim from the status file
7. `requires` line
8. **More apps strip** — every other app's icon + name, from `apps.json`.
   Non-negotiable on every app page; it is the reason a shared site exists
9. Privacy · Support links

### Privacy page

Written from the status file's actual behaviour, in plain language, no
boilerplate generator text. Cover: what is stored on device and that it stays
there; whether there is an account (there isn't); what leaves the device and to
whom, for each network feature; what the camera and notifications are used for;
that purchases go through Apple and no payment data is seen; the support email;
a last-updated date. Add required attributions at the bottom.

Accurate and short beats long and generic. A reviewer reads this.

### Support page

Contact email, expected response time, and three or four real answers pulled
from features that actually confuse people — restoring a purchase, trial
length, why a feature needs a real device, how to delete data. Link back to the
app page.

---

## 4. Design system

The shell is shared and fixed. The accent is the only thing that varies per
app, and it always comes from that app's status file. Set it as a CSS custom
property on the page root so a single stylesheet themes every app:

```css
:root { --accent: #FF7A00; --accent-dark: #FF8F2A; }
```

**The base neutrals carry no hue.** The portfolio spans warm and cool accents
(Kcal orange, Dose mint, Lapse cobalt), so a warm paper or a warm line colour
reads as a colour cast next to the cool ones. Keep `--paper`, `--bone`,
`--smoke` and their dark counterparts hue-free, and let each app page tint them
with its own accent instead:

```css
:root { --tint: 0%; }          /* portfolio home: no accent, no tint */
body[data-app] { --tint: 3%; } /* app page: tinted by its own accent */
```

The home page has no accent of its own and must stay neutral — it belongs to the
portfolio, not to whichever app shipped first. Do not hardcode any app's accent
into the shared header, footer, or home page.

Light and dark both supported via `prefers-color-scheme`, because the apps are
and because the screenshot sets exist in both.

The visual language is defined by the reference build (see
`claude-design-prompt.md`). Once that reference exists, treat it as law: read
`css/site.css` and the existing app pages before writing anything, and match
them. Do not introduce a new font, spacing scale, radius, or shadow for a new
app. If you believe the system needs to change, say so and wait — a change
applies to all apps at once or not at all.

Quality floor, unannounced: responsive to 320px, visible keyboard focus,
`prefers-reduced-motion` respected, real `<img>` dimensions to stop layout
shift, screenshots as WebP under 150KB each, semantic headings, `<title>` and
meta description per page, Open Graph image per app so Instagram link previews
aren't blank.

---

## 5. Store links and attribution

The store URL lives in `apps.json` as `appStoreUrl`, with its campaign token
already baked in, and every page reads it from there:

```
https://apps.apple.com/app/id<id>?ct=web_<app>&mt=8
```

### Static mirrors

`apps.json` is the source of truth, but it is not the only copy. Anything a
visitor must still get with JavaScript off — or when the fetch fails — is
written into the HTML as a **static mirror** of the data, and the script
replaces it on load:

| Page | Mirrored |
|---|---|
| Home | the app card, and a direct store link that exists only in the fallback |
| App page | the store badge, price line, `requires` |
| Privacy · Support | the support address |

Two rules keep the duplication honest:

1. **The script clears before it renders.** It never appends to a mirror, so a
   successful load leaves exactly one copy — the data's.
2. **A mirror never states more than the data does.** If `appStoreUrl` is
   unset or the app is `pending`, the static markup is the "Coming soon"
   element, not a badge with a dead `href`. A pending app gets no store link
   in the home fallback either.

Every mirror carries a comment saying so. Edit `apps.json`, edit the mirror —
the home card's store link is the one place a card may point at the store,
because in that state there is no working page to send anyone to.

Instagram video links use their own token per video (`ct=ig_<app>_<nn>`) — keep
those out of the repo; they belong in the link-in-bio destination or the post
itself. Verify the exact parameter set in App Store Connect before relying on
the numbers; token behaviour changes and the docs are the authority, not this
file.

Official Apple "Download on the App Store" badge artwork only, unmodified,
with the required clear space. A hand-made badge is a guideline violation and
looks it.

### Screenshots

`shots` in `apps.json` gives the count, `schemes` says which sets exist. Files
are `assets/shots/<app>/light-N.webp` and `dark-N.webp`, paired and gapless, and
the rail swaps sets with the colour scheme — so a light and a dark capture of the
same screen are **one slot, not two**. A dark-only app has only `dark-N.webp`
and no swap. Every `<img>` carries explicit `width` and `height`. Placeholder
captions must be gone once real captures land.

Captures are exported at 1320×2868 and converted for the web by `shots.sh`
(WebP, ~600px wide, under 150KB each). Never ship the native-resolution PNGs:
the traffic is mobile and mostly on cellular.

---

## 6. Ownership boundary — content vs code

The owner fills in content through the GitHub web interface. Claude Code builds
the machinery that reads it. These are separate jobs and the line does not move.

**Claude Code never writes a content value.** It may add a *key* to
`apps.json` when the schema needs one, with a `TODO:` placeholder as the value,
and it may fix a malformed structure. It must not invent, guess, or fill in a
URL, a price, an App Store ID, an email, a tagline, or an image. If a value is
needed and absent, leave the placeholder and list it in the report.

**Placeholders are marked, never empty.** Any value the owner must supply is the
string `TODO:<fieldname>` — for example `"appStoreUrl": "TODO:appStoreUrl"`.
Empty strings are forbidden: an empty `href` silently reloads the page, an empty
`src` fires a second request for the document, and neither is visible as a bug.
Every renderer must treat a `TODO:` value as absent and degrade honestly:

- `appStoreUrl` unset → render the "Coming soon" element, not a dead badge
- `icon` unset → render the CSS gradient `.tile` wordmark
- a screenshot file missing → the striped placeholder slot, no caption
- `instagram` / `supportEmail` unset → omit that footer link entirely

A page with unfilled placeholders must still be a valid, presentable page. It
should never show the literal text `TODO:` to a visitor.

Rendering a value the owner supplied is not writing one. The static mirrors in
§5 exist so a supplied value survives a dead fetch; a value the owner has *not*
supplied never gets mirrored, because there is nothing to mirror.

**Image paths are conventional, so the owner can upload without touching code.**
Fixed locations, so a file dropped in the right place simply appears:

```
assets/icons/<app>.png              512px square, square corners
assets/shots/<app>/light-1.webp     …-2, -3, -4
assets/shots/<app>/dark-1.webp      dark-only apps have these only
assets/og/<app>.png                 1200×630
```

Every folder holds a committed `.gitkeep` so it exists in the repo and the
GitHub upload UI can target it. Never rename these paths to match a file that
happens to exist; the paths are the contract.

---

## 7. Before you finish

- Every claim on the page traces to a line in the status file
- Nothing from the "never publish" list appears in the HTML, including comments
- `apps.json` is the only place any app appears twice
- The new app's More apps strip lists every other app, and every other app's
  strip now lists the new one
- Accent hex matches the status file exactly
- Privacy and support pages exist and their URLs are ready to paste into App
  Store Connect
- Page renders correctly at 390px wide, in light and dark
- No dead links, no placeholder text, no lorem
