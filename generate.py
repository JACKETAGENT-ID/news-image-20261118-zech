#!/usr/bin/env python3
"""Draw the zech entry image for news-image-20261118.

One cinematic dawn scene over a Manila skyline (APEC / Quad day) with a
clear date banner and six short, verified headlines from Wednesday
18 November 2026. Pure PIL, no network, no external images.
Output: entry.png, 1024x1024, under 1 MiB.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SKY_H = 560  # height of the skyline scene; the rest is the news panel

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_sky(img):
    d = ImageDraw.Draw(img)
    top = (16, 22, 58)       # deep indigo night
    mid = (74, 52, 110)      # violet
    low = (214, 110, 58)     # dawn orange at the horizon
    for y in range(SKY_H):
        t = y / SKY_H
        if t < 0.55:
            c = lerp(top, mid, t / 0.55)
        else:
            c = lerp(mid, low, (t - 0.55) / 0.45)
        d.line([(0, y), (W, y)], fill=c)
    # stars fading out toward the horizon
    rng = random.Random(1811)
    for _ in range(90):
        x = rng.randrange(W)
        y = rng.randrange(int(SKY_H * 0.45))
        r = rng.choice([1, 1, 2])
        a = max(40, 255 - int(y / (SKY_H * 0.45) * 220))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 240, a) if False else (235, 235, 255))
    # rising sun with glow
    cx, cy = 800, 430
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, alpha in ((190, 26), (150, 40), (110, 60), (75, 90)):
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 190, 90, alpha))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=(255, 214, 130))
    d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(255, 232, 170))
    # thin clouds catching the dawn light: soft overlapping ellipses
    for (cx0, cy0, wdt, col) in [
        (200, 128, 260, (255, 178, 132)),
        (560, 96, 240, (244, 158, 138)),
        (280, 216, 280, (255, 196, 148)),
        (780, 186, 300, (255, 182, 132)),
    ]:
        for k, (ox, oy, ow, oh) in enumerate(
                [(-wdt // 2, 0, wdt // 2, 10), (-wdt // 4, -6, wdt // 2, 12),
                 (0, 0, wdt // 2, 10), (wdt // 6, 4, wdt // 3, 8)]):
            d.ellipse([cx0 + ox, cy0 + oy, cx0 + ox + ow, cy0 + oy + oh], fill=col)
    return d


def draw_plane_and_satellite(d):
    # small jet crossing the dawn sky, with a contrail
    d.line([(150, 150), (330, 128)], fill=(255, 255, 255), width=3)
    d.polygon([(330, 128), (352, 122), (352, 134), (330, 134)], fill=(255, 255, 255))
    d.polygon([(338, 126), (322, 112), (330, 126)], fill=(240, 240, 240))
    d.polygon([(338, 130), (322, 144), (330, 130)], fill=(240, 240, 240))
    # small satellite high in the sky
    d.rectangle([880, 96, 906, 110], fill=(200, 210, 230))
    d.rectangle([858, 100, 880, 106], fill=(90, 130, 200))
    d.rectangle([906, 100, 928, 106], fill=(90, 130, 200))
    d.line([(893, 110), (893, 122)], fill=(220, 220, 220), width=2)
    d.ellipse([890, 122, 896, 128], fill=(255, 220, 120))
    # birds
    for (bx, by, s) in [(500, 200, 12), (540, 224, 9), (470, 240, 8)]:
        d.arc([bx - s, by - s // 2, bx, by + s // 2], 200, 340, fill=(30, 30, 50), width=2)
        d.arc([bx, by - s // 2, bx + s, by + s // 2], 200, 340, fill=(30, 30, 50), width=2)


def draw_skyline(d):
    rng = random.Random(20261118)
    base = SKY_H
    # far skyline (lighter, hazy)
    x = -10
    while x < W:
        bw = rng.randrange(50, 110)
        bh = rng.randrange(90, 210)
        d.rectangle([x, base - bh, x + bw, base], fill=(58, 48, 96))
        x += bw + rng.randrange(4, 18)
    # near skyline (dark, with lit windows)
    x = -10
    while x < W:
        bw = rng.randrange(60, 130)
        bh = rng.randrange(150, 320)
        d.rectangle([x, base - bh, x + bw, base], fill=(18, 20, 44))
        # rooftop antenna / spire on some towers
        if rng.random() < 0.35:
            ax = x + bw // 2
            d.line([(ax, base - bh), (ax, base - bh - 34)], fill=(18, 20, 44), width=4)
            d.ellipse([ax - 3, base - bh - 40, ax + 3, base - bh - 34], fill=(255, 80, 80))
        # lit windows
        for wy in range(base - bh + 16, base - 14, 26):
            for wx in range(x + 10, x + bw - 10, 22):
                if rng.random() < 0.38:
                    d.rectangle([wx, wy, wx + 9, wy + 12],
                                fill=rng.choice([(255, 205, 110), (255, 225, 160), (150, 200, 255)]))
        x += bw + rng.randrange(2, 10)
    # two flag poles on the tallest-looking towers, summit flags
    for (fx, fy, colors) in [
        (205, 300, [(200, 40, 40), (255, 255, 255), (40, 60, 180)]),
        (700, 330, [(40, 140, 60), (255, 255, 255), (220, 60, 60)]),
    ]:
        d.line([(fx, fy), (fx, fy - 62)], fill=(220, 220, 220), width=3)
        for i, col in enumerate(colors):
            d.rectangle([fx + 2, fy - 62 + i * 11, fx + 42, fy - 62 + (i + 1) * 11], fill=col)
    # water / bay shimmer at the very bottom of the scene
    for i in range(14):
        y = base - 8 + i * 1
        d.line([(0, y), (W, y)], fill=lerp((214, 110, 58), (30, 30, 70), i / 14))


def draw_panel(d):
    panel_top = SKY_H
    d.rectangle([0, panel_top, W, H], fill=(10, 14, 34))
    d.line([(0, panel_top), (W, panel_top)], fill=(255, 176, 66), width=4)
    # kicker + date
    d.text((48, panel_top + 26), "THE WORLD IN ONE DAY",
           font=font(24, bold=True), fill=(255, 176, 66))
    d.text((48, panel_top + 58), "WEDNESDAY 18 NOVEMBER 2026",
           font=font(46, bold=True), fill=(255, 255, 255))
    d.text((48, panel_top + 122), "Summed up in one picture  \u2014  from Shenzhen to Gaza, orbit to the IPL",
           font=font(22), fill=(170, 180, 205))
    d.line([(48, panel_top + 162), (W - 48, panel_top + 162)], fill=(60, 70, 110), width=2)

    headlines = [
        ("APEC opens in Shenzhen; Trump in Manila for Quad talks", (255, 176, 66)),
        ("Nvidia revenue $115.84bn \u2014 doubles in a year", (120, 200, 255)),
        ("Gaza ceasefire at risk; WFP: one hot meal every two days", (255, 120, 120)),
        ("Drone strikes continue over Qeshm and Bahrain", (255, 120, 120)),
        ("Dhoni retires from IPL, to mentor Chennai Super Kings", (140, 230, 160)),
        ("Voyager 1 nears one light-day from Earth", (200, 170, 255)),
    ]
    y = panel_top + 182
    for text, dot in headlines:
        d.ellipse([48, y + 8, 64, y + 24], fill=dot)
        d.text((80, y), text, font=font(25, bold=True), fill=(240, 242, 248))
        y += 42
    # also-ran line
    d.text((48, y + 4), "Also: Cyclone Akvan strengthens \u00b7 Latvia approves new government \u00b7 Baidu warns of AI bubble",
           font=font(20), fill=(150, 160, 190))


def main():
    img = Image.new("RGB", (W, H), (10, 14, 34))
    draw_sky(img)
    d = ImageDraw.Draw(img)
    draw_plane_and_satellite(d)
    draw_skyline(d)
    draw_panel(ImageDraw.Draw(img))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
