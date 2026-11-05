/* Smile & Glow: shared page extras, loaded on every page.
   1. Live "open now" badges   2. Listen (read aloud) button   3. Skin weather for Lucknow (homepage only)
   4. Festive banner (homepage only, shows automatically between START and END below)
   Runs in the browser; nothing is stored or sent anywhere except the free Open-Meteo weather request. */
(function () {
  "use strict";
  var HI = (document.documentElement.lang || "").indexOf("hi") === 0;

  /* ---------------- 1. Open now ----------------
     Confirmed hours (Mon–Sat). Sunday: by appointment only. */
  var BR = {
    it: { en: "I.T Chauraha", hi: "आई.टी. चौराहा", open: 11 * 60, close: 15 * 60 },
    aa: { en: "Aashiyana", hi: "आशियाना", open: 16 * 60, close: 21 * 60 }
  };
  var DAYS_EN = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  var DAYS_HI = ["रविवार", "सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार"];

  function istNow() {
    var parts = {};
    new Intl.DateTimeFormat("en-GB", { timeZone: "Asia/Kolkata", weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23" })
      .formatToParts(new Date()).forEach(function (p) { parts[p.type] = p.value; });
    var day = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(parts.weekday);
    return { day: day, min: parseInt(parts.hour, 10) * 60 + parseInt(parts.minute, 10) };
  }
  function fmt(m) {
    var h = Math.floor(m / 60), mm = m % 60;
    if (HI) {
      var part = h < 12 ? "सुबह" : (h < 16 ? "दोपहर" : (h < 19 ? "शाम" : "रात"));
      var h12 = h % 12 || 12;
      return part + " " + h12 + (mm ? ":" + (mm < 10 ? "0" : "") + mm : "") + " बजे";
    }
    var ap = h < 12 ? "AM" : "PM";
    return (h % 12 || 12) + (mm ? ":" + (mm < 10 ? "0" : "") + mm : "") + " " + ap;
  }
  /* returns {open:bool, soon:bool, text} */
  function status(key, now) {
    var b = BR[key], n = now || istNow(), d = n.day, m = n.min;
    var working = d >= 1 && d <= 6;
    if (working && m >= b.open && m < b.close) {
      var soon = b.close - m <= 60;
      return { open: true, soon: soon, text: HI ? (soon ? "जल्द बंद होगा · " : "अभी खुला है · ") + fmt(b.close) + " तक"
                                           : (soon ? "Closing soon · " : "Open now · ") + "until " + fmt(b.close) };
    }
    if (working && m < b.open) {
      return { open: false, text: HI ? "बंद · आज " + fmt(b.open) + " खुलेगा" : "Closed · opens today at " + fmt(b.open) };
    }
    // after closing, or Sunday: find next working day
    var next = (d + 1) % 7; if (next === 0) next = 1;
    var label;
    if (HI) label = next === (d + 1) % 7 ? "कल" : DAYS_HI[next];
    else label = next === (d + 1) % 7 ? "tomorrow" : DAYS_EN[next];
    var pre = d === 0 ? (HI ? "रविवार: सिर्फ़ अपॉइंटमेंट · " : "Sunday: by appointment · ") : (HI ? "बंद · " : "Closed · ");
    return { open: false, text: pre + (HI ? label + " " + fmt(b.open) + " खुलेगा" : "opens " + label + " " + fmt(b.open)) };
  }
  window.sgOpenStatus = status; // used by the chatbot

  function paintOpen() {
    document.querySelectorAll("[data-open]").forEach(function (el) {
      var s = status(el.getAttribute("data-open"));
      el.textContent = s.text;
      el.className = "open-badge " + (s.open ? (s.soon ? "is-soon" : "is-open") : "is-closed");
    });
    var sum = document.querySelector("[data-open-summary]");
    if (sum) {
      var a = status("it"), b = status("aa");
      sum.innerHTML = "";
      [["it", a], ["aa", b]].forEach(function (x) {
        var s = document.createElement("span");
        s.className = "open-badge " + (x[1].open ? (x[1].soon ? "is-soon" : "is-open") : "is-closed");
        s.textContent = (HI ? BR[x[0]].hi : BR[x[0]].en) + ": " + x[1].text;
        sum.appendChild(s);
      });
      sum.hidden = false;
    }
  }
  paintOpen();
  setInterval(paintOpen, 60000);

  /* ---------------- 2. Listen ---------------- */
  var synth = window.speechSynthesis;
  var nav = document.querySelector(".nav");
  if (synth && window.SpeechSynthesisUtterance && nav) {
    var btn = document.createElement("button");
    btn.type = "button"; btn.className = "listen-btn"; btn.setAttribute("aria-pressed", "false");
    var LBL = HI ? ["सुनें", "रोकें"] : ["Listen", "Stop"];
    var ICON = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13"/></svg>';
    function setLabel(on) { btn.innerHTML = ICON + "<span>" + LBL[on ? 1 : 0] + "</span>"; btn.setAttribute("aria-pressed", on ? "true" : "false"); btn.setAttribute("aria-label", HI ? (on ? "पढ़ना रोकें" : "यह पेज सुनें") : (on ? "Stop reading" : "Listen to this page")); }
    setLabel(false);
    var menu = nav.querySelector(".menu-btn");
    nav.insertBefore(btn, menu || null);

    var queue = [], speaking = false;
    function pageText() {
      var main = document.querySelector("main"); if (!main) return "";
      var c = main.cloneNode(true);
      c.querySelectorAll("script,style,svg,form,select,button,iframe,noscript,[aria-hidden=true],.crumbs,.sgc-panel,.tools-grid p,.no-speak").forEach(function (e) { e.remove(); });
      c.querySelectorAll("h1,h2,h3,h4,p,li,figcaption,summary,td,th,blockquote").forEach(function (e) { e.insertAdjacentText("afterend", ". "); });
      return c.textContent.replace(/\s+/g, " ").replace(/(\.\s*){2,}/g, ". ").trim();
    }
    function chunks(t) {
      var out = [], parts = t.replace(/([.!?।])\s+/g, "$1\u0001").split("\u0001");
      parts.forEach(function (s) {
        while (s.length > 220) { var i = s.lastIndexOf(" ", 220); if (i < 60) i = 220; out.push(s.slice(0, i)); s = s.slice(i); }
        if (s.trim().length > 1) out.push(s);
      });
      return out;
    }
    function pickVoice() {
      var want = HI ? "hi" : "en", vs = synth.getVoices();
      return vs.filter(function (v) { return v.lang.toLowerCase().indexOf(want + "-in") === 0; })[0] ||
             vs.filter(function (v) { return v.lang.toLowerCase().indexOf(want) === 0; })[0] || null;
    }
    function next() {
      if (!speaking) return;
      var t = queue.shift();
      if (!t) { stop(); return; }
      var u = new SpeechSynthesisUtterance(t);
      u.lang = HI ? "hi-IN" : "en-IN"; u.rate = 0.95;
      var v = pickVoice(); if (v) u.voice = v;
      u.onend = next; u.onerror = function () { stop(); };
      synth.speak(u);
    }
    function stop() { speaking = false; queue = []; synth.cancel(); setLabel(false); }
    btn.addEventListener("click", function () {
      if (speaking) { stop(); return; }
      synth.cancel(); queue = chunks(pageText()); speaking = true; setLabel(true); next();
    });
    window.addEventListener("pagehide", stop);
    if (synth.onvoiceschanged !== undefined) synth.onvoiceschanged = function () {};
  }

  /* ---------------- 3. Skin weather (homepage) ---------------- */
  var box = document.getElementById("skin-weather");
  if (box) {
    var T = HI ? {
      title: "लखनऊ में आज की स्किन वेदर", uv: "UV (आज अधिकतम)", hum: "नमी", aqi: "हवा (AQI)", temp: "तापमान",
      lv: { low: "कम", mod: "मध्यम", high: "ज़्यादा", vhigh: "बहुत ज़्यादा", ext: "अत्यधिक" },
      aq: ["अच्छी", "ठीक", "संवेदनशील लोगों के लिए खराब", "खराब", "बहुत खराब", "ख़तरनाक"],
      tip: {
        uvx: "आज UV बहुत तेज़ है: SPF 30+ सनस्क्रीन लगाएँ, बाहर हों तो हर 2–3 घंटे में दोबारा लगाएँ, और दोपहर की धूप से बचें।",
        uvh: "आज UV ज़्यादा है: बाहर निकलने से 15 मिनट पहले सनस्क्रीन लगाएँ और टोपी या छाता साथ रखें।",
        uvm: "आज UV मध्यम है: रोज़ की तरह सुबह सनस्क्रीन लगाना न भूलें।",
        aqi: "आज हवा खराब है: बाहर से आकर चेहरा हल्के फ़ेस वॉश से धोएँ और मॉइस्चराइज़र लगाएँ — प्रदूषण त्वचा को रूखा और बेजान करता है।",
        humid: "आज नमी ज़्यादा है: हल्का जेल मॉइस्चराइज़र इस्तेमाल करें, पसीना पोंछते रहें, और त्वचा की तहों को सूखा रखें ताकि फंगल इन्फ़ेक्शन न हो।",
        dry: "आज हवा रूखी है: गाढ़ा मॉइस्चराइज़र और लिप बाम लगाएँ, और बहुत गर्म पानी से न नहाएँ।",
        hot: "आज बहुत गर्मी है: खूब पानी पिएँ, हल्के कपड़े पहनें, और पसीने के बाद चेहरा धोएँ।",
        ok: "आज मौसम संतुलित है: हल्का फ़ेस वॉश, मॉइस्चराइज़र और सनस्क्रीन — बस इतना काफ़ी है।"
      },
      src: "लाइव मौसम: Open-Meteo · सामान्य सलाह, जांच का विकल्प नहीं"
    } : {
      title: "Skin weather in Lucknow today", uv: "UV (today's max)", hum: "Humidity", aqi: "Air quality (AQI)", temp: "Temperature",
      lv: { low: "low", mod: "moderate", high: "high", vhigh: "very high", ext: "extreme" },
      aq: ["good", "moderate", "unhealthy for sensitive groups", "unhealthy", "very unhealthy", "hazardous"],
      tip: {
        uvx: "UV is very high today: wear SPF 30+ sunscreen, reapply every 2–3 hours outdoors and avoid the midday sun.",
        uvh: "UV is high today: apply sunscreen 15 minutes before going out and carry a cap or umbrella.",
        uvm: "UV is moderate today: don't skip your morning sunscreen.",
        aqi: "Air quality is poor today: wash your face with a gentle cleanser when you get home and moisturise — pollution dries and dulls skin.",
        humid: "It's humid today: switch to a light gel moisturiser, wipe off sweat, and keep skin folds dry to prevent fungal infections.",
        dry: "The air is dry today: use a richer moisturiser and lip balm, and avoid very hot showers.",
        hot: "It's very hot today: drink plenty of water, wear loose cotton clothes and rinse your face after sweating.",
        ok: "Balanced weather today: a gentle face wash, moisturiser and sunscreen are all your skin needs."
      },
      src: "Live weather from Open-Meteo · general advice, not a diagnosis"
    };
    function uvLevel(u) { return u < 3 ? "low" : u < 6 ? "mod" : u < 8 ? "high" : u < 11 ? "vhigh" : "ext"; }
    function aqLevel(a) { return a <= 50 ? 0 : a <= 100 ? 1 : a <= 150 ? 2 : a <= 200 ? 3 : a <= 300 ? 4 : 5; }
    var LAT = 26.85, LON = 80.95;
    Promise.all([
      fetch("https://api.open-meteo.com/v1/forecast?latitude=" + LAT + "&longitude=" + LON + "&current=temperature_2m,relative_humidity_2m&daily=uv_index_max,temperature_2m_max&timezone=Asia%2FKolkata&forecast_days=1").then(function (r) { return r.json(); }),
      fetch("https://air-quality-api.open-meteo.com/v1/air-quality?latitude=" + LAT + "&longitude=" + LON + "&current=us_aqi&timezone=Asia%2FKolkata").then(function (r) { return r.json(); }).catch(function () { return null; })
    ]).then(function (res) {
      var w = res[0], a = res[1];
      if (!w || !w.current || !w.daily) return;
      var uv = Math.round(w.daily.uv_index_max[0] || 0), hum = Math.round(w.current.relative_humidity_2m),
          temp = Math.round(w.current.temperature_2m), tmax = Math.round(w.daily.temperature_2m_max[0] || temp),
          aqi = a && a.current && a.current.us_aqi != null ? Math.round(a.current.us_aqi) : null;
      var tip = uv >= 8 ? "uvx" : (aqi != null && aqi > 150) ? "aqi" : uv >= 6 ? "uvh" : tmax >= 38 ? "hot" : hum >= 75 ? "humid" : hum <= 35 ? "dry" : uv >= 3 ? "uvm" : "ok";
      var lv = uvLevel(uv);
      var items = [
        [T.uv, uv + " · " + T.lv[lv], "uv-" + lv],
        [T.hum, hum + "%", ""],
        [T.temp, temp + "°C", ""]
      ];
      if (aqi != null) items.push([T.aqi, aqi + " · " + T.aq[aqLevel(aqi)], aqLevel(aqi) >= 3 ? "aq-bad" : ""]);
      box.innerHTML = '<div class="sw-head"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg><b></b></div><dl class="sw-stats"></dl><p class="sw-tip"></p><p class="sw-src"></p>';
      box.querySelector(".sw-head b").textContent = T.title;
      var dl = box.querySelector(".sw-stats");
      items.forEach(function (it) { var d = document.createElement("div"); if (it[2]) d.className = it[2]; d.innerHTML = "<dt></dt><dd></dd>"; d.firstChild.textContent = it[0]; d.lastChild.textContent = it[1]; dl.appendChild(d); });
      box.querySelector(".sw-tip").textContent = T.tip[tip];
      box.querySelector(".sw-src").textContent = T.src;
      box.hidden = false;
    }).catch(function () { /* stay hidden if weather can't be fetched */ });
  }
  /* ---------------- 4. Festive banner (Dhanteras / Diwali / Bhai Dooj 2026) ----------------
     Shows on the homepage only, from START until END (India time), then disappears by itself.
     No discounts or free treatment (Dental Council of India advertising rules): gift cards at normal price,
     festive appointment slots and health tips only. To reuse next year, change the dates and texts. */
  (function () {
    var START = Date.parse("2026-11-04T00:00:00+05:30"), END = Date.parse("2026-11-11T00:00:00+05:30");
    var DIWALI_OVER = Date.parse("2026-11-09T00:00:00+05:30");
    var now = Date.now(), path = location.pathname;
    if (now < START || now >= END || (path !== "/" && path !== "/index.html" && path !== "/hi/" && path !== "/hi/index.html")) return;
    var KEY = "sgFest2026";
    try { if (localStorage.getItem(KEY) === "x") return; } catch (e) {}
    var main = document.querySelector("main"); if (!main) return;
    var WA = "https://wa.me/917275433783?text=";
    var after = now >= DIWALI_OVER;
    var T = HI ? {
      head: after ? "🪔 दीपावली की शुभकामनाएँ! इस भाई दूज, मुस्कान तोहफ़े में दें" : "🪔 धनतेरस और दीपावली की शुभकामनाएँ",
      sub: "धनतेरस भगवान धन्वंतरि, यानी आयुर्वेद और चिकित्सा के देवता, का दिन है। इस त्योहार सेहत में निवेश करें।",
      party: ["दीपावली से पहले चमकें", "दांतों की सफ़ेदी, कार्बन लेज़र पील और ग्लो फ़ेशियल के लिए 6–7 नवंबर के स्लॉट।", "स्लॉट बुक करें", "नमस्ते Smile & Glow, मुझे दीपावली से पहले (6–7 नवंबर) व्हाइटनिंग / कार्बन पील / ग्लो फ़ेशियल का स्लॉट चाहिए।"],
      gift: ["भाई दूज पर ‘गिफ़्ट अ स्माइल’", "भाई या बहन को दांतों की सफ़ाई, व्हाइटनिंग, ग्लो फ़ेशियल या परामर्श का गिफ़्ट कार्ड दें।", "गिफ़्ट कार्ड लें", "नमस्ते Smile & Glow, मैं भाई दूज पर ‘गिफ़्ट अ स्माइल’ गिफ़्ट कार्ड लेना चाहता/चाहती हूँ। कृपया विकल्प बताएँ।"],
      tips: ["त्योहार में सेहत", "मिठाई के बाद दांत और त्वचा की देखभाल के आसान टिप्स।", "टिप्स पढ़ें", "/food-for-teeth-and-skin/"],
      close: "बंद करें"
    } : {
      head: after ? "🪔 Happy Diwali! Gift a Smile this Bhai Dooj" : "🪔 Happy Dhanteras & Diwali from Smile & Glow",
      sub: "Dhanteras is the day of Lord Dhanvantari, the god of medicine. This festive season, invest in your health.",
      party: ["Party-ready by Diwali", "Slots on 6–7 Nov for teeth whitening, carbon laser peel and glow facials.", "Book a slot", "Hi Smile & Glow, I'd like a slot on 6–7 Nov before Diwali for whitening / carbon peel / glow facial."],
      gift: ["Gift a Smile for Bhai Dooj", "Give your brother or sister a gift card for a dental cleaning, whitening, glow facial or consultation.", "Get a gift card", "Hi Smile & Glow, I'd like a 'Gift a Smile' gift card for Bhai Dooj. Please share the options."],
      tips: ["Festive health tips", "Simple ways to protect teeth and skin through the sweets and late nights.", "Read the tips", "/food-for-teeth-and-skin/"],
      close: "Close"
    };
    var css = ".fest{position:relative;margin:16px auto 0;max-width:1160px;width:calc(100% - 32px);padding:20px 22px;border-radius:20px;background:linear-gradient(135deg,var(--brand-soft,#e3eef8),var(--surface,#fff));border:1.5px solid var(--accent,#c2125f);color:var(--ink,#1d2733)}" +
      ".fest h2{font-size:1.3rem;line-height:1.3;margin:0 44px 4px 0;color:var(--brand,#1b5c8c)}" +
      ".fest .fest-sub{margin:0 0 14px;color:var(--muted,#525d6b);font-size:.95rem}" +
      ".fest-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}" +
      ".fest-card{display:flex;flex-direction:column;gap:6px;padding:14px;border-radius:14px;background:var(--surface,#fff)}" +
      ".fest-card b{font-size:1rem}.fest-card p{margin:0;font-size:.9rem;line-height:1.45;flex:1}" +
      ".fest-card a{align-self:flex-start;display:inline-flex;align-items:center;min-height:40px;padding:0 14px;border-radius:999px;font-weight:600;font-size:.9rem;text-decoration:none;background:var(--accent,#c2125f);color:var(--accent-ink,#fff)}" +
      ".fest-card a.fest-wa{background:#167a40;color:#fff}" +
      ".fest-x{position:absolute;top:8px;right:8px;width:44px;height:44px;border:0;border-radius:10px;background:transparent;color:inherit;font-size:1.5rem;cursor:pointer}";
    var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    var box = document.createElement("aside");
    box.className = "fest no-speak"; box.setAttribute("aria-label", T.head.replace(/^\S+\s/, ""));
    function card(c, wa) {
      var href = wa ? WA + encodeURIComponent(c[3]) : c[3];
      return '<div class="fest-card"><b></b><p></p><a href="' + href + '"' + (wa ? ' class="fest-wa" target="_blank" rel="noopener"' : "") + "></a></div>";
    }
    var cards = (after ? [] : [[T.party, 1]]).concat([[T.gift, 1], [T.tips, 0]]);
    box.innerHTML = '<button type="button" class="fest-x" aria-label="' + T.close + '">×</button><h2></h2><p class="fest-sub"></p><div class="fest-grid">' +
      cards.map(function (c) { return card(c[0], c[1]); }).join("") + "</div>";
    box.querySelector("h2").textContent = T.head;
    box.querySelector(".fest-sub").textContent = T.sub;
    box.querySelectorAll(".fest-card").forEach(function (el, i) {
      var c = cards[i][0]; el.querySelector("b").textContent = c[0]; el.querySelector("p").textContent = c[1]; el.querySelector("a").textContent = c[2];
    });
    box.querySelector(".fest-x").addEventListener("click", function () { box.remove(); try { localStorage.setItem(KEY, "x"); } catch (e) {} });
    main.insertBefore(box, main.firstChild);
  })();
})();
