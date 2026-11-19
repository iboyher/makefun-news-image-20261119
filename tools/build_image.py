#!/usr/bin/env python3
"""Build the front page for the make.fun news-image-20261119 bounty.

Renders THE WORLD, a one-page newspaper front page summing up Thursday
19 November 2026, to entry.png (1024x1024, PNG, deterministic).

Editorial line-up by ClaudePeak (nex-n2.6-swift) from verified news of the
day; hero art is an AI illustration of the Shenzhen skyline at dawn.
Run: python3 tools/build_image.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HERO = os.path.join(ROOT, "assets", "hero-shenzhen.png")
OUT = os.path.join(ROOT, "entry.png")

W, H = 1024, 1024
MARGIN = 24
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 244, 236)
INK = (20, 20, 20)
ACCENT = (200, 16, 46)
BLUE = (27, 95, 170)
GREEN = (30, 122, 76)
GRAY = (110, 105, 95)
LIGHT_RULE = (190, 184, 172)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, leading, fill=INK, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines and len(lines) > max_lines:
        print("TRUNCATED:", text[:70], "->", len(lines), "lines, kept", max_lines)
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hairline(draw, y, x0=MARGIN, x1=W - MARGIN, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- content
LEAD = {
    "kicker": "THE SUMMIT IN SHENZHEN",
    "headline": "Trump, Xi, Putin Hold First Trilateral Summit",
    "deck": "90 minutes, joint peace pledge; no breakthrough",
    "byline": "SHENZHEN, CHINA",
}

SECOND_LEADS = [
    ("WORLD COURT", ACCENT, "World Court Rules Against Myanmar on Rohingya",
     "Landmark ruling in Gambia's Rohingya genocide case"),
    ("UKRAINE", ACCENT, "Ukraine Hits Kerch Bridge for Third Time in Week",
     "Third strike in a week; Putin vows painful reply"),
    ("IRAN", ACCENT, "Iran Widens War With Attacks on Gulf States",
     "Drones hit Gulf; Trump warns over chemical arms"),
    ("BANGLADESH", BLUE, "Shutdown Grips Bangladesh as Violence Flares",
     "Yunus ancestral home torched; Hasina return blocked"),
    ("ASIA", BLUE, "Cyclone Akvan Weakens Ahead of Landfall",
     "Landfall Friday; 100 km/h winds, evacuations"),
]

# (region, color, headline, deck) — two briefs per column, five columns
REGION_COLS = [
    ("AMERICAS", BLUE, [
        ("US Asks Supreme Court to End TPS Shield",
         "Venezuelan migrants' protections at stake"),
        ("GOP's Begich Keeps Alaska House Seat",
         "Republican wins after ranked-choice count"),
    ]),
    ("EUROPE", BLUE, [
        ("COP31 in Final Hours Over Fossil Fuels",
         "Phaseout wording, finance talks stall deal"),
        ("Russian Military Jet Crashes, 19 Dead",
         "Aircraft went down with no survivors"),
    ]),
    ("ASIA-PACIFIC", ACCENT, [
        ("N. Korea Expanded Enrichment, IAEA Says",
         "Watchdog cites growth at Yongbyon site"),
        ("Lee Renews Call for North Korea Dialogue",
         "Seoul hopes engagement can secure lasting peace"),
    ]),
    ("MIDEAST", GREEN, [
        ("Israeli Tanks Cross Gaza Truce Line",
         "Hamas: a violation; residents flee artillery"),
        ("Strike on Nasser Hospital Kills Six",
         "Surgeon among the dead in Gaza attack"),
    ]),
    ("SPACE & TECH", ACCENT, [
        ("Anthropic's Debut Raises Record Sum",
         "Record haul for the AI company"),
        ("NASA Sets Coverage for CRS-25 Launch",
         "Northrop Grumman cargo mission to station"),
    ]),
]

NUMBERS = [
    ("90", "MINUTES OF TRILATERAL TALKS"),
    ("620", "CHINA'S NUCLEAR WARHEADS"),
    ("3", "KERCH BRIDGE STRIKES IN A WEEK"),
    ("19", "KILLED IN RUSSIAN PLANE CRASH"),
    ("3,400", "TONNES OF LPG ON SUNK TANKER"),
]

TICKER = ("ALSO TODAY  —  Trump presses Xi on US farm buys, Hormuz oil flows  "
          "•  LPG tanker Gas Husky sinks off Bulgaria after being struck")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 10

    # ---------------------------------------------------------- masthead
    hairline(d, y)
    y += 8
    f_title = font(SERIF_B, 60)
    d.text((W // 2, y), "THE WORLD", font=f_title, fill=INK, anchor="ma")
    y += 70
    f_date = font(SERIF, 16)
    d.text((W // 2, y), "Thursday, 19 November 2026  —  The day in 18 stories",
           font=f_date, fill=INK, anchor="ma")
    y += 26
    hairline(d, y, width=3)
    y += 10

    # ---------------------------------------------------------- lead
    hero = Image.open(HERO).convert("RGB")
    hw, hh = hero.size
    target_ratio = CONTENT_W / 220.0
    src_ratio = hw / hh
    if src_ratio > target_ratio:  # too wide: crop sides
        new_w = int(hh * target_ratio)
        x0 = (hw - new_w) // 2
        hero = hero.crop((x0, 0, x0 + new_w, hh))
    else:  # too tall: crop top/bottom, band centred on the skyline + water
        new_h = int(hw / target_ratio)
        y0 = max(0, int(hh * 0.60) - new_h // 2)
        y0 = min(y0, hh - new_h)
        hero = hero.crop((0, y0, hw, y0 + new_h))
    hero = hero.resize((CONTENT_W, 220), Image.LANCZOS)
    img.paste(hero, (MARGIN, y))
    y += 220 + 8
    f_kick = font(SANS_B, 13)
    d.text((MARGIN, y), LEAD["kicker"], font=f_kick, fill=ACCENT)
    y += 20
    f_lead_h = font(SERIF_B, 44)
    y = draw_wrapped(d, MARGIN, y, LEAD["headline"], f_lead_h, CONTENT_W,
                     leading=50, max_lines=2)
    y += 2
    f_lead_d = font(SERIF, 19)
    y = draw_wrapped(d, MARGIN, y, LEAD["deck"], f_lead_d, CONTENT_W,
                     leading=22, max_lines=1)
    y += 2
    f_by = font(SERIF_I, 13)
    d.text((MARGIN, y), LEAD["byline"], font=f_by, fill=GRAY)
    y += 20
    hairline(d, y)
    y += 10

    # ---------------------------------------------------------- second leads
    col_w = (CONTENT_W - 4 * 12) // 5
    f_tag = font(SANS_B, 11)
    f_sl_h = font(SERIF_B, 21)
    f_sl_d = font(SERIF, 15)
    max_y = y
    for i, (tag, color, head, deck) in enumerate(SECOND_LEADS):
        x = MARGIN + i * (col_w + 12)
        cy = y
        d.text((x, cy), tag, font=f_tag, fill=color)
        cy += 18
        cy = draw_wrapped(d, x, cy, head, f_sl_h, col_w, leading=25,
                          max_lines=3)
        cy += 2
        cy = draw_wrapped(d, x, cy, deck, f_sl_d, col_w, leading=19,
                          max_lines=2)
        max_y = max(max_y, cy)
        if i < 4:
            d.line([(x + col_w + 6, y), (x + col_w + 6, max_y)],
                   fill=LIGHT_RULE, width=1)
    y = max_y + 12
    hairline(d, y)
    y += 10

    # ---------------------------------------------------------- region grid
    f_col = font(SANS_B, 12)
    f_rh = font(SERIF_B, 16)
    f_rd = font(SERIF, 14)
    max_y = y
    for i, (region, color, briefs) in enumerate(REGION_COLS):
        x = MARGIN + i * (col_w + 12)
        cy = y
        d.rectangle([x, cy, x + col_w, cy + 22], fill=color)
        tw = d.textlength(region, font=f_col)
        d.text((x + (col_w - tw) / 2, cy + 4), region, font=f_col,
               fill=(255, 255, 255))
        cy += 30
        for head, deck in briefs:
            cy = draw_wrapped(d, x, cy, head, f_rh, col_w, leading=20,
                              max_lines=2)
            cy += 1
            cy = draw_wrapped(d, x, cy, deck, f_rd, col_w, leading=17,
                              max_lines=2, fill=(60, 58, 52))
            cy += 16
        max_y = max(max_y, cy)
        if i < 4:
            d.line([(x + col_w + 6, y), (x + col_w + 6, max_y)],
                   fill=LIGHT_RULE, width=1)
    y = max_y + 2
    hairline(d, y)
    y += 8

    # ---------------------------------------------------------- by the numbers
    f_num = font(SERIF_B, 34)
    f_num_l = font(SANS_B, 11)
    num_w = CONTENT_W // 5
    max_y = y
    for i, (num, label) in enumerate(NUMBERS):
        x = MARGIN + i * num_w
        d.text((x + num_w // 2, y), num, font=f_num, fill=ACCENT, anchor="ma")
        ly = y + 44
        for ln in wrap(d, label, f_num_l, num_w - 8):
            lw = d.textlength(ln, font=f_num_l)
            d.text((x + (num_w - lw) / 2, ly), ln, font=f_num_l, fill=INK)
            ly += 13
        max_y = max(max_y, ly)
    y = max_y + 6
    hairline(d, y)
    y += 8

    # ---------------------------------------------------------- ticker
    f_tick = font(SANS_B, 16)
    y = draw_wrapped(d, MARGIN, y, TICKER, f_tick, CONTENT_W, leading=19,
                     max_lines=2)
    y += 10
    hairline(d, y)
    y += 8

    # ---------------------------------------------------------- footer
    f_foot = font(SERIF, 12)
    d.text((MARGIN, y),
           "All stories dated Thursday 19 November 2026  •  Sources: AP, AFP, Reuters, BBC, IAEA",
           font=f_foot, fill=GRAY)
    d.text((W - MARGIN, y), "Page 1", font=f_foot, fill=GRAY, anchor="ra")
    y += 20

    print("final y:", y, "of", H)
    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print("wrote", OUT, size, "bytes,", img.size)
    assert img.size == (1024, 1024)
    assert size <= 1024 * 1024, "over 1 MiB!"
    return OUT


if __name__ == "__main__":
    build()
