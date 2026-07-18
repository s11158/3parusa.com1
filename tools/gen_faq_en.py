# -*- coding: utf-8 -*-
"""Generates /faq.html (EN): FAQPage JSON-LD, main-page brand style, accordion.
Voice — "we / our team" (a company, not one person). Plain, no sailor jargon.
Also patches sitemap.xml and llms.txt."""
import io, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERO = "/assets/static.tildacdn.com/tild3662-3766-4663-a466-383465653737/_.jpg"

QA = [
("💰", "Price & payment", [
("How much does a yacht tour cost?", "A place in a shared cabin — from €1,100 per week; a whole cabin for two — from €2,200. The entire yacht (4 cabins, up to 8 guests) — from €6,700 per week. Far-away destinations (Seychelles, Caribbean) — from €12,000. The exact price depends on the country, season and boat — message us and we'll work out a quote for your dates."),
("What's included in the price?", "A double cabin with its own bathroom, a thought-out route, the captain's work, bed linen and towels, WiFi (60 GB), airport–marina transfer and our 24/7 support."),
("What's paid separately?", "Flights and the boat kitty — the shared onboard costs: food, fuel, mooring fees in ports. We collect it at the start of the tour and show a full receipt-based breakdown at the end. Optional extras: a chef (€1,200), a photographer (€1,000), a paddleboard (€100), a fishing rod (€75)."),
("How can I pay?", "Whatever is easiest for you: cash (euros, dollars), bank transfer or card. We'll explain all the details when you book."),
("What is the security deposit?", "It's a refundable deposit for the yacht, held by the company that owns the boat (about €500 per person). If the yacht is fine — and it almost always is — the deposit comes back in full. Often you can take out insurance instead (around €330 for the whole yacht), so no money gets frozen. We'll tell you which option is better in your case."),
]),
("📅", "Dates & booking", [
("How do I book a place?", "You message us → we pick a tour and cabin → a deposit secures your place → the balance is paid before departure. Everything is clear: amounts, deadlines and what each part is for — we go through it all upfront."),
("Can I pay in instalments?", "Yes, the payment can be split into parts before the tour begins."),
("What if I can't make it?", "We sort it out individually: you can pass your place to someone else, move the trip to other dates, or we find a replacement — we do our best so nobody loses money."),
]),
("🛏", "Cabins & the yacht", [
("What kind of yacht is it?", "It's a VIP catamaran of 100–150 m²: four cabins on the level of a good hotel room, each with its own bathroom and shower, several decks and lounge areas. A catamaran sails level and steady — none of the rocking you get on a small boat."),
("We're a couple — will we get our own cabin?", "Yes, the cabin will be yours alone, with a private bathroom. Getting some privacy on board is easy — there are plenty of decks and quiet corners."),
]),
("🍽", "Food", [
("How does food work on board?", "We cook breakfasts and some lunches right on the yacht (groceries come from the boat kitty), and for dinner we usually go to seaside restaurants with local cuisine. You can bring a chef on board (€1,200 per week) — then you don't have to think about food at all."),
("I have an allergy or a special diet — what then?", "Just tell us in advance — we'll take it into account when buying groceries and choosing restaurants."),
]),
("✈️", "Getting there & documents", [
("How do I get there — will someone meet me?", "You buy the flights, everything else is on us: we meet you at the airport and drive you to the marina and back (the transfer is included in the price)."),
("Do I need a visa?", "It depends on the destination: Turkey — visa-free for many, Europe — a Schengen visa, Seychelles and Thailand — a stamp on arrival. Before the trip we send a short guide for your country."),
("Do I need insurance?", "Yes, every guest needs ordinary travel insurance — you can arrange it online in a day. We'll suggest trusted options."),
]),
("🎒", "What to pack", [
("What should I bring?", "A soft bag instead of a suitcase (there's nowhere to store a suitcase on a yacht), swimwear, light clothes, a windbreaker for the evening, shoes with a light soft sole for the deck, sunscreen and a hat. Towels and linen are already on board. We'll send a full list before the trip."),
]),
("⛵", "Experience & safety", [
("I've never been on a yacht. Will I manage?", "Of course! No experience is needed at all: the captain handles everything to do with the yacht, and you just relax. If you'd like, we'll teach you to take the helm and work the sails; if not — just sunbathe."),
("What if I get seasick?", "We deliberately plan the route in short hops: we spend more time anchored in bays, swimming and sunbathing, than actually sailing. At anchor there's no rocking at all. Seasickness is easy to handle these days — there are tablets and special wristbands. And for anyone who's worried, we choose the calmest route through sheltered bays."),
("Is it safe?", "The captain holds an international licence (IYT/ICC), with over 20,000 nautical miles and 100+ tours behind them. We plan the route only through tried-and-tested places and always check the weather forecast. For beginners we choose calm, sheltered bays."),
]),
("🌤", "Weather & season", [
("When is the best time to go?", "Turkey and Greece — from May to October (Turkey's best late season is September–November; for beginners, May in Turkey is the most pleasant). Seychelles and Thailand — during our winter. Tell us your dates and we'll say where the sea is best at that time."),
]),
("👨‍👩‍👧", "Kids", [
("Can we bring children?", "Not just can — you should! Family tours are our favourite format: half the time is relaxed holiday, half is a programme for the kids. We put the group together so there are other families with children on board too. Children's life jackets and constant supervision go without saying."),
]),
]

METRICA = """<script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");ym(110049558, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", accurateTrackBounce:true, trackLinks:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/110049558" style="position:absolute; left:-9999px;" alt="" /></div></noscript>"""

schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
    for _, _, items in QA for q, a in items]}

chips, sections = [], []
for i, (emoji, title, items) in enumerate(QA):
    cid = "cat%d" % i
    chips.append('<a class="chip" href="#%s">%s %s</a>' % (cid, emoji, title))
    block = '<section id="%s" class="cat"><h2><span class="ce">%s</span>%s</h2>' % (cid, emoji, title)
    for q, a in items:
        block += '<details class="qa"><summary>%s</summary><div class="a"><p>%s</p></div></details>' % (q, a)
    block += '</section>'
    sections.append(block)
chips_html = "\n".join(chips)
body = "\n".join(sections)

html = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Yacht Tour FAQ: Prices, Cabins, Seasickness, Kids | 3Parusa</title>
<meta name="description" content="21 most common questions about catamaran tours: prices, payment, cabins, food, visas, seasickness, kids, safety. Plain answers from the 3Parusa team.">
<link rel="canonical" href="https://3parusa.com/faq.html">
<link rel="alternate" hreflang="en" href="https://3parusa.com/faq.html">
<link rel="alternate" hreflang="ru" href="https://3parusa.ru/faq.html">
<meta property="og:title" content="Yacht Tour FAQ: Prices, Cabins, Seasickness, Kids | 3Parusa"><meta property="og:description" content="21 most common questions about catamaran tours: prices, payment, cabins, food, visas, seasickness, kids, safety."><meta property="og:type" content="website"><meta property="og:image" content="https://3parusa.com@@HERO@@">
<script type="application/ld+json">@@SCHEMA@@</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root{--dark:#191f28;--navy:#06112a;--gold:#d3aa31;--gold2:#d6a000;--sand:#eddba6;--txt:#454545;--bg2:#f8f8f8}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',Arial,sans-serif;font-weight:300;color:var(--txt);line-height:1.7;background:#fff}
h1,h2,h3,.logo,summary,.chip{font-family:'Montserrat',Arial,sans-serif}
header{background:#fff;padding:16px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;border-bottom:1px solid #eee;position:sticky;top:0;z-index:20}
header a.logo{color:var(--dark);font-size:21px;text-decoration:none;font-weight:700;letter-spacing:.5px}
header nav a{color:var(--dark);text-decoration:none;margin-left:18px;font-size:14px;font-weight:500;font-family:'Montserrat',Arial,sans-serif}
header nav a:hover,header nav a.active{color:var(--gold2)}
.hero{position:relative;color:#fff;padding:88px 20px 78px;text-align:center;background:linear-gradient(rgba(15,20,28,.62),rgba(15,20,28,.72)),url('@@HERO@@') center/cover no-repeat}
.hero h1{font-size:clamp(28px,5vw,46px);font-weight:700;max-width:860px;margin:0 auto 16px;line-height:1.22;text-shadow:0 2px 18px rgba(0,0,0,.35)}
.hero p{max-width:640px;margin:0 auto;font-size:18px;font-weight:300;color:#eef1f5}
.cta{display:inline-block;margin-top:28px;background:var(--gold);color:var(--dark);padding:16px 42px;border-radius:100px;text-decoration:none;font-weight:600;font-family:'Montserrat',Arial,sans-serif;font-size:15px;transition:background .2s}
.cta:hover{background:var(--gold2)}
.nav{position:sticky;top:59px;z-index:15;background:#fff;border-bottom:1px solid #eee;padding:14px 16px}
.nav-in{max-width:900px;margin:0 auto;display:flex;flex-wrap:wrap;gap:9px;justify-content:center}
.chip{font-size:13px;font-weight:500;color:var(--dark);text-decoration:none;border:1px solid #e3d9bf;background:#fbf7ea;padding:7px 15px;border-radius:100px;transition:all .18s}
.chip:hover{background:var(--gold);border-color:var(--gold)}
main{max-width:760px;margin:0 auto;padding:44px 20px 20px}
.cat{margin-bottom:34px;scroll-margin-top:130px}
.cat h2{color:var(--dark);font-size:24px;font-weight:600;display:flex;align-items:center;gap:12px;margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid #f0ead7}
.cat h2 .ce{font-size:26px}
.qa{border:1px solid #ececec;border-radius:12px;margin-bottom:12px;background:#fff;overflow:hidden;transition:box-shadow .2s,border-color .2s}
.qa[open]{border-color:var(--gold);box-shadow:0 6px 22px rgba(25,31,40,.07)}
.qa summary{list-style:none;cursor:pointer;padding:18px 52px 18px 22px;font-size:17px;font-weight:600;color:var(--navy);position:relative;user-select:none}
.qa summary::-webkit-details-marker{display:none}
.qa summary::after{content:"+";position:absolute;right:20px;top:50%;transform:translateY(-50%);font-size:24px;font-weight:400;color:var(--gold2);transition:transform .2s}
.qa[open] summary::after{content:"–";transform:translateY(-50%)}
.qa summary:hover{color:var(--gold2)}
.qa .a{padding:0 22px 20px}
.qa .a p{font-size:16.5px;margin:0;color:var(--txt)}
.box{background:var(--bg2);border-left:4px solid var(--gold);padding:20px 22px;border-radius:8px;margin:30px 0 8px}
.box b{color:var(--dark)}
.more{font-size:15.5px;margin-top:18px}
footer{background:var(--dark);color:#aab3bf;text-align:center;padding:30px 20px;margin-top:44px;font-size:14px}
footer a{color:var(--sand);text-decoration:none}
@media(max-width:640px){.hero{padding:64px 18px 56px}.nav{top:57px}.cat{scroll-margin-top:150px}.qa summary{font-size:16px;padding:16px 46px 16px 18px}}
</style>@@METRICA@@</head><body>
<header><a class="logo" href="/">⛵ 3Parusa</a><nav><a href="/#rec">Tours</a><a href="/blog/">Blog</a><a href="/faq.html" class="active">FAQ</a><a href="https://t.me/stas_kochukov">Telegram</a></nav></header>
<div class="hero"><h1>Questions &amp; Answers</h1><p>The 21 questions guests ask us most often. The answers come from thousands of real conversations with our guests — in plain words, straight to the point.</p><a class="cta" href="https://wa.me/79104651420">Ask your question</a></div>
<div class="nav"><div class="nav-in">@@CHIPS@@</div></div>
<main>@@BODY@@
<div class="box"><b>Still have questions?</b> Message us directly — we reply fast and to the point: <a href="https://wa.me/79104651420">WhatsApp +7 910 465-14-20</a> · <a href="https://t.me/stas_kochukov">Telegram @stas_kochukov</a>. — The 3Parusa team
<p class="more">Want more detail? Take a look at our <a href="/blog/">blog</a>: <a href="/blog/do-you-get-seasick-on-a-catamaran.html">about seasickness</a>.</p></div>
</main>
<footer>3Parusa — curated sailing tours worldwide · 20,000 nm · 20+ countries · 1,000 happy guests<br><a href="/">3parusa.com</a> · <a href="/privacy.html">Privacy policy</a></footer>
</body></html>"""
html = (html.replace("@@SCHEMA@@", json.dumps(schema, ensure_ascii=False))
            .replace("@@METRICA@@", METRICA).replace("@@CHIPS@@", chips_html)
            .replace("@@BODY@@", body).replace("@@HERO@@", HERO))

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
