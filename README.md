# udapt.isafenet.app

The Udapt marketing site: https://udapt.isafenet.app (GitHub Pages, custom domain in `CNAME`).

Plain static HTML/CSS, no build step — matches the `airreveal-legal` / `glpmgr-legal` sites' design system (`styles.css` is the same file). Enable GitHub Pages on this repo (Settings → Pages → deploy from the `main` branch, root), then point `udapt.isafenet.app` at GitHub Pages with a `CNAME` DNS record in isafenet.app's DNS.

- `index.html` — marketing homepage
- `privacy.html` — Privacy Policy (kept in sync with `docs/PRIVACY_POLICY.md` in the main `Udapt` repo)
- `terms.html` — Terms of Use, including subscription pricing and the wellness/no-medical-advice disclaimer
- `support.html` — FAQ and contact
- `science.html` — the research behind each rule, with charts and cited sources (generated from the rules in `docs/PLAN_ENGINE_SPEC.md` and sources in `docs/EVIDENCE.md`; keep in sync)
- `guide.html` — plain-English user guide (linked from the app's Settings → Help and information)

Pricing, feature copy and privacy claims here should stay in sync with the main app repo (`docs/SUBSCRIPTION.md`, `docs/PLAN_ENGINE_SPEC.md`, `docs/PRIVACY_POLICY.md`) — update both sides when either changes.
