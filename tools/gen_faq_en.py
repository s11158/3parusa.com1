# -*- coding: utf-8 -*-
"""Generates /faq.html (EN) with FAQPage JSON-LD + patches sitemap.xml and llms.txt."""
import io, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

QA = [
("💰 Price & payment", [
("How much does a yacht tour cost?", "A berth in a shared cabin — from €1,100 per week; a whole cabin for two — from €2,200. The entire catamaran (4 cabins, up to 8 guests) — from €6,700 per week. Exotic destinations (Seychelles, Caribbean) — from €12,000. The exact price depends on country, season and boat — message me and I'll quote your dates."),
("What's included in the price?", "A double cabin with private bathroom, the curated route, the captain's work, bed linen and towels, WiFi (60 GB), airport–marina transfers and our 24/7 support."),
("What's paid separately?", "Flights and the boat kitty — shared onboard expenses: food, fuel, marina fees. We collect it at the start of the tour and I show a full receipt-based breakdown at the end. Optional: a chef (€1,200), photographer (€1,000), SUP (€100), fishing rod (€75)."),
("How can I pay?", "Whatever suits you: cash (EUR, USD, TRY), bank transfer, or card. We'll sort out the details when you book."),
("What is the security deposit?", "A refundable deposit held by the charter company for the boat (≈€500 per person). If the boat is fine — and it almost always is — it's returned in full. Often you can buy a full damage waiver instead (~€330 per boat) so nothing gets frozen; I'll tell you which is better in your case."),
]),
("📅 Dates & booking", [
("How do I book a spot?", "You message us → we pick a tour and cabin → a deposit locks your spot → the balance is due before the start. Everything is transparent: amounts, deadlines and what goes where — agreed upfront."),
("Can I pay in installments?", "Yes, we split the payment into parts before the tour starts."),
("What if I can't make it?", "We handle it case by case: you can transfer your spot, move to other dates or we find a replacement — we do our best so nobody loses money."),
]),
("🛏 Cabins & the boat", [
("What kind of boat is it?", "A VIP catamaran of 100–150 m²: 4 hotel-room-style cabins, each with its own bathroom and shower, several decks and lounge areas. The ride is flat and stable — this is not 'bouncing around on a little yacht'."),
("We're a couple — do we get our own cabin?", "Yes, the cabin is yours alone, with a private bathroom. Privacy on board is easy: there are plenty of decks and corners."),
]),
("🍽 Food", [
("How does food work on board?", "Breakfasts and some lunches we cook on board (groceries come from the boat kitty); dinners are usually in seaside restaurants with local cuisine: the fish market in Fethiye, oysters in Ston, wineries. You can hire an onboard chef (€1,200/week) — then you don't think about anything at all."),
("I have an allergy / special diet.", "Tell us in advance — we'll account for it when buying groceries and choosing restaurants."),
]),
("✈️ Getting there & documents", [
("How do I get there — will you meet me?", "You buy the flight, everything else is on us: we meet you at the airport and take you to the marina and back (transfer included)."),
("Do I need a visa?", "Depends on the destination: Turkey — visa-free for many nationalities, Europe — Schengen, Seychelles/Thailand — stamp on arrival. Before the tour I send a checklist for your country."),
("Do I need insurance?", "Yes, every guest needs regular travel insurance — it takes a day to arrange online. I'll suggest proven options."),
]),
("🎒 What to pack", [
("What should I bring?", "A soft bag (not a suitcase — there's nowhere to store it), swimwear, light clothes, a windbreaker for evenings, light-soled deck shoes, SPF cream, a hat. Towels and linen are already on board. I'll send a full checklist before the tour."),
]),
("⛵ Experience & safety", [
("I've never been on a yacht. Will I manage?", "Of course! Zero experience needed: the captain does all the work, you relax. Want to learn? I'll teach you to helm and work the sails; don't want to — just sunbathe."),
("What if I get seasick?", "We deliberately plan routes with short hops: we spend more time anchored in bays, swimming and sunbathing, than underway. At anchor there's no rolling. Seasickness is easily managed today — tablets, wristbands, and rum at sunset has never been cancelled 🙂 For sensitive guests we pick the calmest route."),
("Is it safe?", "The captain is licensed (IYT/ICC) with 20,000+ nautical miles and 100+ tours. Routes only follow proven waters with the forecast in mind. For first-timers we choose sheltered, calm cruising grounds."),
]),
("🌤 Weather & season", [
("When is the best time to go?", "Turkey and Greece — May to October (Turkey's velvet season is September–November; for first-timers May in Turkey is ideal). Seychelles and Thailand — our winter. Tell me your dates and I'll say where the sea is best at that time."),
]),
("👨‍👩‍👧 Kids", [
("Can we bring children?", "You should! Family tours are our favourite format: 50% relaxed holiday, 50% kids' programme, and we match the crew so there are other families with children on board. Kids' life jackets and constant supervision go without saying."),
]),
]

METRICA = """<script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");ym(110049558, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", accurateTrackBounce:true, trackLinks:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/110049558" style="position:absolute; left:-9999px;" alt="" /></div></noscript>"""

schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
    for _, items in QA for q, a in items]}

sections = []
for title, items in QA:
    block = "<h2>%s</h2>" % title
    for q, a in items:
        block += '<h3 class="q">%s</h3><p>%s</p>' % (q, a)
    sections.append(block)
body = "\n".join(sections)

html = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Yacht Tour FAQ: Prices, Cabins, Seasickness, Kids | 3Parusa</title>
<meta name="description" content="21 most common questions about catamaran tours: prices, payment, cabins, food, visas, seasickness, kids, safety. Answered by captain Stas Kochukov.">
<link rel="canonical" href="https://3parusa.com/faq.html">
<link rel="alternate" hreflang="en" href="https://3parusa.com/faq.html">
<link rel="alternate" hreflang="ru" href="https://3parusa.ru/faq.html">
<meta property="og:title" content="Yacht Tour FAQ: Prices, Cabins, Seasickness, Kids | 3Parusa"><meta property="og:description" content="21 most common questions about catamaran tours: prices, payment, cabins, food, visas, seasickness, kids, safety."><meta property="og:type" content="website">
<script type="application/ld+json">%s</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root{--dark:#191f28;--navy:#06112a;--gold:#d3aa31;--gold2:#d6a000;--sand:#eddba6;--txt:#454545;--bg2:#f8f8f8}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',Arial,sans-serif;font-weight:300;color:var(--txt);line-height:1.7;background:#fff}
h1,h2,h3,.logo{font-family:'Montserrat',Arial,sans-serif}
header{background:#fff;padding:16px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;border-bottom:1px solid #eee;position:sticky;top:0;z-index:10}
header a.logo{color:var(--dark);font-size:21px;text-decoration:none;font-weight:700;letter-spacing:.5px}
header nav a{color:var(--dark);text-decoration:none;margin-left:18px;font-size:14px;font-weight:500;font-family:'Montserrat',Arial,sans-serif}
header nav a:hover{color:var(--gold2)}
.hero{background:var(--dark);color:#fff;padding:64px 20px 52px;text-align:center}
.hero h1{font-size:clamp(26px,4.5vw,44px);font-weight:700;max-width:860px;margin:0 auto 16px;line-height:1.25}
.hero p{max-width:680px;margin:0 auto;font-size:18px;font-weight:300;color:#d9dee6}
.cta{display:inline-block;margin-top:26px;background:var(--gold);color:var(--dark);padding:16px 42px;border-radius:100px;text-decoration:none;font-weight:600;font-family:'Montserrat',Arial,sans-serif;font-size:15px}
.cta:hover{background:var(--gold2)}
main{max-width:740px;margin:0 auto;padding:40px 20px 20px}
main h2{color:var(--dark);margin:36px 0 10px;font-size:25px;font-weight:600}
main h3.q{color:var(--navy);margin:20px 0 6px;font-size:18px;font-weight:600}
main p, main li{font-size:17px;margin-bottom:12px}
main a{color:var(--gold2)}
.box{background:var(--bg2);border-left:4px solid var(--gold);padding:18px 20px;border-radius:8px;margin:22px 0}
footer{background:var(--dark);color:#aab3bf;text-align:center;padding:30px 20px;margin-top:48px;font-size:14px}
footer a{color:var(--sand);text-decoration:none}
</style>%s</head><body>
<header><a class="logo" href="/">⛵ 3Parusa</a><nav><a href="/#rec">Tours</a><a href="/blog/">Blog</a><a href="/faq.html">FAQ</a><a href="https://t.me/stas_kochukov">Telegram</a></nav></header>
<div class="hero"><h1>Questions &amp; Answers</h1><p>The 21 questions guests have been asking me for ten years — answered exactly the way I answer them in person.</p><a class="cta" href="https://wa.me/79104651420">Ask your question</a></div>
<main>%s
<div class="box"><b>Still have questions? Message the captain directly:</b> <a href="https://wa.me/79104651420">WhatsApp +7 910 465-14-20</a> · <a href="https://t.me/stas_kochukov">Telegram @stas_kochukov</a>. I answer personally. — Stas Kochukov, captain of 3Parusa</div>
<p>Deep dives in the <a href="/blog/">captain's blog</a>: <a href="/blog/do-you-get-seasick-on-a-catamaran.html">seasickness on a catamaran</a>.</p>
</main>
<footer>3Parusa — curated sailing tours worldwide · 20,000 nm · 20+ countries · 1,000 happy guests<br><a href="/">3parusa.com</a> · <a href="/privacy.html">Privacy policy</a></footer>
</body></html>""" % (json.dumps(schema, ensure_ascii=False), METRICA, body)

io.open(os.path.join(ROOT, "faq.html"), "w", encoding="utf-8", newline="\n").write(html)

sm_path = os.path.join(ROOT, "sitemap.xml")
sm = io.open(sm_path, encoding="utf-8").read()
if "3parusa.com/faq.html" not in sm:
    sm = sm.replace("</urlset>", "<url><loc>https://3parusa.com/faq.html</loc></url></urlset>")
    io.open(sm_path, "w", encoding="utf-8", newline="\n").write(sm)

llms_path = os.path.join(ROOT, "llms.txt")
llms = io.open(llms_path, encoding="utf-8").read()
if "3parusa.com/faq.html" not in llms:
    llms = llms.rstrip("\n") + "\n- FAQ (21 questions answered): https://3parusa.com/faq.html\n"
    io.open(llms_path, "w", encoding="utf-8", newline="\n").write(llms)
print("faq en ok")
