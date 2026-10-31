"""Third set of pages (1 Nov 2026). Built by tools/build.py.

  /myth-or-fact/ + /hi/myth-or-fact/   "Myth or Fact?" game based on Dr. Pallavi's Skin Myths series
  /ask/          + /hi/ask/            "Ask Dr. Pallavi" question box, sent to the clinic on WhatsApp
"""
import json

from treatments import SITE, WHATSAPP
from extras import shell, e

CSS = """
/* ---------- Myth or Fact, Ask ---------- */
.mf-card{background:var(--surface);border-radius:var(--radius);padding:28px;max-width:720px}
.mf-prog{font-size:var(--t-s);color:var(--muted)}
.mf-q{font-family:"Playfair Display","Mukta",serif;font-size:var(--t-xl);color:var(--ink);line-height:1.3;margin:10px 0 20px}
:lang(hi) .mf-q{font-family:"Mukta",sans-serif;font-weight:700}
.mf-btns{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.mf-btns button{min-height:56px;border-radius:14px;border:2px solid var(--bg-2);background:var(--bg);color:var(--ink);font:inherit;font-weight:700;font-size:var(--t-l);cursor:pointer}
.mf-btns button:hover{border-color:var(--brand)}
.mf-btns button[disabled]{cursor:default;opacity:.6}
.mf-btns button.pick-right{border-color:#1f9d55;background:#d9f2e3;color:#14532d;opacity:1}
.mf-btns button.pick-wrong{border-color:var(--accent);background:#fde4ee;color:#7a0b3c;opacity:1}
.mf-exp{margin-top:18px;padding:16px 18px;border-radius:12px;background:var(--brand-soft)}
.mf-exp b{display:block;color:var(--ink);margin-bottom:4px}
.mf-exp p{color:var(--ink)}
.mf-next{margin-top:18px}
.mf-score{font-family:"Playfair Display","Mukta",serif;font-size:var(--t-3xl);color:var(--brand);line-height:1}
:lang(hi) .mf-score{font-family:"Mukta",sans-serif;font-weight:700}
.ask-note{max-width:760px;margin-top:16px;padding:14px 18px;border-radius:12px;background:var(--brand-soft);color:var(--ink)}
"""

# (statement, is_fact, explanation) — explanations reviewed for general accuracy; Dr. Pallavi to confirm wording
MYTHS = {
    "en": [
        ("Putting toothpaste on a pimple dries it out overnight.", False,
         "Toothpaste isn't made for skin. Ingredients like menthol and baking soda can irritate and even burn the skin, leaving a dark mark. A spot treatment with salicylic acid or benzoyl peroxide works better — or ask us."),
        ("Expensive skincare always works better than affordable products.", False,
         "Price doesn't decide results — the right ingredients for your skin type do. Many budget products work very well. Dr. Pallavi reviews products honestly on Instagram for exactly this reason."),
        ("You need sunscreen even on cloudy days and indoors near windows.", True,
         "UVA rays pass through clouds and glass. They cause tanning, pigmentation and early ageing, so a daily SPF 30+ helps even when the sun isn't strong."),
        ("Darker Indian skin doesn't need sunscreen.", False,
         "Indian skin tans and develops pigmentation and melasma easily. Daily sunscreen is one of the best ways to prevent dark spots and uneven tone."),
        ("Brushing harder cleans your teeth better.", False,
         "Hard brushing wears away enamel and pushes gums back, causing sensitivity. Brush gently with a soft brush for 2 minutes, twice a day."),
        ("Root canal treatment is extremely painful.", False,
         "Modern root canal treatment is done under local anaesthesia — most patients feel no more than a regular filling. It's the infection beforehand that hurts; treatment brings relief."),
        ("Milk teeth don't need treatment because they fall out anyway.", False,
         "Milk teeth hold space for adult teeth and help children eat and speak. Untreated decay can cause pain, infection and crooked adult teeth."),
        ("Oily skin still needs a moisturiser.", True,
         "Skipping moisturiser can make skin produce even more oil. A light, oil-free gel moisturiser keeps oily skin balanced."),
        ("Bleeding gums while brushing is normal.", False,
         "Bleeding gums are usually a sign of gum inflammation (gingivitis). A professional cleaning and better brushing can reverse it early — don't ignore it."),
        ("Laser hair reduction gives permanent results in one session.", False,
         "Hair grows in cycles, so most people need 6–8 sessions a few weeks apart. Results are long-lasting reduction, and some people need an occasional top-up."),
    ],
    "hi": [
        ("मुंहासे पर टूथपेस्ट लगाने से वह रात भर में सूख जाता है।", False,
         "टूथपेस्ट त्वचा के लिए नहीं बना। इसमें मेंथॉल और बेकिंग सोडा जैसे तत्व त्वचा में जलन कर सकते हैं और काला दाग छोड़ सकते हैं। सैलिसिलिक एसिड या बेंज़ोयल पेरॉक्साइड वाला स्पॉट ट्रीटमेंट बेहतर है — या हमसे पूछें।"),
        ("महंगे स्किनकेयर प्रोडक्ट हमेशा सस्ते प्रोडक्ट से बेहतर होते हैं।", False,
         "नतीजे कीमत से नहीं, आपकी त्वचा के हिसाब से सही तत्वों से आते हैं। कई सस्ते प्रोडक्ट बहुत अच्छा काम करते हैं। इसीलिए डॉ. पल्लवी Instagram पर ईमानदार रिव्यू करती हैं।"),
        ("बादल वाले दिन और घर में खिड़की के पास भी सनस्क्रीन ज़रूरी है।", True,
         "UVA किरणें बादलों और कांच से भी गुज़रती हैं। ये टैनिंग, पिगमेंटेशन और समय से पहले झुर्रियाँ लाती हैं, इसलिए रोज़ SPF 30+ लगाना फ़ायदेमंद है।"),
        ("सांवली भारतीय त्वचा को सनस्क्रीन की ज़रूरत नहीं होती।", False,
         "भारतीय त्वचा पर टैनिंग, पिगमेंटेशन और झाइयाँ आसानी से होती हैं। रोज़ सनस्क्रीन काले धब्बों और असमान रंगत से बचाने का सबसे अच्छा तरीका है।"),
        ("ज़ोर से ब्रश करने से दांत ज़्यादा साफ़ होते हैं।", False,
         "ज़ोर से ब्रश करने से दांतों की ऊपरी परत घिसती है और मसूड़े पीछे हटते हैं, जिससे झनझनाहट होती है। नरम ब्रश से हल्के हाथ, दिन में दो बार, 2 मिनट ब्रश करें।"),
        ("रूट कैनाल बहुत दर्दनाक होता है।", False,
         "आजकल रूट कैनाल लोकल एनेस्थीसिया में होता है — ज़्यादातर मरीज़ों को सामान्य फ़िलिंग जितना ही महसूस होता है। दर्द पहले के इन्फ़ेक्शन से होता है; इलाज से आराम मिलता है।"),
        ("दूध के दांत तो गिर ही जाएँगे, उनका इलाज ज़रूरी नहीं।", False,
         "दूध के दांत पक्के दांतों के लिए जगह बनाए रखते हैं और बच्चे को खाने-बोलने में मदद करते हैं। सड़न छोड़ने से दर्द, इन्फ़ेक्शन और टेढ़े पक्के दांत हो सकते हैं।"),
        ("ऑयली त्वचा को भी मॉइस्चराइज़र चाहिए।", True,
         "मॉइस्चराइज़र छोड़ने से त्वचा और ज़्यादा तेल बना सकती है। हल्का, ऑयल-फ़्री जेल मॉइस्चराइज़र ऑयली त्वचा को संतुलित रखता है।"),
        ("ब्रश करते समय मसूड़ों से खून आना सामान्य है।", False,
         "मसूड़ों से खून आना आमतौर पर मसूड़ों की सूजन (जिंजिवाइटिस) का संकेत है। समय पर सफ़ाई और सही ब्रशिंग से यह ठीक हो सकता है — इसे नज़रअंदाज़ न करें।"),
        ("लेज़र हेयर रिडक्शन एक ही सेशन में हमेशा के लिए बाल हटा देता है।", False,
         "बाल चक्र में उगते हैं, इसलिए ज़्यादातर लोगों को कुछ हफ़्तों के अंतर पर 6–8 सेशन लगते हैं। नतीजा लंबे समय तक बालों में कमी है, और कभी-कभी टॉप-अप की ज़रूरत पड़ती है।"),
    ],
}

MF_T = {
    "en": {"title": "Myth or Fact? Skin & Dental Quiz | Smile & Glow Lucknow",
           "desc": "10 common skin and dental beliefs — myth or fact? Play Dr. Pallavi's quick quiz, learn the truth and share your score.",
           "crumb": "Myth or Fact?", "h1": "Myth or Fact?", "lead": "10 things people believe about skin and teeth. Tap your answer and see what Dr. Pallavi says.",
           "myth": "Myth", "fact": "Fact", "q": "Statement {n} of {t}", "right": "Correct!", "wrong": "Not quite.", "isMyth": "It's a myth.", "isFact": "It's a fact.",
           "next": "Next", "see": "See my score", "score": "Your score", "of": "out of", "again": "Play again", "share": "Share on WhatsApp",
           "msgs": ["Good start — now you know the truth!", "Nice! You know your basics.", "Excellent — you could teach this!"],
           "shareText": "I scored {s}/{t} on Dr. Pallavi's Myth or Fact skin & dental quiz! Can you beat me?", "cta": "Have a question of your own?", "ask": "Ask Dr. Pallavi",
           "fine": "General information for awareness, not a diagnosis. Ask us about your own skin or teeth."},
    "hi": {"title": "मिथक या सच? त्वचा और दांत क्विज़ | स्माइल एंड ग्लो लखनऊ",
           "desc": "त्वचा और दांतों से जुड़ी 10 आम बातें — मिथक या सच? डॉ. पल्लवी का छोटा क्विज़ खेलें और अपना स्कोर शेयर करें।",
           "crumb": "मिथक या सच?", "h1": "मिथक या सच?", "lead": "त्वचा और दांतों के बारे में 10 आम बातें। जवाब चुनें और देखें डॉ. पल्लवी क्या कहती हैं।",
           "myth": "मिथक", "fact": "सच", "q": "कथन {n} / {t}", "right": "सही!", "wrong": "नहीं।", "isMyth": "यह मिथक है।", "isFact": "यह सच है।",
           "next": "आगे", "see": "मेरा स्कोर देखें", "score": "आपका स्कोर", "of": "में से", "again": "फिर से खेलें", "share": "WhatsApp पर शेयर करें",
           "msgs": ["अच्छी शुरुआत — अब आप सच जानते हैं!", "बढ़िया! आपको बुनियादी बातें पता हैं।", "शानदार — आप दूसरों को सिखा सकते हैं!"],
           "shareText": "मैंने डॉ. पल्लवी के मिथक या सच क्विज़ में {s}/{t} स्कोर किया! क्या आप मुझे हरा सकते हैं?", "cta": "अपना कोई सवाल है?", "ask": "डॉ. पल्लवी से पूछें",
           "fine": "यह सामान्य जानकारी है, जांच नहीं। अपनी त्वचा या दांतों के बारे में हमसे पूछें।"},
}

MF_JS = r"""<script>
(function(){
  const D=__D__, T=__T__, URL_=__U__, box=document.getElementById('mf'), N=D.length;
  let i=0, score=0;
  const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function q(){
    const [st,fact]=D[i];
    box.innerHTML='<p class="mf-prog">'+T.q.replace('{n}',i+1).replace('{t}',N)+'</p><p class="mf-q" id="mfq" tabindex="-1">'+esc(st)+'</p>'+
      '<div class="mf-btns"><button type="button" data-a="0">'+T.myth+'</button><button type="button" data-a="1">'+T.fact+'</button></div><div id="mfx" aria-live="polite"></div>';
    box.querySelectorAll('.mf-btns button').forEach(b=>b.addEventListener('click',()=>answer(b)));
    if(i) box.querySelector('#mfq').focus();
  }
  function answer(b){
    const fact=D[i][1], picked=b.dataset.a==='1', ok=picked===fact; if(ok) score++;
    box.querySelectorAll('.mf-btns button').forEach(x=>{x.disabled=true; if((x.dataset.a==='1')===fact) x.classList.add('pick-right'); else if(x===b) x.classList.add('pick-wrong');});
    box.querySelector('#mfx').innerHTML='<div class="mf-exp"><b>'+(ok?T.right:T.wrong)+' '+(fact?T.isFact:T.isMyth)+'</b><p>'+esc(D[i][2])+'</p></div>'+
      '<div class="mf-next"><button type="button" class="btn rose" id="mfn">'+(i===N-1?T.see:T.next)+'</button></div>';
    const n=box.querySelector('#mfn'); n.focus(); n.addEventListener('click',()=>{ i++; i<N?q():done(); });
  }
  function done(){
    const m=T.msgs[score<5?0:score<8?1:2], txt=T.shareText.replace('{s}',score).replace('{t}',N)+' '+URL_;
    box.innerHTML='<p class="mf-prog">'+T.score+'</p><p class="mf-score" id="mfs" tabindex="-1">'+score+' <small style="font-size:.4em">'+T.of+' '+N+'</small></p><p style="margin:12px 0 18px">'+m+'</p>'+
      '<div class="cta-row"><a class="btn rose" target="_blank" rel="noopener" href="https://wa.me/?text='+encodeURIComponent(txt)+'">'+T.share+'</a><button type="button" class="btn ghost" id="mfa">'+T.again+'</button></div>';
    box.querySelector('#mfa').addEventListener('click',()=>{i=0;score=0;q();});
    box.querySelector('#mfs').focus();
  }
  q();
})();
</script>"""


def myth_page(parts, lang):
    T = MF_T[lang]
    path = "/hi/myth-or-fact/" if lang == "hi" else "/myth-or-fact/"
    ask = "/hi/ask/" if lang == "hi" else "/ask/"
    body = f"""<section class="tool">
  <div class="wrap">
    <h1>{e(T['h1'])}</h1>
    <p class="lead">{e(T['lead'])}</p>
    <div class="mf-card" id="mf" aria-live="polite"><noscript>Please turn on JavaScript to play.</noscript></div>
    <p class="ask-note">{e(T['cta'])} <a class="link" href="{ask}">{e(T['ask'])}</a></p>
    <p class="fine">{e(T['fine'])}</p>
  </div>
</section>"""
    js = (MF_JS.replace("__D__", json.dumps(MYTHS[lang], ensure_ascii=False)).replace("__T__", json.dumps(T, ensure_ascii=False))
          .replace("__U__", json.dumps(SITE + path)))
    faq = [{"@type": "Question", "name": s, "acceptedAnswer": {"@type": "Answer", "text": ("Fact. " if f else "Myth. ") + x if lang == "en" else ("सच। " if f else "मिथक। ") + x}}
           for s, f, x in MYTHS[lang]]
    return path, shell(parts, lang=lang, path=path, title=T["title"], desc=T["desc"], body=body, script=js, crumbs=T["crumb"],
                       alt={"en": "/myth-or-fact/", "hi": "/hi/myth-or-fact/"},
                       ld=[{"@type": "FAQPage", "@id": f"{SITE}{path}#faq", "inLanguage": lang, "mainEntity": faq}])


ASK_T = {
    "en": {"title": "Ask Dr. Pallavi — Skin & Dental Questions | Smile & Glow Lucknow",
           "desc": "Send your skin, hair or dental question to Dr. Pallavi at Smile & Glow, Lucknow. It goes to the clinic on WhatsApp.",
           "crumb": "Ask Dr. Pallavi", "h1": "Ask Dr. Pallavi", "lead": "Got a question about your skin, hair or teeth? Send it here — it goes to the clinic on WhatsApp.",
           "name": "Your name (optional)", "topic": "Topic", "topics": ["Teeth", "Skin", "Hair", "Laser", "Products & routine", "Other"],
           "q": "Your question", "ph": "e.g. Is it safe to use vitamin C serum with sunscreen in the morning?",
           "ok": "Dr. Pallavi may answer my question in an Instagram video — without my name",
           "send": "Send on WhatsApp", "msgH": "Question for Dr. Pallavi (from the website)",
           "lblTopic": "Topic", "lblName": "Name", "lblOk": "OK to answer anonymously on Instagram", "yes": "Yes", "no": "No",
           "note1": "This is for general questions. It can't replace an examination — for treatment advice, please book a consultation.",
           "note2": "In pain, bleeding or swelling?", "emerg": "See what to do in a dental emergency",
           "fine": "Your question opens in WhatsApp for you to check before sending. Nothing is stored on this website."},
    "hi": {"title": "डॉ. पल्लवी से पूछें — त्वचा और दांत के सवाल | स्माइल एंड ग्लो लखनऊ",
           "desc": "त्वचा, बाल या दांत से जुड़ा सवाल स्माइल एंड ग्लो, लखनऊ की डॉ. पल्लवी को भेजें। यह WhatsApp पर क्लिनिक को जाता है।",
           "crumb": "डॉ. पल्लवी से पूछें", "h1": "डॉ. पल्लवी से पूछें", "lead": "त्वचा, बाल या दांतों के बारे में कोई सवाल है? यहाँ भेजें — यह WhatsApp पर क्लिनिक को जाता है।",
           "name": "आपका नाम (ज़रूरी नहीं)", "topic": "विषय", "topics": ["दांत", "त्वचा", "बाल", "लेज़र", "प्रोडक्ट और रूटीन", "अन्य"],
           "q": "आपका सवाल", "ph": "जैसे: क्या सुबह विटामिन C सीरम और सनस्क्रीन साथ लगा सकते हैं?",
           "ok": "डॉ. पल्लवी मेरे सवाल का जवाब Instagram वीडियो में दे सकती हैं — मेरे नाम के बिना",
           "send": "WhatsApp पर भेजें", "msgH": "डॉ. पल्लवी के लिए सवाल (वेबसाइट से)",
           "lblTopic": "विषय", "lblName": "नाम", "lblOk": "Instagram पर बिना नाम जवाब देना ठीक है", "yes": "हाँ", "no": "नहीं",
           "note1": "यह सामान्य सवालों के लिए है। यह जांच का विकल्प नहीं — इलाज की सलाह के लिए परामर्श बुक करें।",
           "note2": "दर्द, खून या सूजन है?", "emerg": "दांत की इमरजेंसी में क्या करें",
           "fine": "आपका सवाल WhatsApp में खुलेगा, भेजने से पहले जांच लें। वेबसाइट पर कुछ सेव नहीं होता।"},
}

ASK_JS = r"""<script>
(function(){
  const T=__T__, f=document.getElementById('askf');
  f.addEventListener('submit',e=>{
    e.preventDefault();
    const d=new FormData(f), q=(d.get('q')||'').toString().trim(); if(!q){ f.q.focus(); return; }
    const lines=[T.msgH, T.lblTopic+': '+d.get('topic')];
    if(d.get('name')) lines.push(T.lblName+': '+d.get('name'));
    lines.push('', q, '', T.lblOk+': '+(d.get('ok')?T.yes:T.no));
    window.open('https://wa.me/__WA__?text='+encodeURIComponent(lines.join('\n')),'_blank');
  });
})();
</script>"""


def ask_page(parts, lang):
    T = ASK_T[lang]
    path = "/hi/ask/" if lang == "hi" else "/ask/"
    em = "/hi/dental-emergency/" if lang == "hi" else "/dental-emergency/"
    opts = "".join(f"<option>{e(t)}</option>" for t in T["topics"])
    body = f"""<section class="tool">
  <div class="wrap">
    <h1>{e(T['h1'])}</h1>
    <p class="lead">{e(T['lead'])}</p>
    <form id="askf" class="tool-box form-grid" autocomplete="on">
      <div class="row2"><label>{e(T['name'])}<input name="name" autocomplete="given-name" maxlength="60"></label>
        <label>{e(T['topic'])}<select name="topic">{opts}</select></label></div>
      <label>{e(T['q'])}<textarea name="q" rows="5" required maxlength="1000" placeholder="{e(T['ph'])}"></textarea></label>
      <label class="bt-sound" style="color:var(--ink)"><input type="checkbox" name="ok" value="1" checked> {e(T['ok'])}</label>
      <button class="btn rose" type="submit" style="justify-self:start">{e(T['send'])}</button>
      <p class="note">{e(T['fine'])}</p>
    </form>
    <p class="ask-note">{e(T['note1'])} <b>{e(T['note2'])}</b> <a class="link" href="{em}">{e(T['emerg'])}</a></p>
  </div>
</section>"""
    js = ASK_JS.replace("__T__", json.dumps(T, ensure_ascii=False)).replace("__WA__", WHATSAPP)
    return path, shell(parts, lang=lang, path=path, title=T["title"], desc=T["desc"], body=body, script=js, crumbs=T["crumb"],
                       alt={"en": "/ask/", "hi": "/hi/ask/"})


def build_extras3(root, en, hi):
    pages = [myth_page(en, "en"), myth_page(hi, "hi"), ask_page(en, "en"), ask_page(hi, "hi")]
    for path, doc in pages:
        out = root / path.strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(doc, encoding="utf-8")
    with open(root / "assets" / "site.css", "a", encoding="utf-8") as f:
        f.write(CSS)
    return [p for p, _ in pages]
