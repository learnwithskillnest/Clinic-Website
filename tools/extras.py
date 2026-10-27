"""Patient tools and guides built alongside the treatment pages.

  /cost-calculator/      + /hi/cost-calculator/   treatment cost estimator (prices from treatments.py)
  /skin-quiz/            + /hi/skin-quiz/         skin-type quiz with a basic routine
  /treatment-guide/                               "which treatment is right for me?" comparisons
  /hi/samjhiye/                                   plain-Hindi explainers
  /aftercare/                                     aftercare cards in English + Hindi, shareable on WhatsApp

Run through tools/build.py.
"""
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

from treatments import TREATMENTS, BY_SLUG, SITE, PHONE_DISPLAY, PHONE_TEL, WHATSAPP, extract

UPDATED_ISO = "2026-10-26"


def e(s):
    return html.escape(s, quote=False)


def wa(msg):
    return f"https://wa.me/{WHATSAPP}?text={quote(msg)}"


# ---------------------------------------------------------------- Hindi copy of data kept in treatments.py
NAME_HI = {
    "root-canal-treatment-lucknow": "रूट कैनाल ट्रीटमेंट",
    "dental-implants-lucknow": "डेंटल इम्प्लांट",
    "teeth-whitening-lucknow": "दांतों की सफ़ेदी",
    "laser-hair-removal-lucknow": "लेज़र हेयर रिडक्शन",
    "hair-prp-treatment-lucknow": "हेयर PRP",
    "chemical-peel-lucknow": "केमिकल पील",
}
ROW_HI = {
    "Front tooth (1 canal)": "आगे का दांत (1 कैनाल)",
    "Premolar (1–2 canals)": "प्रीमोलर (1–2 कैनाल)",
    "Molar (3–4 canals)": "दाढ़ (3–4 कैनाल)",
    "Re-treatment of an old root canal": "पुराने रूट कैनाल का दोबारा इलाज",
    "Crown after RCT (metal, ceramic or zirconia)": "RCT के बाद क्राउन (मेटल, सेरामिक या ज़िरकोनिया)",
    "Single implant (standard system)": "एक इम्प्लांट (स्टैंडर्ड सिस्टम)",
    "Single implant (premium imported system)": "एक इम्प्लांट (प्रीमियम इम्पोर्टेड सिस्टम)",
    "Bone grafting (only if needed)": "बोन ग्राफ़्टिंग (ज़रूरत हो तो ही)",
    "Sinus lift (only if needed, upper back teeth)": "साइनस लिफ़्ट (ज़रूरत हो तो ही, ऊपर के पिछले दांत)",
    "In-clinic professional whitening (one session)": "क्लिनिक में प्रोफ़ेशनल व्हाइटनिंग (एक सेशन)",
    "Laser / light-activated whitening": "लेज़र / लाइट व्हाइटनिंग",
    "Upper lip or chin": "ऊपरी होंठ या ठोड़ी",
    "Full face": "पूरा चेहरा",
    "Underarms": "अंडरआर्म्स",
    "Full arms": "पूरी बाहें",
    "Full legs": "पूरे पैर",
    "Single PRP session": "एक PRP सेशन",
    "Full course (4–6 sessions)": "पूरा कोर्स (4–6 सेशन)",
    "Glycolic peel — dullness, tan, fine lines": "ग्लाइकोलिक पील — रूखापन, टैन, बारीक रेखाएँ",
    "Salicylic peel — acne, oily skin": "सैलिसिलिक पील — मुंहासे, ऑयली त्वचा",
    "Lactic peel — dry or sensitive skin": "लैक्टिक पील — रूखी या संवेदनशील त्वचा",
    "Mandelic peel — pigmentation, sensitive skin": "मैंडेलिक पील — पिगमेंटेशन, संवेदनशील त्वचा",
    "TCA medium peel — marks, deeper pigmentation": "TCA मीडियम पील — दाग, गहरा पिगमेंटेशन",
}
AFTERCARE_HI = {
    "root-canal-treatment-lucknow": [
        "सुन्नपन खत्म होने और फ़ाइनल फ़िलिंग या क्राउन लगने तक उस तरफ़ से न चबाएँ।",
        "2–3 दिन हल्का दर्द सामान्य है; दर्द की दवा सिर्फ़ बताए अनुसार लें।",
        "क्राउन समय पर लगवाएँ — बिना क्राउन के इलाज किया हुआ दांत टूट सकता है।",
        "दिन में दो बार ब्रश करते रहें और रिव्यू विज़िट पर ज़रूर आएँ।",
    ],
    "dental-implants-lucknow": [
        "पहले कुछ दिन नरम खाना खाएँ और दूसरी तरफ़ से चबाएँ।",
        "धूम्रपान न करें — इससे घाव देर से भरता है और इम्प्लांट फ़ेल होने का खतरा बढ़ता है।",
        "उस जगह के आसपास हल्के से ब्रश करें और बताया गया माउथवॉश इस्तेमाल करें।",
        "नियमित जांच और सफ़ाई के लिए आएँ ताकि इम्प्लांट के आसपास के मसूड़े स्वस्थ रहें।",
    ],
    "teeth-whitening-lucknow": [
        "48 घंटे तक चाय, कॉफ़ी, कोला, ज़्यादा हल्दी वाली सब्ज़ी और धूम्रपान से बचें।",
        "एक-दो दिन हल्की झनझनाहट सामान्य है; सेंसिटिविटी टूथपेस्ट मदद करता है।",
        "दिन में दो बार ब्रश करें और हर 6 महीने में सफ़ाई करवाएँ ताकि असर लंबे समय तक रहे।",
    ],
    "laser-hair-removal-lucknow": [
        "एक हफ़्ते तक सीधी धूप से बचें और ट्रीटमेंट वाली जगह पर सनस्क्रीन लगाएँ।",
        "कुछ घंटे हल्की लालिमा रह सकती है — ठंडी सिकाई मदद करती है।",
        "सेशन के बीच ज़रूरत हो तो शेव करें, लेकिन वैक्सिंग, थ्रेडिंग या प्लकिंग न करें।",
        "24 घंटे तक गर्म पानी से नहाना, सॉना और जिम में पसीना बहाने से बचें।",
    ],
    "hair-prp-treatment-lucknow": [
        "उस दिन बाल न धोएँ।",
        "कुछ दिन तक हेयर कलर, रीबॉन्डिंग और दूसरे केमिकल ट्रीटमेंट से बचें।",
        "ट्रीटमेंट वाले दिन भारी कसरत और पसीने से बचें।",
        "एक-दो दिन हल्का दर्द या कोमलता सामान्य है।",
    ],
    "chemical-peel-lucknow": [
        "रोज़ सनस्क्रीन लगाएँ और सीधी धूप से बचें, ख़ासकर पहले हफ़्ते।",
        "उतरती त्वचा को न खींचें — उसे अपने आप उतरने दें।",
        "हल्का क्लेंज़र और मॉइस्चराइज़र इस्तेमाल करें; बताए अनुसार कुछ दिन स्क्रब और रेटिनॉइड बंद रखें।",
        "एक हफ़्ते तक उस जगह पर वैक्सिंग, थ्रेडिंग या फ़ेशियल न करवाएँ।",
    ],
}

# ---------------------------------------------------------------- cost calculator config
# unit = what the quantity counts; addons = row indexes shown as tick boxes; fixed = rows that are a whole package
CALC = {
    "root-canal-treatment-lucknow": {"unit": ("Number of teeth", "दांतों की संख्या"), "q": (1, 1, 8), "addons": [4], "fixed": []},
    "dental-implants-lucknow": {"unit": ("Number of implants", "इम्प्लांट की संख्या"), "q": (1, 1, 8), "addons": [2, 3], "fixed": []},
    "teeth-whitening-lucknow": {"unit": ("Sessions", "सेशन"), "q": (1, 1, 3), "addons": [], "fixed": []},
    "laser-hair-removal-lucknow": {"unit": ("Sessions", "सेशन"), "q": (6, 1, 10), "addons": [], "fixed": [],
                                   "tip": ("Most people need 6–8 sessions, 4–6 weeks apart.", "ज़्यादातर लोगों को 4–6 हफ़्ते के अंतर पर 6–8 सेशन लगते हैं।")},
    "hair-prp-treatment-lucknow": {"unit": ("Sessions", "सेशन"), "q": (4, 1, 8), "addons": [], "fixed": [1],
                                   "tip": ("A course is usually 4–6 sessions, about a month apart.", "कोर्स आमतौर पर महीने भर के अंतर पर 4–6 सेशन का होता है।")},
    "chemical-peel-lucknow": {"unit": ("Sessions", "सेशन"), "q": (4, 1, 8), "addons": [], "fixed": [],
                              "tip": ("Most peel plans are 4–6 sessions, every 2–3 weeks.", "ज़्यादातर पील प्लान हर 2–3 हफ़्ते पर 4–6 सेशन के होते हैं।")},
}
CALC_TIP_ADDON = {
    "root-canal-treatment-lucknow": ("Back teeth usually need a crown after a root canal.", "पिछले दांतों में रूट कैनाल के बाद आमतौर पर क्राउन लगता है।"),
    "dental-implants-lucknow": ("Bone grafting or a sinus lift is needed only in some cases — your X-ray will show.", "बोन ग्राफ़्टिंग या साइनस लिफ़्ट कुछ ही मामलों में चाहिए — एक्स-रे से पता चलेगा।"),
}


def rng(text):
    nums = [int(x.replace(",", "")) for x in re.findall(r"₹([\d,]+)", text)]
    return (nums[0], nums[-1]) if nums else None


def calc_data():
    out = []
    for t in TREATMENTS:
        c = CALC[t["slug"]]
        opts, adds = [], []
        for i, (label, price) in enumerate(t["prices"]):
            r = rng(price)
            if not r:
                continue
            item = {"en": label, "hi": ROW_HI.get(label, label), "lo": r[0], "hi_": r[1], "fixed": i in c["fixed"]}
            (adds if i in c["addons"] else opts).append(item)
        out.append({"slug": t["slug"], "en": t["name"], "hi": NAME_HI[t["slug"]], "unit": c["unit"], "q": c["q"],
                    "opts": opts, "adds": adds, "tip": c.get("tip"), "addTip": CALC_TIP_ADDON.get(t["slug"])})
    return out


# ---------------------------------------------------------------- shared page shell
EXTRA_CSS = """
/* ---------- Patient tools ---------- */
.tool [hidden]{display:none!important}
.tool{padding:8px 0 64px}
.tool h1{font-size:var(--t-3xl);margin:6px 0 12px}
.tool .lead{font-size:var(--t-l);color:var(--muted);margin-bottom:28px}
.tool-box{background:var(--surface);border-radius:var(--radius);padding:28px;max-width:760px}
.tool-box h2{font-size:var(--t-xl);margin-bottom:14px}
.field{display:grid;gap:6px;margin-bottom:18px}
.field > span{font-weight:600;color:var(--ink)}
.opts{display:grid;gap:10px}
.opt{display:flex;gap:12px;align-items:flex-start;padding:14px 16px;border-radius:12px;background:var(--bg);cursor:pointer;border:2px solid transparent;font-weight:500;color:var(--ink)}
.opt:has(input:checked){border-color:var(--brand)}
.opt input{width:20px;height:20px;min-height:0;margin:2px 0 0;flex-shrink:0;accent-color:var(--brand)}
.opt small{display:block;color:var(--muted);font-weight:400}
.stepper{display:inline-flex;align-items:center;gap:6px}
.stepper button{width:48px;height:48px;border-radius:50%;border:0;background:var(--brand-soft);color:var(--brand);font-size:1.5rem;cursor:pointer;font-family:inherit}
.stepper output{min-width:48px;text-align:center;font-size:var(--t-l);font-weight:700}
.result{margin-top:24px;padding:22px 24px;border-radius:var(--radius);background:var(--brand-soft)}
.result .big{font-family:"Playfair Display","Mukta",serif;font-size:var(--t-2xl);color:var(--brand);line-height:1.2;margin:4px 0 8px}
:lang(hi) .result .big{font-family:"Mukta",sans-serif;font-weight:700}
.result ul{margin:8px 0 0 20px;color:var(--muted)}
.result .cta-row{margin-top:18px}
.fine{font-size:var(--t-s);color:var(--muted);margin-top:16px}
.q-prog{font-size:var(--t-s);color:var(--muted);margin-bottom:6px}
.q-bar{height:6px;border-radius:6px;background:var(--bg-2);margin-bottom:22px;overflow:hidden}
.q-bar i{display:block;height:100%;background:var(--brand);transition:width .2s}
.q-nav{display:flex;gap:12px;flex-wrap:wrap;margin-top:20px}
.routine{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:14px}
.routine div{background:var(--surface);border-radius:12px;padding:16px 18px}
.routine h3{font-size:var(--t-l);margin-bottom:6px}
.routine ol{margin-left:20px;color:var(--muted)}
.guide-list{display:grid;gap:28px;max-width:900px}
.guide-list > *,.care-grid > *,.explain > *{min-width:0}
.guide{background:var(--surface);border-radius:var(--radius);padding:26px 28px}
.guide h2{font-size:var(--t-xl);margin-bottom:8px}
.guide > p{color:var(--muted);margin-bottom:14px}
.cmp{width:100%;min-width:560px;border-collapse:collapse;margin:6px 0 14px;font-size:var(--t-s)}
.cmp-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.swipe{display:none;font-size:var(--t-s);color:var(--muted);margin-bottom:4px}
@media (max-width:640px){.swipe{display:block}}
.cmp th,.cmp td{text-align:left;padding:10px 12px;vertical-align:top}
.cmp thead th{background:var(--bg-2);color:var(--ink);font-weight:600}
.cmp tbody tr + tr td,.cmp tbody tr + tr th{border-top:1px solid var(--bg-2)}
.cmp tbody th{font-weight:600;color:var(--ink);white-space:nowrap}
.cmp td{color:var(--muted)}
.choose{list-style:none;display:grid;gap:8px;margin-bottom:12px}
.choose li{padding-left:16px;border-left:3px solid var(--brand-soft);color:var(--muted)}
.choose b{color:var(--ink)}
.toc{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 28px}
.toc a{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border-radius:999px;background:var(--surface);color:var(--brand);font-weight:600;text-decoration:none}
.care-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.care{background:var(--surface);border-radius:var(--radius);padding:24px 26px;scroll-margin-top:96px}
.care h2{font-size:var(--t-xl);margin-bottom:12px}
.care h3{font-size:var(--t-s);color:var(--muted);font-family:"Mukta",sans-serif;font-weight:600;margin:14px 0 4px}
.care ul{margin-left:20px}
.care li{margin:4px 0}
.care .cta-row{margin-top:16px}
.care .btn{min-height:44px;padding:8px 18px}
.explain{display:grid;gap:22px;max-width:820px}
.explain article{background:var(--surface);border-radius:var(--radius);padding:24px 26px}
.explain h2{font-size:var(--t-xl);margin-bottom:8px}
.explain p{color:var(--muted)}
.explain p + p{margin-top:8px}
@media (max-width:900px){.care-grid,.routine{grid-template-columns:1fr}}
@media (max-width:520px){.tool-box,.guide,.care{padding:22px 18px}}
@media print{header,footer,.mbar,.wa,.sgc-launch,.toc,.care .cta-row{display:none!important}.care{break-inside:avoid}}
"""


def hi_parts(hi_src):
    p = extract(hi_src)
    p["header"] = p["header"].replace('href="/#', 'href="/hi/#')
    p["footer"] = p["footer"].replace('href="/#', 'href="/hi/#')
    return p


def shell(parts, *, lang, path, title, desc, body, alt=None, ld=None, script="", crumbs=None):
    url = f"{SITE}{path}"
    footer = parts["footer"]
    if alt:  # point the language switch at the matching page
        footer = footer.replace('href="/" hreflang="en"', f'href="{alt["en"]}" hreflang="en"').replace(
            'href="/hi/" hreflang="hi"', f'href="{alt["hi"]}" hreflang="hi"')
    cur = 'hreflang="hi"' if lang == "hi" else 'hreflang="en"'
    footer = footer.replace(cur, cur + ' aria-current="page"', 1)
    alts = ""
    if alt:
        alts = (f'<link rel="alternate" hreflang="en" href="{SITE}{alt["en"]}">\n'
                f'<link rel="alternate" hreflang="hi" href="{SITE}{alt["hi"]}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{SITE}{alt["en"]}">\n')
    home = "/hi/" if lang == "hi" else "/"
    crumb_html = ""
    if crumbs:
        crumb_html = ('<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="' + home + '">'
                      + ("होम" if lang == "hi" else "Home") + "</a><span>›</span>" + e(crumbs) + "</nav></div>")
        bl = {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}{home}"},
            {"@type": "ListItem", "position": 2, "name": crumbs, "item": url}]}
        graph = [bl, {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": title, "description": desc,
                      "inLanguage": lang, "isPartOf": {"@id": f"{SITE}/#website"}, "dateModified": UPDATED_ISO,
                      "publisher": {"@id": f"{SITE}/#org"}}] + (ld or [])
        ld_html = '<script type="application/ld+json">' + json.dumps(
            {"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")) + "</script>"
    else:
        ld_html = ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
{alts}<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#1b5c8c">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/img/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Smile &amp; Glow">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/gallery-sign.webp">
<meta property="og:locale" content="{'hi_IN' if lang == 'hi' else 'en_IN'}">
{parts['fonts']}
<link rel="stylesheet" href="/assets/site.css?v=3">
{ld_html}
</head>
<body>
{parts['header']}

<main id="top">
{crumb_html}
{body}
</main>

{footer}

{parts['wa_btn']}

<script>
  const yr = document.getElementById('yr'); if (yr) yr.textContent = new Date().getFullYear();
  document.querySelectorAll('.js-wa').forEach(a => a.href = "https://wa.me/{WHATSAPP}?text=" + encodeURIComponent("Hi Smile & Glow Clinic, I'd like to book an appointment."));
  const menuBtn = document.querySelector('.menu-btn'), links = document.getElementById('links');
  if (menuBtn) menuBtn.addEventListener('click', () => {{ const o = links.classList.toggle('open'); menuBtn.setAttribute('aria-expanded', o); }});
  document.querySelectorAll('#links a').forEach(a => a.addEventListener('click', () => links.classList.remove('open')));
</script>
{script}
</body>
</html>
"""


# ---------------------------------------------------------------- 1) cost calculator
CALC_T = {
    "en": {"title": "Dental & Skin Treatment Cost Calculator, Lucknow | Smile & Glow",
           "desc": "Estimate the cost of root canal, implants, teeth whitening, laser hair reduction, hair PRP and chemical peels at Smile & Glow, Lucknow — in seconds.",
           "crumb": "Cost calculator", "h1": "Treatment cost calculator",
           "lead": "Pick a treatment and get a price range in seconds — the same prices we publish on our treatment pages.",
           "pick": "1. Choose a treatment", "opt": "2. Choose an option", "qty": "3. How many?", "add": "Optional extras",
           "est": "Estimated cost", "send": "Send this estimate on WhatsApp", "details": "Full price details",
           "fine": "Typical costs at Smile & Glow, October 2026. Your exact cost is confirmed after the check-up and explained before treatment starts. Consultation charges, X-rays and medicines may be extra.",
           "minus": "Fewer", "plus": "More", "fixedNote": "Package price", "msg": "Hi Smile & Glow Clinic, I used the cost calculator:"},
    "hi": {"title": "इलाज की कीमत का कैलकुलेटर, लखनऊ | स्माइल एंड ग्लो",
           "desc": "स्माइल एंड ग्लो, लखनऊ में रूट कैनाल, इम्प्लांट, दांतों की सफ़ेदी, लेज़र हेयर रिडक्शन, हेयर PRP और केमिकल पील की कीमत तुरंत जानें।",
           "crumb": "कीमत कैलकुलेटर", "h1": "इलाज की कीमत का कैलकुलेटर",
           "lead": "ट्रीटमेंट चुनें और तुरंत अनुमानित कीमत देखें — वही कीमतें जो हमारे ट्रीटमेंट पेज पर लिखी हैं।",
           "pick": "1. ट्रीटमेंट चुनें", "opt": "2. विकल्प चुनें", "qty": "3. कितने?", "add": "अतिरिक्त (ज़रूरत हो तो)",
           "est": "अनुमानित कीमत", "send": "यह अनुमान WhatsApp पर भेजें", "details": "पूरी कीमत और जानकारी (अंग्रेज़ी)",
           "fine": "स्माइल एंड ग्लो की सामान्य कीमतें, अक्टूबर 2026। सही कीमत जांच के बाद पक्की होती है और इलाज शुरू होने से पहले बताई जाती है। परामर्श फ़ीस, एक्स-रे और दवाइयाँ अलग हो सकती हैं।",
           "minus": "कम करें", "plus": "बढ़ाएँ", "fixedNote": "पैकेज कीमत", "msg": "नमस्ते Smile & Glow, मैंने कीमत कैलकुलेटर इस्तेमाल किया:"},
}

CALC_JS = r"""<script>
(function(){
  const D = __DATA__, T = __T__, L = document.documentElement.lang === 'hi' ? 'hi' : 'en';
  const nm = o => L === 'hi' ? o.hi : o.en;
  const inr = n => '₹' + n.toLocaleString('en-IN');
  const $ = s => document.querySelector(s);
  const pick = $('#c-treat'), optBox = $('#c-opts'), addBox = $('#c-adds'), addWrap = $('#c-addwrap'),
        qtyWrap = $('#c-qtywrap'), qtyOut = $('#c-qty'), qtyLabel = $('#c-qtylabel'), tip = $('#c-tip'),
        out = $('#c-out'), list = $('#c-list'), sendBtn = $('#c-send'), more = $('#c-more');
  let t, qty = 1;
  D.forEach((d, i) => { const o = document.createElement('option'); o.value = i; o.textContent = nm(d); pick.appendChild(o); });
  const start = D.findIndex(d => location.hash === '#' + d.slug); if (start > -1) pick.value = start;
  function radio(name, item, i, checked, type) {
    const l = document.createElement('label'); l.className = 'opt';
    l.innerHTML = '<input type="' + type + '" name="' + name + '" value="' + i + '"' + (checked ? ' checked' : '') + '><span>' +
      nm(item) + '<small>' + inr(item.lo) + ' – ' + inr(item.hi_) + (item.fixed ? ' · ' + T.fixedNote : '') + '</small></span>';
    return l;
  }
  function load() {
    t = D[+pick.value]; qty = t.q[0];
    optBox.innerHTML = ''; t.opts.forEach((o, i) => optBox.appendChild(radio('c-opt', o, i, i === 0, 'radio')));
    addBox.innerHTML = ''; t.adds.forEach((o, i) => addBox.appendChild(radio('c-add', o, i, false, 'checkbox')));
    addWrap.hidden = !t.adds.length;
    qtyLabel.textContent = t.unit[L === 'hi' ? 1 : 0];
    tip.textContent = [t.tip && t.tip[L === 'hi' ? 1 : 0], t.addTip && t.addTip[L === 'hi' ? 1 : 0]].filter(Boolean).join(' ');
    tip.hidden = !tip.textContent;
    more.href = '/' + t.slug + '/#cost';
    calc();
  }
  function calc() {
    const o = t.opts[+(document.querySelector('input[name=c-opt]:checked') || {value: 0}).value];
    qtyWrap.hidden = o.fixed;
    const n = o.fixed ? 1 : qty; qtyOut.textContent = qty;
    let lo = o.lo * n, hi = o.hi_ * n;
    const lines = [nm(o) + (o.fixed ? '' : ' × ' + n) + ': ' + inr(o.lo * n) + ' – ' + inr(o.hi_ * n)];
    document.querySelectorAll('input[name=c-add]:checked').forEach(c => {
      const a = t.adds[+c.value]; lo += a.lo * n; hi += a.hi_ * n;
      lines.push(nm(a) + ' × ' + n + ': ' + inr(a.lo * n) + ' – ' + inr(a.hi_ * n));
    });
    out.textContent = inr(lo) + ' – ' + inr(hi);
    list.innerHTML = ''; lines.forEach(s => { const li = document.createElement('li'); li.textContent = s; list.appendChild(li); });
    const msg = T.msg + '\n' + nm(t) + '\n' + lines.join('\n') + '\n' + T.est + ': ' + inr(lo) + ' – ' + inr(hi);
    sendBtn.href = 'https://wa.me/__WA__?text=' + encodeURIComponent(msg);
  }
  pick.addEventListener('change', load);
  document.addEventListener('change', e => { if (e.target.name === 'c-opt' || e.target.name === 'c-add') calc(); });
  $('#c-minus').addEventListener('click', () => { qty = Math.max(t.q[1], qty - 1); calc(); });
  $('#c-plus').addEventListener('click', () => { qty = Math.min(t.q[2], qty + 1); calc(); });
  load();
})();
</script>"""


def calc_page(parts, lang):
    T = CALC_T[lang]
    body = f"""<section class="tool">
  <div class="wrap">
    <h1>{e(T['h1'])}</h1>
    <p class="lead">{e(T['lead'])}</p>
    <div class="tool-box">
      <label class="field"><span>{e(T['pick'])}</span><select id="c-treat"></select></label>
      <fieldset class="field" style="border:0"><legend style="font-weight:600;margin-bottom:6px">{e(T['opt'])}</legend><div class="opts" id="c-opts"></div></fieldset>
      <fieldset class="field" id="c-addwrap" style="border:0"><legend style="font-weight:600;margin-bottom:6px">{e(T['add'])}</legend><div class="opts" id="c-adds"></div></fieldset>
      <div class="field" id="c-qtywrap"><span id="c-qtylabel"></span>
        <div class="stepper"><button type="button" id="c-minus" aria-label="{e(T['minus'])}">−</button><output id="c-qty" aria-live="polite">1</output><button type="button" id="c-plus" aria-label="{e(T['plus'])}">+</button></div>
      </div>
      <p class="fine" id="c-tip"></p>
      <div class="result" aria-live="polite">
        <span>{e(T['est'])}</span>
        <div class="big" id="c-out"></div>
        <ul id="c-list"></ul>
        <div class="cta-row"><a class="btn rose" id="c-send" href="#" target="_blank" rel="noopener">{e(T['send'])}</a><a class="link" id="c-more" href="#">{e(T['details'])}</a></div>
      </div>
      <p class="fine">{e(T['fine'])}</p>
    </div>
  </div>
</section>"""
    js = (CALC_JS.replace("__DATA__", json.dumps(calc_data(), ensure_ascii=False))
          .replace("__T__", json.dumps(T, ensure_ascii=False)).replace("__WA__", WHATSAPP))
    path = "/hi/cost-calculator/" if lang == "hi" else "/cost-calculator/"
    return path, shell(parts, lang=lang, path=path, title=T["title"], desc=T["desc"], body=body, script=js,
                       crumbs=T["crumb"], alt={"en": "/cost-calculator/", "hi": "/hi/cost-calculator/"})


# ---------------------------------------------------------------- 2) skin quiz
QUIZ = {
    "en": {
        "title": "Skin Type Quiz — Find Your Skin Type in 1 Minute | Smile & Glow Lucknow",
        "desc": "Free 6-question skin type quiz by Smile & Glow, Lucknow. Find out if your skin is oily, dry, combination, normal or sensitive, and get a simple routine.",
        "crumb": "Skin type quiz", "h1": "What's your skin type?",
        "lead": "Six quick questions. You'll get your likely skin type and a simple, budget-friendly routine.",
        "q": "Question {n} of {t}", "back": "Back", "next": "Next", "see": "See my result", "again": "Take the quiz again",
        "res": "Your skin looks", "am": "Morning", "pm": "Night", "concern": "For your main concern",
        "book": "Book a skin consultation", "send": "Send my result on WhatsApp",
        "fine": "This quiz gives a general idea, not a diagnosis. Patch-test new products on your inner arm first. Dr. Pallavi can check your skin properly at a consultation.",
        "msg": "Hi Smile & Glow Clinic, my skin quiz result: {r}. Main concern: {c}. I'd like a skin consultation.",
        "questions": [
            ["About 2–3 hours after washing your face, how does it feel?", [["Tight or dry", {"dry": 2}], ["Shiny only on forehead and nose", {"combination": 2}], ["Shiny or greasy all over", {"oily": 2}], ["Comfortable — not tight, not oily", {"normal": 2}]]],
            ["How do your pores look?", [["Barely visible", {"dry": 1, "normal": 1}], ["Visible on the nose and forehead", {"combination": 2}], ["Large and visible across the face", {"oily": 2}]]],
            ["How often do you get pimples?", [["Rarely", {"normal": 1, "dry": 1}], ["Sometimes, mostly on forehead, nose or chin", {"combination": 1}], ["Often", {"oily": 2}]]],
            ["By afternoon, how does your face look?", [["Dull or flaky in places", {"dry": 2}], ["Oily forehead and nose, rest is fine", {"combination": 2}], ["Oily all over", {"oily": 2}], ["Much the same as in the morning", {"normal": 2}]]],
            ["Does your skin sting, itch or turn red with new products or sun?", [["Often", {"sensitive": 2}], ["Sometimes", {"sensitive": 1}], ["Rarely or never", {}]]],
            ["What's your main skin concern?", [["Pimples and marks", {"_c": "acne"}], ["Tan, dark spots or pigmentation", {"_c": "pigment"}], ["Fine lines or ageing", {"_c": "ageing"}], ["Dullness or uneven texture", {"_c": "dull"}], ["Nothing in particular", {"_c": "none"}]]],
        ],
        "types": {
            "oily": ["oily", "Your skin makes extra oil, so pores can look larger and pimples are more likely. The aim is to control oil without stripping the skin.",
                     ["Gentle gel or foaming face wash", "Light, oil-free (gel) moisturiser", "Sunscreen SPF 30+, gel or matte"], ["Face wash (a salicylic acid face wash can help with pimples)", "Light, oil-free moisturiser"]],
            "dry": ["dry", "Your skin makes less oil and loses water easily, so it can feel tight or look flaky. The aim is to protect the skin barrier and lock in moisture.",
                    ["Mild, creamy face wash — or just water", "Rich moisturiser (look for ceramides or glycerin)", "Sunscreen SPF 30+, cream-based"], ["Mild, creamy face wash", "Rich moisturiser; skip hot water and scrubs"]],
            "combination": ["combination", "Your forehead and nose (the T-zone) are oily while cheeks are normal or dry. The aim is balance — light products, with extra moisture where you need it.",
                            ["Gentle face wash", "Light moisturiser all over", "Sunscreen SPF 30+"], ["Gentle face wash", "Light moisturiser; a richer one on dry cheeks"]],
            "normal": ["normal", "Your skin is well balanced — not too oily or dry. The aim is to keep it that way with a simple routine and daily sun protection.",
                       ["Gentle face wash", "Moisturiser", "Sunscreen SPF 30+"], ["Gentle face wash", "Moisturiser"]],
        },
        "sensitive": "Your skin also seems sensitive: choose fragrance-free products, add only one new product at a time, and patch-test first.",
        "concerns": {
            "acne": ["Pimples and marks can usually be controlled with the right routine, and stubborn marks respond well to peels.", [["/chemical-peel-lucknow/", "Chemical peels"], ["/#services", "Acne & scar care"]]],
            "pigment": ["Daily sunscreen is the single biggest help. For existing tan and spots, peels or laser toning work well.", [["/chemical-peel-lucknow/", "Chemical peels"], ["/#laser", "Laser toning"]]],
            "ageing": ["Sunscreen every day slows ageing more than any cream. For lines and loss of firmness there are clinic options too.", [["/#services", "Anti-ageing treatments"]]],
            "dull": ["Regular sunscreen, enough sleep and water help. For a quick lift, peels and glow treatments work well.", [["/chemical-peel-lucknow/", "Chemical peels"], ["/#services", "Face PRP & glow facials"]]],
            "none": ["Keep it simple — a gentle routine and daily sunscreen are enough for most people.", []],
        },
        "cname": {"acne": "pimples and marks", "pigment": "tan or pigmentation", "ageing": "fine lines", "dull": "dullness", "none": "none"},
        "and_sensitive": "and sensitive",
    },
    "hi": {
        "title": "स्किन टाइप क्विज़ — 1 मिनट में अपनी त्वचा का प्रकार जानें | स्माइल एंड ग्लो लखनऊ",
        "desc": "स्माइल एंड ग्लो, लखनऊ का मुफ़्त 6 सवालों का स्किन टाइप क्विज़। जानें आपकी त्वचा ऑयली, रूखी, मिली-जुली, नॉर्मल या संवेदनशील है, और आसान रूटीन पाएँ।",
        "crumb": "स्किन टाइप क्विज़", "h1": "आपकी त्वचा कैसी है?",
        "lead": "छह आसान सवाल। आपको अपनी त्वचा का प्रकार और एक सरल, बजट में रूटीन मिलेगा।",
        "q": "सवाल {n} / {t}", "back": "पीछे", "next": "आगे", "see": "मेरा नतीजा देखें", "again": "क्विज़ दोबारा करें",
        "res": "आपकी त्वचा", "am": "सुबह", "pm": "रात", "concern": "आपकी मुख्य समस्या के लिए",
        "book": "स्किन परामर्श बुक करें", "send": "मेरा नतीजा WhatsApp पर भेजें",
        "fine": "यह क्विज़ सिर्फ़ एक अंदाज़ा देता है, जांच नहीं। नया प्रोडक्ट पहले कलाई के अंदर लगाकर पैच टेस्ट करें। डॉ. पल्लवी परामर्श में आपकी त्वचा की सही जांच कर सकती हैं।",
        "msg": "नमस्ते Smile & Glow, मेरा स्किन क्विज़ नतीजा: {r}। मुख्य समस्या: {c}। मुझे स्किन परामर्श चाहिए।",
        "questions": [
            ["चेहरा धोने के 2–3 घंटे बाद त्वचा कैसी लगती है?", [["खिंची हुई या रूखी", {"dry": 2}], ["सिर्फ़ माथे और नाक पर चमक", {"combination": 2}], ["पूरे चेहरे पर चमक या चिकनाई", {"oily": 2}], ["आरामदायक — न खिंची, न ऑयली", {"normal": 2}]]],
            ["आपके रोमछिद्र (पोर्स) कैसे दिखते हैं?", [["मुश्किल से दिखते हैं", {"dry": 1, "normal": 1}], ["नाक और माथे पर दिखते हैं", {"combination": 2}], ["पूरे चेहरे पर बड़े दिखते हैं", {"oily": 2}]]],
            ["मुंहासे कितनी बार होते हैं?", [["कभी-कभार ही", {"normal": 1, "dry": 1}], ["कभी-कभी, ज़्यादातर माथे, नाक या ठोड़ी पर", {"combination": 1}], ["अक्सर", {"oily": 2}]]],
            ["दोपहर तक चेहरा कैसा दिखता है?", [["रूखा या कहीं-कहीं पपड़ी", {"dry": 2}], ["माथा और नाक ऑयली, बाकी ठीक", {"combination": 2}], ["पूरा चेहरा ऑयली", {"oily": 2}], ["लगभग सुबह जैसा", {"normal": 2}]]],
            ["क्या नए प्रोडक्ट या धूप से त्वचा में जलन, खुजली या लालिमा होती है?", [["अक्सर", {"sensitive": 2}], ["कभी-कभी", {"sensitive": 1}], ["बहुत कम या कभी नहीं", {}]]],
            ["आपकी त्वचा की मुख्य समस्या क्या है?", [["मुंहासे और दाग", {"_c": "acne"}], ["टैन, काले धब्बे या पिगमेंटेशन", {"_c": "pigment"}], ["बारीक रेखाएँ या बढ़ती उम्र", {"_c": "ageing"}], ["रूखापन या असमान बनावट", {"_c": "dull"}], ["कोई ख़ास नहीं", {"_c": "none"}]]],
        ],
        "types": {
            "oily": ["ऑयली (तैलीय)", "आपकी त्वचा ज़्यादा तेल बनाती है, इसलिए रोमछिद्र बड़े दिख सकते हैं और मुंहासे ज़्यादा हो सकते हैं। मकसद है तेल को नियंत्रित करना, त्वचा को रूखा किए बिना।",
                     ["हल्का जेल या फ़ोम फ़ेस वॉश", "हल्का, ऑयल-फ़्री (जेल) मॉइस्चराइज़र", "सनस्क्रीन SPF 30+, जेल या मैट"], ["फ़ेस वॉश (मुंहासों में सैलिसिलिक एसिड फ़ेस वॉश मदद कर सकता है)", "हल्का, ऑयल-फ़्री मॉइस्चराइज़र"]],
            "dry": ["रूखी (ड्राई)", "आपकी त्वचा कम तेल बनाती है और जल्दी नमी खो देती है, इसलिए खिंची या पपड़ीदार लग सकती है। मकसद है त्वचा की सुरक्षा परत बचाना और नमी बनाए रखना।",
                    ["हल्का, क्रीमी फ़ेस वॉश — या सिर्फ़ पानी", "गाढ़ा मॉइस्चराइज़र (सेरामाइड या ग्लिसरीन वाला)", "सनस्क्रीन SPF 30+, क्रीम वाला"], ["हल्का, क्रीमी फ़ेस वॉश", "गाढ़ा मॉइस्चराइज़र; गर्म पानी और स्क्रब से बचें"]],
            "combination": ["मिली-जुली (कॉम्बिनेशन)", "आपका माथा और नाक (T-ज़ोन) ऑयली हैं, जबकि गाल नॉर्मल या रूखे। मकसद है संतुलन — हल्के प्रोडक्ट, और जहाँ ज़रूरत हो वहाँ ज़्यादा नमी।",
                            ["हल्का फ़ेस वॉश", "पूरे चेहरे पर हल्का मॉइस्चराइज़र", "सनस्क्रीन SPF 30+"], ["हल्का फ़ेस वॉश", "हल्का मॉइस्चराइज़र; रूखे गालों पर थोड़ा गाढ़ा"]],
            "normal": ["नॉर्मल", "आपकी त्वचा संतुलित है — न ज़्यादा ऑयली, न रूखी। मकसद है आसान रूटीन और रोज़ सनस्क्रीन से इसे ऐसा ही बनाए रखना।",
                       ["हल्का फ़ेस वॉश", "मॉइस्चराइज़र", "सनस्क्रीन SPF 30+"], ["हल्का फ़ेस वॉश", "मॉइस्चराइज़र"]],
        },
        "sensitive": "आपकी त्वचा संवेदनशील भी लगती है: बिना ख़ुशबू वाले प्रोडक्ट चुनें, एक बार में एक ही नया प्रोडक्ट शुरू करें, और पहले पैच टेस्ट करें।",
        "concerns": {
            "acne": ["सही रूटीन से मुंहासे आमतौर पर नियंत्रित हो जाते हैं, और ज़िद्दी दागों पर पील अच्छा असर करते हैं।", [["/chemical-peel-lucknow/", "केमिकल पील"], ["/hi/#services", "मुंहासे और दाग की देखभाल"]]],
            "pigment": ["रोज़ सनस्क्रीन सबसे बड़ी मदद है। मौजूदा टैन और धब्बों के लिए पील या लेज़र टोनिंग अच्छा काम करते हैं।", [["/chemical-peel-lucknow/", "केमिकल पील"], ["/hi/#laser", "लेज़र टोनिंग"]]],
            "ageing": ["रोज़ सनस्क्रीन किसी भी क्रीम से ज़्यादा उम्र के असर को धीमा करता है। रेखाओं और ढीलेपन के लिए क्लिनिक में भी विकल्प हैं।", [["/hi/#services", "एंटी-एजिंग ट्रीटमेंट"]]],
            "dull": ["रोज़ सनस्क्रीन, पूरी नींद और पानी मदद करते हैं। जल्दी निखार के लिए पील और ग्लो ट्रीटमेंट अच्छे हैं।", [["/chemical-peel-lucknow/", "केमिकल पील"], ["/hi/#services", "फ़ेस PRP और ग्लो फ़ेशियल"]]],
            "none": ["सब आसान रखें — ज़्यादातर लोगों के लिए हल्का रूटीन और रोज़ सनस्क्रीन काफ़ी है।", []],
        },
        "cname": {"acne": "मुंहासे और दाग", "pigment": "टैन या पिगमेंटेशन", "ageing": "बारीक रेखाएँ", "dull": "रूखापन", "none": "कोई नहीं"},
        "and_sensitive": "और संवेदनशील",
    },
}

QUIZ_JS = r"""<script>
(function(){
  const Q = __Q__, WA = '__WA__';
  const box = document.getElementById('quiz'), N = Q.questions.length;
  let i = 0; const ans = new Array(N).fill(null);
  const esc = s => s.replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function render() {
    const [q, opts] = Q.questions[i];
    box.innerHTML = '<p class="q-prog">' + Q.q.replace('{n}', i + 1).replace('{t}', N) + '</p><div class="q-bar"><i style="width:' + (i / N * 100) + '%"></i></div>' +
      '<fieldset style="border:0"><legend><h2 tabindex="-1" id="qh">' + esc(q) + '</h2></legend><div class="opts">' +
      opts.map((o, k) => '<label class="opt"><input type="radio" name="qa" value="' + k + '"' + (ans[i] === k ? ' checked' : '') + '><span>' + esc(o[0]) + '</span></label>').join('') +
      '</div></fieldset><div class="q-nav">' + (i ? '<button type="button" class="btn ghost" id="qb">' + Q.back + '</button>' : '') +
      '<button type="button" class="btn rose" id="qn"' + (ans[i] === null ? ' disabled' : '') + '>' + (i === N - 1 ? Q.see : Q.next) + '</button></div>';
    box.querySelectorAll('input').forEach(r => r.addEventListener('change', () => { ans[i] = +r.value; box.querySelector('#qn').disabled = false; }));
    box.querySelector('#qn').addEventListener('click', () => { if (ans[i] === null) return; if (i < N - 1) { i++; render(); } else result(); });
    const b = box.querySelector('#qb'); if (b) b.addEventListener('click', () => { i--; render(); });
    const h = box.querySelector('#qh'); if (h && i) h.focus({preventScroll: false});
  }
  function result() {
    const s = {oily: 0, dry: 0, combination: 0, normal: 0, sensitive: 0}; let concern = 'none';
    ans.forEach((a, k) => { const w = Q.questions[k][1][a][1]; for (const key in w) { if (key === '_c') concern = w[key]; else s[key] += w[key]; } });
    const type = ['combination', 'oily', 'dry', 'normal'].sort((x, y) => s[y] - s[x])[0];
    const sens = s.sensitive >= 2, T = Q.types[type], C = Q.concerns[concern];
    const label = T[0] + (sens ? ' ' + Q.and_sensitive : '');
    const msg = Q.msg.replace('{r}', label).replace('{c}', Q.cname[concern]);
    box.innerHTML = '<div class="result" style="margin-top:0"><span>' + Q.res + '</span><div class="big" tabindex="-1" id="qr">' + esc(label) + '</div><p>' + esc(T[1]) + '</p>' +
      (sens ? '<p style="margin-top:8px">' + esc(Q.sensitive) + '</p>' : '') +
      '<div class="routine"><div><h3>' + Q.am + '</h3><ol>' + T[2].map(x => '<li>' + esc(x) + '</li>').join('') + '</ol></div>' +
      '<div><h3>' + Q.pm + '</h3><ol>' + T[3].map(x => '<li>' + esc(x) + '</li>').join('') + '</ol></div></div>' +
      '<h3 style="margin-top:18px;font-size:var(--t-l)">' + Q.concern + '</h3><p>' + esc(C[0]) + '</p>' +
      (C[1].length ? '<p style="margin-top:6px">' + C[1].map(l => '<a class="link" href="' + l[0] + '">' + esc(l[1]) + '</a>').join(' · ') + '</p>' : '') +
      '<div class="cta-row"><a class="btn rose" target="_blank" rel="noopener" href="https://wa.me/' + WA + '?text=' + encodeURIComponent(msg) + '">' + Q.send + '</a>' +
      '<button type="button" class="btn ghost" id="qa2">' + Q.again + '</button></div></div>';
    box.querySelector('#qa2').addEventListener('click', () => { ans.fill(null); i = 0; render(); });
    box.querySelector('#qr').focus();
  }
  render();
})();
</script>"""


def quiz_page(parts, lang):
    Q = QUIZ[lang]
    body = f"""<section class="tool">
  <div class="wrap">
    <h1>{e(Q['h1'])}</h1>
    <p class="lead">{e(Q['lead'])}</p>
    <div class="tool-box" id="quiz" aria-live="polite"><noscript>Please turn on JavaScript to take the quiz.</noscript></div>
    <p class="fine" style="max-width:760px">{e(Q['fine'])}</p>
  </div>
</section>"""
    js = QUIZ_JS.replace("__Q__", json.dumps(Q, ensure_ascii=False)).replace("__WA__", WHATSAPP)
    path = "/hi/skin-quiz/" if lang == "hi" else "/skin-quiz/"
    return path, shell(parts, lang=lang, path=path, title=Q["title"], desc=Q["desc"], body=body, script=js,
                       crumbs=Q["crumb"], alt={"en": "/skin-quiz/", "hi": "/hi/skin-quiz/"})


# ---------------------------------------------------------------- 3) treatment guide (English)
P = {t["slug"]: t for t in TREATMENTS}


def from_price(slug):
    return "₹" + format(rng(P[slug]["prices"][0][1])[0], ",")


GUIDE = [
    ("missing-tooth", "Missing tooth: implant, bridge or denture?",
     "All three fill the gap. They differ in how long they last, whether neighbouring teeth are touched, and cost.",
     ["", "Implant", "Bridge", "Denture"],
     [["How it works", "A titanium post in the jaw holds a crown", "A crown on each side holds a false tooth", "Removable plate with false teeth"],
      ["Neighbouring teeth", "Not touched", "Trimmed to hold the bridge", "Not trimmed; clasps may rest on them"],
      ["Time", "3–6 months (healing)", "2–3 visits", "2–4 visits"],
      ["Lasts", "Many years, often decades with care", "Around 10–15 years", "Needs relining or replacing every few years"],
      ["Cost", f"From {from_price('dental-implants-lucknow')} per tooth", "Ask at your check-up", "Ask at your check-up"]],
     [("Choose an implant if", "you want the closest thing to a natural tooth, your gums are healthy and you don't smoke heavily."),
      ("Choose a bridge if", "the teeth on both sides already need crowns, or you want a fixed tooth faster."),
      ("Choose a denture if", "several teeth are missing or you need the most affordable option.")],
     [("/dental-implants-lucknow/", "Dental implant costs")]),
    ("toothache", "Toothache: filling, root canal or extraction?",
     "The right treatment depends on how deep the decay goes — an X-ray shows this.",
     ["", "Filling", "Root canal (RCT)", "Extraction"],
     [["When", "Decay hasn't reached the nerve", "Infection or decay has reached the nerve (pulp)", "Tooth can't be saved"],
      ["Typical signs", "Sensitivity to sweet or cold", "Lingering pain, pain at night, swelling, pain on biting", "Badly broken tooth, very loose tooth"],
      ["Keeps your tooth?", "Yes", "Yes — usually with a crown", "No — the gap should be replaced"],
      ["Cost", "Ask at your check-up", f"From {from_price('root-canal-treatment-lucknow')} per tooth", "Ask at your check-up"]],
     [("Don't wait if", "pain lingers or wakes you at night — treating early can mean a simple filling instead of a root canal."),
      ("Saving the tooth", "with RCT is almost always better than pulling it and replacing it later.")],
     [("/root-canal-treatment-lucknow/", "Root canal costs and FAQs")]),
    ("yellow-teeth", "Yellow or stained teeth: cleaning, whitening or veneers?",
     "Surface stains, natural colour and damaged teeth each need a different fix.",
     ["", "Cleaning (scaling)", "Whitening", "Veneers / bonding"],
     [["Fixes", "Tea, tobacco and tartar stains on the surface", "Overall shade of natural teeth", "Deep stains, chips, gaps, uneven shape"],
      ["Changes tooth?", "No", "No — lightens the shade", "Thin layer is added on the front"],
      ["Result lasts", "Until stains build up again", "1–2 years, longer with care", "Many years"],
      ["Cost", "Ask at your check-up", f"From {from_price('teeth-whitening-lucknow')}", "Ask at your check-up"]],
     [("Start with a cleaning", "— many people find their teeth are whiter than they thought."),
      ("Whitening won't change", "the colour of crowns, fillings or veneers, so plan these together.")],
     [("/teeth-whitening-lucknow/", "Teeth whitening costs")]),
    ("pigmentation", "Tan and pigmentation: peel, laser toning or skincare?",
     "Most tan and pigmentation improves with a mix of daily sunscreen and clinic treatment.",
     ["", "Skincare + sunscreen", "Chemical peel", "Laser toning"],
     [["Best for", "Mild tan, prevention", "Tan, dullness, marks", "Stubborn pigmentation, melasma"],
      ["Sessions", "Daily habit", "4–6, every 2–3 weeks", "Several, spaced weeks apart"],
      ["Downtime", "None", "0–5 days of mild flaking", "Little or none"],
      ["Cost", "Product cost only", f"From {from_price('chemical-peel-lucknow')} per session", "Ask at your check-up"]],
     [("Sunscreen comes first", "— without it, any treatment result fades."),
      ("Melasma", "needs gentle, careful treatment; Dr. Pallavi will check which option suits your skin.")],
     [("/chemical-peel-lucknow/", "Chemical peel costs"), ("/#laser", "Laser treatments")]),
    ("acne-scars", "Acne marks vs acne scars: peel or fractional laser?",
     "Flat dark marks and pitted scars are different problems.",
     ["", "Chemical peel", "Fractional laser"],
     [["Best for", "Flat dark or red marks after pimples, active acne", "Pitted or depressed scars, open pores"],
      ["How it works", "Removes the top layer, clears pores", "Triggers new collagen in the deeper skin"],
      ["Sessions", "4–6", "A few, spaced weeks apart"],
      ["Cost", f"From {from_price('chemical-peel-lucknow')} per session", "Ask at your check-up"]],
     [("Control active pimples first", "— scars are treated once new breakouts are under control."),
      ("Often a mix works best", ", for example peels for marks and fractional laser for pits.")],
     [("/chemical-peel-lucknow/", "Chemical peels"), ("/#laser", "Fractional laser")]),
    ("unwanted-hair", "Unwanted hair: laser or waxing and threading?",
     "Waxing and threading remove hair for a few weeks; laser reduces regrowth for the long term.",
     ["", "Waxing / threading", "Laser hair reduction"],
     [["Results last", "2–4 weeks", "Long-term reduction after a course"],
      ["Comfort", "Pulling pain each time", "Quick snaps of warmth; cooled handpiece"],
      ["Ingrown hair, darkening", "Common", "Usually improves"],
      ["Cost", "Small cost, every few weeks", f"From {from_price('laser-hair-removal-lucknow')} per session, 6–8 sessions"]],
     [("Laser works best", "on dark hair; very light, grey or red hair responds less."),
      ("Hormonal causes", " (such as PCOS) should be checked — Dr. Pallavi will ask about this.")],
     [("/laser-hair-removal-lucknow/", "Laser hair reduction costs")]),
    ("hair-fall", "Hair fall: hair PRP, medicines or diet?",
     "Hair fall has many causes. Finding the cause comes first; PRP then helps regrowth.",
     ["", "Check the cause", "Medicines / nutrition", "Hair PRP"],
     [["What it is", "Questions, scalp check, sometimes blood tests (thyroid, iron, vitamin D)", "Treat deficiencies; medicines if advised", "Your own platelet-rich plasma injected into the scalp"],
      ["Helps with", "Every case", "Deficiencies, some hair loss patterns", "Thinning and hair fall, alongside other care"],
      ["Sessions", "One consultation", "Ongoing", "4–6, about a month apart"],
      ["Cost", "Consultation", "Depends on treatment", f"From {from_price('hair-prp-treatment-lucknow')} per session"]],
     [("Sudden heavy hair fall", "after illness, stress or childbirth often settles on its own in a few months."),
      ("Dr. Pallavi's nutrition training", "means diet and deficiencies are part of the plan, not an afterthought.")],
     [("/hair-prp-treatment-lucknow/", "Hair PRP costs")]),
]


def guide_page(parts):
    toc = "".join(f'<a href="#{gid}">{e(title.split(":")[0])}</a>' for gid, title, *_ in GUIDE)
    cards = []
    faq = []
    for gid, title, intro, head, rows, choose, links in GUIDE:
        th = "".join(f"<th scope=\"col\">{e(h)}</th>" for h in head)
        tb = "".join("<tr><th scope=\"row\">" + e(r[0]) + "</th>" + "".join(f"<td>{e(c)}</td>" for c in r[1:]) + "</tr>" for r in rows)
        ch = "".join(f"<li><b>{e(a)}</b> {e(b)}</li>" for a, b in choose)
        ln = " · ".join(f'<a class="link" href="{h}">{e(t)}</a>' for h, t in links)
        cards.append(f"""<article class="guide" id="{gid}"><h2>{e(title)}</h2><p>{e(intro)}</p>
<p class="swipe">Swipe the table to see all options →</p><div class="cmp-wrap" tabindex="0" role="region" aria-label="Comparison table"><table class="cmp"><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>
<ul class="choose">{ch}</ul><p>{ln}</p></article>""")
        faq.append({"@type": "Question", "name": title,
                    "acceptedAnswer": {"@type": "Answer", "text": intro + " " + " ".join(a + " " + b for a, b in choose)}})
    body = f"""<section class="tool">
  <div class="wrap">
    <h1>Which treatment is right for me?</h1>
    <p class="lead">Plain-English comparisons of the choices patients ask us about most. Dr. Pallavi confirms the best option for you at your check-up.</p>
    <nav class="toc" aria-label="Topics">{toc}</nav>
    <div class="guide-list">{''.join(cards)}</div>
    <div class="combo" style="max-width:900px"><p>Still not sure? Send us your question on WhatsApp — or book a check-up and get a clear plan.</p>
      <div class="cta-row"><a class="btn rose" href="{wa("Hi Smile & Glow Clinic, I'm not sure which treatment I need. Can you help?")}" target="_blank" rel="noopener">Ask on WhatsApp</a><a class="btn ghost" href="/#book-form">Book a check-up</a></div></div>
    <p class="fine">General information only, reviewed for Smile &amp; Glow, Lucknow. Not a substitute for an examination. Last updated 26 October 2026.</p>
  </div>
</section>"""
    path = "/treatment-guide/"
    return path, shell(parts, lang="en", path=path,
                       title="Which Dental or Skin Treatment Is Right for Me? | Smile & Glow Lucknow",
                       desc="Implant vs bridge, filling vs root canal, peel vs laser toning, laser vs waxing, hair PRP — simple comparisons with Lucknow prices from Smile & Glow.",
                       body=body, crumbs="Treatment guide",
                       ld=[{"@type": "FAQPage", "@id": f"{SITE}{path}#faq", "inLanguage": "en", "mainEntity": faq}])


# ---------------------------------------------------------------- 4) Hindi explainers
SAMJHIYE = [
    ("rct", "रूट कैनाल (RCT) क्या है?",
     ["जब दांत की सड़न या चोट दांत के अंदर की नस (पल्प) तक पहुँच जाती है, तो दांत में तेज़ दर्द, रात में दर्द या सूजन हो सकती है। रूट कैनाल में दांत के अंदर का संक्रमित हिस्सा साफ़ करके उसे भर दिया जाता है, ताकि दांत निकालना न पड़े।",
      "यह लोकल एनेस्थीसिया में होता है, इसलिए ज़्यादातर मरीज़ों को सामान्य फ़िलिंग जितना ही महसूस होता है। पिछले दांतों में बाद में क्राउन (कैप) लगवाना ज़रूरी होता है।"],
     "/root-canal-treatment-lucknow/", "रूट कैनाल की कीमत: " + from_price("root-canal-treatment-lucknow") + " से"),
    ("implant", "डेंटल इम्प्लांट क्या है?",
     ["इम्प्लांट एक छोटा टाइटेनियम का पेंच है जो जबड़े की हड्डी में लगाया जाता है। हड्डी से जुड़ जाने के बाद उस पर नया दांत (क्राउन) लगता है। यह असली दांत जैसा दिखता और काम करता है, और आसपास के दांतों को घिसना नहीं पड़ता।",
      "पूरा इलाज आमतौर पर 3–6 महीने में होता है। धूम्रपान करने वालों में इम्प्लांट फ़ेल होने का खतरा ज़्यादा होता है।"],
     "/dental-implants-lucknow/", "इम्प्लांट की कीमत: " + from_price("dental-implants-lucknow") + " प्रति दांत से"),
    ("whitening", "क्या दांत सफ़ेद करवाना सुरक्षित है?",
     ["हाँ, जब डॉक्टर की देखरेख में किया जाए। क्लिनिक में की गई व्हाइटनिंग दांतों की ऊपरी परत को नुकसान नहीं पहुँचाती। एक-दो दिन हल्की झनझनाहट हो सकती है, जो अपने आप ठीक हो जाती है।",
      "पहले सफ़ाई (स्केलिंग) करवाने से कई बार ही दांत काफ़ी साफ़ दिखने लगते हैं। व्हाइटनिंग से क्राउन या फ़िलिंग का रंग नहीं बदलता।"],
     "/teeth-whitening-lucknow/", "व्हाइटनिंग की कीमत: " + from_price("teeth-whitening-lucknow") + " से"),
    ("laser", "लेज़र हेयर रिडक्शन कैसे काम करता है?",
     ["लेज़र की रोशनी बालों की जड़ के रंग (पिगमेंट) तक पहुँचकर उसे कमज़ोर कर देती है, जिससे बाल धीरे-धीरे कम और पतले उगते हैं। आमतौर पर 4–6 हफ़्ते के अंतर पर 6–8 सेशन लगते हैं।",
      "हर लेज़र प्लान त्वचा की जांच और पैच टेस्ट से शुरू होता है, और सेटिंग भारतीय त्वचा के हिसाब से चुनी जाती है। सेशन के बीच वैक्सिंग या थ्रेडिंग न करें — ज़रूरत हो तो शेव करें।"],
     "/laser-hair-removal-lucknow/", "लेज़र की कीमत: " + from_price("laser-hair-removal-lucknow") + " प्रति सेशन से"),
    ("peel", "केमिकल पील क्या होता है?",
     ["केमिकल पील में त्वचा पर एक हल्का एसिड का घोल कुछ मिनट के लिए लगाया जाता है, जो पुरानी, बेजान ऊपरी परत को हटाता है। इससे टैन, दाग, मुंहासे और रूखापन कम होता है और त्वचा में निखार आता है।",
      "हल्के पील में लगभग कोई डाउनटाइम नहीं होता — कुछ दिन हल्की पपड़ी उतर सकती है। इलाज के बाद रोज़ सनस्क्रीन लगाना बहुत ज़रूरी है।"],
     "/chemical-peel-lucknow/", "पील की कीमत: " + from_price("chemical-peel-lucknow") + " प्रति सेशन से"),
    ("prp", "हेयर PRP क्या है?",
     ["PRP में आपके अपने खून से प्लेटलेट-रिच प्लाज़्मा अलग करके सिर की त्वचा में लगाया जाता है। इसमें मौजूद ग्रोथ फ़ैक्टर बालों की जड़ों को मज़बूत करने और झड़ना कम करने में मदद करते हैं।",
      "पहले बाल झड़ने का कारण देखा जाता है — जैसे थायरॉइड, आयरन या विटामिन की कमी। आमतौर पर महीने भर के अंतर पर 4–6 सेशन लगते हैं।"],
     "/hair-prp-treatment-lucknow/", "हेयर PRP की कीमत: " + from_price("hair-prp-treatment-lucknow") + " प्रति सेशन से"),
    ("sunscreen", "सनस्क्रीन रोज़ क्यों ज़रूरी है?",
     ["धूप की UV किरणें टैनिंग, काले धब्बे, झाइयाँ और समय से पहले झुर्रियों की सबसे बड़ी वजह हैं — बादल वाले दिन और घर के अंदर खिड़की के पास भी। रोज़ SPF 30 या उससे ज़्यादा वाला सनस्क्रीन लगाएँ और बाहर रहें तो 2–3 घंटे में दोबारा लगाएँ।",
      "पील या लेज़र के बाद सनस्क्रीन न लगाने से इलाज का असर कम हो जाता है।"],
     "/hi/skin-quiz/", "अपनी त्वचा का प्रकार जानें — स्किन क्विज़"),
    ("expensive", "क्या महंगे स्किनकेयर प्रोडक्ट ज़रूरी हैं?",
     ["नहीं। अगर प्रोडक्ट आपकी त्वचा के प्रकार के हिसाब से चुने जाएँ, तो कई सस्ते प्रोडक्ट भी उतना ही अच्छा काम करते हैं। ज़्यादातर लोगों के लिए हल्का फ़ेस वॉश, मॉइस्चराइज़र और सनस्क्रीन काफ़ी है।",
      "डॉ. पल्लवी आपकी त्वचा और बजट के हिसाब से रूटीन बताती हैं — बेवजह के प्रोडक्ट नहीं।"],
     "/hi/#book-form", "स्किन परामर्श बुक करें"),
]


def samjhiye_page(parts):
    arts = "".join(f'<article id="{i}"><h2>{e(q)}</h2>' + "".join(f"<p>{e(p)}</p>" for p in ps) +
                   f'<p style="margin-top:12px"><a class="link" href="{href}">{e(lt)}</a></p></article>'
                   for i, q, ps, href, lt in SAMJHIYE)
    toc = "".join(f'<a href="#{i}">{e(q.replace(" क्या है?", "").replace("?", ""))}</a>' for i, q, *_ in SAMJHIYE)
    faq = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(ps)}} for _, q, ps, *_ in SAMJHIYE]
    body = f"""<section class="tool">
  <div class="wrap">
    <h1>आसान भाषा में समझिए</h1>
    <p class="lead">दांत, त्वचा और बालों के इलाज से जुड़े आम सवाल — सीधी, सरल हिंदी में, डॉ. पल्लवी के क्लिनिक से।</p>
    <nav class="toc" aria-label="विषय">{toc}</nav>
    <div class="explain">{arts}</div>
    <div class="combo" style="max-width:820px"><p>और सवाल हैं? Instagram पर डॉ. पल्लवी के हिंदी वीडियो देखें या WhatsApp पर पूछें।</p>
      <div class="cta-row"><a class="btn rose" href="{wa("नमस्ते Smile & Glow, मेरा एक सवाल है:")}" target="_blank" rel="noopener">WhatsApp पर पूछें</a><a class="btn ghost" href="https://www.instagram.com/smileandglowclinic/" target="_blank" rel="noopener">Instagram</a></div></div>
    <p class="fine">यह जानकारी सामान्य जागरूकता के लिए है, डॉक्टर की जांच का विकल्प नहीं। अपडेट: 26 अक्टूबर 2026।</p>
  </div>
</section>"""
    path = "/hi/samjhiye/"
    return path, shell(parts, lang="hi", path=path, title="आसान भाषा में समझिए — दांत और त्वचा के इलाज | स्माइल एंड ग्लो लखनऊ",
                       desc="रूट कैनाल, इम्प्लांट, दांत सफ़ेद करना, लेज़र, केमिकल पील, हेयर PRP और सनस्क्रीन — आसान हिंदी में, स्माइल एंड ग्लो लखनऊ से।",
                       body=body, crumbs="आसान भाषा में समझिए",
                       ld=[{"@type": "FAQPage", "@id": f"{SITE}{path}#faq", "inLanguage": "hi", "mainEntity": faq}])


# ---------------------------------------------------------------- 5) aftercare cards
def aftercare_page(parts):
    cards = []
    for t in TREATMENTS:
        s = t["slug"]
        aid = s.replace("-lucknow", "").replace("-treatment", "")
        en, hi = t["aftercare"], AFTERCARE_HI[s]
        text = (f"Smile & Glow — aftercare: {t['name']}\n" + "\n".join("• " + x for x in en) +
                f"\n\n{NAME_HI[s]} — देखभाल:\n" + "\n".join("• " + x for x in hi) +
                f"\n\nQuestions? Call/WhatsApp {PHONE_DISPLAY}\n{SITE}/aftercare/#{aid}")
        cards.append(f"""<article class="care" id="{aid}"><h2>{e(t['name'])}</h2>
<h3>English</h3><ul>{''.join(f'<li>{e(x)}</li>' for x in en)}</ul>
<h3 lang="hi">हिंदी — {e(NAME_HI[s])}</h3><ul lang="hi">{''.join(f'<li>{e(x)}</li>' for x in hi)}</ul>
<div class="cta-row"><a class="btn ghost" href="https://wa.me/?text={quote(text)}" target="_blank" rel="noopener">Share on WhatsApp</a><a class="link" href="/{s}/">About this treatment</a></div></article>""")
    toc = "".join(f'<a href="#{t["slug"].replace("-lucknow", "").replace("-treatment", "")}">{e(t["short"])}</a>' for t in TREATMENTS)
    body = f"""<section class="tool">
  <div class="wrap">
    <h1>Aftercare instructions · देखभाल</h1>
    <p class="lead">What to do after your treatment at Smile &amp; Glow, in English and Hindi. Save this page or share a card on WhatsApp.</p>
    <nav class="toc" aria-label="Treatments">{toc}</nav>
    <div class="care-grid">{''.join(cards)}</div>
    <div class="combo"><p><b>Call us straight away</b> on <a class="link" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> if you have heavy bleeding, swelling that keeps getting worse, fever, or pain that pain relief doesn't help. · तेज़ खून, बढ़ती सूजन, बुखार या दवा से भी न रुकने वाले दर्द में तुरंत कॉल करें।</p></div>
    <p class="fine">Follow any specific instructions Dr. Pallavi gives you — they take priority over this general guide.</p>
  </div>
</section>"""
    path = "/aftercare/"
    return path, shell(parts, lang="en", path=path, title="Aftercare After Dental & Skin Treatment (English + Hindi) | Smile & Glow",
                       desc="Aftercare for root canal, implants, teeth whitening, laser hair reduction, hair PRP and chemical peels — in English and Hindi, from Smile & Glow, Lucknow.",
                       body=body, crumbs="Aftercare")


# ---------------------------------------------------------------- build
def build_extras(root: Path, en_src: str, hi_src: str):
    en, hi = extract(en_src), hi_parts(hi_src)
    pages = [calc_page(en, "en"), calc_page(hi, "hi"), quiz_page(en, "en"), quiz_page(hi, "hi"),
             guide_page(en), samjhiye_page(hi), aftercare_page(en)]
    for path, doc in pages:
        out = root / path.strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(doc, encoding="utf-8")
    with open(root / "assets" / "site.css", "a", encoding="utf-8") as f:
        f.write(EXTRA_CSS)
    return [p for p, _ in pages]
