# Smile & Glow — Dental & Aesthetic Clinic, Lucknow

Website for **Smile & Glow** (Dr. Pallavi — BDS, MDS (Maxillofacial Medicine & Radiology), FMC (Fellow in Cosmetology), PG Diploma in Nutrition).

- Branches: **I.T Chauraha** (Mon–Sat 11 AM–3 PM) and **Aashiyana** (Mon–Sat 4 PM–9 PM); Sundays by appointment
- Phone / booking: +91 72754 33783
- Instagram: [@smileandglowclinic](https://www.instagram.com/smileandglowclinic/)

## What's in the site
Single static page (`index.html`) — no build step:
- Hero photo slideshow, dental and skin & hair treatment cards with photos, swipeable laser treatments carousel
- "Inside Smile & Glow" photo gallery carousel (real clinic photos)
- About Dr. Pallavi, "Inside our clinic", visit steps, FAQs
- Both branches with timings, maps and directions
- Booking form that opens WhatsApp with the patient's details (nothing stored)
- English at `/`, Hindi at `/hi/` (switcher in the footer)
- Light/dark mode, mobile-friendly, schema.org data for Google

## Editing
- **English page:** edit `index.html`.
- **Hindi page:** don't edit `hi/index.html` by hand. Add or change translations in `i18n/hi.json`, then run:
  ```
  pip install beautifulsoup4   # once
  python3 tools/build.py
  ```
  This rebuilds `hi/index.html`, refreshes the structured data (JSON-LD) in both pages from the visible FAQ and clinic details, and lists any text that still needs a Hindi translation.
- Clinic WhatsApp number: `CLINIC_WHATSAPP` near the bottom of `index.html`
- Images: `assets/img/` (stock photo sources listed in `docs/image-sources.md`)

## SEO / AEO
- `sitemap.xml` (English + Hindi with hreflang), `robots.txt`, `llms.txt` (plain-text summary for AI assistants)
- Structured data: Organization, Dr. Pallavi (Person with credentials), both branches (Dentist + MedicalClinic with hours, Google Maps place, services, rating), WebSite, MedicalWebPage, FAQPage
- Keep clinic hours/address identical on the site, `llms.txt`, Google Business Profiles and directories.

## Live site
https://smileandglow.co.in (GitHub Pages, custom domain via `CNAME`)

## Deploy
Any static host works (GitHub Pages, Netlify, Vercel, Cloudflare Pages). For GitHub Pages: Settings → Pages → Deploy from branch `main`, folder `/ (root)`, then add your custom domain.
