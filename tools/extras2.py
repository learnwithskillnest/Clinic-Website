"""Second set of patient pages (27 Oct 2026). Built by tools/build.py.

  /dental-emergency/      + /hi/dental-emergency/      what to do right now
  /before-your-visit/     + /hi/before-your-visit/     medical-history form sent on WhatsApp
  /scared-of-the-dentist/                              dental anxiety
  /food-for-teeth-and-skin/                            nutrition guide (Dr. Pallavi: PG Diploma in Nutrition)
  /kids/                                               kids' corner, brushing chart, brave-patient certificate
  /review/                                             leave a Google review (QR posters point here)
"""
import html
import json
from urllib.parse import quote

from treatments import SITE, PHONE_DISPLAY, PHONE_TEL, WHATSAPP
from extras import shell, e, wa

REVIEW = {
    "it": "https://search.google.com/local/writereview?placeid=ChIJ094uDo0lmjkRLkvx18o19vM",
    "aa": "https://search.google.com/local/writereview?placeid=ChIJE16LLUj9mzkR8VgXSvsgumU",
}

CSS = """
/* ---------- Patient pages, set 2 ---------- */
.alert{display:flex;gap:16px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding:20px 24px;border-radius:var(--radius);background:var(--accent);color:var(--accent-ink);margin-bottom:28px;max-width:900px}
.alert p{color:inherit;font-weight:600;font-size:var(--t-l)}
.alert .btn{background:var(--accent-ink);color:var(--accent)}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:900px}
.cards > *{min-width:0}
.card{background:var(--surface);border-radius:var(--radius);padding:22px 24px}
.card h2{font-size:var(--t-xl);margin-bottom:8px}
.card h3{font-size:var(--t-l);margin-bottom:6px}
.card ol,.card ul{margin-left:20px;color:var(--muted)}
.card li{margin:5px 0}
.card p{color:var(--muted)}
.card.warn{box-shadow:inset 4px 0 0 var(--accent)}
.prose{max-width:760px}
.prose h2{font-size:var(--t-2xl);margin:36px 0 10px}
.prose h3{font-size:var(--t-l);margin:20px 0 6px}
.prose p,.prose li{color:var(--muted)}
.prose ul,.prose ol{margin:8px 0 8px 22px}
.prose li{margin:5px 0}
.prose .card{margin:14px 0}
.form-grid{display:grid;gap:16px}
.checks{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.checks label{display:flex;gap:10px;align-items:center;padding:10px 12px;border-radius:10px;background:var(--bg);font-weight:500;min-height:44px}
.checks input{width:20px;height:20px;min-height:0;margin:0;accent-color:var(--brand)}
.review-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:760px}
.review-grid .card{display:flex;flex-direction:column;gap:12px;align-items:flex-start}
.chart{width:100%;border-collapse:collapse;margin-top:12px;font-size:var(--t-s)}
.chart th,.chart td{border:1.5px solid var(--bg-2);padding:8px;text-align:center}
.chart td{height:44px}
.cert{max-width:720px;margin:16px 0;padding:36px 28px;border-radius:var(--radius);background:var(--surface);text-align:center;border:3px dashed var(--brand)}
.cert h2{font-size:var(--t-2xl)}
.cert .who{font-family:"Playfair Display","Mukta",serif;font-size:var(--t-2xl);color:var(--accent-text);margin:10px 0;min-height:1.3em;border-bottom:2px solid var(--bg-2)}
.print-only{display:none}
@media (max-width:760px){.cards,.review-grid,.checks{grid-template-columns:1fr}}
@media print{.no-print{display:none!important}.print-only{display:block}body{background:#fff}.tool{padding:0}.cert,.card{border-color:#1b5c8c}}
"""


def page_wrap(h1, lead, inner):
    return f"""<section class="tool">
  <div class="wrap">
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    {inner}
  </div>
</section>"""


# ---------------------------------------------------------------- emergency
EMERG = {
    "en": {
        "title": "Dental Emergency in Lucknow: What to Do Now | Smile & Glow",
        "desc": "Severe toothache, knocked-out or broken tooth, swelling or bleeding? What to do now and when to go to hospital. Smile & Glow Lucknow: +91 72754 33783.",
        "crumb": "Dental emergency", "h1": "Dental emergency? What to do right now",
        "lead": "Simple first steps until you can see a dentist — and the signs that mean you should go to a hospital straight away.",
        "call": "Call the clinic now", "alert": "In pain or had an accident? Call us and we'll try to see you as soon as possible.",
        "hosp_t": "Go to a hospital emergency department now if you have",
        "hosp": ["Swelling spreading to the eye, neck or under the jaw", "Difficulty breathing or swallowing", "High fever with tooth or face swelling",
                 "Bleeding that doesn't stop after 30 minutes of firm pressure", "A hard blow to the face or jaw, or a possible broken jaw"],
        "cards": [
            ("Severe toothache", ["Rinse with warm salt water (half a teaspoon of salt in a glass of water).", "Gently floss to remove any food stuck between teeth.",
                                  "Hold a cold pack on the outside of your cheek for 15 minutes at a time.", "Take a painkiller you normally use safely, as directed on the pack.",
                                  "Don't put aspirin, clove oil soaked cotton or any tablet directly on the gum — it can burn.", "Book a visit soon: pain that wakes you at night usually needs treatment."]),
            ("Knocked-out adult tooth", ["Act fast — the best chance is within 30–60 minutes.", "Hold the tooth by the crown (white part), not the root.",
                                         "If dirty, rinse briefly with milk or water. Don't scrub it.", "If you can, push it gently back into its socket and bite on a clean cloth.",
                                         "Otherwise keep it in a small cup of milk (or inside the cheek for adults) and call us now.", "A knocked-out milk (baby) tooth should not be put back — just see us."]),
            ("Broken or chipped tooth", ["Rinse your mouth with warm water.", "Save any broken pieces in milk or water.", "Use a cold pack if there's swelling.",
                                         "Avoid chewing on that side and very hot or cold food.", "See us within a day or two — sooner if there's pain or the break is large."]),
            ("Swelling of the gum or face", ["This often means an infection — call us the same day.", "Use a cold pack outside the face; don't use heat.",
                                             "Don't try to pop or squeeze a gum boil.", "If swelling spreads to the eye or neck, or you have fever or trouble swallowing, go to a hospital."]),
            ("Bleeding after a tooth extraction", ["Bite firmly on a clean gauze or cloth pad over the socket for 30–45 minutes.", "Keep your head raised; don't spit, rinse hard or use a straw today.",
                                                   "A slight ooze for a day is normal.", "If heavy bleeding continues after 2 rounds of pressure, call us or go to a hospital."]),
            ("Lost filling or crown, broken braces wire", ["Keep a lost crown safe and bring it with you.", "Cover a sharp edge or poking wire with orthodontic wax or sugar-free chewing gum.",
                                                           "Don't glue a crown back with household glue.", "Book a visit in the next few days."]),
        ],
        "hours_t": "Clinic timings",
        "hours": "I.T Chauraha: Monday–Saturday, 11:00 AM – 3:00 PM · Aashiyana: Monday–Saturday, 4:00 PM – 9:00 PM · Sunday: by appointment only — call or WhatsApp.",
        "fine": "This page is first-aid guidance only and doesn't replace an examination. If in doubt, call us or go to the nearest hospital.",
    },
    "hi": {
        "title": "दांत की इमरजेंसी, लखनऊ: अभी क्या करें | स्माइल एंड ग्लो",
        "desc": "तेज़ दांत दर्द, गिरा या टूटा दांत, सूजन या दांत निकलवाने के बाद खून — अभी क्या करें और कब अस्पताल जाएँ। स्माइल एंड ग्लो, लखनऊ: +91 72754 33783।",
        "crumb": "दांत की इमरजेंसी", "h1": "दांत की इमरजेंसी? अभी क्या करें",
        "lead": "डेंटिस्ट तक पहुँचने से पहले के आसान कदम — और वे लक्षण जिनमें तुरंत अस्पताल जाना चाहिए।",
        "call": "अभी क्लिनिक को कॉल करें", "alert": "दर्द है या चोट लगी है? कॉल करें, हम जल्द से जल्द देखने की कोशिश करेंगे।",
        "hosp_t": "इनमें से कुछ हो तो तुरंत अस्पताल की इमरजेंसी में जाएँ",
        "hosp": ["सूजन आँख, गर्दन या जबड़े के नीचे तक फैल रही हो", "सांस लेने या निगलने में दिक्कत", "दांत या चेहरे की सूजन के साथ तेज़ बुखार",
                 "30 मिनट तक दबाने के बाद भी खून न रुके", "चेहरे या जबड़े पर ज़ोर की चोट, या जबड़ा टूटने का शक"],
        "cards": [
            ("तेज़ दांत दर्द", ["गुनगुने नमक-पानी से कुल्ला करें (एक गिलास पानी में आधा चम्मच नमक)।", "दांतों के बीच फँसा खाना धागे (फ़्लॉस) से धीरे से निकालें।",
                               "गाल के बाहर 15-15 मिनट ठंडी सिकाई करें।", "जो दर्द की दवा आप आमतौर पर सुरक्षित रूप से लेते हैं, पैक पर लिखे अनुसार लें।",
                               "एस्पिरिन, लौंग के तेल वाली रुई या कोई गोली सीधे मसूड़े पर न रखें — इससे जलन हो सकती है।", "जल्द विज़िट बुक करें: रात में जगाने वाले दर्द में आमतौर पर इलाज ज़रूरी होता है।"]),
            ("बड़ों का दांत पूरा गिर जाए", ["जल्दी करें — 30–60 मिनट के अंदर सबसे अच्छा मौका होता है।", "दांत को ऊपर के सफ़ेद हिस्से से पकड़ें, जड़ से नहीं।",
                                          "गंदा हो तो दूध या पानी से हल्का धो लें। रगड़ें नहीं।", "हो सके तो उसे धीरे से उसकी जगह वापस लगाकर साफ़ कपड़ा दबाएँ।",
                                          "वरना दांत को थोड़े दूध में रखें और तुरंत कॉल करें।", "बच्चे का दूध का दांत वापस न लगाएँ — बस हमें दिखाएँ।"]),
            ("दांत टूट जाए या किनारा टूटे", ["गुनगुने पानी से कुल्ला करें।", "टूटे टुकड़े दूध या पानी में रख लें।", "सूजन हो तो ठंडी सिकाई करें।",
                                             "उस तरफ़ से न चबाएँ, बहुत गर्म या ठंडा न खाएँ।", "एक-दो दिन में दिखाएँ — दर्द हो या टूटना बड़ा हो तो जल्दी।"]),
            ("मसूड़े या चेहरे पर सूजन", ["यह अक्सर इन्फ़ेक्शन होता है — उसी दिन कॉल करें।", "चेहरे के बाहर ठंडी सिकाई करें; गर्म सिकाई न करें।",
                                       "मसूड़े के फोड़े को दबाएँ या फोड़ें नहीं।", "सूजन आँख या गर्दन तक फैले, बुखार हो या निगलने में दिक्कत हो तो अस्पताल जाएँ।"]),
            ("दांत निकलवाने के बाद खून", ["साफ़ गॉज़ या कपड़े की गद्दी को 30–45 मिनट तक ज़ोर से दबाकर रखें।", "सिर ऊँचा रखें; आज थूकें नहीं, ज़ोर से कुल्ला न करें, स्ट्रॉ न इस्तेमाल करें।",
                                          "एक दिन तक हल्का रिसना सामान्य है।", "दो बार दबाने के बाद भी ज़्यादा खून आए तो कॉल करें या अस्पताल जाएँ।"]),
            ("फ़िलिंग या क्राउन निकल जाए, ब्रेसेस का तार चुभे", ["निकला हुआ क्राउन संभालकर रखें और साथ लाएँ।", "चुभते किनारे या तार पर ऑर्थोडॉन्टिक वैक्स या बिना चीनी की च्युइंग गम लगाएँ।",
                                                             "क्राउन को घर के गोंद से न चिपकाएँ।", "अगले कुछ दिनों में विज़िट बुक करें।"]),
        ],
        "hours_t": "क्लिनिक का समय",
        "hours": "आई.टी. चौराहा: सोमवार–शनिवार, सुबह 11:00 – दोपहर 3:00 · आशियाना: सोमवार–शनिवार, शाम 4:00 – रात 9:00 · रविवार: सिर्फ़ अपॉइंटमेंट पर — कॉल या WhatsApp करें।",
        "fine": "यह पेज सिर्फ़ प्राथमिक उपचार की जानकारी है, जांच का विकल्प नहीं। शक हो तो कॉल करें या नज़दीकी अस्पताल जाएँ।",
    },
}


def emergency_page(parts, lang):
    T = EMERG[lang]
    cards = "".join(f'<article class="card"><h2>{e(t)}</h2><ol>' + "".join(f"<li>{e(x)}</li>" for x in xs) + "</ol></article>"
                    for t, xs in T["cards"])
    inner = f"""<div class="alert"><p>{e(T['alert'])}</p><a class="btn" href="tel:{PHONE_TEL}">{e(T['call'])} · {PHONE_DISPLAY}</a></div>
    <div class="cards">
      <article class="card warn" style="grid-column:1/-1"><h2>{e(T['hosp_t'])}</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in T['hosp'])}</ul></article>
      {cards}
      <article class="card" style="grid-column:1/-1"><h2>{e(T['hours_t'])}</h2><p>{e(T['hours'])}</p>
        <div class="cta-row" style="margin-top:12px"><a class="btn rose" href="tel:{PHONE_TEL}">{e(T['call'])}</a><a class="btn ghost" href="{wa('Hi Smile & Glow Clinic, I have a dental emergency.' if lang == 'en' else 'नमस्ते Smile & Glow, मुझे दांत की इमरजेंसी है।')}" target="_blank" rel="noopener">WhatsApp</a></div></article>
    </div>
    <p class="fine">{e(T['fine'])}</p>"""
    faq = [{"@type": "Question", "name": t, "acceptedAnswer": {"@type": "Answer", "text": " ".join(xs)}} for t, xs in T["cards"]]
    path = "/hi/dental-emergency/" if lang == "hi" else "/dental-emergency/"
    return path, shell(parts, lang=lang, path=path, title=T["title"], desc=T["desc"], crumbs=T["crumb"],
                       body=page_wrap(e(T["h1"]), e(T["lead"]), inner),
                       alt={"en": "/dental-emergency/", "hi": "/hi/dental-emergency/"},
                       ld=[{"@type": "FAQPage", "@id": f"{SITE}{path}#faq", "inLanguage": lang, "mainEntity": faq}])


# ---------------------------------------------------------------- before your visit
VISIT = {
    "en": {
        "title": "Before Your Visit — Medical History Form | Smile & Glow Lucknow",
        "desc": "Fill in your medical history before your appointment at Smile & Glow, Lucknow. It's sent to the clinic on WhatsApp, so check-in is quicker.",
        "crumb": "Before your visit", "h1": "Before your visit",
        "lead": "Fill this in before you come — it takes 2 minutes and saves time at the clinic. It's sent to us on WhatsApp; nothing is stored on this website.",
        "name": "Patient's name", "age": "Age", "phone": "Phone", "branch": "Branch", "date": "Appointment date (if booked)",
        "for": "Visit for", "for_opts": ["Teeth", "Skin", "Hair", "Laser", "Not sure"],
        "concern": "Main concern", "concern_ph": "e.g. pain in lower left tooth for 3 days; pigmentation on cheeks",
        "cond": "Do you have any of these?", "conds": ["Diabetes", "High or low blood pressure", "Heart problem", "Thyroid", "Asthma", "Epilepsy",
                                                     "Bleeding problem or on blood thinners", "Pregnant or breastfeeding", "Kidney or liver problem", "Recent surgery"],
        "none": "None of these",
        "allergy": "Allergies (medicines, latex, anaesthesia, food)", "meds": "Medicines you take regularly", "prev": "Past dental or skin treatment, if relevant",
        "smoke": "Do you smoke or chew tobacco?", "yn": ["No", "Yes", "Occasionally"],
        "anx": "Do you feel nervous about treatment?", "anx_opts": ["No", "A little", "Very"],
        "send": "Send to the clinic on WhatsApp", "branches": ["I.T Chauraha", "Aashiyana"],
        "fine": "Your answers open in WhatsApp for you to check before sending. Bring your medicine strips and any old reports or X-rays to the visit.",
        "msg_h": "Before-visit form — Smile & Glow", "lbl_none": "none",
    },
    "hi": {
        "title": "विज़िट से पहले — मेडिकल हिस्ट्री फ़ॉर्म | स्माइल एंड ग्लो लखनऊ",
        "desc": "स्माइल एंड ग्लो, लखनऊ में अपॉइंटमेंट से पहले अपनी मेडिकल जानकारी भरें। यह WhatsApp पर क्लिनिक को जाती है, जिससे समय बचता है।",
        "crumb": "विज़िट से पहले", "h1": "विज़िट से पहले",
        "lead": "आने से पहले यह भर दें — 2 मिनट लगते हैं और क्लिनिक में समय बचता है। यह WhatsApp पर हमें जाता है; वेबसाइट पर कुछ सेव नहीं होता।",
        "name": "मरीज़ का नाम", "age": "उम्र", "phone": "फ़ोन", "branch": "क्लिनिक", "date": "अपॉइंटमेंट की तारीख़ (अगर बुक है)",
        "for": "किसके लिए", "for_opts": ["दांत", "त्वचा", "बाल", "लेज़र", "पता नहीं"],
        "concern": "मुख्य समस्या", "concern_ph": "जैसे: 3 दिन से नीचे बाएँ दांत में दर्द; गालों पर पिगमेंटेशन",
        "cond": "क्या आपको इनमें से कुछ है?", "conds": ["डायबिटीज़ (शुगर)", "हाई या लो ब्लड प्रेशर", "दिल की बीमारी", "थायरॉइड", "अस्थमा", "मिर्गी",
                                                   "खून न रुकने की समस्या या खून पतला करने की दवा", "गर्भवती या स्तनपान", "किडनी या लिवर की समस्या", "हाल ही में सर्जरी"],
        "none": "इनमें से कुछ नहीं",
        "allergy": "एलर्जी (दवा, लेटेक्स, एनेस्थीसिया, खाना)", "meds": "रोज़ ली जाने वाली दवाइयाँ", "prev": "पहले हुआ दांत या त्वचा का इलाज (अगर हो)",
        "smoke": "क्या आप धूम्रपान करते हैं या तंबाकू/गुटखा खाते हैं?", "yn": ["नहीं", "हाँ", "कभी-कभी"],
        "anx": "क्या इलाज से घबराहट होती है?", "anx_opts": ["नहीं", "थोड़ी", "बहुत"],
        "send": "WhatsApp पर क्लिनिक को भेजें", "branches": ["आई.टी. चौराहा", "आशियाना"],
        "fine": "आपके जवाब WhatsApp में खुलेंगे, भेजने से पहले जांच लें। विज़िट पर अपनी दवाओं के पत्ते और पुरानी रिपोर्ट या एक्स-रे साथ लाएँ।",
        "msg_h": "विज़िट से पहले फ़ॉर्म — Smile & Glow", "lbl_none": "कुछ नहीं",
    },
}

VISIT_JS = r"""<script>
(function(){
  const T = __T__, f = document.getElementById('pv');
  const none = f.querySelector('input[name=none]');
  f.querySelectorAll('input[name=cond]').forEach(c => c.addEventListener('change', () => { if (c.checked) none.checked = false; }));
  none.addEventListener('change', () => { if (none.checked) f.querySelectorAll('input[name=cond]').forEach(c => c.checked = false); });
  f.addEventListener('submit', ev => {
    ev.preventDefault();
    const d = new FormData(f), g = k => (d.get(k) || '').toString().trim();
    const conds = d.getAll('cond'), fors = d.getAll('for');
    const lines = [T.msg_h,
      T.name + ': ' + g('name') + (g('age') ? ' (' + g('age') + ')' : ''),
      T.phone + ': ' + g('phone'),
      T.branch + ': ' + g('branch') + (g('date') ? ' · ' + g('date') : ''),
      T['for'] + ': ' + (fors.join(', ') || '-'),
      T.concern + ': ' + (g('concern') || '-'),
      T.cond + ' ' + (conds.length ? conds.join(', ') : T.lbl_none),
      T.allergy + ': ' + (g('allergy') || T.lbl_none),
      T.meds + ': ' + (g('meds') || T.lbl_none),
      g('prev') ? T.prev + ': ' + g('prev') : '',
      T.smoke + ' ' + g('smoke'),
      T.anx + ' ' + g('anx')].filter(Boolean);
    window.open('https://wa.me/__WA__?text=' + encodeURIComponent(lines.join('\n')), '_blank');
  });
})();
</script>"""


def visit_page(parts, lang):
    T = VISIT[lang]
    radios = lambda name, opts: '<div class="checks">' + "".join(
        f'<label><input type="radio" name="{name}" value="{e(o)}"{" checked" if i == 0 else ""}>{e(o)}</label>' for i, o in enumerate(opts)) + "</div>"
    inner = f"""<form id="pv" class="tool-box form-grid" autocomplete="on">
      <div class="row2"><label>{e(T['name'])}<input name="name" required autocomplete="name"></label><label>{e(T['age'])}<input name="age" inputmode="numeric" maxlength="3"></label></div>
      <div class="row2"><label>{e(T['phone'])}<input name="phone" type="tel" required autocomplete="tel"></label>
        <label>{e(T['branch'])}<select name="branch">{''.join(f'<option>{e(b)}</option>' for b in T['branches'])}</select></label></div>
      <label>{e(T['date'])}<input name="date" type="date"></label>
      <fieldset style="border:0"><legend style="font-weight:600;margin-bottom:6px">{e(T['for'])}</legend><div class="checks">{''.join(f'<label><input type="checkbox" name="for" value="{e(o)}">{e(o)}</label>' for o in T['for_opts'])}</div></fieldset>
      <label>{e(T['concern'])}<textarea name="concern" rows="2" placeholder="{html.escape(T['concern_ph'])}"></textarea></label>
      <fieldset style="border:0"><legend style="font-weight:600;margin-bottom:6px">{e(T['cond'])}</legend><div class="checks">{''.join(f'<label><input type="checkbox" name="cond" value="{e(o)}">{e(o)}</label>' for o in T['conds'])}<label><input type="checkbox" name="none" value="1">{e(T['none'])}</label></div></fieldset>
      <label>{e(T['allergy'])}<input name="allergy"></label>
      <label>{e(T['meds'])}<input name="meds"></label>
      <label>{e(T['prev'])}<input name="prev"></label>
      <fieldset style="border:0"><legend style="font-weight:600;margin-bottom:6px">{e(T['smoke'])}</legend>{radios('smoke', T['yn'])}</fieldset>
      <fieldset style="border:0"><legend style="font-weight:600;margin-bottom:6px">{e(T['anx'])}</legend>{radios('anx', T['anx_opts'])}</fieldset>
      <button class="btn rose" type="submit" style="justify-self:start">{e(T['send'])}</button>
      <p class="note">{e(T['fine'])}</p>
    </form>"""
    js = VISIT_JS.replace("__T__", json.dumps(T, ensure_ascii=False)).replace("__WA__", WHATSAPP)
    path = "/hi/before-your-visit/" if lang == "hi" else "/before-your-visit/"
    return path, shell(parts, lang=lang, path=path, title=T["title"], desc=T["desc"], crumbs=T["crumb"],
                       body=page_wrap(e(T["h1"]), e(T["lead"]), inner), script=js,
                       alt={"en": "/before-your-visit/", "hi": "/hi/before-your-visit/"})


# ---------------------------------------------------------------- scared of the dentist
def anxiety_page(parts):
    inner = f"""<div class="prose">
<p>Feeling nervous about the dentist is very common — many adults put off treatment for years because of it. The good news: modern dentistry is far gentler than most people remember, and you stay in control the whole time.</p>
<h2>What happens at your first visit</h2>
<ol><li><b>A chat first.</b> Tell us what worries you — pain, needles, the sound of the drill, or a bad past experience. Nothing is done until you're ready.</li>
<li><b>A gentle check-up.</b> We look at your teeth and gums, and take an X-ray only if it's needed.</li>
<li><b>Your options, explained.</b> What needs doing now, what can wait, how many visits and what it costs. You decide.</li>
<li><b>Treatment can be on another day.</b> If you'd rather just meet us first, that's completely fine.</li></ol>
<h2>How pain is controlled</h2>
<ul><li>A numbing gel is applied to the gum before any injection, so you barely feel it.</li>
<li>Local anaesthesia numbs the area fully — most patients feel pressure or vibration, not pain.</li>
<li>We check that you're numb before starting, and add more if you need it.</li>
<li>After treatment, you'll know exactly what to expect and which pain relief to take.</li></ul>
<h2>You stay in control</h2>
<ul><li><b>Agree a stop signal</b> — raise your hand and we pause straight away.</li>
<li><b>Ask for breaks</b> whenever you need to rest your jaw.</li>
<li><b>Ask us to explain</b> each step before we do it — or to stay quiet, if you'd rather not know.</li>
<li><b>Bring headphones</b> and listen to music during treatment.</li>
<li><b>Bring someone</b> you trust to sit with you.</li></ul>
<h2>Tips that help</h2>
<ul><li>Book a time when you're not rushed — evenings at Aashiyana suit many working patients.</li>
<li>Eat a light meal before, unless told otherwise; avoid too much tea or coffee.</li>
<li>Slow breathing helps: in for 4 counts, out for 6.</li>
<li>Start small — a cleaning or check-up first builds confidence before bigger treatment.</li>
<li>Don't wait for pain. Small problems need small treatment; waiting usually makes treatment longer.</li></ul>
<div class="card"><h3>Coming with a child?</h3><p>See our <a class="link" href="/kids/">kids' corner</a> for how to prepare children for their first visit.</p></div>
<div class="cta-row" style="margin-top:24px"><a class="btn rose" href="{wa("Hi Smile & Glow Clinic, I'm a bit nervous about dental treatment and would like a first consultation.")}" target="_blank" rel="noopener">Book a no-pressure first visit</a><a class="btn ghost" href="/before-your-visit/">Fill the before-your-visit form</a></div>
<p class="fine">Tell us on the form or when booking that you feel nervous — we'll plan extra time for you.</p>
</div>"""
    path = "/scared-of-the-dentist/"
    return path, shell(parts, lang="en", path=path, title="Scared of the Dentist? Gentle Dental Care | Smile & Glow Lucknow",
                       desc="Nervous about dental treatment? What happens at your first visit, how pain is controlled and how you stay in control at Smile & Glow, Lucknow.",
                       body=page_wrap("Scared of the dentist?", "You're not alone — and you're in charge. Here's exactly what to expect.", inner),
                       crumbs="Scared of the dentist?")


# ---------------------------------------------------------------- food for teeth and skin
def food_page(parts):
    inner = f"""<div class="prose">
<p>Dr. Pallavi is a dental surgeon and aesthetic physician with a PG Diploma in Nutrition, so food is part of every plan for teeth, skin and hair. These are simple, everyday Indian food habits that help — no expensive supplements needed.</p>

<h2>For healthy teeth and gums</h2>
<ul><li><b>How often matters more than how much sugar.</b> Sweets, biscuits, sweet chai and juice sipped through the day keep teeth under attack. Have sweets with a meal, not as snacks.</li>
<li><b>Sticky sweets</b> like toffee, chikki and gulab jamun syrup cling to teeth — rinse with water after.</li>
<li><b>Calcium:</b> milk, curd, paneer, ragi and til (sesame) support teeth and bones.</li>
<li><b>Crunchy vegetables and fruit</b> — carrot, cucumber, apple, guava — clean teeth naturally and need chewing.</li>
<li><b>Vitamin C for gums:</b> amla, guava, oranges, lemon. Bleeding gums can be a sign of poor gum health — see us rather than only changing diet.</li>
<li><b>Water</b> after meals and tea washes away sugar and acid. Fluoride toothpaste twice a day still matters most.</li>
<li><b>Tobacco, gutkha and paan</b> stain teeth, cause gum disease and mouth cancer. Ask us for help to quit.</li></ul>

<h2>For clear, healthy skin</h2>
<ul><li><b>Protein</b> at every meal — dal, chana, rajma, curd, paneer, eggs, fish or chicken — helps skin repair.</li>
<li><b>Colourful vegetables and fruit</b> (carrot, spinach, tomato, papaya, amla) give antioxidants and vitamins A and C.</li>
<li><b>Healthy fats:</b> a handful of nuts, flaxseed (alsi), walnuts or fish support the skin barrier, especially for dry skin.</li>
<li><b>Acne:</b> for some people, lots of sugary foods, refined flour (maida) and large amounts of milk can make breakouts worse. Try cutting down for 6–8 weeks and see.</li>
<li><b>Water:</b> 2–3 litres a day for most adults, more in summer. Drinking more water won't cure dry skin on its own — a moisturiser still helps.</li>
<li><b>Sun protection</b> matters more than any food for pigmentation and ageing.</li></ul>

<h2>For hair fall</h2>
<ul><li>Hair is made of protein — low protein intake is a common cause of thin hair.</li>
<li><b>Iron:</b> green leafy vegetables, beans, dates, jaggery in small amounts, and meat if you eat it. Have them with a vitamin C food (lemon, amla) to absorb more.</li>
<li><b>Vitamin D:</b> 15–20 minutes of morning sun; many people in India are low.</li>
<li><b>Crash diets</b> often cause heavy hair fall 2–3 months later.</li>
<li>Don't start iron, biotin or vitamin D tablets without checking — a simple blood test shows what you actually need.</li></ul>

<h2>For children</h2>
<ul><li>No milk or juice bottle in bed — it's a common cause of decay in toddlers.</li>
<li>Offer water between meals instead of juice or soft drinks.</li>
<li>Keep sweets for after meals; choose fruit, roasted chana or makhana as snacks.</li>
<li>Read more in our <a class="link" href="/kids/">kids' corner</a>.</li></ul>

<div class="card"><h3>Want a plan for you?</h3><p>Dr. Pallavi can suggest a simple diet plan alongside your dental, skin or hair treatment — based on your routine, budget and any blood test results.</p>
<div class="cta-row" style="margin-top:12px"><a class="btn rose" href="{wa("Hi Smile & Glow Clinic, I'd like diet advice along with my treatment.")}" target="_blank" rel="noopener">Ask on WhatsApp</a></div></div>
<p class="fine">General information for healthy adults and children. If you have diabetes, kidney disease, are pregnant or follow a medical diet, please ask your doctor first.</p>
</div>"""
    path = "/food-for-teeth-and-skin/"
    return path, shell(parts, lang="en", path=path, title="Food for Healthy Teeth, Skin & Hair | Smile & Glow Lucknow",
                       desc="Simple Indian diet tips for healthy teeth and gums, clear skin, less hair fall and kids' teeth, from Dr. Pallavi (PG Diploma in Nutrition), Lucknow.",
                       body=page_wrap("Food for healthy teeth, skin and hair", "Everyday Indian food habits that help — from a doctor trained in nutrition.", inner),
                       crumbs="Food for teeth & skin")


# ---------------------------------------------------------------- kids' corner
KIDS_JS = r"""<script>
(function(){
  const n = document.getElementById('kname'), out = document.getElementById('kwho'), d = document.getElementById('kdate');
  const f = new Date(); d.textContent = f.toLocaleDateString('en-IN', {day: 'numeric', month: 'long', year: 'numeric'});
  n.addEventListener('input', () => { out.textContent = n.value || ' '; });
  document.querySelectorAll('[data-print]').forEach(b => b.addEventListener('click', () => {
    document.body.dataset.print = b.dataset.print; window.print();
  }));
  window.addEventListener('afterprint', () => { delete document.body.dataset.print; });
})();
</script>"""


def kids_page(parts):
    days = "".join(f"<th scope=\"col\">{d}</th>" for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    rows = "".join(f"<tr><th scope=\"row\">{t}</th>" + "<td></td>" * 7 + "</tr>" for t in ["Week 1 — morning", "Week 1 — night", "Week 2 — morning", "Week 2 — night"])
    inner = f"""<style>
@media print{{
  body[data-print] main > *, body[data-print] header, body[data-print] footer{{display:none!important}}
  body[data-print] main > section.tool{{display:block!important}}
  body[data-print] .tool .wrap > *:not(.printable){{display:none!important}}
  body[data-print="chart"] .printable:not(#chart), body[data-print="cert"] .printable:not(#cert){{display:none!important}}
}}
</style>
<div class="cards no-print">
  <article class="card"><h2>When to start</h2><ul>
    <li>First dental visit: by the first birthday, or when the first tooth appears.</li>
    <li>Then a check-up every 6 months.</li>
    <li>Milk teeth matter — they hold space for adult teeth and help children eat and speak.</li></ul></article>
  <article class="card"><h2>Brushing by age</h2><ul>
    <li><b>Under 3:</b> a smear of fluoride toothpaste, the size of a grain of rice.</li>
    <li><b>3–6 years:</b> a pea-sized amount. Teach them to spit, not rinse.</li>
    <li>Brush twice a day for 2 minutes. Parents should help until about age 7–8.</li></ul></article>
  <article class="card"><h2>Preparing for the first visit</h2><ul>
    <li>Keep it positive — avoid words like "hurt", "injection" or "pain".</li>
    <li>Play "dentist" at home: count their teeth with a toothbrush.</li>
    <li>Book a morning or after-nap time when your child is fresh.</li>
    <li>Stay calm yourself — children pick up on worry.</li></ul></article>
  <article class="card"><h2>Habits that protect teeth</h2><ul>
    <li>No milk or juice bottle at bedtime.</li>
    <li>Water between meals; sweets only after meals.</li>
    <li>Ask us about fluoride varnish and sealants for back teeth.</li>
    <li>Thumb-sucking beyond age 4–5? Mention it at the check-up.</li></ul></article>
</div>

<section class="printable card" id="chart" style="margin-top:28px;max-width:900px">
  <h2>2-minute brushing chart</h2>
  <p>Tick or put a sticker each time you brush for 2 minutes. Name: ____________________</p>
  <div class="cmp-wrap"><table class="chart"><thead><tr><th></th>{days}</tr></thead><tbody>{rows}</tbody></table></div>
  <p class="fine">Smile &amp; Glow · I.T Chauraha &amp; Aashiyana, Lucknow · {PHONE_DISPLAY}</p>
  <div class="cta-row no-print" style="margin-top:12px"><button type="button" class="btn rose" data-print="chart">Print the chart</button></div>
</section>

<section class="printable" id="cert">
  <div class="cert">
    <p style="font-weight:600;color:var(--muted)">Smile &amp; Glow · Lucknow</p>
    <h2>Brave Patient Certificate</h2>
    <p>This is to certify that</p>
    <div class="who" id="kwho"> </div>
    <p>was super brave at the dentist today and is a Smile &amp; Glow star!</p>
    <p style="margin-top:16px"><span id="kdate"></span> · Dr. Pallavi</p>
  </div>
  <div class="no-print" style="max-width:720px">
    <label>Child's name<input id="kname" maxlength="40" placeholder="Type the name to add it to the certificate"></label>
    <div class="cta-row" style="margin-top:12px"><button type="button" class="btn rose" data-print="cert">Print the certificate</button></div>
  </div>
</section>

<div class="cta-row no-print" style="margin-top:28px"><a class="btn rose" href="{wa("Hi Smile & Glow Clinic, I'd like to book a dental check-up for my child.")}" target="_blank" rel="noopener">Book a check-up for your child</a><a class="btn ghost" href="/food-for-teeth-and-skin/">Food tips for kids' teeth</a></div>"""
    path = "/kids/"
    return path, shell(parts, lang="en", path=path, title="Kids' Dental Corner: Tips & Brushing Chart | Smile & Glow Lucknow",
                       desc="Kids' dental tips from Smile & Glow, Lucknow: when to start, how much toothpaste, the first visit, plus a printable brushing chart and certificate.",
                       body=page_wrap("Kids' dental corner", "Healthy milk teeth, happy visits — with a free brushing chart and a brave-patient certificate to print.", inner),
                       crumbs="Kids' corner", script=KIDS_JS)


# ---------------------------------------------------------------- review page
def review_page(parts):
    inner = f"""<div class="review-grid">
  <article class="card"><h2>I.T Chauraha</h2><p>Faizabad Rd, opp. IT Girls College, Hasanganj</p><a class="btn rose" href="{REVIEW['it']}" target="_blank" rel="noopener">Review I.T Chauraha on Google</a></article>
  <article class="card"><h2>Aashiyana</h2><p>Sector H, LDA Colony, behind Aastha Hospital</p><a class="btn rose" href="{REVIEW['aa']}" target="_blank" rel="noopener">Review Aashiyana on Google</a></article>
</div>
<div class="prose" style="margin-top:28px">
<h2>What to write</h2>
<ul><li>Which treatment you had — for example root canal, laser hair reduction or a skin consultation.</li>
<li>How you were treated and how you felt afterwards.</li>
<li>Anything that could be better — honest feedback helps us improve.</li></ul>
<p lang="hi" style="margin-top:12px">आपका रिव्यू दूसरे मरीज़ों को सही क्लिनिक चुनने में मदद करता है। अपनी ब्रांच चुनें, स्टार दें और कुछ शब्द लिखें — हिंदी या अंग्रेज़ी में।</p>
<p class="fine">Not happy with something? Please tell us directly on WhatsApp ({PHONE_DISPLAY}) so we can put it right.</p>
<p class="fine">For clinic staff: print the A5 QR poster for <a class="link" href="/assets/print/review-poster-it-chauraha.pdf">I.T Chauraha</a> or <a class="link" href="/assets/print/review-poster-aashiyana.pdf">Aashiyana</a>.</p>
</div>"""
    path = "/review/"
    doc = shell(parts, lang="en", path=path, title="Review Smile & Glow on Google | Lucknow",
                desc="Thank you for visiting Smile & Glow. Leave a Google review for our I.T Chauraha or Aashiyana clinic.",
                body=page_wrap("Thank you for visiting Smile &amp; Glow", "If you're happy with your care, a short Google review helps other patients find us. It takes a minute.", inner),
                crumbs="Leave a review")
    return path, doc.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex, follow">')


def build_extras2(root, en, hi):
    pages = [emergency_page(en, "en"), emergency_page(hi, "hi"), visit_page(en, "en"), visit_page(hi, "hi"),
             anxiety_page(en), food_page(en), kids_page(en), review_page(en)]
    for path, doc in pages:
        out = root / path.strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(doc, encoding="utf-8")
    with open(root / "assets" / "site.css", "a", encoding="utf-8") as f:
        f.write(CSS)
    return [p for p, _ in pages if p != "/review/"]
