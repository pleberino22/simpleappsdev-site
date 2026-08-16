#!/usr/bin/env python3
"""Open Graph images for simpleappsdev — one per app, plus the home card.

Writes assets/og/home.png and assets/og/<id>.png at 1200×630, drawing each
app's tile in the same visual language as .tile in css/site.css: the same
colour-mix gradient stops, the same 15/64 corner radius, the same 17/64
wordmark ratio, the same inset highlight.

Everything that could drift — name, tagline, accents, the portfolio line —
is read from apps.json, so this file holds no content of its own. Run it
from the repo root after adding an app or editing a tagline:

    python3 og.py

Output is deterministic: same apps.json in, byte-identical PNGs out, so a
re-run only shows up in git when the data actually changed.

Needs Pillow and macOS system fonts (SF Pro Rounded / SF Pro Text).
"""
import json
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
PAPER = (250, 250, 249)
INK = (28, 26, 23)
SMOKE = (138, 133, 125)

ROUNDED = '/System/Library/Fonts/SFNSRounded.ttf'
TEXT = '/System/Library/Fonts/SFNS.ttf'


def font(path, size, weight='Regular'):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def mix(c, other, pct):
    """color-mix(in srgb, c pct%, other) — the same formula as .tile in site.css"""
    return tuple(round(a * pct + b * (1 - pct)) for a, b in zip(c, other))


def hex_rgb(s):
    s = s.lstrip('#')
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def tile(size, accent, word):
    """the .tile visual language: accent gradient, rounded, white wordmark"""
    top = mix(accent, (255, 255, 255), 0.72)
    bottom = mix(accent, (0, 0, 0), 0.92)

    grad = Image.new('RGB', (1, size))
    for y in range(size):
        t = y / (size - 1)
        grad.putpixel((0, y), tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))
    grad = grad.resize((size, size))

    radius = round(size * 15 / 64)
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius, fill=255)

    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    out.paste(grad, (0, 0), mask)

    # inset 0 1px 0 rgb(255 255 255 / .35), scaled — a highlight, not a ring
    line = Image.new('L', (size, size), 0)
    ImageDraw.Draw(line).rounded_rectangle(
        [1, 1, size - 2, size - 2], radius - 1, outline=90, width=max(2, size // 70))
    ramp = Image.new('L', (1, size))
    for y in range(size):
        ramp.putpixel((0, y), max(0, round(255 * (1 - y / (size * 0.35)))))
    line = Image.composite(line, Image.new('L', (size, size), 0), ramp.resize((size, size)))
    out.paste(Image.new('RGB', (size, size), (255, 255, 255)), (0, 0),
              Image.composite(line, Image.new('L', (size, size), 0), mask))

    f = font(ROUNDED, round(size * 17 / 64), 'Bold')
    d = ImageDraw.Draw(out)
    box = d.textbbox((0, 0), word, font=f)
    d.text(((size - (box[2] - box[0])) / 2 - box[0], (size - (box[3] - box[1])) / 2 - box[1]),
           word, font=f, fill=(255, 255, 255))
    return out


def wrap(draw, text, f, width):
    lines, line = [], ''
    for w in text.split():
        trial = (line + ' ' + w).strip()
        if draw.textlength(trial, font=f) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def app_card(app, out):
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    accent = hex_rgb(app['accentLight'])

    size = 220
    icon = tile(size, accent, app['name'])
    img.paste(icon, (90, (H - size) // 2 - 24), icon)

    x = 90 + size + 60
    name_f = font(ROUNDED, 86, 'Bold')
    tag_f = font(TEXT, 34, 'Regular')
    tag_lines = wrap(d, app['tagline'], tag_f, W - x - 90)

    block = 96 + 18 + 44 * len(tag_lines)
    y = (H - 24 - block) // 2
    d.text((x, y), app['name'], font=name_f, fill=INK)
    y += 96 + 18
    for line in tag_lines:
        d.text((x, y), line, font=tag_f, fill=SMOKE)
        y += 44

    handle_f = font(ROUNDED, 26, 'Semibold')
    d.text((90, H - 90), 'simpleappsdev', font=handle_f, fill=SMOKE)
    dot = 90 + d.textlength('simpleappsdev', font=handle_f) + 12
    d.ellipse([dot, H - 82, dot + 10, H - 72], fill=accent)

    img.save(out)
    print('wrote', out)


def home_card(data, out):
    """the portfolio's own card: no app accent, no tint — it belongs to no app"""
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)

    handle_f = font(ROUNDED, 34, 'Semibold')
    d.text((90, 84), data['handle'], font=handle_f, fill=INK)
    dot = 90 + d.textlength(data['handle'], font=handle_f) + 14
    d.ellipse([dot, 98, dot + 13, 111], fill=INK)

    line_f = font(ROUNDED, 92, 'Bold')
    lines = wrap(d, data['line'], line_f, 720)
    y = H - 96 - 104 * len(lines)
    for line in lines:
        d.text((90, y), line, font=line_f, fill=INK)
        y += 104

    img.save(out)
    print('wrote', out)


if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    data = json.load(open(root + '/apps.json'))
    home_card(data, root + '/assets/og/home.png')
    for app in data['apps']:
        app_card(app, root + '/assets/og/' + app['id'] + '.png')
