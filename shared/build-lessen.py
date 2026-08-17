#!/usr/bin/env python3
"""Build Aqua Power + Aqua Joggen booklet HTML from aligned exercise data."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def li(name, cue=""):
    if cue:
        return f"<li>{escape(name)} <small>{escape(cue)}</small></li>"
    return f"<li>{escape(name)}</li>"


def ol(items, klass=None):
    cls = f' class="{klass}"' if klass else ""
    inner = "\n            ".join(li(n, c) for n, c in items)
    return f"<ol{cls}>\n            {inner}\n          </ol>"


def card(kind, les):
    n = les["n"]
    return f'''      <article class="card" id="les-{n}" data-les="{n}">
        <header class="card-head">
          <p class="brand">FeelFitCentrum · {kind}</p>
          <h1>Les {n} · {escape(les["title"])}</h1>
          <p class="meta">45′ · {escape(les["mat"])} · klok = 1′</p>
        </header>
        <p class="cue">{escape(les["cue"])}</p>
        <div class="block">
          <h2>WU <span>5×1′ · geen mat.</span></h2>
          {ol(les["wu"])}
        </div>
        <div class="block kern">
          <h2>Kern 1 <span>8×1′ · 2 ronden · {escape(les["k1mat"])}</span></h2>
          {ol(les["k1"], "grid-ex")}
        </div>
        <div class="block kern">
          <h2>Kern 2 <span>8×1′ · 2 ronden · {escape(les["k2mat"])}</span></h2>
          {ol(les["k2"], "grid-ex")}
        </div>
        <div class="block">
          <h2>Buik <span>5×1′</span></h2>
          {ol(les["buik"])}
        </div>
        <div class="block cool">
          <h2>CD <span>5′</span></h2>
          <p>{escape(les["cd"])}</p>
        </div>
      </article>'''


# Imposition: [08|01] [02|07] [06|03] [04|05]
SHEETS = [("08", "01"), ("02", "07"), ("06", "03"), ("04", "05")]


def booklet(kind, slug, theme, hint, extra_guide, lessons):
    by_n = {x["n"]: x for x in lessons}
    sheets = []
    for a, b in SHEETS:
        sheets.append(
            "    <section class=\"sheet\">\n"
            + card(kind, by_n[a])
            + "\n\n"
            + card(kind, by_n[b])
            + "\n    </section>"
        )
    body_cls = f' class="{theme}"' if theme else ""
    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{kind} — Lesboekje | FeelFitCentrum</title>
  <link rel="stylesheet" href="../shared/print.css" />
</head>
<body{body_cls}>
  <header class="screen-only toolbar">
    <div>
      <strong>FeelFitCentrum</strong> · {kind}
      <span class="hint">{escape(hint)}</span>
    </div>
    <button type="button" onclick="window.print()">Printen</button>
  </header>

  <nav class="screen-only les-nav" aria-label="Lessen">
    <a href="#les-01">01</a>
    <a href="#les-02">02</a>
    <a href="#les-03">03</a>
    <a href="#les-04">04</a>
    <a href="#les-05">05</a>
    <a href="#les-06">06</a>
    <a href="#les-07">07</a>
    <a href="#les-08">08</a>
  </nav>

  <main class="booklet">
{chr(10).join(sheets)}
  </main>

  <aside class="screen-only guide">
    <h2>{kind} — printen</h2>
    <ol>
      <li>A4 liggend · dubbelzijdig · <strong>omkeer korte zijde</strong>.</li>
      <li>Vel 2 in vel 1 · vouwen → A5-boekje Les 01–08.</li>
      <li>{escape(extra_guide)}</li>
    </ol>
  </aside>
</body>
</html>
'''


WU_POWER = [
    ("Jog + circels", "Op de plek joggen, armen groot draaien"),
    ("Open/dicht + sweep", "Benen open-dicht, armen door het water"),
    ("Kick V-N-A", "Kick voor, naast, achter — wissel"),
    ("Skippen + hakken", "High knees ↔ hakken tegen de billen"),
    ("Jack + tempo omhoog", "Jumping jack, laatste 20″ sneller"),
]

WU_JOG = [
    ("Jog + circels", "Drijf rechtop, joggen, armen groot draaien"),
    ("Open/dicht + sweep", "Benen open-dicht, armen door het water"),
    ("Kick V-N-A", "Kick voor, naast, achter — wissel"),
    ("Skippen + hakken", "Knieën hoog ↔ hakken naar de billen"),
    ("Jack + tempo omhoog", "Open/dicht jack, laatste 20″ sneller"),
]

CD_POWER = "Langzaam joggen → stretch borst, schouder, heup, kuit → adem 1′"
CD_JOG = "Easy jog → stretch in drijf (borst, schouder, heup) → lange uitademing 1′"

POWER = [
    {
        "n": "01",
        "title": "Waterwerk",
        "mat": "geen materiaal",
        "k1mat": "geen mat.",
        "k2mat": "geen mat.",
        "cue": "1 materiaalregel: niks in de hand · been ↔ arm",
        "wu": WU_POWER,
        "k1": [
            ("Jumping jack", "Open-dicht springen, armen mee"),
            ("Skippen + jog", "Knieën hoog, jog tussendoor"),
            ("Hakken + knie", "Hakken-billen wissel kniehef"),
            ("High jack", "Brede jack, armen hoog"),
            ("Kikker sprong", "Frog: knieën zij, strek af"),
            ("Onder knie kijken", "Tilt knie, kijk eronder, wissel"),
            ("Water scheppen V/A", "Schep water voor én achter"),
            ("Twist", "Romp draait, bekken stabiel"),
        ],
        "k2": [
            ("Circels + jog", "Armcircels voor je, joggen"),
            ("Dippen + jog", "Duwen omlaag naast heup, jog"),
            ("Boxen", "Jab-cross, schouders laag"),
            ("Side press + kick", "Zijpress + zijkick zelfde kant"),
            ("Fly + jog", "Armen open-dicht borsthoog, jog"),
            ("Row laag", "Trek naar ribben, ellebogen langs"),
            ("Uppercuts + jog", "Uppercut L/R, lichte jog"),
            ("Press + jog", "Duwen naar voren, jog op de plek"),
        ],
        "buik": [
            ("Twist laag", "Draai laag in het water, 1′"),
            ("Onder knie", "Knie tuck + lichte crunch"),
            ("Side crunch L/R", "30″ links, 30″ rechts"),
            ("Flutter kick", "Kleine trappeltjes, core strak"),
            ("Boten hold", "V-zit gevoel, 40″ + adem 20″"),
        ],
        "cd": CD_POWER,
    },
    {
        "n": "02",
        "title": "Dumbbells",
        "mat": "1 materiaal: dumbbells",
        "k1mat": "DB",
        "k2mat": "DB",
        "cue": "DB de hele les · lang = groot/traag · laag = diep in het water",
        "wu": WU_POWER,
        "k1": [
            ("Circel press + jog", "DB voor borst, circels, jog"),
            ("Reverse fly + lang", "Buig licht, open armen traag"),
            ("Side raises + lang", "Zijwaarts tillen, volle baan"),
            ("Upright row + benen", "Trek naar kin + open/dicht"),
            ("Biceps + laag", "Curl diep in het water"),
            ("Onder knie kijken", "DB bij schouder, kijk onder knie"),
            ("Wood chopper", "Hoog→laag diagonaal, wissel L/R"),
            ("Pull down + jump", "Trek omlaag + kleine sprong"),
        ],
        "k2": [
            ("Press + jog", "Chest press, jog op de plek"),
            ("Uppercuts + jog", "Uppercut met DB, jog"),
            ("Boxen + lang", "Lange stoot, traag krachtig"),
            ("Side press + kick", "Zijpress + kick"),
            ("Circels + jog", "Grote armcircels, jog"),
            ("Boten + lang", "Roeibeweging, lange haal"),
            ("Fly + jog", "Chest fly, jog"),
            ("Twist", "DB voor je, romp draait"),
        ],
        "buik": [
            ("Twist + DB", "Russian twist staand/drijf licht"),
            ("Wood chopper slow", "Langzaam hakken L/R"),
            ("Standing crunch", "Knie op, DB naar knie"),
            ("Side bend L/R", "DB 1 kant, buig zij"),
            ("Hold press 30″ + adem", "Press vasthouden, dan adem"),
        ],
        "cd": CD_POWER,
    },
    {
        "n": "03",
        "title": "Barbell burn",
        "mat": "1 materiaal: aqua barbells",
        "k1mat": "barbell",
        "k2mat": "barbell",
        "cue": "Stang de hele les · grip wisselt,zelfde stang",
        "wu": WU_POWER,
        "k1": [
            ("Press + jog", "Stang vooruit duwen, jog"),
            ("Upright row + benen", "Trek omhoog + kniehef"),
            ("Boten + lang", "Roeihaals, lange arm"),
            ("Row + lang", "Stang naar ribben, traag"),
            ("Circel press", "Circels met stang voor je"),
            ("Dippen + jog", "Stang omlaag duwen, jog"),
            ("Pull down + jump", "Omlaag trekken + sprong"),
            ("Biceps / triceps", "30″ curl, 30″ kickback"),
        ],
        "k2": [
            ("Side press + kick", "Stang opzij + kick"),
            ("Kanoen", "Peddel L/R, romp draait mee"),
            ("Wood chopper", "Diagonaal hakken over stang"),
            ("Leg press + hold", "Squat tegen water, stang voor"),
            ("High jack + hold", "Jack, stang op borst"),
            ("Boxen", "Stootgevoel met stang kort"),
            ("Twist + lang", "Draai met stang, groot"),
            ("Jumping jack", "Jack, stang mee of hold"),
        ],
        "buik": [
            ("Twist + stang", "Romp roteert, heup stil"),
            ("Kanoen slow", "Lange peddel, core"),
            ("Standing crunch", "Knie op, stang naar knie"),
            ("Side bend", "Stang overhead of voor"),
            ("Hold 40″ + adem", "Stang op borst, strak"),
        ],
        "cd": CD_POWER,
    },
    {
        "n": "04",
        "title": "Noodle lang",
        "mat": "1 materiaal: noodles",
        "k1mat": "noodle",
        "k2mat": "noodle",
        "cue": "Noodle de hele les · lang = grote baan door het water",
        "wu": WU_POWER,
        "k1": [
            ("Circel press + lang", "Noodle voor je, grote circels"),
            ("Reverse fly", "Open de borst, noodle in handen"),
            ("Press-out", "Duwen naar voren, terug gecontroleerd"),
            ("Pull down + jump", "Noodle omlaag + sprong"),
            ("Side raises + lang", "Zijwaarts tillen met noodle"),
            ("Row + lang", "Trek naar je toe, lange haal"),
            ("Wood chopper", "Noodle hoog→laag diagonaal"),
            ("Water scheppen", "Schep met noodle voor/achter"),
        ],
        "k2": [
            ("Dippen + jog", "Noodle naast heup omlaag, jog"),
            ("Boxen", "Stoten met noodle als stok"),
            ("Side press + kick", "Zijduw + kick"),
            ("Kanoen", "Peddel met noodle L/R"),
            ("Circels zijwaarts", "Circels naast het lichaam"),
            ("Twist", "Noodle voor je, draai"),
            ("Figure-8", "Achtjes door het water"),
            ("Sprint + hold", "Jog hard, noodle voor je"),
        ],
        "buik": [
            ("Noodle crunch", "Zit/drijf licht op noodle"),
            ("Twist", "Noodle voor, romp draait"),
            ("Leg lifts", "Noodle onder oksels, benen op"),
            ("Side crunch L/R", "Noodle mee"),
            ("Hollow hold", "Lang lichaam, 40″"),
        ],
        "cd": CD_POWER,
    },
    {
        "n": "05",
        "title": "Schijven",
        "mat": "1 materiaal: schijven",
        "k1mat": "schijf",
        "k2mat": "schijf",
        "cue": "Schijven de hele les · plat = meer weerstand",
        "wu": WU_POWER,
        "k1": [
            ("Dippen + jog", "Schijven omlaag, jog"),
            ("Circels zijwaarts", "Circels naast je, plat in water"),
            ("Side press + kick", "Zijpress + kick"),
            ("Boxen + laag", "Stoten laag in het water"),
            ("Upright row + benen", "Trek omhoog + kniehef"),
            ("Biceps / triceps + jog", "Curl ↔ kickback, jog"),
            ("Reverse fly + laag", "Open armen, diep"),
            ("Water scheppen V/A", "Schep voor en achter"),
        ],
        "k2": [
            ("Press + jog", "Vooruit duwen, jog"),
            ("Jumping jack", "Jack, schijven mee"),
            ("Uppercuts + jog", "Uppercut, schijven in hand"),
            ("Onderknie + kick", "Kijk onder knie + kick"),
            ("Fly + jog", "Open-dicht, jog"),
            ("Row + laag", "Trek laag naar ribben"),
            ("Circels + jog", "Circels voor je, jog"),
            ("Twist + laag", "Draai diep, schijven voor"),
        ],
        "buik": [
            ("Twist + schijf", "Romp roteert"),
            ("Wood chopper slow", "Schijf hoog→laag"),
            ("Standing crunch", "Knie op, schijf naar knie"),
            ("Side bend L/R", "1 schijf, buig zij"),
            ("Hold scoop 30″", "Schephouding, core aan"),
        ],
        "cd": CD_POWER,
    },
    {
        "n": "06",
        "title": "Bal",
        "mat": "1 materiaal: bal",
        "k1mat": "bal",
        "k2mat": "bal",
        "cue": "1 bal de hele les · doorgeven = onder knie / achter",
        "wu": WU_POWER,
        "k1": [
            ("Circels + jog", "Bal voor je, circels, jog"),
            ("Row + laag", "Bal naar je toe, laag"),
            ("Onder knie doorgeven", "Bal onder knie wissel L/R"),
            ("Basketball + jog", "Dribbelgevoel in water, jog"),
            ("Side press + kick", "Bal opzij duwen + kick"),
            ("Achter doorgeven", "Bal achter de rug wisselen"),
            ("Biceps + laag", "Bal omhoog curl-achtig"),
            ("Twist + laag", "Bal voor heup, draai diep"),
        ],
        "k2": [
            ("Press + jog", "Bal vooruit, jog"),
            ("Kikker sprong", "Frog, bal op borst"),
            ("Dippen + jog", "Bal omlaag duwen, jog"),
            ("Boten + laag", "Roei met bal, laag"),
            ("Upright row + benen", "Bal naar kin + kniehef"),
            ("Kniehef / hakken", "Kniehef ↔ hakken, bal hold"),
            ("Water scheppen", "Bal schept water V/A"),
            ("Fly + hold", "Open-dicht om de bal"),
        ],
        "buik": [
            ("Twist + bal", "Russian twist"),
            ("Crunch + reach", "Bal naar knieën"),
            ("Onder knie doorgeven", "Langzaam, core"),
            ("Side crunch L/R", "Bal op heup"),
            ("Hold 40″ + adem", "Bal op borst, strak"),
        ],
        "cd": CD_POWER,
    },
    {
        "n": "07",
        "title": "Tempo jump",
        "mat": "geen materiaal",
        "k1mat": "geen mat.",
        "k2mat": "geen mat.",
        "cue": "Geen mat. · extra sprong/tempo t.o.v. les 01",
        "wu": WU_POWER,
        "k1": [
            ("Fast feet", "Korte snelle stappen op de plek"),
            ("Grapevine L/R", "Zijwaarts kruisloop"),
            ("Kick power V-N-A", "Krachtige kick 3 richtingen"),
            ("Ski / cross-country", "Diagonaal arm-been"),
            ("Open/dicht jack", "Jack zonder extra sprongdruk"),
            ("Kniehef sprong", "Knie omhoog, klein afzetten"),
            ("Heel digs", "Hak in de bodem, wissel"),
            ("Side shuffle + punch", "Shuffle + stoot"),
        ],
        "k2": [
            ("Squat pulse + reach", "Klein squatten, armen reiken"),
            ("Lunge switch L/R", "Uitval wissel, 30″ per been"),
            ("Jump kick", "Kick met lichte sprong"),
            ("Breaststroke + jog", "Schoolslag-armen, jog"),
            ("Crawl + ski", "Crawl-armen + ski-benen"),
            ("Pendulum benen", "Benen L/R als slinger"),
            ("Mountain climber", "Staand, knieën snel"),
            ("Twist sprint", "Draai + korte versnelling"),
        ],
        "buik": [
            ("Twist jog light", "Lichte jog, romp draait"),
            ("Kikker hold", "Frog-positie vasthouden"),
            ("Side crunch march", "Knie zij + crunch"),
            ("Flutter kick", "Trappelen, core"),
            ("Wall sit 30″ + adem", "Rug tegen wand, dan adem"),
        ],
        "cd": CD_POWER,
    },
    {
        "n": "08",
        "title": "DB boxen",
        "mat": "1 materiaal: dumbbells",
        "k1mat": "DB",
        "k2mat": "DB",
        "cue": "DB de hele les · andere set dan les 02 (meer stoot/combo)",
        "wu": WU_POWER,
        "k1": [
            ("Cross punch L/R", "Kruisstoot, DB licht"),
            ("Uppercut combo", "3 uppercuts + jog 10″"),
            ("Hook + jog", "Hoekstoot L/R, jog"),
            ("Speed punch", "Korte snelle stoten"),
            ("Press + squat", "Squat en duw uit"),
            ("Row + open/dicht", "Row, benen open-dicht"),
            ("Hammer curl", "Duim-omhoog curl"),
            ("Front raise + kick", "Voor tillen + frontkick"),
        ],
        "k2": [
            ("Circel press + squat", "Circels in squat"),
            ("Side raise + side step", "Zijtillen + sidestep"),
            ("Pull down + kikker", "Omlaag + frog"),
            ("Wood chopper + kick", "Hak + kick"),
            ("Dippen + high jack", "Dip + brede jack"),
            ("Upright row + hakken", "Row + hakken-billen"),
            ("Boxen + grapevine", "Stoten tijdens grapevine"),
            ("Press + lunge", "Uitval L/R + press"),
        ],
        "buik": [
            ("Uppercut slow", "Traag, core draait mee"),
            ("Twist + DB", "Romp, heup stil"),
            ("Crunch + press", "Knie op + lichte press"),
            ("Side punch L/R", "Stoot laag opzij"),
            ("Hold 30″ + adem", "DB op borst"),
        ],
        "cd": CD_POWER,
    },
]


def jog_adapt(power_lessons):
    """Same lesson names/materials; standing-only moves → float versions."""
    swap_name = {
        "Jumping jack": "Jack (open/dicht)",
        "High jack": "Wide jack",
        "High jack + hold": "Wide jack + hold",
        "Kikker sprong": "Kikker kick",
        "Pull down + jump": "Pull down + kick",
        "Fast feet": "Fast jog",
        "Grapevine L/R": "Side kick travel L/R",
        "Heel digs": "Hakken drijf",
        "Side shuffle + punch": "Side kick + punch",
        "Squat pulse + reach": "Bicycle + reach",
        "Lunge switch L/R": "Kick-back L/R",
        "Jump kick": "Power kick",
        "Mountain climber": "High knees snel",
        "Press + squat": "Press + bicycle",
        "Circel press + squat": "Circel press + bicycle",
        "Dippen + high jack": "Dippen + wide jack",
        "Boxen + grapevine": "Boxen + side travel",
        "Press + lunge": "Press + kick-back",
        "Kniehef sprong": "Kniehef power",
        "Leg press + hold": "Bicycle + press hold",
        "Wall sit 30″ + adem": "V-sit 30″ + adem",
        "Sprint + hold": "Sprint jog + hold",
    }
    swap_cue = {
        "Open-dicht springen, armen mee": "Open-dicht in drijf, armen mee",
        "Frog: knieën zij, strek af": "Frogkick: knieën zij, strek (geen bodem)",
        "Trek omlaag + kleine sprong": "Trek omlaag + krachtige kick",
        "Noodle omlaag + sprong": "Noodle omlaag + kick",
        "Stang omlaag duwen, jog": "Stang omlaag, jog in drijf",
        "Squat tegen water, stang voor": "Bicycle, stang voor je duwen",
        "Jack, stang op borst": "Open/dicht, stang op borst",
        "Jack, stang mee of hold": "Jack-benen, stang hold",
        "Noodle omlaag + sprong": "Noodle omlaag + kick",
        "Jog hard, noodle voor je": "Sprint-jog, noodle voor je",
        "Korte snelle stappen op de plek": "Korte snelle jog, geen bodem",
        "Zijwaarts kruisloop": "Zijkick, verplaats L/R",
        "Hak in de bodem, wissel": "Hakken naar billen, drijf",
        "Shuffle + stoot": "Zijkick + stoot",
        "Klein squatten, armen reiken": "Bicycle, armen reiken",
        "Uitval wissel, 30″ per been": "Kick-back, 30″ per been",
        "Kick met lichte sprong": "Krachtige kick, heup stabiel",
        "Staand, knieën snel": "Knieën snel, rechtop drijven",
        "Squat en duw uit": "Bicycle + press",
        "Circels in squat": "Circels + bicycle",
        "Dip + brede jack": "Dip + wide jack",
        "Stoten tijdens grapevine": "Stoten + zijkick travel",
        "Uitval L/R + press": "Kick-back L/R + press",
        "Knie omhoog, klein afzetten": "Kniehef krachtig, drijf",
        "Rug tegen wand, dan adem": "Lange V-sit, dan adem",
        "Jack, schijven mee": "Open/dicht, schijven mee",
        "Frog, bal op borst": "Frogkick, bal op borst",
        "Omlaag + frog": "Omlaag + frogkick",
        "Jack + kleine sprong": "Open/dicht jack drijf",
    }
    out = []
    for les in power_lessons:
        nles = dict(les)
        nles["wu"] = WU_JOG
        nles["cd"] = CD_JOG
        if nles["n"] == "07":
            nles["cue"] = "Geen mat. · drijven · extra tempo t.o.v. les 01"
        if nles["title"] == "Tempo jump":
            nles["title"] = "Tempo drijf"

        def conv(items):
            r = []
            for name, cue in items:
                r.append((swap_name.get(name, name), swap_cue.get(cue, cue)))
            return r

        nles["k1"] = conv(les["k1"])
        nles["k2"] = conv(les["k2"])
        nles["buik"] = conv(les["buik"])
        # extra jog cue on first
        if nles["n"] == "01":
            nles["cue"] = "Geen mat. · band om · geen bodem · been ↔ arm"
        out.append(nles)
    return out


JOG = jog_adapt(POWER)


def main():
    (ROOT / "aqua-power" / "index.html").write_text(
        booklet(
            "Aqua Power",
            "aqua-power",
            "",
            "Staan · 1,2–1,5 m · 1 mat./les · tik 01–08 of print A4",
            "Bad 1,2–1,5 m (staan) · 1 klokslag = 1′ · 1 type materiaal per les (of geen).",
            POWER,
        ),
        encoding="utf-8",
    )
    (ROOT / "aqua-joggen" / "index.html").write_text(
        booklet(
            "Aqua Joggen",
            "aqua-joggen",
            "theme-joggen",
            "Drijven · band · 1,90 m · 1 mat./les · tik 01–08 of print A4",
            "Bad 1,90 m · band om, drijven · geen bodem · 1 type materiaal per les (of geen).",
            JOG,
        ),
        encoding="utf-8",
    )
    print("wrote aqua-power/index.html and aqua-joggen/index.html")


if __name__ == "__main__":
    main()
