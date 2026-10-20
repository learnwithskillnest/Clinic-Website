#!/usr/bin/env python3
"""Build script for smileandglow.co.in

Run after editing index.html or i18n/hi.json:
    python3 tools/build.py

It does two things:
1. Regenerates the structured data (JSON-LD) in index.html from the page's
   own FAQ and clinic details, so Google / AI answer engines always see data
   that matches the visible page.
2. Builds the Hindi page hi/index.html by translating every visible text in
   index.html with i18n/hi.json, and lists any text still missing a translation.
"""
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Comment, Doctype

sys.path.insert(0, str(Path(__file__).resolve().parent))
from treatments import build_treatments, TREATMENTS, REG_NO  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://smileandglow.co.in"
PHONE = "+91-72754-33783"
INSTAGRAM = "https://www.instagram.com/smileandglowclinic/"
CID_IT = int("f3f635cad7f14b2e", 16)   # Google Maps place: Smile & Glow - I.T Chauraha
CID_AA = int("65ba20fb4a1758f1", 16)   # Google Maps place: Smile & Glow - Aasiyana
JUSTDIAL_IT = ("https://www.justdial.com/Lucknow/Smile-Glow-It-Girls-College-Gate-No-4-Babuganj/"
               "0522PX522-X522-230105184820-S3Q7_BZDET")
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

SERVICES = [
    "Root canal treatment", "Dental implants", "Smile makeover", "Teeth whitening",
    "Oral medicine and radiology", "Kids and family dentistry",
    "Chemical peels", "Acne and scar treatment", "Anti-ageing treatment",
    "Face PRP", "Hair PRP", "Skincare consultation",
    "Laser hair reduction", "Laser toning", "Carbon laser peel",
    "Fractional laser resurfacing", "IPL photofacial", "Laser tattoo removal",
]

HEAD_HI = {
    "title": "लखनऊ में डेंटल और स्किन क्लिनिक | स्माइल एंड ग्लो – डॉ. पल्लवी",
    "description": ("डॉ. पल्लवी द्वारा स्माइल एंड ग्लो, आई.टी. चौराहा और आशियाना, लखनऊ में दांत, "
                    "त्वचा, बाल और लेज़र उपचार। Google पर 4.9★ रेटिंग। बुकिंग: +91 72754 33783"),
}

# Visible strings that are fine to leave untranslated on the Hindi page
KEEP = re.compile(r"^(@smileandglowclinic|Instagram|English|हिंदी|PRP|IPL|RCT|BDS|MDS|FMC|"
                  r"[\d\s+().:–\-★·/,]+|0[1-9]|\+91 72754 33783|072754 33783|"
                  r"smileandglow\.co\.in|· smileandglow\.co\.in|©)$")


def clinic(slug, name, street, postcode, lat, lng, opens, closes, cid, rating, reviews, extra_same_as=()):
    return {
        "@type": ["Dentist", "MedicalClinic"],
        "@id": f"{SITE}/#{slug}",
        "name": name,
        "alternateName": ["Smile and Glow Clinic", "Dr. Pallavi's Clinic"],
        "description": ("Dental, skin, hair and laser clinic run by Dr. Pallavi (BDS, MDS, FMC). "
                        "Root canal, implants, teeth whitening, chemical peels, hair PRP and laser hair reduction."),
        "url": f"{SITE}/",
        "priceRange": "₹₹",
        "currenciesAccepted": "INR",
        "areaServed": {"@type": "City", "name": "Lucknow"},
        "image": f"{SITE}/assets/img/gallery-sign.webp",
        "logo": f"{SITE}/assets/img/logo.png",
        "telephone": PHONE,
        "address": {"@type": "PostalAddress", "streetAddress": street, "addressLocality": "Lucknow",
                    "addressRegion": "Uttar Pradesh", "postalCode": postcode, "addressCountry": "IN"},
        "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng},
        "hasMap": f"https://maps.google.com/?cid={cid}",
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": DAYS,
                                       "opens": opens, "closes": closes}],
        "isAcceptingNewPatients": True,
        "medicalSpecialty": "Dentistry",
        "availableService": [{"@type": "MedicalProcedure", "name": s} for s in SERVICES],
        "parentOrganization": {"@id": f"{SITE}/#org"},
        "employee": {"@id": f"{SITE}/#dr-pallavi"},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": rating, "reviewCount": reviews,
                            "bestRating": "5"},
        "sameAs": [f"https://maps.google.com/?cid={cid}", INSTAGRAM, *extra_same_as],
    }


def json_ld(lang, page_url, faqs):
    graph = [
        {"@type": "Organization", "@id": f"{SITE}/#org", "name": "Smile & Glow",
         "description": "Dental, skin, hair and laser clinics in Lucknow, run by Dr. Pallavi.",
         "areaServed": {"@type": "City", "name": "Lucknow"},
         "alternateName": ["Smile and Glow Clinic", "Dr. Pallavi's Clinic"], "url": f"{SITE}/",
         "logo": f"{SITE}/assets/img/logo.png", "telephone": PHONE, "sameAs": [INSTAGRAM],
         "founder": {"@id": f"{SITE}/#dr-pallavi"},
         "subOrganization": [{"@id": f"{SITE}/#it-chauraha"}, {"@id": f"{SITE}/#aashiyana"}]},
        {"@type": "Person", "@id": f"{SITE}/#dr-pallavi", "name": "Dr. Pallavi", "honorificPrefix": "Dr.",
         "jobTitle": "Dental Surgeon and Aesthetic Physician",
         "image": f"{SITE}/assets/img/clinic-treatment-room.webp",
         "hasCredential": [
             {"@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": "BDS"},
             {"@type": "EducationalOccupationalCredential", "credentialCategory": "degree",
              "name": "MDS (Maxillofacial Medicine & Radiology)"},
             {"@type": "EducationalOccupationalCredential", "credentialCategory": "certificate",
              "name": "FMC (Fellow in Cosmetology)"},
             {"@type": "EducationalOccupationalCredential", "credentialCategory": "certificate",
              "name": "PG Diploma in Nutrition"}],
         "knowsAbout": ["Dentistry", "Oral medicine", "Dental radiology", "Cosmetology", "Skin care",
                        "Laser treatments", "Nutrition"],
         "identifier": {"@type": "PropertyValue", "propertyID": "Dental registration number", "value": REG_NO},
         "worksFor": [{"@id": f"{SITE}/#it-chauraha"}, {"@id": f"{SITE}/#aashiyana"}],
         "sameAs": [INSTAGRAM]},
        clinic("it-chauraha", "Smile & Glow – I.T Chauraha",
               "Gate No. 4, 1/2 Shivsthali, Faizabad Rd, opp. IT Girls College, New Hyderabad, Hasanganj",
               "226007", 26.8710086, 80.9419724, "11:00", "15:00", CID_IT, "4.9", "13", [JUSTDIAL_IT]),
        clinic("aashiyana", "Smile & Glow – Aashiyana",
               "SS-771, behind Aastha Hospital, Sector H, LDA Colony, Aashiyana",
               "226012", 26.797045, 80.912754, "16:00", "21:00", CID_AA, "5.0", "8"),
        {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Smile & Glow",
         "inLanguage": ["en", "hi"], "publisher": {"@id": f"{SITE}/#org"}},
        {"@type": ["WebPage", "MedicalWebPage"], "@id": f"{page_url}#webpage", "url": page_url,
         "inLanguage": lang, "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#org"},
         "dateModified": "2026-10-19",
         "hasPart": [{"@type": "WebPage", "url": f"{SITE}/{t['slug']}/", "name": f"{t['name']} in Lucknow"} for t in TREATMENTS]},
        {"@type": "FAQPage", "@id": f"{page_url}#faq", "inLanguage": lang,
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
    ]
    return {"@context": "https://schema.org", "@graph": graph}


def faqs_from(soup):
    out = []
    for d in soup.select(".faq details"):
        q = d.find("summary").get_text(" ", strip=True)
        a = d.find("p").get_text(" ", strip=True)
        out.append((q, a))
    return out


def set_ld(soup, data):
    tag = soup.find("script", type="application/ld+json")
    tag.string = json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def write_ld_into_source(html, data):
    """Replace JSON-LD in the source text without re-serialising the whole page."""
    new = '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>"
    out, n = re.subn(r'<script type="application/ld\+json">.*?</script>', lambda m: new, html, count=1, flags=re.S)
    assert n == 1, "JSON-LD script tag not found"
    return out


def translate(soup, d):
    missing = set()
    for node in soup.find_all(string=True):
        if isinstance(node, (Comment, Doctype)):
            continue
        parent = node.parent
        if parent.name in ("script", "style", "noscript", "title") or parent.find_parent(class_="lang"):
            continue
        raw = str(node)
        key = raw.strip()
        if not key:
            continue
        if key in d:
            node.replace_with(NavigableString(raw.replace(key, d[key])))
        elif re.search(r"[A-Za-z]{3,}", key) and not KEEP.match(key):
            missing.add(key)
    for el in soup.select("[placeholder]"):
        el["placeholder"] = d.get("PH:" + el["placeholder"], el["placeholder"])
    for el in soup.select("optgroup"):
        el["label"] = d.get("OG:" + el["label"], el["label"])
    return missing


def main():
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    d = json.loads((ROOT / "i18n" / "hi.json").read_text(encoding="utf-8"))

    # 1) English page: refresh JSON-LD from its own visible FAQ
    en_soup = BeautifulSoup(src, "html.parser")
    src = write_ld_into_source(src, json_ld("en", f"{SITE}/", faqs_from(en_soup)))
    (ROOT / "index.html").write_text(src, encoding="utf-8")

    # 2) Hindi page
    soup = BeautifulSoup(src, "html.parser")
    soup.html["lang"] = "hi"
    soup.title.string = HEAD_HI["title"]
    for sel, val in [('meta[name="description"]', HEAD_HI["description"]),
                     ('meta[property="og:title"]', HEAD_HI["title"]),
                     ('meta[property="og:description"]', HEAD_HI["description"]),
                     ('meta[property="og:url"]', f"{SITE}/hi/"),
                     ('meta[property="og:locale"]', "hi_IN")]:
        soup.select_one(sel)["content"] = val
    soup.select_one('link[rel="canonical"]')["href"] = f"{SITE}/hi/"
    for a in soup.select(".lang a"):
        if a.get("hreflang") == "hi":
            a["aria-current"] = "page"
        elif a.has_attr("aria-current"):
            del a["aria-current"]
    missing = translate(soup, d)
    set_ld(soup, json_ld("hi", f"{SITE}/hi/", faqs_from(soup)))

    out = ROOT / "hi" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(str(soup), encoding="utf-8")

    # 3) Treatment pages + shared stylesheet
    slugs = build_treatments(ROOT, src)

    # 4) Sitemap
    alt = ('    <xhtml:link rel="alternate" hreflang="en" href="{s}/"/>\n'
           '    <xhtml:link rel="alternate" hreflang="hi" href="{s}/hi/"/>\n'
           '    <xhtml:link rel="alternate" hreflang="x-default" href="{s}/"/>\n').format(s=SITE)
    urls = [f"  <url>\n    <loc>{SITE}/</loc>\n    <lastmod>2026-10-19</lastmod>\n{alt}  </url>",
            f"  <url>\n    <loc>{SITE}/hi/</loc>\n    <lastmod>2026-10-19</lastmod>\n{alt}  </url>"]
    urls += [f"  <url>\n    <loc>{SITE}/{slug}/</loc>\n    <lastmod>2026-10-19</lastmod>\n  </url>" for slug in slugs]
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")

    print(f"Built {out.relative_to(ROOT)}, {len(slugs)} treatment pages, sitemap.xml; refreshed JSON-LD in index.html")
    if missing:
        print(f"\n{len(missing)} visible text(s) without a Hindi translation (add them to i18n/hi.json):")
        for m in sorted(missing):
            print("  -", m)
        sys.exit(1 if "--strict" in sys.argv else 0)


if __name__ == "__main__":
    main()
