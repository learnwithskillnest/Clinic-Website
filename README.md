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
- English by default with a Hindi switcher in the footer
- Light/dark mode, mobile-friendly, schema.org data for Google

## Editing
- Clinic WhatsApp number: `CLINIC_WHATSAPP` near the bottom of `index.html`
- Images: `assets/img/` (stock photo sources listed in `docs/image-sources.md`)
- Hindi text: the `I18N.hi` dictionary in `index.html`

## Deploy
Any static host works (GitHub Pages, Netlify, Vercel, Cloudflare Pages). For GitHub Pages: Settings → Pages → Deploy from branch `main`, folder `/ (root)`, then add your custom domain.
