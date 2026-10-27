/* Smile & Glow clinic assistant.
   Runs entirely in the visitor's browser: no server, no AI service, nothing stored or sent.
   Answers come from the clinic information below. Booking is handed over to WhatsApp.
   Built from tools/chat_src.js by tools/build.py (prices are filled in from tools/treatments.py). */
(function () {
  "use strict";
  if (window.__sgChat) return; window.__sgChat = true;

  var WA = "917275433783";
  var TEL = "+917275433783";
  var PHONE = "+91 72754 33783";
  var PRICES = __PRICES__;
  var PAGE_HI = (document.documentElement.lang || "").indexOf("hi") === 0;
  var HOME = PAGE_HI ? "/hi/" : "/";
  var BOOK = (location.pathname === HOME ? "" : HOME) + "#book-form";
  var MAP_IT = "https://maps.google.com/?cid=17579297340809890606";
  var MAP_AS = "https://maps.google.com/?cid=7330207607150827761";

  function wa(msg) { return "https://wa.me/" + WA + "?text=" + encodeURIComponent(msg || "Hi Smile & Glow Clinic, I'd like to book an appointment."); }
  function a(href, label, ext) { return '<a href="' + href + '"' + (ext ? ' target="_blank" rel="noopener"' : "") + ">" + label + "</a>"; }
  function priceList(slug, hi) {
    var p = PRICES[slug]; if (!p) return "";
    if (hi) return "";
    return "<ul>" + p.rows.map(function (r) { return "<li>" + r[0] + ": <b>" + r[1] + "</b></li>"; }).join("") + "</ul>";
  }
  function from(slug) { return PRICES[slug] ? PRICES[slug].from : ""; }
  var NOTE_EN = "Typical costs — your exact cost is confirmed after the check-up.";
  var NOTE_HI = "ये अनुमानित कीमतें हैं — सही कीमत जांच के बाद बताई जाती है।";

  /* ---------- Knowledge base ----------
     k: keywords (English, Hinglish and Hindi). Multi-word keys match as phrases.
     en / hi: answer HTML. act: buttons shown under the answer. */
  function treat(slug, nameEn, nameHi, en, hi, keys, waName) {
    return {
      id: slug, k: keys, treatment: true,
      en: "<b>" + nameEn + "</b> — " + en + (PRICES[slug] ? "<br>Costs at Smile &amp; Glow:" + priceList(slug) + "<small>" + NOTE_EN + "</small>" : ""),
      hi: "<b>" + nameHi + "</b> — " + hi + (PRICES[slug] ? "<br>कीमत: <b>" + from(slug) + "</b> से शुरू।<br><small>" + NOTE_HI + "</small>" : ""),
      act: [["page", PRICES[slug] ? "/" + slug + "/" : null], ["wa", waName || nameEn]]
    };
  }
  function info(id, keys, en, hi, act) { return { id: id, k: keys, en: en, hi: hi, act: act || [] }; }

  var KB = [
    info("hello", ["hi", "hello", "hey", "hii", "namaste", "namaskar", "good morning", "good evening", "नमस्ते", "नमस्कार", "हेलो"],
      "Hello! I can help with timings, addresses, treatments, prices and booking. What would you like to know?",
      "नमस्ते! मैं समय, पता, ट्रीटमेंट, कीमत और अपॉइंटमेंट के बारे में मदद कर सकता हूँ। आप क्या जानना चाहेंगे?", [["chips"]]),

    info("timings", ["time", "timing", "timings", "open", "opening", "close", "closing", "hours", "kab", "khula", "khulta", "band", "today", "aaj", "samay", "समय", "टाइम", "टाइमिंग", "खुला", "खुलता", "कब", "बंद"],
      "<b>I.T Chauraha</b>: Monday–Saturday, 11:00 AM – 3:00 PM<br><b>Aashiyana</b>: Monday–Saturday, 4:00 PM – 9:00 PM (evening)<br><b>Sunday</b>: both branches by appointment only.",
      "<b>आई.टी. चौराहा</b>: सोमवार–शनिवार, सुबह 11:00 – दोपहर 3:00<br><b>आशियाना</b>: सोमवार–शनिवार, शाम 4:00 – रात 9:00<br><b>रविवार</b>: दोनों क्लिनिक सिर्फ़ अपॉइंटमेंट पर।",
      [["form"], ["wa"]]),

    info("sunday", ["sunday", "ravivar", "itwar", "रविवार", "संडे"],
      "On Sundays both branches see patients <b>by appointment only</b>. Message us on WhatsApp to fix a Sunday slot.",
      "रविवार को दोनों क्लिनिक <b>सिर्फ़ अपॉइंटमेंट पर</b> खुलते हैं। रविवार का समय तय करने के लिए WhatsApp करें।",
      [["wa", "a Sunday appointment"]]),

    info("location", ["where", "address", "location", "locate", "direction", "directions", "map", "branch", "branches", "kahan", "kaha", "pata", "near", "पता", "कहाँ", "कहां", "लोकेशन", "ब्रांच", "रास्ता"],
      "We have two clinics in Lucknow:<br><b>I.T Chauraha</b> — Gate No. 4, 1/2 Shivsthali, Faizabad Rd, opp. IT Girls College, Hasanganj, Lucknow 226007 (" + a(MAP_IT, "map", 1) + ")<br><b>Aashiyana</b> — SS-771, behind Aastha Hospital, Sector H, LDA Colony, Lucknow 226012 (" + a(MAP_AS, "map", 1) + ")",
      "लखनऊ में हमारे दो क्लिनिक हैं:<br><b>आई.टी. चौराहा</b> — गेट नं. 4, 1/2 शिवस्थली, फ़ैज़ाबाद रोड, आई.टी. गर्ल्स कॉलेज के सामने, हसनगंज, लखनऊ 226007 (" + a(MAP_IT, "मैप", 1) + ")<br><b>आशियाना</b> — SS-771, आस्था हॉस्पिटल के पीछे, सेक्टर H, LDA कॉलोनी, लखनऊ 226012 (" + a(MAP_AS, "मैप", 1) + ")",
      [["form"]]),

    info("it", ["it chauraha", "i.t chauraha", "i.t. chauraha", "hasanganj", "faizabad", "girls college", "new hyderabad", "babuganj", "आई.टी", "आईटी", "चौराहा", "हसनगंज"],
      "<b>I.T Chauraha clinic</b><br>Gate No. 4, 1/2 Shivsthali, Faizabad Rd, opp. IT Girls College, New Hyderabad, Hasanganj, Lucknow 226007<br>Open Monday–Saturday, 11:00 AM – 3:00 PM. Sunday by appointment.<br>" + a(MAP_IT, "Get directions", 1),
      "<b>आई.टी. चौराहा क्लिनिक</b><br>गेट नं. 4, 1/2 शिवस्थली, फ़ैज़ाबाद रोड, आई.टी. गर्ल्स कॉलेज के सामने, हसनगंज, लखनऊ 226007<br>सोमवार–शनिवार, सुबह 11:00 – दोपहर 3:00। रविवार अपॉइंटमेंट पर।<br>" + a(MAP_IT, "रास्ता देखें", 1),
      [["wa", "the I.T Chauraha clinic"]]),

    info("aashiyana", ["aashiyana", "ashiyana", "asiyana", "ldA colony", "lda", "aastha", "sector h", "आशियाना", "आस्था"],
      "<b>Aashiyana clinic</b><br>SS-771, behind Aastha Hospital, Sector H, LDA Colony, Aashiyana, Lucknow 226012<br>Open Monday–Saturday, 4:00 PM – 9:00 PM. Sunday by appointment.<br>" + a(MAP_AS, "Get directions", 1),
      "<b>आशियाना क्लिनिक</b><br>SS-771, आस्था हॉस्पिटल के पीछे, सेक्टर H, LDA कॉलोनी, आशियाना, लखनऊ 226012<br>सोमवार–शनिवार, शाम 4:00 – रात 9:00। रविवार अपॉइंटमेंट पर।<br>" + a(MAP_AS, "रास्ता देखें", 1),
      [["wa", "the Aashiyana clinic"]]),

    info("book", ["book", "booking", "appointment", "slot", "consult", "consultation", "visit", "meet", "milna", "dikhana", "अपॉइंटमेंट", "बुक", "मिलना", "दिखाना", "परामर्श"],
      "You can book in three ways:<br>• WhatsApp or call <b>" + PHONE + "</b><br>• Fill the " + a(BOOK, "booking form") + " — it opens WhatsApp with your details filled in<br>We'll confirm your slot on WhatsApp.",
      "अपॉइंटमेंट के तीन तरीके:<br>• WhatsApp या कॉल करें <b>" + PHONE + "</b><br>• " + a(BOOK, "बुकिंग फ़ॉर्म") + " भरें — यह आपकी जानकारी के साथ WhatsApp खोल देता है<br>हम WhatsApp पर समय पक्का करेंगे।",
      [["wa"], ["call"], ["form"]]),

    info("contact", ["phone", "number", "call", "contact", "mobile", "whatsapp", "phone number", "nambar", "फ़ोन", "फोन", "नंबर", "कॉल", "संपर्क", "व्हाट्सएप"],
      "Call or WhatsApp us on <b>" + PHONE + "</b>. The same number works for both branches.",
      "कॉल या WhatsApp करें: <b>" + PHONE + "</b>। दोनों क्लिनिक के लिए यही नंबर है।",
      [["call"], ["wa"]]),

    info("doctor", ["doctor", "dr", "pallavi", "qualification", "qualified", "degree", "bds", "mds", "who", "experience", "registration", "dermatologist", "dentist", "डॉक्टर", "पल्लवी", "डिग्री", "कौन"],
      "<b>Dr. Pallavi</b> — BDS, MDS (Maxillofacial Medicine &amp; Radiology), FMC (Fellow in Cosmetology) and PG Diploma in Nutrition. Dental Registration No. 15199/11/02/2016.<br>She is a dental surgeon and aesthetic physician, and treats teeth, skin and hair herself.",
      "<b>डॉ. पल्लवी</b> — BDS, MDS (मैक्सिलोफ़ेशियल मेडिसिन और रेडियोलॉजी), FMC (कॉस्मेटोलॉजी फ़ेलो) और पोषण में PG डिप्लोमा। डेंटल रजिस्ट्रेशन नं. 15199/11/02/2016।<br>वे डेंटल सर्जन और एस्थेटिक फ़िज़िशियन हैं, और दांत, त्वचा व बालों का इलाज खुद करती हैं।",
      [["link", HOME + "#about", PAGE_HI ? "डॉ. पल्लवी के बारे में" : "About Dr. Pallavi"]]),

    info("prices", ["price", "prices", "cost", "costs", "fee", "fees", "charge", "charges", "rate", "rates", "kitna", "kitne", "paisa", "paise", "rupees", "budget", "cheap", "कीमत", "फीस", "फ़ीस", "खर्च", "कितना", "कितने", "रेट", "पैसे", "चार्ज"],
      "Starting prices at Smile &amp; Glow:<ul>" +
        "<li>" + a("/root-canal-treatment-lucknow/", "Root canal") + ": from " + from("root-canal-treatment-lucknow") + "</li>" +
        "<li>" + a("/dental-implants-lucknow/", "Dental implant") + ": from " + from("dental-implants-lucknow") + "</li>" +
        "<li>" + a("/teeth-whitening-lucknow/", "Teeth whitening") + ": from " + from("teeth-whitening-lucknow") + "</li>" +
        "<li>" + a("/laser-hair-removal-lucknow/", "Laser hair reduction") + ": from " + from("laser-hair-removal-lucknow") + "</li>" +
        "<li>" + a("/hair-prp-treatment-lucknow/", "Hair PRP") + ": from " + from("hair-prp-treatment-lucknow") + "</li>" +
        "<li>" + a("/chemical-peel-lucknow/", "Chemical peel") + ": from " + from("chemical-peel-lucknow") + "</li></ul>" +
        "<small>" + NOTE_EN + " For other treatments, ask us on WhatsApp.</small>",
      "Smile &amp; Glow में शुरुआती कीमतें:<ul>" +
        "<li>" + a("/root-canal-treatment-lucknow/", "रूट कैनाल") + ": " + from("root-canal-treatment-lucknow") + " से</li>" +
        "<li>" + a("/dental-implants-lucknow/", "डेंटल इम्प्लांट") + ": " + from("dental-implants-lucknow") + " से</li>" +
        "<li>" + a("/teeth-whitening-lucknow/", "दांतों की सफ़ेदी") + ": " + from("teeth-whitening-lucknow") + " से</li>" +
        "<li>" + a("/laser-hair-removal-lucknow/", "लेज़र हेयर रिडक्शन") + ": " + from("laser-hair-removal-lucknow") + " से</li>" +
        "<li>" + a("/hair-prp-treatment-lucknow/", "हेयर PRP") + ": " + from("hair-prp-treatment-lucknow") + " से</li>" +
        "<li>" + a("/chemical-peel-lucknow/", "केमिकल पील") + ": " + from("chemical-peel-lucknow") + " से</li></ul>" +
        "<small>" + NOTE_HI + " दूसरे ट्रीटमेंट के लिए WhatsApp पर पूछें।</small>",
      [["wa", "treatment prices"]]),

    treat("root-canal-treatment-lucknow", "Root canal treatment (RCT)", "रूट कैनाल ट्रीटमेंट (RCT)",
      "saves an infected tooth instead of pulling it out. Done under local anaesthesia, so most patients feel little more than a regular filling. Usually 1–2 visits.",
      "संक्रमित दांत को निकालने के बजाय बचाता है। लोकल एनेस्थीसिया में होता है, इसलिए ज़्यादातर मरीज़ों को सामान्य फ़िलिंग जितना ही महसूस होता है। आमतौर पर 1–2 विज़िट।",
      ["root canal", "rct", "root", "canal", "toothache", "tooth pain", "dant dard", "daant dard", "infection", "रूट", "कैनाल", "दांत दर्द", "दाँत दर्द"], "root canal treatment"),
    treat("dental-implants-lucknow", "Dental implants", "डेंटल इम्प्लांट",
      "permanent, natural-looking replacements for missing teeth that restore your bite.",
      "गायब दांतों के लिए स्थायी, प्राकृतिक दिखने वाला विकल्प, जिससे चबाना फिर आसान हो।",
      ["implant", "implants", "missing tooth", "missing teeth", "new tooth", "naya dant", "इम्प्लांट", "नया दांत"], "dental implants"),
    treat("teeth-whitening-lucknow", "Teeth whitening", "दांतों की सफ़ेदी",
      "safe, professional whitening that lifts stains and brightens your smile.",
      "सुरक्षित, प्रोफ़ेशनल व्हाइटनिंग जो दाग हटाकर मुस्कान को चमकाए।",
      ["whitening", "whiten", "white teeth", "yellow teeth", "stains", "bleaching", "peele dant", "सफ़ेदी", "सफेदी", "पीले दांत", "व्हाइटनिंग"], "teeth whitening"),
    treat("laser-hair-removal-lucknow", "Laser hair reduction", "लेज़र हेयर रिडक्शन",
      "long-lasting reduction of unwanted hair on face and body, with a cooled handpiece for comfort. Usually 6–8 sessions.",
      "चेहरे और शरीर के अनचाहे बालों में लंबे समय तक कमी, ठंडे हैंडपीस के साथ। आमतौर पर 6–8 सेशन।",
      ["laser hair", "hair removal", "hair reduction", "unwanted hair", "facial hair", "upper lip", "underarm", "underarms", "waxing", "बाल हटाना", "अनचाहे बाल", "लेज़र हेयर"], "laser hair reduction"),
    treat("hair-prp-treatment-lucknow", "Hair PRP", "हेयर PRP",
      "therapy using your own platelet-rich plasma to help reduce hair fall and support thicker regrowth. Usually 4–6 sessions a month apart.",
      "आपके अपने प्लेटलेट-रिच प्लाज़्मा से बालों का झड़ना कम करने और घने बाल उगाने में मदद। आमतौर पर महीने में एक बार, 4–6 सेशन।",
      ["hair prp", "hair fall", "hairfall", "hair loss", "baldness", "thinning", "baal jhadna", "bal jhadna", "बाल झड़ना", "झड़ना", "गंजापन", "हेयर पीआरपी"], "hair PRP"),
    treat("chemical-peel-lucknow", "Chemical peels", "केमिकल पील",
      "clinical peels for pigmentation, tan, dullness, acne and uneven tone. Light peels have little or no downtime.",
      "पिगमेंटेशन, टैनिंग, रूखापन, मुंहासे और असमान रंगत के लिए क्लिनिकल पील। हल्के पील में लगभग कोई डाउनटाइम नहीं।",
      ["peel", "peels", "chemical", "tan", "tanning", "pigmentation", "dullness", "glycolic", "salicylic", "पील", "केमिकल", "टैनिंग", "पिगमेंटेशन"], "a chemical peel"),

    treat("smile", "Smile makeover", "स्माइल मेकओवर", "veneers, bonding, crowns and smile design.", "विनियर, बॉन्डिंग, क्राउन और स्माइल डिज़ाइन।",
      ["smile makeover", "veneer", "veneers", "bonding", "crown", "crowns", "cap", "gap", "smile design", "मेकओवर", "क्राउन", "विनियर"], "a smile makeover"),
    treat("kids", "Kids &amp; family dentistry", "बच्चों और परिवार के लिए दंत चिकित्सा", "check-ups, cleaning and fillings for the whole family.", "पूरे परिवार के लिए जांच, सफ़ाई और फ़िलिंग।",
      ["kid", "kids", "child", "children", "baby", "family", "cleaning", "scaling", "filling", "cavity", "check up", "checkup", "बच्चे", "बच्चों", "सफ़ाई", "फ़िलिंग", "कीड़ा"], "a dental check-up"),
    treat("oral", "Oral medicine &amp; radiology", "ओरल मेडिसिन और रेडियोलॉजी", "diagnosis of mouth ulcers, oral lesions and jaw problems, with dental X-ray evaluation.", "मुंह के छाले, मुंह के घाव और जबड़े की समस्याओं की जांच, डेंटल एक्स-रे के साथ।",
      ["ulcer", "ulcers", "mouth ulcer", "lesion", "jaw", "x-ray", "xray", "oral medicine", "chhale", "छाले", "जबड़ा", "एक्स-रे"], "an oral medicine consultation"),
    treat("acne", "Acne &amp; scar care", "मुंहासे और दाग की देखभाल", "personalised plans to control active acne and reduce marks and scars.", "मुंहासों को नियंत्रित करने और दाग-धब्बे कम करने का व्यक्तिगत प्लान।",
      ["acne", "pimple", "pimples", "scar", "scars", "marks", "breakout", "muhase", "dane", "मुंहासे", "पिंपल", "दाग", "दाने"], "acne treatment"),
    treat("ageing", "Anti-ageing", "एंटी-एजिंग", "treatments for fine lines, wrinkles and sagging skin.", "बारीक रेखाओं, झुर्रियों और ढीली त्वचा के लिए ट्रीटमेंट।",
      ["ageing", "aging", "anti ageing", "anti-ageing", "wrinkle", "wrinkles", "fine lines", "sagging", "jhurriyan", "झुर्रियां", "झुर्रियाँ", "एंटी"], "anti-ageing treatment"),
    treat("faceprp", "Face PRP &amp; glow facials", "फ़ेस PRP और ग्लो फ़ेशियल", "collagen-boosting treatments to improve texture and restore a natural glow.", "कोलेजन बढ़ाने वाले ट्रीटमेंट, जो त्वचा की बनावट सुधारें और प्राकृतिक चमक लौटाएँ।",
      ["face prp", "vampire", "glow", "facial", "facials", "dull skin", "texture", "ग्लो", "फ़ेशियल", "फेशियल", "चमक"], "face PRP"),
    treat("skincare", "Skincare consultation", "स्किनकेयर परामर्श", "a routine that suits your skin and budget — no unnecessary products. Many affordable products work well when chosen for your skin type.", "आपकी त्वचा और बजट के हिसाब से रूटीन — बेवजह के प्रोडक्ट नहीं। सही चुने जाएँ तो सस्ते प्रोडक्ट भी अच्छा काम करते हैं।",
      ["skincare", "skin care", "routine", "product", "products", "sunscreen", "moisturiser", "moisturizer", "serum", "cream", "dry skin", "oily skin", "स्किनकेयर", "रूटीन", "क्रीम", "सनस्क्रीन"], "a skincare consultation"),

    treat("toning", "Laser toning", "लेज़र टोनिंग", "for pigmentation, melasma, tan and uneven tone, with little or no downtime.", "पिगमेंटेशन, मेलाज़्मा, टैन और असमान रंगत के लिए, लगभग बिना डाउनटाइम।",
      ["toning", "laser toning", "melasma", "uneven tone", "झाइयां", "झाइयाँ", "टोनिंग", "मेलाज़्मा"], "laser toning"),
    treat("carbon", "Carbon laser peel", "कार्बन लेज़र पील", "deep-cleans pores, controls oil and gives instant glow. Also called the \"Hollywood peel\".", "रोमछिद्रों की गहरी सफ़ाई, तेल नियंत्रण और तुरंत चमक। इसे \"हॉलीवुड पील\" भी कहते हैं।",
      ["carbon", "hollywood", "pores", "open pores", "oil control", "कार्बन", "हॉलीवुड"], "a carbon laser peel"),
    treat("fractional", "Fractional laser resurfacing", "फ़्रैक्शनल लेज़र", "triggers new collagen to smooth acne scars, open pores and fine lines over a few sessions.", "नया कोलेजन बनाकर कुछ सेशन में मुंहासों के गड्ढे, खुले रोमछिद्र और बारीक रेखाएँ कम करता है।",
      ["fractional", "resurfacing", "acne scars", "pits", "gaddhe", "फ़्रैक्शनल", "गड्ढे"], "fractional laser"),
    treat("ipl", "IPL photofacial", "IPL फ़ोटोफ़ेशियल", "broad-spectrum light that targets redness, sun spots and dullness.", "लालिमा, धूप के धब्बे और रूखेपन पर काम करने वाली ब्रॉड-स्पेक्ट्रम लाइट।",
      ["ipl", "photofacial", "redness", "sun spots", "sunspots", "फ़ोटोफ़ेशियल"], "an IPL photofacial"),
    treat("tattoo", "Laser tattoo removal", "लेज़र टैटू रिमूवल", "breaks tattoo ink into fine particles that the body clears over several spaced-out sessions.", "टैटू की स्याही को बारीक कणों में तोड़ता है, जिन्हें शरीर कई सेशन में साफ़ कर देता है।",
      ["tattoo", "tatoo", "tattoos", "टैटू"], "laser tattoo removal"),

    info("laser", ["laser", "lasers", "laser treatment", "laser treatments", "लेज़र", "लेजर"],
      "Our laser and light treatments: laser hair reduction (from " + from("laser-hair-removal-lucknow") + " a session), laser toning, carbon laser peel, fractional laser resurfacing, IPL photofacial and laser tattoo removal. Every laser plan starts with a skin assessment and a patch test.",
      "हमारे लेज़र ट्रीटमेंट: लेज़र हेयर रिडक्शन (" + from("laser-hair-removal-lucknow") + " प्रति सेशन से), लेज़र टोनिंग, कार्बन लेज़र पील, फ़्रैक्शनल लेज़र, IPL फ़ोटोफ़ेशियल और लेज़र टैटू रिमूवल। हर लेज़र प्लान स्किन जांच और पैच टेस्ट से शुरू होता है।",
      [["link", HOME + "#laser", PAGE_HI ? "लेज़र ट्रीटमेंट देखें" : "See laser treatments"], ["wa", "a laser treatment"]]),

    info("treatments", ["treatment", "treatments", "service", "services", "what do you do", "offer", "ilaj", "इलाज", "ट्रीटमेंट", "सेवाएं", "सेवाएँ"],
      "<b>Dental</b>: root canal, implants, teeth whitening, smile makeover, oral medicine &amp; X-ray, kids &amp; family dentistry.<br><b>Skin &amp; hair</b>: chemical peels, acne &amp; scars, anti-ageing, face PRP, hair PRP, skincare consultation.<br><b>Laser</b>: hair reduction, toning, carbon peel, fractional laser, IPL, tattoo removal.",
      "<b>दांत</b>: रूट कैनाल, इम्प्लांट, दांतों की सफ़ेदी, स्माइल मेकओवर, ओरल मेडिसिन और एक्स-रे, बच्चों की दंत चिकित्सा।<br><b>त्वचा और बाल</b>: केमिकल पील, मुंहासे और दाग, एंटी-एजिंग, फ़ेस PRP, हेयर PRP, स्किनकेयर परामर्श।<br><b>लेज़र</b>: हेयर रिडक्शन, टोनिंग, कार्बन पील, फ़्रैक्शनल लेज़र, IPL, टैटू रिमूवल।",
      [["link", HOME + "#services", PAGE_HI ? "सभी ट्रीटमेंट" : "All treatments"]]),

    info("pain", ["painful", "pain", "hurt", "hurts", "dard", "dukhega", "scared", "fear", "dar", "दर्द", "डर", "दुखेगा"],
      "Most treatments are comfortable. Root canal treatment is done under local anaesthesia, so most patients feel little more than a regular filling — it's usually the infection beforehand that hurts. Laser hair reduction uses a cooled handpiece. Tell Dr. Pallavi if you're anxious and she'll go step by step — and see our page for " + a("/scared-of-the-dentist/", "nervous patients") + ".",
      "ज़्यादातर ट्रीटमेंट आरामदायक होते हैं। रूट कैनाल लोकल एनेस्थीसिया में होता है, इसलिए ज़्यादातर मरीज़ों को सामान्य फ़िलिंग जितना ही महसूस होता है — दर्द आमतौर पर पहले के इन्फ़ेक्शन से होता है। लेज़र हेयर रिडक्शन में ठंडा हैंडपीस इस्तेमाल होता है। घबराहट हो तो डॉ. पल्लवी को बताएँ — घबराहट वाले मरीज़ों के लिए " + a("/scared-of-the-dentist/", "यह पेज") + " (अंग्रेज़ी) देखें।",
      [["wa"]]),

    info("indian", ["indian skin", "dark skin", "brown skin", "skin type", "safe", "side effect", "side effects", "patch test", "सुरक्षित", "साइड इफ़ेक्ट", "साइड इफेक्ट"],
      "Every laser plan starts with a skin assessment and a patch test, and the settings are chosen for your skin type. If laser isn't the right option for you, Dr. Pallavi will tell you.",
      "हर लेज़र प्लान स्किन जांच और पैच टेस्ट से शुरू होता है, और सेटिंग आपकी त्वचा के हिसाब से चुनी जाती है। अगर लेज़र आपके लिए सही नहीं है, तो डॉ. पल्लवी साफ़ बता देंगी।",
      [["wa", "a skin assessment"]]),

    info("downtime", ["downtime", "recovery", "work after", "office", "redness after", "peeling", "aftercare", "डाउनटाइम", "रिकवरी"],
      "Light chemical peels and laser toning usually have little or no downtime — perhaps mild redness or flaking for a few days. After a root canal most people return to work the same day. You'll get clear aftercare instructions, including sun protection.",
      "हल्के केमिकल पील और लेज़र टोनिंग में आमतौर पर लगभग कोई डाउनटाइम नहीं होता — कुछ दिन हल्की लालिमा या पपड़ी हो सकती है। रूट कैनाल के बाद ज़्यादातर लोग उसी दिन काम पर लौट जाते हैं। आपको धूप से बचाव समेत पूरी देखभाल की जानकारी दी जाएगी।",
      []),

    info("both", ["both", "same visit", "one visit", "dental and skin", "skin and dental", "together", "dono", "दोनों", "एक साथ"],
      "Yes — that's the idea behind Smile &amp; Glow. Tell us both concerns when you book and we'll plan your visit accordingly.",
      "हाँ — Smile &amp; Glow का यही मकसद है। बुक करते समय दोनों समस्याएँ बताएँ, हम उसी हिसाब से आपकी विज़िट प्लान करेंगे।",
      [["wa", "a combined dental + skin visit"], ["form"]]),

    info("language", ["hindi", "english", "language", "bhasha", "हिंदी", "भाषा", "अंग्रेज़ी"],
      "Consultations are available in both Hindi and English. You can also ask me in Hindi.",
      "परामर्श हिंदी और अंग्रेज़ी दोनों में होता है। आप मुझसे हिंदी में भी पूछ सकते हैं।",
      [["link", PAGE_HI ? "/" : "/hi/", PAGE_HI ? "English website" : "हिंदी वेबसाइट"]]),

    info("instagram", ["instagram", "insta", "reels", "videos", "follow", "इंस्टाग्राम"],
      "Dr. Pallavi shares daily skin and dental tips, honest product reviews and Hindi explainers on Instagram: " + a("https://www.instagram.com/smileandglowclinic/", "@smileandglowclinic", 1),
      "डॉ. पल्लवी Instagram पर रोज़ स्किन और डेंटल टिप्स, ईमानदार प्रोडक्ट रिव्यू और हिंदी वीडियो शेयर करती हैं: " + a("https://www.instagram.com/smileandglowclinic/", "@smileandglowclinic", 1),
      []),

    info("reviews", ["review", "reviews", "rating", "ratings", "google", "good", "best", "रिव्यू", "रेटिंग"],
      "Patients rate us <b>4.9★</b> on Google at I.T Chauraha (14 reviews) and <b>5.0★</b> at Aashiyana (15 reviews).",
      "Google पर मरीज़ों ने आई.टी. चौराहा को <b>4.9★</b> (14 रिव्यू) और आशियाना को <b>5.0★</b> (15 रिव्यू) दिए हैं।",
      [["link", MAP_IT, PAGE_HI ? "Google रिव्यू" : "Read Google reviews", 1], ["link", "/review/", PAGE_HI ? "रिव्यू लिखें" : "Write a review"]]),

    info("calculator", ["calculator", "calculate", "estimate", "total cost", "total price", "how much total", "kul kharch", "कैलकुलेटर", "कुल खर्च", "अनुमान"],
      "Use our " + a(PAGE_HI ? "/hi/cost-calculator/" : "/cost-calculator/", "cost calculator") + " — pick a treatment, the option and the number of teeth or sessions, and it shows the price range. You can send the estimate to us on WhatsApp.",
      "हमारा " + a("/hi/cost-calculator/", "कीमत कैलकुलेटर") + " इस्तेमाल करें — ट्रीटमेंट, विकल्प और दांत या सेशन की संख्या चुनें, और अनुमानित कीमत देखें। अनुमान WhatsApp पर भी भेज सकते हैं।",
      [["link", PAGE_HI ? "/hi/cost-calculator/" : "/cost-calculator/", PAGE_HI ? "कैलकुलेटर खोलें" : "Open the calculator"]]),

    info("quiz", ["skin type", "quiz", "my skin", "oily", "dry", "combination skin", "sensitive skin", "which skin", "skin test", "त्वचा का प्रकार", "क्विज़", "ऑयली", "रूखी", "स्किन टाइप"],
      "Take our free " + a(PAGE_HI ? "/hi/skin-quiz/" : "/skin-quiz/", "skin type quiz") + " — six questions, then you get your likely skin type and a simple morning and night routine.",
      "हमारा मुफ़्त " + a("/hi/skin-quiz/", "स्किन टाइप क्विज़") + " करें — छह सवाल, फिर आपकी त्वचा का प्रकार और सुबह-रात का आसान रूटीन।",
      [["link", PAGE_HI ? "/hi/skin-quiz/" : "/skin-quiz/", PAGE_HI ? "क्विज़ शुरू करें" : "Start the quiz"]]),

    info("aftercare", ["aftercare", "after care", "after treatment", "care after", "instructions", "precautions", "what to do after", "parhez", "परहेज़", "परहेज", "देखभाल", "बाद में क्या"],
      "Aftercare for root canal, implants, whitening, laser hair reduction, hair PRP and chemical peels is on our " + a("/aftercare/", "aftercare page") + ", in English and Hindi. Always follow any specific instructions Dr. Pallavi gives you.",
      "रूट कैनाल, इम्प्लांट, व्हाइटनिंग, लेज़र, हेयर PRP और केमिकल पील के बाद की देखभाल हमारे " + a("/aftercare/", "देखभाल पेज") + " पर हिंदी और अंग्रेज़ी में है। डॉ. पल्लवी के बताए ख़ास निर्देश हमेशा मानें।",
      [["link", "/aftercare/", PAGE_HI ? "देखभाल पेज" : "Aftercare page"], ["call"]]),

    info("guide", ["which treatment", "which is better", "difference", "vs", "versus", "or bridge", "bridge", "denture", "filling", "extraction", "kaun sa", "konsa", "कौन सा", "फ़र्क", "अंतर"],
      "Our " + a("/treatment-guide/", "treatment guide") + " compares the choices patients ask about most: implant vs bridge vs denture, filling vs root canal, whitening vs veneers, peel vs laser toning, laser vs waxing, and hair PRP. Dr. Pallavi confirms the best option at your check-up.",
      "हमारे " + a("/hi/samjhiye/", "आसान भाषा में समझिए") + " पेज पर रूट कैनाल, इम्प्लांट, व्हाइटनिंग, लेज़र, पील और हेयर PRP की सरल हिंदी जानकारी है। अंग्रेज़ी में " + a("/treatment-guide/", "तुलना गाइड") + " भी है। सही विकल्प डॉ. पल्लवी जांच में बताएँगी।",
      [["link", PAGE_HI ? "/hi/samjhiye/" : "/treatment-guide/", PAGE_HI ? "आसान भाषा में समझिए" : "Open the guide"]]),

    info("previsit", ["medical history", "history form", "before visit", "before my visit", "what to bring", "what should i bring", "documents", "क्या लाना", "मेडिकल हिस्ट्री"],
      "Fill our 2-minute " + a(PAGE_HI ? "/hi/before-your-visit/" : "/before-your-visit/", "before-your-visit form") + " — it sends your medical history to us on WhatsApp so check-in is quicker. Bring your medicine strips and any old reports or X-rays.",
      "2 मिनट का " + a("/hi/before-your-visit/", "विज़िट से पहले फ़ॉर्म") + " भरें — यह आपकी मेडिकल जानकारी WhatsApp पर हमें भेज देता है। अपनी दवाओं के पत्ते और पुरानी रिपोर्ट या एक्स-रे साथ लाएँ।",
      [["link", PAGE_HI ? "/hi/before-your-visit/" : "/before-your-visit/", PAGE_HI ? "फ़ॉर्म खोलें" : "Open the form"]]),

    info("diet", ["diet", "food", "nutrition", "vitamin", "vitamins", "protein", "khana", "khaana", "डाइट", "पोषण", "विटामिन", "खान-पान"],
      "Dr. Pallavi also has a PG Diploma in Nutrition. See " + a("/food-for-teeth-and-skin/", "food for healthy teeth, skin and hair") + " for simple Indian diet tips — or ask for a diet plan with your treatment.",
      "डॉ. पल्लवी के पास पोषण में PG डिप्लोमा भी है। दांत, त्वचा और बालों के लिए आसान भारतीय खान-पान टिप्स " + a("/food-for-teeth-and-skin/", "यहाँ") + " (अंग्रेज़ी) देखें — या इलाज के साथ डाइट प्लान पूछें।",
      [["link", "/food-for-teeth-and-skin/", PAGE_HI ? "खान-पान टिप्स" : "Diet tips"], ["wa", "diet advice"]]),

    info("kidscorner", ["brushing chart", "certificate", "toothpaste", "kids corner", "baby teeth", "milk teeth", "milk tooth", "toddler", "दूध के दांत", "टूथपेस्ट"],
      "Our " + a("/kids/", "kids' corner") + " has first-visit tips, how much toothpaste to use by age, a printable 2-minute brushing chart and a brave-patient certificate.",
      "हमारे " + a("/kids/", "बच्चों के कोने") + " (अंग्रेज़ी) में पहली विज़िट के टिप्स, उम्र के हिसाब से टूथपेस्ट की मात्रा, ब्रशिंग चार्ट और सर्टिफ़िकेट है।",
      [["link", "/kids/", PAGE_HI ? "बच्चों का कोना" : "Kids' corner"], ["wa", "a check-up for my child"]]),

    info("thanks", ["thanks", "thank", "thank you", "ok", "okay", "great", "bye", "dhanyavad", "shukriya", "धन्यवाद", "शुक्रिया", "ठीक"],
      "You're welcome! If you need anything else, just ask — or message us on WhatsApp.",
      "आपका स्वागत है! कुछ और पूछना हो तो बेझिझक पूछें — या WhatsApp करें।",
      [])
  ];

  var URGENT = ["swelling", "swollen", "bleeding", "unbearable", "severe", "emergency", "urgent", "accident", "broken tooth", "fever", "sujan", "soojan", "khoon", "सूजन", "खून", "इमरजेंसी", "बहुत दर्द", "तेज़ दर्द"];
  var URGENT_EN = "If it's urgent, please <b>call us now on " + a("tel:" + TEL, PHONE) + "</b> so we can fit you in. For heavy bleeding, swelling that affects breathing or swallowing, a high fever or an injury, go to the nearest hospital emergency department straight away.";
  var URGENT_HI = "अगर तुरंत ज़रूरत है, तो <b>अभी कॉल करें " + a("tel:" + TEL, PHONE) + "</b> ताकि हम जल्दी समय दे सकें। ज़्यादा खून बहने, सांस या निगलने में दिक्कत वाली सूजन, तेज़ बुखार या चोट में तुरंत नज़दीकी अस्पताल की इमरजेंसी में जाएँ।";
  var FALLBACK_EN = "Sorry, I'm not sure about that. I can answer questions on timings, addresses, treatments, prices and booking — or you can ask the clinic directly on WhatsApp. I can't diagnose problems; Dr. Pallavi will advise you at your consultation.";
  var FALLBACK_HI = "माफ़ कीजिए, इसकी जानकारी मेरे पास नहीं है। मैं समय, पता, ट्रीटमेंट, कीमत और अपॉइंटमेंट के बारे में बता सकता हूँ — या आप सीधे WhatsApp पर क्लिनिक से पूछ सकते हैं। मैं बीमारी की जांच नहीं कर सकता; डॉ. पल्लवी परामर्श में सलाह देंगी।";

  var CHIPS_EN = [["Timings", "timings"], ["Locations", "address"], ["Prices", "prices"], ["Book appointment", "book appointment"], ["Laser", "laser"], ["About the doctor", "doctor"]];
  var CHIPS_HI = [["समय", "समय"], ["पता", "पता"], ["कीमत", "कीमत"], ["अपॉइंटमेंट", "अपॉइंटमेंट"], ["लेज़र", "लेज़र"], ["डॉक्टर", "डॉक्टर"]];

  /* ---------- Matching ---------- */
  function norm(s) { return (" " + s.toLowerCase().replace(/[’']/g, "").replace(/[^\p{L}\p{N}\p{M}.\- ]+/gu, " ").replace(/\s+/g, " ") + " "); }
  function lev1(x, y) { // edit distance <= 1, or one swapped pair of letters
    if (Math.abs(x.length - y.length) > 1) return false;
    if (x.length === y.length) {
      var diff = []; for (var n = 0; n < x.length; n++) if (x[n] !== y[n]) diff.push(n);
      if (diff.length === 2 && diff[1] === diff[0] + 1 && x[diff[0]] === y[diff[1]] && x[diff[1]] === y[diff[0]]) return true;
    }
    var i = 0, j = 0, d = 0;
    while (i < x.length && j < y.length) {
      if (x[i] === y[j]) { i++; j++; continue; }
      if (++d > 1) return false;
      if (x.length > y.length) i++; else if (y.length > x.length) j++; else { i++; j++; }
    }
    return d + (x.length - i) + (y.length - j) <= 1;
  }
  function score(text, words, item) {
    var s = 0, used = {};
    item.k.forEach(function (k) {
      k = k.toLowerCase();
      if (k.indexOf(" ") > -1 || /[^\x00-\x7f]/.test(k)) {
        if (text.indexOf(" " + k) > -1 || (/[^\x00-\x7f]/.test(k) && text.indexOf(k) > -1)) {
          s += k.indexOf(" ") > -1 ? 3 : 2;
          k.split(" ").forEach(function (part) { var n = words.indexOf(part); if (n > -1) used[n] = 1; }); // a phrase uses up its words
        }
        return;
      }
      for (var i = 0; i < words.length; i++) {
        var w = words[i]; if (used[i]) continue;
        if (w === k) { s += 2; used[i] = 1; return; }
        if (k.length >= 5 && w.length >= 5 && (w.indexOf(k) === 0 || k.indexOf(w) === 0 || lev1(w, k))) { s += 1; used[i] = 1; return; }
      }
    });
    return s;
  }
  function answer(q) {
    var text = norm(q), words = text.trim().split(" ");
    var hi = PAGE_HI || /[ऀ-ॿ]/.test(q);
    if (URGENT.some(function (u) { return text.indexOf(u) > -1; })) return { html: hi ? URGENT_HI : URGENT_EN, act: [["call"], ["link", hi ? "/hi/dental-emergency/" : "/dental-emergency/", hi ? "अभी क्या करें" : "What to do now"], ["wa", "an urgent appointment"]], hi: hi };
    var best = null, bestS = 0;
    KB.forEach(function (item) {
      var s = score(text, words, item);
      if ((item.treatment || item.id === "it" || item.id === "aashiyana" || item.id === "sunday") && s) s += 0.5; // specific beats generic ("price", "timing")
      if (/^(calculator|quiz|aftercare|guide|previsit|diet|kidscorner)$/.test(item.id) && s) s += 2;                          // tools beat the topic they're about
      if (s > bestS) { best = item; bestS = s; }
    });
    if (!best) return { html: hi ? FALLBACK_HI : FALLBACK_EN, act: [["wa"], ["chips"]], hi: hi };
    return { html: hi ? best.hi : best.en, act: best.act, hi: hi };
  }

  /* ---------- UI ---------- */
  var css = "" +
    ".sgc-launch{position:fixed;right:20px;bottom:88px;z-index:31;display:inline-flex;align-items:center;gap:8px;min-height:48px;padding:0 18px 0 14px;border:0;border-radius:999px;background:var(--brand,#1b5c8c);color:var(--brand-ink,#fff);font-family:inherit;font-size:1rem;font-weight:600;line-height:1;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.18)}" +
    ".sgc-launch:hover{filter:brightness(1.08)}" +
    ".sgc-panel{position:fixed;right:20px;bottom:88px;z-index:32;width:min(380px,calc(100vw - 32px));height:min(560px,calc(100vh - 120px));display:flex;flex-direction:column;background:var(--surface,#fff);color:var(--ink,#1d2733);border-radius:18px;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,.25);font-family:inherit}" +
    ".sgc-panel[hidden]{display:none}" +
    ".sgc-head{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:12px 8px 12px 16px;background:var(--brand,#1b5c8c);color:var(--brand-ink,#fff)}" +
    ".sgc-head b{display:block;font-size:1rem}.sgc-head small{display:block;font-size:.875rem;opacity:.9}" +
    ".sgc-x{width:44px;height:44px;border:0;background:transparent;color:inherit;font-size:1.5rem;cursor:pointer;border-radius:10px}" +
    ".sgc-log{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:10px;background:var(--bg,#f8f9fb);overscroll-behavior:contain}" +
    ".sgc-m{max-width:88%;padding:10px 14px;border-radius:14px;font-size:.9375rem;line-height:1.5;overflow-wrap:anywhere}" +
    ".sgc-bot{align-self:flex-start;background:var(--surface,#fff);color:var(--ink,#1d2733);border-bottom-left-radius:4px}" +
    ".sgc-me{align-self:flex-end;background:var(--brand,#1b5c8c);color:var(--brand-ink,#fff);border-bottom-right-radius:4px}" +
    ".sgc-bot a{color:var(--accent-text,#b0105a);font-weight:600}" +
    ".sgc-bot ul{margin:6px 0 6px 18px}.sgc-bot small{display:block;color:var(--muted,#525d6b);font-size:.875rem;margin-top:6px}" +
    ".sgc-acts{display:flex;flex-wrap:wrap;gap:8px;align-self:flex-start;max-width:100%}" +
    ".sgc-acts a,.sgc-acts button{display:inline-flex;align-items:center;min-height:40px;padding:0 14px;border-radius:999px;font-family:inherit;font-size:.9375rem;font-weight:600;line-height:1.2;text-align:left;text-decoration:none;cursor:pointer;border:0;background:var(--brand-soft,#e3eef8);color:var(--brand,#1b5c8c)}" +
    ".sgc-acts .sgc-wa{background:#167a40;color:#fff}" +
    ".sgc-form{display:flex;gap:8px;padding:10px;border-top:1px solid var(--bg-2,#eef2f7);background:var(--surface,#fff)}" +
    ".sgc-form input{flex:1;min-width:0;min-height:44px;margin:0;padding:0 14px;border-radius:999px;border:1.5px solid var(--bg-2,#c9d2de);background:var(--bg,#f8f9fb);color:var(--ink,#1d2733);font-family:inherit;font-size:1rem}" +
    ".sgc-form input:focus{outline:none;border-color:var(--accent,#c2125f)}" +
    ".sgc-form button{min-height:44px;padding:0 16px;border:0;border-radius:999px;background:var(--accent,#c2125f);color:var(--accent-ink,#fff);font-family:inherit;font-size:1rem;font-weight:600;cursor:pointer}" +
    ".sgc-note{font-size:.8125rem;color:var(--muted,#525d6b);text-align:center;padding:0 12px 8px;background:var(--surface,#fff)}" +
    ".sgc-typing{opacity:.7;font-style:italic}" +
    "@media (max-width:700px){.sgc-launch{right:12px;bottom:calc(84px + env(safe-area-inset-bottom))}" +
    ".sgc-panel{right:0;left:0;bottom:0;width:100%;height:min(85vh,640px);border-radius:18px 18px 0 0;padding-bottom:env(safe-area-inset-bottom)}}" +
    "@media (prefers-reduced-motion:no-preference){.sgc-m{animation:sgcIn .18s ease-out}@keyframes sgcIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}}";

  var T = PAGE_HI ? {
    open: "हमसे बात करें", title: "Smile & Glow सहायक", sub: "आमतौर पर तुरंत जवाब", ph: "अपना सवाल लिखें…", send: "भेजें", close: "बंद करें",
    hello: "नमस्ते! मैं Smile & Glow का सहायक हूँ। समय, पता, ट्रीटमेंट, कीमत या अपॉइंटमेंट — कुछ भी पूछें।",
    note: "जवाब इस वेबसाइट की जानकारी से हैं। आपका लिखा कहीं सेव नहीं होता।",
    wa: "WhatsApp पर बुक करें", call: "कॉल करें", form: "बुकिंग फ़ॉर्म", page: "पूरी कीमत और जानकारी"
  } : {
    open: "Chat with us", title: "Smile & Glow assistant", sub: "Instant answers about the clinic", ph: "Type your question…", send: "Send", close: "Close",
    hello: "Hi! I'm the Smile & Glow assistant. Ask me about timings, locations, treatments, prices or booking.",
    note: "Answers come from this website. Nothing you type is stored.",
    wa: "Book on WhatsApp", call: "Call", form: "Booking form", page: "Full prices & details"
  };

  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
  var launch = document.createElement("button");
  launch.type = "button"; launch.className = "sgc-launch"; launch.setAttribute("aria-haspopup", "dialog"); launch.setAttribute("aria-expanded", "false");
  launch.innerHTML = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/><path d="M8.5 11h.01M12 11h.01M15.5 11h.01"/></svg><span>' + T.open + "</span>";
  var panel = document.createElement("div");
  panel.className = "sgc-panel"; panel.hidden = true; panel.setAttribute("role", "dialog"); panel.setAttribute("aria-label", T.title);
  panel.innerHTML = '<div class="sgc-head"><div><b>' + T.title + "</b><small>" + T.sub + '</small></div><button type="button" class="sgc-x" aria-label="' + T.close + '">×</button></div>' +
    '<div class="sgc-log" role="log" aria-live="polite"></div>' +
    '<form class="sgc-form" autocomplete="off"><input type="text" maxlength="300" aria-label="' + T.ph + '" placeholder="' + T.ph + '"><button type="submit">' + T.send + "</button></form>" +
    '<div class="sgc-note">' + T.note + "</div>";
  document.body.appendChild(launch); document.body.appendChild(panel);
  var log = panel.querySelector(".sgc-log"), form = panel.querySelector("form"), input = form.querySelector("input");

  function scroll() { log.scrollTop = log.scrollHeight; }
  function bubble(cls, html, isText) {
    var d = document.createElement("div"); d.className = "sgc-m " + cls;
    if (isText) d.textContent = html; else d.innerHTML = html;
    log.appendChild(d); scroll(); return d;
  }
  function actions(list, hi) {
    if (!list || !list.length) return;
    var L = hi ? { wa: "WhatsApp पर बुक करें", call: "कॉल करें", form: "बुकिंग फ़ॉर्म", page: "पूरी कीमत और जानकारी" } : (PAGE_HI ? { wa: "Book on WhatsApp", call: "Call", form: "Booking form", page: "Full prices & details" } : T);
    var box = document.createElement("div"); box.className = "sgc-acts";
    list.forEach(function (x) {
      var el;
      if (x[0] === "chips") {
        (hi ? CHIPS_HI : CHIPS_EN).forEach(function (c) {
          var b = document.createElement("button"); b.type = "button"; b.textContent = c[0];
          b.addEventListener("click", function () { ask(c[1], c[0]); }); box.appendChild(b);
        });
        return;
      }
      el = document.createElement("a");
      if (x[0] === "wa") { el.href = wa(x[1] ? "Hi Smile & Glow Clinic, I'd like to book an appointment for " + x[1] + "." : ""); el.target = "_blank"; el.rel = "noopener"; el.className = "sgc-wa"; el.textContent = L.wa; }
      else if (x[0] === "call") { el.href = "tel:" + TEL; el.textContent = L.call + " " + PHONE; }
      else if (x[0] === "form") { el.href = BOOK; el.textContent = L.form; el.addEventListener("click", close); }
      else if (x[0] === "page") { if (!x[1]) return; el.href = x[1]; el.textContent = L.page; }
      else if (x[0] === "link") { el.href = x[1]; el.textContent = x[2]; if (x[3]) { el.target = "_blank"; el.rel = "noopener"; } else el.addEventListener("click", close); }
      box.appendChild(el);
    });
    if (box.children.length) { log.appendChild(box); scroll(); }
  }
  function ask(q, shown) {
    q = (q || "").trim(); if (!q) return;
    bubble("sgc-me", shown || q, true);
    var t = bubble("sgc-bot sgc-typing", "…", true);
    setTimeout(function () {
      var r = answer(q); t.classList.remove("sgc-typing"); t.innerHTML = r.html; actions(r.act, r.hi); scroll();
    }, 350);
  }
  var started = false;
  function open() {
    panel.hidden = false; launch.hidden = true; launch.setAttribute("aria-expanded", "true");
    if (!started) { started = true; bubble("sgc-bot", T.hello); actions([["chips"]], PAGE_HI); }
    setTimeout(function () { if (window.matchMedia("(min-width:701px)").matches) input.focus(); }, 50);
  }
  function close() { panel.hidden = true; launch.hidden = false; launch.setAttribute("aria-expanded", "false"); launch.focus({ preventScroll: true }); }
  launch.addEventListener("click", open);
  panel.querySelector(".sgc-x").addEventListener("click", close);
  panel.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  form.addEventListener("submit", function (e) { e.preventDefault(); var q = input.value; input.value = ""; ask(q); });
  window.sgChatAnswer = answer; // used by the site's tests
})();
