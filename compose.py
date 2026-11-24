#!/usr/bin/env python3
"""THE DAY'S POST — NI23 G4 final3 front page composer (v3).

Original drawing code for account final3 (@meleyotcok). Classic broadsheet
front page for Monday 23 November 2026, exactly 1024x1024.
Palette: light sepia paper, teal ink, brick-red accent.
Usage: python3 compose.py [A|B] [out.png]
"""
import sys
from PIL import Image, ImageDraw, ImageFont

FDIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = H = 1024
PAPER = (243, 233, 210)
PAPER2 = (250, 244, 228)
CARD = (252, 247, 233)
TEAL = (15, 76, 76)
TEAL_D = (9, 52, 54)
TEAL_L = (64, 128, 122)
BRICK = (179, 64, 42)
BRICK_D = (140, 44, 28)
GOLD = (176, 132, 44)
GREY = (96, 92, 80)
LINE = (120, 110, 88)
INK = (40, 40, 36)

def F(name, size):
    return ImageFont.truetype(FDIR + name, size)

PB, PFB, AB, AR = "PlayfairDisplay-Black.ttf", "PlayfairDisplay-Bold.ttf", "Archivo-Bold.ttf", "Archivo.ttf"

def fb(n):
    return F(AB, n)

def fr(n):
    return F(AR, n)

def fsr(n):
    return F(AR, n)

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(d, x, y, text, font, fill, maxw, leading=None, max_lines=None):
    lines = wrap(d, text, font, maxw)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(font.size * 1.18)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

# ---------------------------------------------------------------- scenes
def scene(d, kind, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 222, 192))
    if kind == "blast":
        d.rectangle([x, y + h - 10, x + w, y + h], fill=(150, 128, 92))
        for i, r in enumerate((15, 10, 6)):
            cx = x + w // 2 + (i - 1) * 15
            d.ellipse([cx - r, y + h - 24 - r, cx + r, y + h - 24 + r], fill=BRICK if i == 1 else GOLD)
        for dx in (-24, 0, 24):
            d.line([x + w // 2 + dx, y + h - 22, x + w // 2 + dx * 2, y + 8], fill=GOLD, width=2)
    elif kind == "radar":
        d.rectangle([x, y + h - 8, x + w, y + h], fill=TEAL_L)
        d.polygon([(x + 12, y + h - 8), (x + 26, y + 10), (x + 40, y + h - 8)], outline=TEAL_D, width=3)
        for r in (7, 13, 19):
            d.arc([x + 26 - r, y + 10 - r, x + 26 + r, y + 10 + r], -60, 60, fill=BRICK, width=2)
        d.ellipse([x + w - 22, y + 8, x + w - 12, y + 18], fill=BRICK)
    elif kind == "ship":
        d.rectangle([x, y + h - 14, x + w, y + h], fill=(96, 140, 150))
        d.polygon([(x + 8, y + h - 14), (x + 16, y + h - 26), (x + w - 18, y + h - 26), (x + w - 8, y + h - 14)], fill=TEAL_D)
        d.rectangle([x + 22, y + h - 38, x + 48, y + h - 26], fill=PAPER2)
        for fx in (30, 40):
            d.polygon([(x + fx, y + h - 52), (x + fx + 4, y + h - 38), (x + fx - 4, y + h - 38)], fill=BRICK)
    elif kind == "rubble":
        d.polygon([(x + 4, y + h - 6), (x + 20, y + 12), (x + 36, y + h - 6)], fill=GREY)
        d.polygon([(x + 28, y + h - 6), (x + 46, y + 20), (x + 62, y + h - 6)], fill=(140, 134, 118))
        d.ellipse([x + w - 28, y + 8, x + w - 14, y + 22], fill=GOLD)
        d.line([x + w - 21, y + 22, x + w - 21, y + h - 8], fill=TEAL_D, width=3)
    elif kind == "climate":
        d.ellipse([x + 8, y + 6, x + 48, y + 46], outline=TEAL, width=3)
        d.line([x + 14, y + 27, x + 42, y + 27], fill=TEAL_L, width=2)
        d.polygon([(x + w - 34, y + h - 6), (x + w - 19, y + 10), (x + w - 4, y + h - 6)], fill=(150, 128, 92))
    elif kind == "ballot":
        d.rectangle([x + 8, y + 10, x + w - 8, y + h - 10], outline=TEAL_D, width=3)
        d.line([x + 16, y + 24, x + 30, y + 36], fill=BRICK, width=4)
        d.line([x + 30, y + 36, x + w - 16, y + 14], fill=BRICK, width=4)
    elif kind == "march":
        for cx in (16, 38, 60):
            d.ellipse([x + cx - 5, y + 12, x + cx + 5, y + 22], fill=TEAL_D)
            d.line([x + cx, y + 22, x + cx, y + h - 8], fill=TEAL_D, width=3)
        d.rectangle([x + 4, y + 2, x + w - 4, y + 10], fill=BRICK)
    elif kind == "cricket":
        d.rectangle([x + 6, y + h - 10, x + w - 6, y + h - 5], fill=(122, 156, 96))
        for sx in (w // 2 - 8, w // 2, w // 2 + 8):
            d.rectangle([x + sx, y + 10, x + sx + 3, y + h - 10], fill=GOLD)
        d.ellipse([x + w - 24, y + 6, x + w - 14, y + 16], fill=BRICK)
    elif kind == "court":
        d.polygon([(x + 6, y + 10), (x + w // 2, y + 3), (x + w - 6, y + 10), (x + w - 6, y + 15), (x + 6, y + 15)], fill=TEAL_D)
        for cx in range(x + 12, x + w - 10, 13):
            d.rectangle([cx, y + 18, cx + 5, y + h - 12], fill=TEAL_L)
        d.rectangle([x + 6, y + h - 11, x + w - 6, y + h - 6], fill=TEAL_D)
    elif kind == "drone":
        cx, cy = x + w // 2, y + 16
        d.line([cx - 18, cy, cx + 18, cy], fill=TEAL_D, width=3)
        d.line([cx, cy - 6, cx, cy + 8], fill=TEAL_D, width=3)
        for ex in (cx - 21, cx + 21):
            d.ellipse([ex - 4, cy - 10, ex + 4, cy - 2], outline=BRICK, width=2)
        d.rectangle([x + 10, y + h - 14, x + w - 10, y + h - 6], fill=GREY)
    elif kind == "tennis":
        d.ellipse([x + 10, y + 8, x + 50, y + h - 8], outline=TEAL_D, width=3)
        d.line([x + 45, y + h - 12, x + w - 8, y + h - 3], fill=TEAL_D, width=4)
        d.ellipse([x + w - 28, y + 6, x + w - 16, y + 18], fill=(168, 196, 74))
    else:
        d.ellipse([x + w // 2 - 12, y + 6, x + w // 2 + 12, y + 30], fill=GOLD)
        d.rectangle([x + 6, y + h - 10, x + w - 6, y + h - 5], fill=TEAL_L)

# ---------------------------------------------------------------- data
# grid tuples: (num, region, topic, src, head, deck, kind) — cards 4-12
grid = [
    (4, "STRAIT OF HORMUZ", "MIDDLE EAST · WAR", "AP live · 23 Nov",
     "Tankers Burn in the Gulf", "War spreads to the Gulf; IRGC warns of unrest.", "ship"),
    (5, "KYIV, UKRAINE", "EUROPE · WAR", "BBC · 23 Nov",
     "Kyiv Boy Pulled Alive From Rubble", "A boy of 7 pulled alive from ruins; 6 died.", "rubble"),
    (6, "KYIV REGION", "EUROPE · WAR", "JagranJosh · 23 Nov",
     "14 Missing After Kyiv Strike", "14 missing, Zelenskiy says, after Kyiv drone hit.", "drone"),
    (7, "WASHINGTON, USA", "NORTH AMERICA · POLITICS", "BBC · 23 Nov",
     "Democrats Take House 258-173", "Biggest since 1992; North Carolina seat flips.", "ballot"),
    (8, "GULF OF FINLAND", "EUROPE · SEA", "BBC · 23 Nov",
     "Russian Ship Still Burns", "Cargo ship still ablaze off Finland; 1 more towed.", "ship"),
    (9, "THE HAGUE", "ASIA · LAW", "Guardian/NYT · 23 Nov",
     "ICJ: Myanmar Guilty of Genocide", "Rohingya campaign in Myanmar drove out 700,000+.", "court"),
    (10, "WELLINGTON, NZ", "ASIA · SPORT", "ObserverVoice · 23 Nov",
     "India Declare on Record 720/9", "Record 720 in Wellington, a New Zealand best.", "cricket"),
    (11, "LISBON, PORTUGAL", "EUROPE · SOCIETY", "JagranJosh · 23 Nov",
     "Lisbon Marches on Living Costs", "Thousands march in Lisbon over Portugal prices.", "march"),
    (12, "ATP FINALS", "EUROPE · SPORT", "BBC · 23 Nov",
     "Alcaraz Wins First ATP Finals", "Beats Zverev in Turin for a first Finals crown.", "tennis"),
]
CHIPS = {1: "OFFICIAL", 2: "CLAIM", 3: "OFFICIAL", 4: "REPORTED", 5: "REPORTED", 6: "ON RECORD",
         7: "CONFIRMED", 8: "ONGOING", 9: "OFFICIAL", 10: "REPORTED", 11: "REPORTED", 12: "REPORTED"}

BRIEFS_L = [
    "Houthi missile at Saudi Arabia intercepted",
    "Swimmer crosses Hormuz for Iran's wildlife",
    "States agree to keep UN talks on AI weapons",
    "US declassifies more UFO footage from Mideast",
    "Albanese: COP31 failure a 'hard age' sign",
    "Benghazi ship blast a suspected drone strike",
    "UK-EU reset deal called 'landmark' by Burnham",
    "Myanmar junta calls ASEAN ruling unfair",
    "Escaped lion spreads fear in Turkish town",
    "Nepal PM Shah holds talks with Modi in Delhi",
    "India, Bulgaria discuss IMEC, Black Sea",
    "Guru Nanak Jayanti marked across India",
    "UP air-raid, blackout drills in 75 districts",
    "Indonesia fire update: 7 bodies found, 50 lost",
    "India chase famous win, NZ 119/2 on day five",
]
BRIEFS_R = [
    "India win ODI series in NZ 3-2, Phillips best",
    "Anupama defends IBSF world snooker title",
    "World Chess Championship draws global fans",
    "MP Wadkute dies of heart attack in Delhi",
    "Kota pilgrim bus tragedy kills 9 in Rajasthan",
    "Tata Steel pipe sale to APL Apollo Rs28,000 cr",
    "SpiceJet pilots seek audit; IndiGo at 65.9%",
    "IFFI 2026 hosts BRICS roundtable in Goa",
    "Modi opens IIT Patna AI centre, Rs400 cr",
    "Shah launches Rs4,000 cr Arunachal push",
    "Chief Justice: AI rules a must in law study",
    "Gold slides to $3,538/oz from $5,595 record",
    "NEET PG 2026: 10,105 med seats flagged blocked",
    "Google puts $5m into IIT Kharagpur AI study",
]

dc = ("D1 Xi-Trump-Putin trilateral summit, 19 Nov 2026 · D2 Russian missiles and drones fell in Poland, 20 Nov 2026 · "
      "D3 SpiceJet Rs5,500 crore fundraise approved, 18 Nov 2026 · D4 Hyderabad bomb-threat email sent, 21 Nov 2026 · "
      "D5 Paolo Bulgari died, reported 22 Nov 2026 · D6 Kim Jong-un security speech in Seoul, 22 Nov 2026 · "
      "D7 24 civilians killed in South Sudan, Juba, 22 Nov 2026 · D11 South Korea education minister resigned, first reported 22 Nov 2026 · "
      "D12 Indonesia candy-factory fire itself, 22 Nov 2026")
DATECHECK = [
    "D1 Xi-Trump-Putin summit - 19 Nov 2026",
    "D2 Missiles/drones fell in Poland - 20 Nov",
    "D3 SpiceJet Rs5,500 cr nod - 18 Nov 2026",
    "D4 Hyderabad bomb-threat email - 21 Nov",
    "D5 Paolo Bulgari died - told 22 Nov 2026",
    "D6 Kim Jong-un in Seoul - 22 Nov 2026",
    "D7 24 killed, South Sudan - Juba, 22 Nov",
    "D11 S. Korea minister quit - told 22 Nov",
    "D12 Indonesia factory fire itself - 22 Nov",
]

NUMS = [
    ("258-173", "Democrats' House majority (card 7)"),
    ("720/9d", "India's record Test total (card 10)"),
    ("7 + 50", "bodies found + still missing today"),
    ("14", "missing after Kyiv strike (card 6)"),
    ("6", "dead in the Kyiv strike (card 5)"),
    ("$3,538", "gold per ounce after the slide"),
]

REGIONS = [("MIDEAST", 4, BRICK), ("EUROPE", 9, TEAL), ("S ASIA", 17, TEAL_L),
           ("SE ASIA", 3, GOLD), ("ASIA-PAC", 1, (70, 90, 120)), ("N AMERICA", 3, BRICK_D),
           ("AFRICA", 1, GREY), ("GLOBAL", 3, (110, 84, 140))]

TL = [("00:02Z", "UN AI talks go on"), ("02:00", "Albanese on COP31"),
      ("06:00", "Hormuz tankers ablaze"), ("09:30", "Kyiv boy rescued"),
      ("12:00", "House majority set"), ("16:00", "Iowa blast plan")]

MAPROWS = [
    "........XX....................................",
    ".....XXXXXXX...........XXXXXX....XX...........",
    "...XXXXXXXXX.........XXXXXXXXXXXXXXXX..XX.....",
    "....XXXXXXX...........XXXXXXXXXXXXXXX.........",
    ".....XXXXX.....X......XXXXXXXXXXXX....XX......",
    "......XXX.....XXX......XXXXXXXXXX.............",
    ".......XX......XXXX.....XXXXXXXX.......XX.....",
    ".......XX.......XX.......XXXXXX.......XXXX....",
    "......XXXX................XXXX.........XX.....",
    "......XXXX.................XXX................",
    ".......XXX..................XX.........XX.....",
    ".......XX...................XX........XXXX....",
    "......................................XXXX....",
    ".......................................XX.....",
]
PINS = [(1, 10, 3), (2, 27, 5), (3, 25, 4), (4, 28, 6), (5, 24, 3), (6, 24, 2),
        (7, 6, 4), (8, 23, 1), (9, 33, 8), (10, 43, 12), (11, 20, 5), (12, 21, 4)]

def chip(d, x, y, label):
    f = F(AB, 11)
    w = d.textlength(label, font=f) + 12
    d.rectangle([x, y, x + w, y + 16], fill=BRICK if label == "CLAIM" else TEAL)
    d.text((x + 6, y + 2), label, font=f, fill=(255, 250, 235))
    return w

def lead(d, x, y, w, h, loc, chip_label, src, head, deck, kind):
    """Card 1 — the big lead. Args: loc, chip, src, head, deck, kind last."""
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    d.rectangle([x, y, x + w, y + 17], fill=TEAL)
    d.text((x + 6, y + 3), loc, font=F(AB, 12), fill=(255, 250, 235))
    scene(d, kind, x + 5, y + 21, 210, h - 26)
    tx = x + 222
    tw = x + w - tx - 6
    cy = y + 21
    cw = chip(d, tx, cy, chip_label)
    d.text((tx + cw + 6, cy + 2), "NORTH AMERICA · MILITARY", font=F(AB, 9), fill=GREY)
    cy += 20
    cy = text_block(d, tx, cy, head, fb(27), TEAL_D, tw, leading=30, max_lines=2)
    text_block(d, tx, cy + 1, deck, fr(14), INK, tw, leading=16, max_lines=2)
    d.text((tx, y + h - 14), src, font=F(AB, 10), fill=BRICK_D)

def mini(d, x, y, w, h, loc, chip_label, src, head, deck, kind):
    """Trio cards 2-3. Args: loc, chip, src, head, deck, kind last."""
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    d.rectangle([x, y, x + w, y + 17], fill=TEAL)
    d.text((x + 6, y + 3), loc, font=F(AB, 12), fill=(255, 250, 235))
    scene(d, kind, x + 5, y + 21, 84, h - 26)
    tx = x + 96
    tw = x + w - tx - 6
    cy = y + 21
    cw = chip(d, tx, cy, chip_label)
    cy += 20
    cy = text_block(d, tx, cy, head, fb(21), TEAL_D, tw, leading=23, max_lines=2)
    text_block(d, tx, cy + 1, deck, fr(13), INK, tw, leading=15, max_lines=2)
    d.text((tx, y + h - 14), src, font=F(AB, 10), fill=BRICK_D)

def card_h(d, c, x, y, w, h):
    num, loc, cat, src, head, deck, kind = c
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    d.rectangle([x, y, x + w, y + 17], fill=TEAL)
    d.text((x + 6, y + 3), "%d · %s" % (num, loc), font=F(AB, 12), fill=(255, 250, 235))
    scene(d, kind, x + 5, y + 21, 52, h - 26)
    tx = x + 64
    tw = x + w - tx - 6
    cy = y + 21
    cw = chip(d, tx, cy, CHIPS[num])
    cy += 20
    cy = text_block(d, tx, cy, head, fb(17), TEAL_D, tw, leading=19, max_lines=2)
    text_block(d, tx, cy + 1, deck, fr(12), INK, tw, leading=14, max_lines=2)
    d.text((tx, y + h - 14), src, font=F(AB, 10), fill=BRICK_D)

def header(d):
    d.rectangle([0, 0, W, 24], fill=TEAL_D)
    d.text((10, 5), "THE DAY'S POST", font=F(PFB, 13), fill=(255, 250, 235))
    k = "41 STORIES · 8 REGIONS · EVERY ONE FROM 23 NOVEMBER 2026"
    d.text((W - 10 - d.textlength(k, font=F(AB, 13)), 5), k, font=F(AB, 13), fill=(255, 236, 190))
    t = "THE DAY'S POST"
    d.text(((W - d.textlength(t, font=F(PB, 40))) / 2, 28), t, font=F(PB, 40), fill=TEAL_D)
    dt = "Monday 23 November 2026"
    d.text(((W - d.textlength(dt, font=F(PB, 56))) / 2, 68), dt, font=F(PB, 56), fill=TEAL_D)
    sub = "US Army to detonate unstable explosives in Iowa · IRGC claims Patriot radars hit · COP31 ends without a deal"
    d.text(((W - d.textlength(sub, font=F(PFB, 15))) / 2, 132), sub, font=F(PFB, 15), fill=BRICK_D)
    d.line([10, 154, W - 10, 154], fill=BRICK, width=2)
    x = 10
    for name, n, col in REGIONS:
        label = "%s %d" % (name, n)
        wch = d.textlength(label, font=F(AB, 12)) + 16
        d.rectangle([x, 160, x + wch, 178], fill=col)
        d.text((x + 8, 163), label, font=F(AB, 12), fill=(255, 250, 235))
        x += wch + 6
    d.rectangle([10, 182, W - 10, 202], fill=(233, 222, 192), outline=LINE)
    x = 16
    d.text((x, 186), "UTC", font=F(AB, 12), fill=BRICK_D)
    x += 34
    for tm, ev in TL:
        s = "%s %s" % (tm, ev)
        d.text((x, 186), s, font=F(AR, 12), fill=TEAL_D)
        x += d.textlength(s, font=F(AR, 12)) + 14

def numbers_box(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL_D)
    d.text((x + 10, y + 8), "THE DAY IN NUMBERS", font=F(AB, 15), fill=(255, 236, 190))
    cy = y + 32
    for num, lab in NUMS:
        d.text((x + 10, cy), num, font=F(PB, 25), fill=(255, 250, 235))
        d.text((x + 118, cy + 8), lab, font=F(AR, 12), fill=(210, 224, 214))
        cy += 34

def numbers_strip(d, x, y, w):
    d.rectangle([x, y, x + w, y + 50], fill=TEAL_D)
    d.text((x + 8, y + 4), "THE DAY IN NUMBERS", font=F(AB, 12), fill=(255, 236, 190))
    xx = x + 8
    for num, lab in NUMS:
        d.text((xx, y + 20), num, font=F(PB, 22), fill=(255, 250, 235))
        xx += 166

def dotted_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PAPER2, outline=LINE)
    d.text((x + 8, y + 5), "WHERE IT HAPPENED — pins = card numbers", font=F(AB, 11), fill=TEAL_D)
    cw = (w - 16) / 46.0
    chh = (h - 46) / 14.0
    for r, row in enumerate(MAPROWS):
        for cc, ch in enumerate(row):
            if ch == "X":
                px, py = x + 8 + cc * cw, y + 24 + r * chh
                d.ellipse([px, py, px + 3, py + 3], fill=TEAL_L)
    for num, cc, r in PINS:
        px, py = x + 8 + cc * cw, y + 24 + r * chh
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=BRICK)
        s = str(num)
        d.text((px - d.textlength(s, font=F(AB, 9)) / 2, py - 5), s, font=F(AB, 9), fill=(255, 255, 255))
    d.text((x + 8, y + h - 14), "Teal dots mark land; brick pins mark story numbers.", font=F(AR, 10), fill=GREY)

def datecheck(d, x, y, w, h, fs=12):
    d.rectangle([x, y, x + w, y + h], fill=(248, 232, 224), outline=BRICK, width=2)
    d.text((x + 8, y + 6), "DATE CHECK — NOT 23 NOV, LEFT OUT", font=F(AB, 13), fill=BRICK_D)
    cy = y + 27
    for line in DATECHECK:
        d.text((x + 8, cy), line, font=F(AR, fs), fill=(70, 40, 32))
        cy += fs + 4

def bottom(d):
    y = 828
    d.line([10, y - 5, W - 10, y - 5], fill=BRICK, width=2)
    d.text((10, y), "ALSO ON 23 NOVEMBER — STORIES 13-41", font=F(AB, 13), fill=TEAL_D)
    briefs = BRIEFS_L + BRIEFS_R
    colw = (W - 28) // 3
    cys = [y + 19] * 3
    for i, s in enumerate(briefs):
        c = i % 3
        d.text((10 + c * colw, cys[c]), "%d. %s" % (13 + i, s), font=fsr(11), fill=INK)
        cys[c] += 13
    fy = 982
    d.line([10, fy - 4, W - 10, fy - 4], fill=LINE, width=1)
    foot = ("HOW SURE: REPORTED = independently reported · CLAIM = one side's account, labelled as such · ONGOING = still developing · "
            "OFFICIAL / ON RECORD / CONFIRMED = stated or settled on the record. Every story happened, or was first reported, on Monday "
            "23 November 2026. Contested claims are attributed. Original drawings.")
    text_block(d, 10, fy, foot, F(AR, 11), GREY, W - 20, leading=12, max_lines=3)

def build(variant):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    header(d)
    top = 208
    if variant == "A":
        lead(d, 10, top, 684, 146, "1 · IOWA, USA", "OFFICIAL", "BBC · 23 Nov",
             "US Army to Detonate Unstable Explosives in Iowa",
             "The Army plans to blow up tons of unstable explosives in Iowa, defying a court order, the BBC reports.",
             "blast")
        mini(d, 10, top + 154, 338, 132, "2 · BAHRAIN", "CLAIM", "AP/AFP wire · 23 Nov",
             "IRGC Claims Patriot Radars Hit in Bahrain",
             "IRGC claims 2 Patriot radars destroyed at a Bahrain base; unconfirmed.",
             "radar")
        mini(d, 356, top + 154, 338, 132, "3 · ANTALYA, TURKIYE", "OFFICIAL", "BBC / AP · 23 Nov",
             "COP31 Ends Without a Deal in Antalya",
             "No deal in Antalya; Turkiye's draft omits 'fossil fuels'.",
             "climate")
        gy = top + 294
        for i, c in enumerate(grid):
            r, cc = divmod(i, 3)
            card_h(d, c, 10 + cc * 230, gy + r * 108, 222, 102)
        numbers_box(d, 706, top, 308, 238)
        dotted_map(d, 706, top + 246, 308, 150)
        datecheck(d, 706, top + 404, 308, 212)
    else:
        card_h(d, (1, "IOWA, USA", "NORTH AMERICA · MILITARY", "BBC · 23 Nov",
                   "US Army to Detonate Unstable Explosives in Iowa",
                   "The Army plans to blow up tons of unstable explosives in Iowa, defying a court order, the BBC reports.",
                   "blast"), 10, top, 500, 132)
        card_h(d, (2, "BAHRAIN", "MIDDLE EAST · WAR", "AP/AFP wire · 23 Nov",
                   "IRGC Claims Patriot Radars Hit in Bahrain",
                   "IRGC claims 2 Patriot radars destroyed at a Bahrain base; unconfirmed.",
                   "radar"), 518, top, 496, 132)
        card_h(d, (3, "ANTALYA, TURKIYE", "EUROPE · CLIMATE", "BBC / AP · 23 Nov",
                   "COP31 Ends Without a Deal in Antalya",
                   "No deal in Antalya; Turkiye's draft omits 'fossil fuels'.",
                   "climate"), 10, top + 140, 1004, 74)
        numbers_strip(d, 10, top + 222, 1004)
        gy = top + 280
        for i, c in enumerate(grid):
            r, cc = divmod(i, 3)
            card_h(d, c, 10 + cc * 230, gy + r * 108, 222, 102)
        dotted_map(d, 706, gy, 308, 150)
        datecheck(d, 706, gy + 158, 308, 158, fs=11)
    bottom(d)
    return img

if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ni23g4-final3/entry.png"
    img = build(variant)
    # flat palette keeps the file small (ties go to the smaller file)
    img.quantize(colors=256, method=Image.FASTOCTREE).save(out, optimize=True)
    print(out, img.size)
