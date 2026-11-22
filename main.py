#!/usr/bin/env python3
"""Draw a melted-cheese burger (1024x1024 PNG) with Pillow only.

No network, no external files, no text in the picture. Deterministic:
two runs from different working directories produce byte-identical PNGs.

Usage: python3 main.py        (writes /output/entry.png)
"""
import hashlib
import math

from PIL import Image, ImageDraw, ImageFilter

S = 2                      # 2x supersampling
W = H = 1024 * S
OUT = "/output/entry.png"


def box(x0, y0, x1, y1):
    """1024-space box -> 2048-space box."""
    return (x0 * S, y0 * S, x1 * S, y1 * S)


def pts(points):
    return [(x * S, y * S) for x, y in points]


def soft_ellipse(base, xy, fill, blur):
    """Draw a blurred ellipse on its own overlay, then composite.

    Semi-transparent shading must never be drawn directly on an RGBA
    layer with ImageDraw (it would replace pixels); always go through
    a separate overlay + alpha_composite.
    """
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(box(*xy), fill=fill)
    layer = layer.filter(ImageFilter.GaussianBlur(blur * S))
    base.alpha_composite(layer)


def rotated_ellipse(draw, cx, cy, rx, ry, angle_deg, fill, outline=None):
    """Opaque rotated ellipse as a polygon (no rotation artifacts)."""
    a = math.radians(angle_deg)
    ca, sa = math.cos(a), math.sin(a)
    poly = []
    for i in range(28):
        t = 2 * math.pi * i / 28
        x = rx * math.cos(t)
        y = ry * math.sin(t)
        px = cx + x * ca - y * sa
        py = cy + x * sa + y * ca
        poly.append((px * S, py * S))
    draw.polygon(poly, fill=fill, outline=outline)


def main():
    # ---- background: warm dark-brown vertical gradient ----------------
    grad = Image.new("RGB", (1, 512))
    gd = ImageDraw.Draw(grad)
    top = (62, 34, 18)
    bot = (28, 15, 8)
    for y in range(512):
        t = y / 511.0
        gd.point((0, y), tuple(int(top[i] + (bot[i] - top[i]) * t)
                               for i in range(3)))
    img = grad.resize((W, H)).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # ---- top warm light ----------------------------------------------
    soft_ellipse(img, (180, -220, 844, 320), (255, 205, 130, 66), 130)
    soft_ellipse(img, (330, -140, 694, 180), (255, 225, 170, 60), 90)

    # ---- soft shadow under the burger --------------------------------
    soft_ellipse(img, (210, 748, 814, 812), (0, 0, 0, 95), 26)

    # ---- wooden board -------------------------------------------------
    draw.ellipse(box(58, 780, 966, 948), fill=(124, 74, 33))
    draw.ellipse(box(78, 794, 946, 934), fill=(139, 85, 39))
    draw.ellipse(box(58, 780, 966, 948), outline=(84, 46, 16), width=6 * S)
    # a couple of faint wood-grain arcs
    draw.arc(box(150, 818, 880, 918), start=200, end=340,
             fill=(104, 60, 24), width=4 * S)
    draw.arc(box(220, 838, 820, 928), start=210, end=330,
             fill=(104, 60, 24), width=3 * S)

    # ---- bottom bun ----------------------------------------------------
    draw.rounded_rectangle(box(205, 696, 819, 778), radius=30 * S,
                           fill=(233, 169, 59))
    draw.rounded_rectangle(box(205, 752, 819, 778), radius=30 * S,
                           fill=(214, 146, 44))

    # ---- beef patty ----------------------------------------------------
    draw.rounded_rectangle(box(185, 606, 839, 700), radius=34 * S,
                           fill=(62, 36, 16))
    draw.line(pts([(200, 614), (824, 614)]), fill=(92, 54, 24), width=3 * S)
    # short grill marks, kept inside the patty (single diagonals, no X)
    for x in (300, 400, 512, 624, 724):
        draw.line(pts([(x - 16, 634), (x + 16, 654)]),
                  fill=(36, 20, 8), width=5 * S)

    # ---- melted cheese: one sheet, wavy bottom edge, three soft bumps -
    bottom = []
    for x in range(175, 850, 12):
        y = 600 + 9 * math.sin((x - 175) / 674.0 * math.pi * 3)
        for cx in (330, 512, 694):
            y += 18 * math.exp(-((x - cx) ** 2) / (2 * 55.0 ** 2))
        bottom.append((x, y))
    cheese = [(175, 542), (849, 542)] + list(reversed(bottom))
    draw.polygon(pts(cheese), fill=(247, 148, 29))
    draw.line(pts(bottom), fill=(217, 122, 11), width=3 * S)
    # gentle darker shade along the cheese underside (overlay + blur)
    soft_ellipse(img, (300, 592, 724, 640), (190, 100, 10, 46), 18)

    # ---- tomato slice --------------------------------------------------
    draw.rounded_rectangle(box(212, 502, 812, 546), radius=18 * S,
                           fill=(212, 43, 30))
    draw.rounded_rectangle(box(232, 510, 792, 538), radius=12 * S,
                           fill=(228, 72, 46))

    # ---- lettuce: wavy band + overlapping leaves of varied sizes -----
    band_top = [(x, 470 + 6 * math.sin((x - 190) / 644.0 * math.pi * 4))
                for x in range(190, 835, 12)]
    band_bot = [(x, 506 + 8 * math.sin((x - 190) / 644.0 * math.pi * 4 + 1.2))
                for x in range(190, 835, 12)]
    draw.polygon(pts(band_top + list(reversed(band_bot))), fill=(87, 166, 57))
    leaves = [
        # (cx, cy, rx, ry, angle, color) -- flat leaves hugging the band
        (238, 504, 58, 13, -14, (76, 154, 63)),
        (352, 510, 66, 14, 10, (109, 184, 74)),
        (470, 505, 60, 13, -6, (62, 142, 51)),
        (596, 511, 68, 14, 12, (109, 184, 74)),
        (724, 505, 58, 13, -12, (76, 154, 63)),
        (806, 498, 44, 12, 18, (62, 142, 51)),
        (204, 496, 40, 12, -20, (62, 142, 51)),
    ]
    for cx, cy, rx, ry, ang, col in leaves:
        rotated_ellipse(draw, cx, cy, rx, ry, ang, col)

    # ---- top bun dome: pieslice crown + flat bottom lip ---------------
    # (pieslice 180-360 ends at the diameter y=430, so the lip must sit
    # directly underneath it -- never leave a dark gap between them)
    draw.pieslice(box(187, 330, 837, 530), start=180, end=360,
                  fill=(240, 178, 62))
    draw.rounded_rectangle(box(180, 424, 844, 472), radius=20 * S,
                           fill=(232, 168, 58))
    # soft highlight (big blurred ellipse, never a pieslice) + shade
    soft_ellipse(img, (310, 345, 555, 430), (255, 236, 182, 92), 40)
    soft_ellipse(img, (280, 390, 760, 435), (160, 100, 20, 60), 30)
    # thin warm rim light along the crown's top edge
    draw.arc(box(187, 330, 837, 530), start=230, end=310,
             fill=(250, 205, 110), width=4 * S)

    # ---- sesame seeds on the dome (~15, all inside the crown) --------
    seeds = [
        (330, 368, 20), (430, 364, -15), (540, 366, 10), (640, 370, -25),
        (700, 388, 15),
        (280, 400, -10), (380, 398, 25), (480, 396, -20), (580, 400, 15),
        (690, 402, -15), (758, 414, 20),
        (360, 416, 15), (520, 414, -25), (660, 416, 10),
    ]
    for cx, cy, ang in seeds:
        rotated_ellipse(draw, cx, cy, 11, 7, ang,
                        (251, 231, 184), outline=(201, 162, 75))

    # ---- board garnish: a few seeds + two small herb leaves ----------
    for cx, cy, ang in ((300, 882, 10), (720, 902, -15), (622, 916, 5)):
        rotated_ellipse(draw, cx, cy, 9, 6, ang,
                        (251, 231, 184), outline=(201, 162, 75))
    for cx, cy, ang in ((880, 862, 32), (148, 892, -28)):
        rotated_ellipse(draw, cx, cy, 26, 10, ang, (46, 125, 50))
        a = math.radians(ang)
        dx, dy = 20 * math.cos(a), 20 * math.sin(a)
        draw.line(pts([(cx - dx, cy - dy), (cx + dx, cy + dy)]),
                  fill=(27, 94, 32), width=2 * S)

    # ---- vignette: per-pixel distance mask (low-res, upscaled) -------
    mask = Image.new("L", (256, 256), 0)
    mp = mask.load()
    for yy in range(256):
        for xx in range(256):
            dx = (xx - 127.5) / 127.5
            dy = (yy - 127.5) / 127.5
            d = math.sqrt(dx * dx + dy * dy)
            a = max(0.0, (d - 0.62) / 0.55)
            mp[xx, yy] = int(min(1.0, a) ** 1.6 * 120)
    mask = mask.resize((W, H), Image.BICUBIC)
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    dark.putalpha(mask)
    img.alpha_composite(dark)

    # ---- downscale + save ---------------------------------------------
    out = img.convert("RGB").resize((1024, 1024), Image.LANCZOS)
    out.save(OUT, "PNG")
    with open(OUT, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(f"Wrote {OUT} sha256={digest}")


if __name__ == "__main__":
    main()
