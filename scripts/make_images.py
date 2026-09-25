"""Builds the site's app images from raw simulator screenshots.

Capture the screenshots first with the main repo's `scripts/capture_screenshots.sh <dir>`, then:
    python3 scripts/make_images.py <dir>

Writes images/flat-*.webp (plain screens for the hero and the screenshot rail) and
images/0N-*.webp (the "A closer look" panels: headline + phone on a tinted background).
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SRC = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent.parent / "images"
FONT = "/System/Library/Fonts/SFNS.ttf"

# flat image name -> screenshot name
FLAT = {"today": "today", "workout": "workout", "food": "food", "foodsearch": "foodsearch",
        "joint": "training", "settings": "settings", "readiness": "readiness", "fuel": "fuel", "guide": "guide",
        "training": "trainingwhy"}

# panel file, headline, subline, screenshot, accent colour (the background's brightest band)
PANELS = [
    ("01-ready-in-one-glance", "Ready in one glance", "Readiness, training and food — adjusted together every morning.", "today", (30, 100, 90)),
    ("02-training-that-adapts", "Training that adapts", "Weights go up when you’re ready, and ease off when you’re not.", "workout", (36, 70, 116)),
    ("03-food-that-moves-with-you", "Food that moves with you", "Calories, protein, carbs and fat that shift with your training.", "fuel", (112, 83, 38)),
    ("04-log-food-your-way", "Log food your way", "Search, scan a barcode, or just say what you ate.", "foodsearch", (31, 94, 109)),
    ("05-train-around-an-injury", "Train around an injury", "Protect a joint and Udapt swaps out exercises that load it.", "training", (108, 63, 48)),
    ("06-home-or-gym", "Home or gym, your call", "Full programs either way — switch any time.", "onboarding-schedule", (55, 58, 109)),
    ("07-every-change-explained", "Every change explained", "Tap Why? for charts, plain English and the research behind it.", "readiness", (84, 52, 120)),
]


def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_name(weight)
    return f


def background(w, h, accent):
    """Vertical bands matching the original panels: dim top, bright middle glow, near-black foot."""
    stops = [(0, 0.67), (0.21, 0.45), (0.5, 1.0), (0.78, 0.44)]
    foot = (8, 14, 17)
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        if t >= stops[-1][0]:
            k = (t - stops[-1][0]) / (1 - stops[-1][0])
            a = tuple(c * stops[-1][1] for c in accent)
            col = tuple(int(a[i] + (foot[i] - a[i]) * k) for i in range(3))
        else:
            for (t0, m0), (t1, m1) in zip(stops, stops[1:]):
                if t0 <= t <= t1:
                    k = (t - t0) / (t1 - t0)
                    m = m0 + (m1 - m0) * k
                    col = tuple(int(c * m) for c in accent)
                    break
        for x in range(w):
            px[x, y] = col
    return img


def phone(screen, width):
    """A simple device frame: dark bezel, rounded screen, Dynamic Island."""
    pad = round(width * 0.024)
    sw = width - 2 * pad
    shot = screen.resize((sw, round(screen.height * sw / screen.width)), Image.LANCZOS)
    h = shot.height + 2 * pad
    frame = Image.new("RGBA", (width, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((0, 0, width - 1, h - 1), radius=round(width * 0.145), fill=(12, 18, 24, 255), outline=(43, 55, 66, 255), width=2)
    mask = Image.new("L", shot.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw - 1, shot.height - 1), radius=round(sw * 0.125), fill=255)
    frame.paste(shot, (pad, pad), mask)
    iw, ih = round(sw * 0.26), round(sw * 0.075)
    ix, iy = (width - iw) // 2, pad + round(sw * 0.026)
    d.rounded_rectangle((ix, iy, ix + iw, iy + ih), radius=ih // 2, fill=(0, 0, 0, 255))
    return frame


def wrap(draw, text, f, max_width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=f) <= max_width:
            line = trial
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def panel(name, title, sub, shot, accent):
    W, H = 660, 1405
    img = background(W, H, accent)
    d = ImageDraw.Draw(img)
    y = 64
    for line in wrap(d, title, font(46, "Bold"), W - 60):
        d.text((W / 2, y), line, font=font(46, "Bold"), fill="white", anchor="mt")
        y += 54
    y += 6
    for line in wrap(d, sub, font(22, "Regular"), W - 90):
        d.text((W / 2, y), line, font=font(22, "Regular"), fill=(214, 226, 232), anchor="mt")
        y += 28
    frame = phone(Image.open(SRC / f"{shot}.png").convert("RGB"), 500)
    top = max(y + 34, 250)
    img.paste(frame, ((W - frame.width) // 2, top), frame)
    img.save(OUT / f"{name}.webp", quality=88, method=6)


def flat(name, shot):
    im = Image.open(SRC / f"{shot}.png").convert("RGB")
    im = im.resize((600, round(im.height * 600 / im.width)), Image.LANCZOS).crop((0, 0, 600, 1260))
    im.save(OUT / f"flat-{name}.webp", quality=88, method=6)


for name, shot in FLAT.items():
    flat(name, shot)
for p in PANELS:
    panel(*p)
print("wrote", len(FLAT), "flat images and", len(PANELS), "panels to", OUT)
