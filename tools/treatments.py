"""Treatment pages for smileandglow.co.in — content + page builder.

Edit the TREATMENTS list below, then run:  python3 tools/build.py
Each entry becomes /<slug>/index.html, styled with /assets/site.css
(generated from the homepage's own <style> block, so the look stays in sync).

Prices are an indicative guide to typical costs in Lucknow (researched Oct 2026).
Ask Dr. Pallavi to confirm or adjust them — change the numbers here and rebuild.
"""
import html
import json
import re
from pathlib import Path

SITE = "https://smileandglow.co.in"
PHONE_DISPLAY = "+91 72754 33783"
PHONE_TEL = "+917275433783"
WHATSAPP = "917275433783"
REG_NO = "15199/11/02/2016"
UPDATED = "19 October 2026"
UPDATED_ISO = "2026-10-19"

PRICE_NOTE = ("Prices are a guide to typical costs at Lucknow clinics (October 2026). "
              "Your exact cost depends on your examination and is explained to you before treatment starts.")

TREATMENTS = [
    {
        "slug": "root-canal-treatment-lucknow",
        "name": "Root Canal Treatment",
        "short": "Root canal (RCT)",
        "category": "Dental",
        "book_value": "Root canal",
        "title": "Root Canal Treatment in Lucknow – Cost | Smile & Glow",
        "description": "Root canal treatment in Lucknow by Dr. Pallavi at I.T Chauraha & Aashiyana. Typical cost ₹3,000–₹8,000 per tooth. Visits, procedure, aftercare & FAQs.",
        "image": "dental-root-canal.webp",
        "image_alt": "Dental model showing the inside of a tooth for root canal treatment",
        "intro": ("A root canal saves a tooth whose inner pulp has become infected or inflamed, instead of pulling it out. "
                  "At Smile &amp; Glow, Dr. Pallavi carries out root canal treatment under local anaesthesia, plans it from an X-ray, "
                  "and explains the cost before starting."),
        "facts": [("Visits", "1–3"), ("Time per visit", "45–90 min"), ("Anaesthesia", "Local"), ("Typical cost", "₹3,000–₹8,000 per tooth")],
        "who_title": "Signs you may need a root canal",
        "who": ["Pain that lingers after something hot or cold",
                "Severe toothache when biting or chewing",
                "Swelling, or a pimple-like bump on the gum",
                "A tooth that has turned darker",
                "Deep decay or a crack seen on an X-ray"],
        "steps": [("Examination and X-ray", "We check the tooth and take an X-ray to see the roots and the extent of infection."),
                  ("Local anaesthesia", "The tooth and gum are numbed so you feel pressure, not pain."),
                  ("Cleaning the canals", "The infected pulp is removed and the canals are cleaned, shaped and disinfected."),
                  ("Filling and sealing", "The canals are filled and sealed to keep bacteria out."),
                  ("Protecting the tooth", "Back teeth usually need a crown afterwards, because a root-canal-treated tooth is more brittle.")],
        "prices": [("Front tooth (1 canal)", "₹3,000 – ₹5,000"),
                   ("Premolar (1–2 canals)", "₹3,500 – ₹6,000"),
                   ("Molar (3–4 canals)", "₹4,000 – ₹8,000"),
                   ("Re-treatment of an old root canal", "₹5,000 – ₹8,000"),
                   ("Crown after RCT (metal, ceramic or zirconia)", "₹3,000 – ₹15,000")],
        "price_factors": "The cost depends on the tooth (front teeth have fewer canals than molars), how severe the infection is, whether it is a re-treatment, and the type of crown you choose.",
        "aftercare": ["Don't chew on that side until the numbness wears off and the final filling or crown is in place.",
                      "Mild soreness for 2–3 days is normal; take pain relief only as advised.",
                      "Get the crown fitted on time — a treated tooth without one can crack.",
                      "Keep brushing twice a day and come for your review visit."],
        "faqs": [("How much does root canal treatment cost in Lucknow?",
                  "A root canal typically costs ₹3,000–₹5,000 for a front tooth, ₹3,500–₹6,000 for a premolar and ₹4,000–₹8,000 for a molar. A crown, if needed, costs ₹3,000–₹15,000 depending on the material. Your exact cost is confirmed after an X-ray."),
                 ("Is root canal treatment painful?",
                  "Modern root canal treatment is done under local anaesthesia, so most patients feel little more than they would during a regular filling. It's usually the infection beforehand that hurts — treatment brings relief."),
                 ("How many visits does a root canal take?",
                  "Many root canals are completed in one or two visits. A tooth with a severe infection may need an extra visit so the infection can settle before the canals are sealed."),
                 ("Do I need a crown after a root canal?",
                  "Back teeth usually need a crown because they take the most chewing force and become more brittle after treatment. Front teeth often only need a filling. Dr. Pallavi will advise you based on your tooth."),
                 ("Can I go to work after a root canal?",
                  "Yes. Most people go back to their normal routine the same day. Avoid chewing on the treated side until the numbness has worn off.")],
        "related": ["dental-implants-lucknow", "teeth-whitening-lucknow"],
    },
    {
        "slug": "dental-implants-lucknow",
        "name": "Dental Implants",
        "short": "Dental implants",
        "category": "Dental",
        "book_value": "Implants",
        "title": "Dental Implants in Lucknow – Cost per Tooth | Smile & Glow",
        "description": "Dental implants in Lucknow by Dr. Pallavi at I.T Chauraha & Aashiyana. Typical cost ₹20,000–₹45,000 per tooth. Procedure, healing time, suitability & FAQs.",
        "image": "dental-implants.webp",
        "image_alt": "Dental implant model with a titanium post and crown",
        "intro": ("A dental implant replaces a missing tooth with a small titanium post placed in the jawbone and a natural-looking crown on top. "
                  "Unlike a bridge, it doesn't need the neighbouring teeth to be cut down, and it helps preserve the jawbone."),
        "facts": [("Total treatment time", "3–6 months"), ("Implant placement", "About 1 hour per implant"), ("Anaesthesia", "Local"), ("Typical cost", "From ₹20,000 per tooth")],
        "who_title": "Who dental implants are for",
        "who": ["One or more missing teeth",
                "Loose or uncomfortable dentures",
                "Healthy gums and enough jawbone (bone grafting can help if not)",
                "People whose diabetes is under control, and non-smokers, who tend to heal best"],
        "steps": [("Consultation and scans", "We examine your mouth and take X-rays (and a 3D scan if needed) to check the bone and plan the implant position."),
                  ("Implant placement", "The titanium post is placed in the jawbone under local anaesthesia."),
                  ("Healing", "Over 2–4 months the bone bonds with the implant. A temporary tooth can often be given meanwhile."),
                  ("Crown fitting", "A custom crown is attached so the new tooth looks and works like a natural one.")],
        "prices": [("Single implant (standard system)", "₹20,000 – ₹45,000 per tooth"),
                   ("Single implant (premium imported system)", "₹45,000 – ₹80,000 per tooth"),
                   ("Bone grafting (only if needed)", "₹5,000 – ₹25,000"),
                   ("Sinus lift (only if needed, upper back teeth)", "₹10,000 – ₹40,000")],
        "price_factors": "The cost depends on the implant brand, the crown material, how many teeth are being replaced, and whether bone grafting or a sinus lift is needed.",
        "aftercare": ["Eat soft food for the first few days and chew on the other side.",
                      "Avoid smoking — it slows healing and raises the risk of implant failure.",
                      "Brush gently around the area and use any mouthwash prescribed.",
                      "Come for regular check-ups and cleaning so the gum around the implant stays healthy."],
        "faqs": [("How much does a dental implant cost in Lucknow?",
                  "A single dental implant typically costs ₹20,000–₹45,000 per tooth with a standard implant system, and ₹45,000–₹80,000 with a premium imported system. Bone grafting (₹5,000–₹25,000) or a sinus lift is only added if your scan shows it's needed."),
                 ("Is dental implant surgery painful?",
                  "The implant is placed under local anaesthesia, so most people feel pressure rather than pain. Mild soreness and swelling for a few days afterwards is common and usually managed with simple pain relief."),
                 ("How long do dental implants last?",
                  "With good brushing, regular check-ups and no smoking, dental implants can last for many years — often decades. The crown on top may need replacing after some years of wear."),
                 ("Am I suitable for a dental implant?",
                  "Most adults with healthy gums are suitable. You need enough jawbone to hold the implant; if there isn't enough, bone grafting can often help. Uncontrolled diabetes and heavy smoking reduce success, so Dr. Pallavi will check these first."),
                 ("Implant or bridge — which is better?",
                  "An implant replaces the tooth on its own and doesn't involve cutting the neighbouring teeth, while a bridge relies on them for support. A bridge can be quicker and cheaper. Dr. Pallavi will explain both options for your case.")],
        "related": ["root-canal-treatment-lucknow", "teeth-whitening-lucknow"],
    },
    {
        "slug": "teeth-whitening-lucknow",
        "name": "Teeth Whitening",
        "short": "Teeth whitening",
        "category": "Dental",
        "book_value": "Smile makeover / whitening",
        "title": "Teeth Whitening in Lucknow – Cost & Results | Smile & Glow",
        "description": "Professional teeth whitening in Lucknow by Dr. Pallavi. Typical cost ₹4,000–₹15,000 per session. Who it suits, what to expect, aftercare & FAQs.",
        "image": "dental-whitening.webp",
        "image_alt": "Clear teeth whitening tray held in two hands",
        "intro": ("Professional teeth whitening safely lightens stains from tea, coffee, tobacco and ageing under a dentist's supervision. "
                  "Before whitening, we check your teeth and gums, because cavities and sensitivity need treating first."),
        "facts": [("Session time", "45–60 min"), ("Visits", "Usually 1"), ("Downtime", "None"), ("Typical cost", "₹4,000–₹15,000")],
        "who_title": "Who teeth whitening suits",
        "who": ["Natural teeth that have turned yellow or stained over time",
                "Stains from tea, coffee, paan or smoking",
                "People wanting a brighter smile for a wedding or event",
                "Not suitable during pregnancy, or for crowns and fillings — these don't change colour"],
        "steps": [("Check-up and cleaning", "We check for cavities or gum problems and clean the teeth so the gel works evenly."),
                  ("Shade check", "We record your current shade so you can see the difference."),
                  ("Gum protection", "A protective barrier is placed over the gums."),
                  ("Whitening gel", "Professional whitening gel is applied in timed cycles."),
                  ("Review", "We check the new shade and explain how to keep it.")],
        "prices": [("In-clinic professional whitening (one session)", "₹4,000 – ₹15,000"),
                   ("Laser / light-activated whitening", "₹5,000 – ₹25,000")],
        "price_factors": "The cost depends on the whitening system used, how many shades lighter you want to go, and whether a cleaning is needed first.",
        "aftercare": ["For 48 hours avoid tea, coffee, cola, turmeric-rich curries and smoking.",
                      "Some sensitivity for a day or two is normal; a sensitivity toothpaste helps.",
                      "Brush twice a day and get a cleaning every 6 months to keep the result longer."],
        "faqs": [("How much does teeth whitening cost in Lucknow?",
                  "Professional in-clinic teeth whitening typically costs ₹4,000–₹15,000 per session in Lucknow, and laser or light-activated whitening ₹5,000–₹25,000. The price depends on the system used and the shade you want."),
                 ("Is teeth whitening safe for my teeth?",
                  "When done by a dentist after a check-up, whitening is safe for enamel. Temporary sensitivity is the most common side effect and usually settles within a day or two."),
                 ("How long do whitening results last?",
                  "Results usually last from several months to a couple of years. They fade faster with frequent tea, coffee or tobacco."),
                 ("Will whitening change the colour of my crowns or fillings?",
                  "No. Whitening works only on natural teeth. If you have visible crowns or fillings, Dr. Pallavi will plan around them so your smile looks even."),
                 ("Can I whiten my teeth at home?",
                  "Over-the-counter products are weaker and can irritate the gums if used wrongly. It's best to have a check-up first so stains caused by decay or old fillings aren't missed.")],
        "related": ["root-canal-treatment-lucknow", "dental-implants-lucknow"],
    },
    {
        "slug": "laser-hair-removal-lucknow",
        "name": "Laser Hair Reduction",
        "short": "Laser hair reduction",
        "category": "Laser",
        "book_value": "Laser hair reduction",
        "title": "Laser Hair Removal in Lucknow – Cost | Smile & Glow",
        "description": "Laser hair reduction (laser hair removal) in Lucknow by Dr. Pallavi. From ₹1,500 per session; full face ₹3,500–₹5,000. Sessions, safety for Indian skin & FAQs.",
        "image": "hero-laser-machine.webp",
        "image_alt": "Laser hair reduction machine with handpiece",
        "intro": ("Laser hair reduction (often called laser hair removal) targets the hair root with light, giving long-lasting reduction of unwanted hair. "
                  "Every plan at Smile &amp; Glow starts with a skin assessment and patch test, and the settings are chosen for your skin type."),
        "facts": [("Sessions", "6–8, about 4–6 weeks apart"), ("Session time", "15–60 min (by area)"), ("Downtime", "None to minimal"), ("Typical cost", "From ₹1,500 per session")],
        "who_title": "Who laser hair reduction suits",
        "who": ["Unwanted hair on the face, underarms, arms, legs or bikini line",
                "Facial hair linked to PCOS or hormones (usually 8–10 sessions plus occasional maintenance)",
                "Ingrown hairs and irritation from frequent waxing or shaving",
                "Works best on dark hair; it doesn't work well on very light, grey or white hair"],
        "steps": [("Consultation and skin assessment", "We check your skin type, hair type and medical history."),
                  ("Patch test", "A small area is tested to choose safe, effective settings."),
                  ("Preparation", "Shave the area the day before. Don't wax, thread or bleach for 4 weeks before."),
                  ("Laser session", "The handpiece is moved over the area with cooling for comfort."),
                  ("Follow-up sessions", "Sessions are repeated every 4–6 weeks to catch hair in its growth phase.")],
        "prices": [("Upper lip or chin", "₹1,500 – ₹2,500 per session"),
                   ("Full face", "₹3,500 – ₹5,000 per session"),
                   ("Underarms", "₹2,500 – ₹4,000 per session"),
                   ("Full arms", "₹6,000 – ₹10,000 per session"),
                   ("Full legs", "₹8,000 – ₹12,000 per session")],
        "price_factors": "The cost depends on the size of the area and how many sessions you need. Ask about package prices when booking several sessions.",
        "aftercare": ["Avoid direct sun for a week and use sunscreen on treated skin.",
                      "Mild redness can last a few hours — a cool compress helps.",
                      "Shave between sessions if needed, but don't wax, thread or pluck.",
                      "Avoid hot showers, saunas and gym sweat for 24 hours."],
        "faqs": [("How much does laser hair removal cost in Lucknow?",
                  "Laser hair reduction typically costs ₹1,500–₹2,500 per session for the upper lip or chin, ₹3,500–₹5,000 for the full face, ₹2,500–₹4,000 for underarms, ₹6,000–₹10,000 for full arms and ₹8,000–₹12,000 for full legs. Most people need 6–8 sessions."),
                 ("Is laser hair reduction permanent?",
                  "It gives long-term reduction rather than guaranteed permanent removal. Most treated hair doesn't grow back; some finer hair may return and can be handled with occasional maintenance sessions."),
                 ("Is laser hair reduction safe for Indian skin?",
                  "Yes, when the right laser settings are used for your skin type. That's why every plan starts with a skin assessment and patch test."),
                 ("Does laser hair reduction hurt?",
                  "Most people describe it as a quick snap, like a rubber band, with warmth. Cooling during the session keeps it comfortable."),
                 ("How many sessions will I need?",
                  "Most people need 6–8 sessions, 4–6 weeks apart. Hormonal facial hair, such as with PCOS, usually needs 8–10 sessions and occasional maintenance.")],
        "related": ["chemical-peel-lucknow", "hair-prp-treatment-lucknow"],
    },
    {
        "slug": "hair-prp-treatment-lucknow",
        "name": "Hair PRP Treatment",
        "short": "Hair PRP",
        "category": "Skin & hair",
        "book_value": "Hair PRP",
        "title": "Hair PRP Treatment in Lucknow – Cost | Smile & Glow",
        "description": "Hair PRP treatment for hair fall and thinning in Lucknow by Dr. Pallavi. Typical cost ₹3,000–₹6,000 per session, usually 4–6 sessions. Process & FAQs.",
        "image": "about-hair-prp.webp",
        "image_alt": "Hair PRP treatment in progress at Smile & Glow, Lucknow",
        "real_photo": True,
        "intro": ("PRP (platelet-rich plasma) uses platelets from your own blood, concentrated and placed into the scalp to support hair growth in thinning areas. "
                  "Before starting, Dr. Pallavi looks for the cause of your hair fall — including nutrition, thyroid and iron levels — so the plan treats the cause, not just the symptom."),
        "facts": [("Sessions", "4–6, about a month apart"), ("Session time", "About 60 min"), ("Downtime", "Minimal"), ("Typical cost", "₹3,000–₹6,000 per session")],
        "who_title": "Who hair PRP suits",
        "who": ["Early to moderate male or female pattern thinning",
                "Hair fall with a widening parting or visible scalp",
                "People who want to support results from other hair treatments",
                "Not suitable for complete baldness, active scalp infection or certain blood disorders"],
        "steps": [("Hair and scalp assessment", "We examine the scalp and hair pattern, and may suggest blood tests to find the cause of hair fall."),
                  ("Blood sample", "A small amount of blood is drawn, like a routine blood test."),
                  ("Preparing the PRP", "The blood is spun in a centrifuge to concentrate the platelets."),
                  ("Scalp treatment", "After numbing, the PRP is placed into the thinning areas with fine injections or microneedling."),
                  ("Course and maintenance", "Sessions are repeated about monthly, then every few months to maintain results.")],
        "prices": [("Single PRP session", "₹3,000 – ₹6,000"),
                   ("Full course (4–6 sessions)", "₹12,000 – ₹36,000"),
                   ("Maintenance session (every 4–6 months)", "Same as a single session")],
        "price_factors": "The cost depends on the PRP preparation method, the area being treated and the number of sessions in your plan.",
        "aftercare": ["Don't wash your hair for the rest of the day.",
                      "Avoid hair colour, rebonding and other chemical treatments for a few days.",
                      "Skip heavy exercise and sweating on the day of treatment.",
                      "Mild tenderness for a day or two is normal."],
        "faqs": [("How much does hair PRP cost in Lucknow?",
                  "Hair PRP typically costs ₹3,000–₹6,000 per session in Lucknow. Most people need 4–6 sessions, so a full course usually costs ₹12,000–₹36,000, followed by occasional maintenance sessions."),
                 ("Does PRP really work for hair fall?",
                  "Studies show PRP can reduce hair fall and improve hair density in many people with pattern thinning, though results vary. Improvement is usually seen after 3–4 sessions."),
                 ("Is hair PRP painful?",
                  "The scalp is numbed first, so most people feel only mild pricking or pressure. The scalp may feel tender for a day or two."),
                 ("How many PRP sessions do I need?",
                  "Most plans involve 4–6 sessions about a month apart, followed by maintenance every few months. Dr. Pallavi will recommend a plan after your assessment."),
                 ("Who should not have hair PRP?",
                  "PRP isn't advised for people with certain blood or platelet disorders, active scalp infections, or during cancer treatment. Tell us about your medical history and medicines at the consultation.")],
        "related": ["chemical-peel-lucknow", "laser-hair-removal-lucknow"],
    },
    {
        "slug": "chemical-peel-lucknow",
        "name": "Chemical Peel",
        "short": "Chemical peel",
        "category": "Skin & hair",
        "book_value": "Chemical peel",
        "title": "Chemical Peel in Lucknow – Cost per Session | Smile & Glow",
        "description": "Chemical peels in Lucknow for tan, pigmentation, acne and dull skin by Dr. Pallavi. From ₹1,500 per session. Peel types, downtime, aftercare & FAQs.",
        "image": "skin-chemical-peel.webp",
        "image_alt": "Facial skin treatment in a clinic",
        "intro": ("A clinical chemical peel applies a carefully chosen solution that removes the dull outer layer of skin, helping with tan, pigmentation, acne, marks and fine lines. "
                  "The peel type and strength are chosen for your skin, so Indian skin is treated safely."),
        "facts": [("Sessions", "4–6, every 2–3 weeks"), ("Session time", "20–30 min"), ("Downtime", "0–5 days (depends on peel)"), ("Typical cost", "From ₹1,500 per session")],
        "who_title": "What chemical peels can help with",
        "who": ["Tan, uneven skin tone and dullness",
                "Pigmentation and dark spots (melasma needs a gentle, careful plan)",
                "Active acne, acne marks and oily skin",
                "Open pores and fine lines"],
        "steps": [("Skin assessment", "We check your skin type and concerns to choose the right peel and strength."),
                  ("Preparation", "The skin is cleansed and sensitive areas are protected."),
                  ("Peel application", "The peel is applied and timed carefully."),
                  ("Neutralising", "The peel is neutralised or removed at the right moment."),
                  ("Soothing and sun protection", "A calming cream and sunscreen are applied, and you get aftercare instructions.")],
        "prices": [("Glycolic peel — dullness, tan, fine lines", "₹1,500 – ₹3,000"),
                   ("Salicylic peel — acne, oily skin", "₹1,500 – ₹3,500"),
                   ("Lactic peel — dry or sensitive skin", "₹1,500 – ₹3,000"),
                   ("Mandelic peel — pigmentation, sensitive skin", "₹2,000 – ₹4,000"),
                   ("TCA medium peel — marks, deeper pigmentation", "₹4,000 – ₹8,000")],
        "price_factors": "Prices are per session. The cost depends on the peel type and strength, and the number of sessions in your plan.",
        "aftercare": ["Use sunscreen every day and avoid direct sun, especially in the first week.",
                      "Don't pick or peel flaking skin — let it come off naturally.",
                      "Use a gentle cleanser and moisturiser; stop scrubs and retinoids for a few days as advised.",
                      "Avoid waxing, threading or facials on the treated area for a week."],
        "faqs": [("How much does a chemical peel cost in Lucknow?",
                  "A chemical peel typically costs ₹1,500–₹3,500 per session for light peels such as glycolic, salicylic or lactic, ₹2,000–₹4,000 for a mandelic peel and ₹4,000–₹8,000 for a medium-depth TCA peel. Most people need 4–6 sessions."),
                 ("Is there downtime after a chemical peel?",
                  "Light peels usually have little to no downtime — perhaps mild redness or flaking for a few days. Medium peels can cause peeling for about 5 days. You'll get clear aftercare instructions, including sun protection."),
                 ("Are chemical peels safe for Indian skin?",
                  "Yes, when the right peel and strength are chosen for your skin type and you follow sun protection afterwards. Skin that tans easily needs a careful, gradual plan."),
                 ("How many chemical peel sessions do I need?",
                  "Most people need 4–6 sessions, 2–3 weeks apart, for the best results. Some people continue with occasional maintenance peels."),
                 ("When will I see results?",
                  "Skin often looks brighter within a week of the first peel. Pigmentation and acne marks improve gradually over the course of sessions.")],
        "related": ["laser-hair-removal-lucknow", "hair-prp-treatment-lucknow"],
    },
]

BY_SLUG = {t["slug"]: t for t in TREATMENTS}

EXTRA_CSS = """
/* ---------- Treatment pages ---------- */
.crumbs{font-size:var(--t-s);color:var(--muted);padding:20px 0 0}
.crumbs a{color:var(--muted);display:inline-block;padding:8px 4px}
.crumbs a:hover{color:var(--accent-text)}
.crumbs span{margin:0 8px}
.t-hero{padding:16px 0 56px}
.t-hero-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center}
.t-hero .cat{color:var(--accent-text);font-weight:600;margin-bottom:6px}
.t-hero h1{font-size:var(--t-3xl);margin:0 0 16px}
.t-hero .lead{font-size:var(--t-l);color:var(--muted);margin-bottom:24px}
.t-pic{position:relative;margin:0;border-radius:24px;overflow:hidden;aspect-ratio:4/3;background:var(--bg-2)}
.t-pic img{width:100%;height:100%;object-fit:cover;display:block}
.t-pic figcaption{position:absolute;left:12px;bottom:12px;background:var(--surface);color:var(--ink);font-weight:600;font-size:var(--t-xs);padding:6px 12px;border-radius:999px}
.facts{display:grid;grid-template-columns:repeat(4,1fr);gap:16px 28px;margin:32px 0 0}
.fact span{display:block;font-size:var(--t-s);color:var(--muted)}
.fact b{display:block;color:var(--ink);font-size:var(--t-l);font-weight:600;line-height:1.3;margin-top:2px}
.t-sec{padding:56px 0}
.t-sec h2{font-size:var(--t-2xl);margin-bottom:18px}
.t-two{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
.t-card{background:var(--surface);border-radius:var(--radius);padding:28px}
.t-card ul{padding-left:20px;color:var(--muted)}
.t-card li{margin:8px 0}
.t-steps{counter-reset:ts;list-style:none;padding:0;display:grid;gap:18px}
.t-steps li{counter-increment:ts;display:grid;grid-template-columns:40px 1fr;gap:2px 14px}
.t-steps li::before{content:counter(ts);grid-row:span 2;width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:var(--brand-soft);color:var(--brand);font-weight:700}
.t-steps b{display:block;color:var(--ink);font-size:var(--t-l);font-weight:600;line-height:1.3}
.t-steps p{color:var(--muted)}
.price-wrap{overflow-x:auto;border-radius:var(--radius);background:var(--surface)}
.price{width:100%;border-collapse:collapse;min-width:420px}
.price th,.price td{text-align:left;padding:14px 20px}
.price tbody tr + tr td{border-top:1px solid var(--bg-2)}
.price th{background:var(--bg-2);font-size:var(--t-s);font-weight:600;color:var(--muted)}
.price td:last-child{font-weight:600;color:var(--ink);white-space:nowrap}
.price-note{font-size:var(--t-s);color:var(--muted);margin-top:12px}
.doc-box{display:flex;gap:18px;align-items:center;background:var(--surface);border-radius:var(--radius);padding:22px 24px}
.doc-box img{width:84px;height:84px;border-radius:50%;object-fit:cover;flex-shrink:0}
.doc-box p{color:var(--muted)}
.doc-box b{color:var(--ink)}
.t-branches{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start}
.t-branch{background:var(--surface);border-radius:var(--radius);overflow:hidden}
.t-branch img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}
.t-branch div{padding:20px 24px 24px}
.t-branch h3{font-size:var(--t-xl);margin-bottom:6px}
.t-branch p{color:var(--muted);margin:4px 0}
.t-branch a{display:inline-block;padding:8px 0}
.related{display:flex;flex-wrap:wrap;gap:10px}
.related a{display:inline-flex;align-items:center;min-height:44px;background:var(--surface);color:var(--brand);padding:0 20px;border-radius:999px;text-decoration:none;font-weight:600}
.related a:hover{color:var(--accent-text)}
.t-updated{font-size:var(--t-s);color:var(--muted);margin-top:18px}
@media (max-width:900px){.t-hero-grid,.t-two,.t-branches{grid-template-columns:1fr}.t-hero .lead{font-size:var(--t-m)}.facts{grid-template-columns:1fr 1fr}.t-pic{aspect-ratio:16/10}}
@media (max-width:340px){.facts{grid-template-columns:1fr}}
"""


def e(s):
    """Escape plain text for HTML (content strings may already contain &amp;)."""
    return html.escape(s, quote=False).replace("&amp;amp;", "&amp;")


def wa_link(treatment):
    msg = f"Hi Smile & Glow Clinic, I'd like to book an appointment for {treatment}."
    from urllib.parse import quote
    return f"https://wa.me/{WHATSAPP}?text={quote(msg)}"


def extract(src):
    """Pull the shared pieces out of the homepage so every page stays in sync."""
    css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
    fonts = re.search(r'<!-- FONTS -->(.*?)<!-- /FONTS -->', src, re.S).group(1)
    sprite = re.search(r'(<svg width="0" height="0" style="position:absolute" aria-hidden="true">.*?</svg>)', src, re.S)
    header = re.search(r"(<header>.*?</header>)", src, re.S).group(1)
    footer = re.search(r"(<footer>.*?</footer>)", src, re.S).group(1)
    wa_btn = re.search(r'<!-- FLOAT -->(.*?)<!-- /FLOAT -->', src, re.S).group(1)
    # make in-page links point back to the homepage sections
    header = re.sub(r'href="#', 'href="/#', header)
    footer = re.sub(r'href="#', 'href="/#', footer)
    footer = footer.replace(' aria-current="page"', "")
    return {"css": css, "fonts": fonts, "sprite": sprite.group(1) if sprite else "", "header": header,
            "footer": footer, "wa_btn": wa_btn}


def schema(t, page_url):
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Treatments", "item": f"{SITE}/#services"},
            {"@type": "ListItem", "position": 3, "name": f"{t['name']} in Lucknow", "item": page_url}]},
        {"@type": ["WebPage", "MedicalWebPage"], "@id": f"{page_url}#webpage", "url": page_url, "name": t["title"],
         "description": t["description"], "inLanguage": "en", "isPartOf": {"@id": f"{SITE}/#website"},
         "about": {"@id": f"{page_url}#procedure"}, "dateModified": UPDATED_ISO,
         "primaryImageOfPage": f"{SITE}/assets/img/{t['image']}"},
        {"@type": "MedicalProcedure", "@id": f"{page_url}#procedure", "name": t["name"],
         "description": re.sub(r"<[^>]+>", "", t["intro"]).replace("&amp;", "&"),
         "howPerformed": " ".join(f"{a}: {b}" for a, b in t["steps"]),
         "followup": " ".join(t["aftercare"]),
         "image": f"{SITE}/assets/img/{t['image']}",
         "url": page_url,
         "availableAt": [{"@id": f"{SITE}/#it-chauraha"}, {"@id": f"{SITE}/#aashiyana"}]},
        {"@type": "FAQPage", "@id": f"{page_url}#faq", "inLanguage": "en",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                        for q, a in t["faqs"]]},
    ]}


def page(t, parts):
    url = f"{SITE}/{t['slug']}/"
    facts = "".join(f'<div class="fact"><span>{e(k)}</span><b>{e(v)}</b></div>' for k, v in t["facts"])
    who = "".join(f"<li>{e(x)}</li>" for x in t["who"])
    steps = "".join(f"<li><b>{e(a)}</b><p>{e(b)}</p></li>" for a, b in t["steps"])
    rows = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in t["prices"])
    care = "".join(f"<li>{e(x)}</li>" for x in t["aftercare"])
    faqs = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in t["faqs"])
    rel = "".join(f'<a href="/{s}/">{e(BY_SLUG[s]["name"])} in Lucknow</a>' for s in t["related"])
    real = '<figcaption>At our clinic</figcaption>' if t.get("real_photo") else ""
    from PIL import Image
    w, h = Image.open(Path(__file__).resolve().parent.parent / "assets" / "img" / t["image"]).size
    wa = wa_link(t["name"].lower())
    ld = json.dumps(schema(t, url), ensure_ascii=False, separators=(",", ":"))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t['title'])}</title>
<meta name="description" content="{html.escape(t['description'])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#1b5c8c">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/img/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Smile &amp; Glow">
<meta property="og:title" content="{html.escape(t['title'])}">
<meta property="og:description" content="{html.escape(t['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/{t['image']}">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
{parts['fonts']}
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{parts['sprite']}
{parts['header']}

<main id="top">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>›</span><a href="/#services">Treatments</a><span>›</span>{e(t['name'])}</nav>
  </div>

  <section class="t-hero">
    <div class="wrap t-hero-grid">
      <div>
        <p class="cat">{e(t['category'])} · Smile &amp; Glow, Lucknow</p>
        <h1>{e(t['name'])} in Lucknow</h1>
        <p class="lead">{t['intro']}</p>
        <div class="cta-row">
          <a class="btn rose" href="{wa}" target="_blank" rel="noopener">Book on WhatsApp</a>
          <a class="btn ghost" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
        </div>
      </div>
      <figure class="t-pic"><img src="/assets/img/{t['image']}" width="{w}" height="{h}" alt="{html.escape(t['image_alt'])}" fetchpriority="high">{real}</figure>
    </div>
    <div class="wrap"><div class="facts">{facts}</div></div>
  </section>

  <section class="t-sec" style="padding-top:10px">
    <div class="wrap t-two">
      <div class="t-card"><h2>{e(t['who_title'])}</h2><ul>{who}</ul></div>
      <div><h2>How it's done at Smile &amp; Glow</h2><ol class="t-steps">{steps}</ol></div>
    </div>
  </section>

  <section class="t-sec" id="cost">
    <div class="wrap">
      <h2>{e(t['name'])} cost in Lucknow</h2>
      <div class="price-wrap"><table class="price"><thead><tr><th>Treatment</th><th>Typical cost</th></tr></thead><tbody>{rows}</tbody></table></div>
      <p class="price-note">{e(t['price_factors'])} {e(PRICE_NOTE)}</p>
    </div>
  </section>

  <section class="t-sec">
    <div class="wrap t-two">
      <div class="t-card"><h2>Aftercare</h2><ul>{care}</ul></div>
      <div>
        <h2>Your doctor</h2>
        <div class="doc-box"><img src="/assets/img/doctor-thumb.webp" width="84" height="84" alt="Dr. Pallavi at Smile &amp; Glow" loading="lazy">
          <p><b>Dr. Pallavi</b> — BDS, MDS (Maxillofacial Medicine &amp; Radiology), FMC (Fellow in Cosmetology), PG Diploma in Nutrition.<br>Dental Registration No. {REG_NO}</p></div>
        <p class="t-updated">Consultations in Hindi and English. Treatment results vary from person to person.</p>
      </div>
    </div>
  </section>

  <section class="t-sec" id="faq">
    <div class="wrap">
      <h2>{e(t['name'])} — frequently asked questions</h2>
      <div class="faq">{faqs}</div>
    </div>
  </section>

  <section class="t-sec" id="branches">
    <div class="wrap">
      <h2>Book at our Lucknow clinics</h2>
      <div class="t-branches">
        <div class="t-branch"><img src="/assets/img/gallery-sign.webp" width="800" height="600" loading="lazy" alt="Smile &amp; Glow signboard"><div><h3>I.T Chauraha</h3><p>Gate No. 4, 1/2 Shivsthali, Faizabad Rd, opp. IT Girls College, Hasanganj, Lucknow 226007</p><p>Mon–Sat 11:00 AM – 3:00 PM · Sunday by appointment</p><p><a class="link" href="https://maps.google.com/?cid=17579297340809890606" target="_blank" rel="noopener">Get directions</a></p></div></div>
        <div class="t-branch"><img src="/assets/img/gallery-building.webp" width="800" height="600" loading="lazy" alt="Smile &amp; Glow Aashiyana clinic building"><div><h3>Aashiyana</h3><p>SS-771, behind Aastha Hospital, Sector H, LDA Colony, Lucknow 226012</p><p>Mon–Sat 4:00 PM – 9:00 PM · Sunday by appointment</p><p><a class="link" href="https://maps.google.com/?cid=7330207607150827761" target="_blank" rel="noopener">Get directions</a></p></div></div>
      </div>
      <div class="cta-row" style="margin-top:22px">
        <a class="btn rose" href="{wa}" target="_blank" rel="noopener">Book {e(t['short'])} on WhatsApp</a>
        <a class="btn ghost" href="/#contact">See all booking options</a>
      </div>
      <h2 style="margin-top:44px">Related treatments</h2>
      <div class="related">{rel}<a href="/#services">All treatments</a></div>
      <p class="t-updated">Last updated {UPDATED}.</p>
    </div>
  </section>
</main>

{parts['footer']}

{parts['wa_btn']}

<script>
  const yr = document.getElementById('yr'); if (yr) yr.textContent = new Date().getFullYear();
  document.querySelectorAll('.js-wa').forEach(a => a.href = {json.dumps(wa)});
  const menuBtn = document.querySelector('.menu-btn'), links = document.getElementById('links');
  if (menuBtn) menuBtn.addEventListener('click', () => {{ const o = links.classList.toggle('open'); menuBtn.setAttribute('aria-expanded', o); }});
  document.querySelectorAll('#links a').forEach(a => a.addEventListener('click', () => links.classList.remove('open')));
</script>
</body>
</html>
"""


def build_treatments(root: Path, src: str):
    parts = extract(src)
    (root / "assets" / "site.css").write_text(parts["css"].strip() + "\n" + EXTRA_CSS, encoding="utf-8")
    for t in TREATMENTS:
        out = root / t["slug"] / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(page(t, parts), encoding="utf-8")
    return [t["slug"] for t in TREATMENTS]
