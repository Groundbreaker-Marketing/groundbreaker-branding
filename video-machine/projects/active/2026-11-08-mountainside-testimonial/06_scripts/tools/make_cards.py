"""Draw the logo, end cards and section title cards (Pillow). Output: 04_project-files/cards/.

Brand: forest green #1c352b, accent #cdec60, Montserrat, reverse logo on green.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial"
OUT = P + "/04_project-files/cards"
os.makedirs(OUT, exist_ok=True)
FONTS = "/Users/josh/apps/video-machine/kit/skills/caption-clips/fonts/free_font/"
GREEN, LIME, WHITE = (0x1c, 0x35, 0x2b), (0xcd, 0xec, 0x60), (255, 255, 255)
URL = "groundbreakermarketing.com/calendar"
CTA = "Book a Strategy Call"


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


def logo_reverse():
    """Reverse logo from the source PNG: dark green -> white, lime stays lime, alpha kept."""
    path = OUT + "/gbm-logo-reverse.png"
    if os.path.exists(path):
        return Image.open(path)
    im = Image.open("/Users/josh/apps/clients/groundbreaker-branding/logos/gbm-logo-source.png").convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            px[x, y] = (255, 255, 255, a) if r < 120 else (LIME[0], LIME[1], LIME[2], a)
    im = im.resize((1600, int(1600 * im.height / im.width)), Image.LANCZOS)
    im.save(path)
    return im


def centered(d, text, f, y, fill, w):
    bb = d.textbbox((0, 0), text, font=f)
    d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], y), text, font=f, fill=fill)
    return bb[3] - bb[1]


def end_card(w, h, name):
    im = Image.new("RGB", (w, h), GREEN)
    d = ImageDraw.Draw(im)
    logo = logo_reverse()
    lw = int(w * (0.74 if h > w else 0.42))
    lg = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS)
    vert = h > w
    top = int(h * (0.34 if vert else 0.26))
    im.paste(lg, ((w - lw) // 2, top), lg)
    fs = 66 if vert else 64
    f = font("Montserrat-ExtraBold.otf", fs)
    bb = d.textbbox((0, 0), CTA, font=f)
    pw, ph = bb[2] - bb[0] + 110, bb[3] - bb[1] + 70
    py = top + lg.height + int(h * (0.06 if vert else 0.09))
    d.rounded_rectangle(((w - pw) // 2, py, (w + pw) // 2, py + ph), radius=ph // 2, fill=LIME)
    d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], py + (ph - (bb[3] - bb[1])) / 2 - bb[1]), CTA, font=f, fill=GREEN)
    fu = font("Montserrat-SemiBold.otf", 38 if vert else 40)
    centered(d, URL, fu, py + ph + int(h * 0.035), WHITE, w)
    im.save(f"{OUT}/{name}.png")


def title_card(text, name, w=1920, h=1080):
    im = Image.new("RGB", (w, h), GREEN)
    d = ImageDraw.Draw(im)
    f = font("Montserrat-ExtraBold.otf", 92)
    bb = d.textbbox((0, 0), text, font=f)
    th = bb[3] - bb[1]
    y = (h - th) // 2 - bb[1]
    d.rounded_rectangle(((w - 140) // 2, y - 70, (w + 140) // 2, y - 58), radius=6, fill=LIME)
    centered(d, text, f, y, WHITE, w)
    im.save(f"{OUT}/{name}.png")


REVIEW = ("Can't rave enough about Ashley and her team! Great communication, coaching and now I'm "
          "converting leads on Google. Thanks Ashley!")


def review_card(name="review", w=1920, h=1080):
    im = Image.new("RGB", (w, h), GREEN)
    d = ImageDraw.Draw(im)
    f = font("Montserrat-Bold.otf", 58)
    # wrap to 24 em-ish width
    words, lines, cur = REVIEW.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=f) > w * 0.80 and cur:
            lines.append(cur)
            cur = wd
        else:
            cur = t
    lines.append(cur)
    lh = 84
    total = len(lines) * lh
    y0 = (h - total) // 2 - 20
    centered(d, "Google review", font("Montserrat-ExtraBold.otf", 40), y0 - 100, LIME, w)
    for i, ln in enumerate(lines):
        centered(d, ln, f, y0 + i * lh, WHITE, w)
    centered(d, "John Vandervalk, Mountainside ER+ · August 2026", font("Montserrat-Medium.otf", 36),
             y0 + total + 40, LIME, w)
    im.save(f"{OUT}/{name}.png")


if __name__ == "__main__":
    review_card()
    end_card(1080, 1920, "endcard-9x16")
    end_card(1920, 1080, "endcard-16x9")
    titles = json.load(open(P + "/06_scripts/titles.json")) if os.path.exists(P + "/06_scripts/titles.json") else {}
    for k, v in titles.items():
        title_card(v, "title-" + k)
    print("cards ok")
