# App pages

The app pages share navigation and information structure, while each app keeps
its own stylesheet, colors, typography and visual details.

## Support pages

Use this order in each app's `index.html` (and in Unroller's root `support.html`):

1. App name, short description and App Store badge when publicly available.
2. On-page navigation: Getting started, Purchases, Data & privacy, Help.
3. Sections with the IDs `getting-started`, `purchases`, `data-privacy`, `help`.
4. App-specific troubleshooting and contact instructions in the Help section.
5. Footer with All apps, Support, Privacy, Terms and the support address.

Keep the `#de` entry points and existing translations on Margly's pages.

## Shared navigation

Support, privacy and terms pages use the same header and footer links. Mark the
current header link with `aria-current="page"`. Link All apps to `../`.
Keep a skip link to `#main-content` and descriptive navigation labels.

Load `../app-structure.css` after the individual app stylesheet. The shared file
controls layout, section spacing and mobile touch targets; it uses the existing
theme variables instead of defining a new palette. Policy and terms content
remains independent of the support-page structure.

## Download badges

Only show a download badge after verifying that the app's public App Store page
is available. The portfolio's `/` and `/apps/` entry points must remain in sync.

Use `assets/app-store-badge.svg`, downloaded without modification from
https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg.
Follow Apple's badge guidance at
https://developer.apple.com/app-store/marketing/guidelines/.
The badge is displayed at 44px high, with 11px clear space on every side.
Use the app-specific App Store link and accessible label on the enclosing anchor.

Unroller uses the same repository on unroller.app. Keep `support.html` available
at the root because it is the support URL already used in App Store Connect. Its
existing root privacy and terms pages use the same navigation and keep their
legal content. Unroller retains the palette and typography from `styles.css`,
with page layout in `unroller.css`.
