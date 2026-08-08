from PIL import Image, ImageDraw, ImageFont
import os
OUT = r"C:\Dev\portfolio\verify\cta-pass"

def font(sz):
    try:
        return ImageFont.truetype("arial.ttf", sz)
    except Exception:
        return ImageFont.load_default()

LABEL_H = 30
PAD = 16
BG = (250, 250, 250)
INK = (40, 40, 46)

def stack(paths_labels, out_name, title):
    imgs = [Image.open(os.path.join(OUT, p)).convert("RGB") for p, _ in paths_labels]
    w = max(i.width for i in imgs) + PAD * 2
    title_h = 34
    total_h = title_h + sum(i.height + LABEL_H for i in imgs) + PAD
    canvas = Image.new("RGB", (w, total_h), BG)
    d = ImageDraw.Draw(canvas)
    d.text((PAD, 10), title, fill=INK, font=font(18))
    y = title_h
    for (p, lab), img in zip(paths_labels, imgs):
        d.text((PAD, y + 6), lab, fill=(90, 90, 98), font=font(14))
        y += LABEL_H
        canvas.paste(img, (PAD, y))
        y += img.height
    canvas.save(os.path.join(OUT, out_name))
    print("wrote", out_name, canvas.size)

stack([("before-light-rest.png", "BEFORE  (v22: white rim, softer edge)"),
       ("after-light-rest.png",  "AFTER   (v23: accent rim rgba(26,111,212,0.28), deepened fill)")],
      "sxs-light-rest.png", "Light CTA - REST : before vs after")

stack([("before-light-hover.png", "BEFORE  (v22)"),
       ("after-light-hover.png",  "AFTER   (v23)")],
      "sxs-light-hover.png", "Light CTA - HOVER : before vs after")

stack([("after-dark-rest.png",  "DARK rest  (reference, unchanged)"),
       ("after-dark-hover.png", "DARK hover (reference, unchanged)")],
      "ref-dark.png", "Dark CTA - reference (untouched, rim lighter than fill)")

stack([("before-light-fullrow.png", "BEFORE light - full index list"),
       ("after-light-fullrow.png",  "AFTER light - full index list")],
      "sxs-light-fullrow.png", "Light full row context : before vs after")
print("done")
