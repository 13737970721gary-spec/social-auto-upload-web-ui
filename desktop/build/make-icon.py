import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
]
font_path = next((f for f in FONT_CANDIDATES if os.path.exists(f)), None)
if not font_path:
    print("ERROR: 找不到中文字体", file=sys.stderr); sys.exit(1)
print(f"使用字体: {font_path}", file=sys.stderr)

SIZE = 1024
img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
radius = 224

bg = Image.new("RGBA", (SIZE, SIZE), 0)
bg_pixels = bg.load()
top_color = (79, 70, 229)
mid_color = (37, 99, 235)
bot_color = (6, 182, 212)
def smoothstep(t): return t*t*(3-2*t)
for y in range(SIZE):
    t = y / (SIZE - 1)
    if t < 0.5:
        a = smoothstep(t / 0.5)
        c = tuple(int(top_color[i]*(1-a) + mid_color[i]*a) for i in range(3))
    else:
        a = smoothstep((t - 0.5) / 0.5)
        c = tuple(int(mid_color[i]*(1-a) + bot_color[i]*a) for i in range(3))
    for x in range(SIZE):
        bg_pixels[x, y] = c + (255,)

mask = Image.new("L", (SIZE, SIZE), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([0, 0, SIZE-1, SIZE-1], radius=radius, fill=255)
img.paste(bg, (0, 0), mask)

glow = Image.new("RGBA", (SIZE, SIZE), 0)
gd = ImageDraw.Draw(glow)
for y in range(int(SIZE*0.65)):
    t = y / (SIZE*0.65)
    a = max(0, int(90 * (1 - t)))
    gd.line([(0, y), (SIZE, y)], fill=(255, 255, 255, a))
img.alpha_composite(glow)

shine = Image.new("RGBA", (SIZE, SIZE), 0)
sd = ImageDraw.Draw(shine)
for y in range(int(SIZE*0.3)):
    yy = SIZE - 1 - y
    a = max(0, int(38 * (1 - y / (SIZE*0.3))))
    sd.line([(0, yy), (SIZE, yy)], fill=(255, 255, 255, a))
img.alpha_composite(shine)

deco = Image.new("RGBA", (SIZE, SIZE), 0)
dd2 = ImageDraw.Draw(deco)
dd2.polygon([(-100, 870), (1124, 600), (1240, 640), (-50, 920)], fill=(255, 255, 255, 28))
dd2.polygon([(-100, 950), (1124, 680), (1240, 720), (-50, 1000)], fill=(255, 255, 255, 18))
img.alpha_composite(deco)

font_size = 720
font = ImageFont.truetype(font_path, font_size)
text = "千"
bbox = draw.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
tx = (SIZE - tw) // 2 - bbox[0]
ty = (SIZE - th) // 2 - bbox[1]   # 0 偏移：纯几何居中

shadow = Image.new("RGBA", (SIZE, SIZE), 0)
sd2 = ImageDraw.Draw(shadow)
sd2.text((tx+8, ty+14), text, font=font, fill=(0, 0, 0, 100))
shadow = shadow.filter(ImageFilter.GaussianBlur(10))
img.alpha_composite(shadow)
draw.text((tx, ty), text, font=font, fill=(255, 255, 255, 255))

img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=110, threshold=2))

out = r"D:\work\QianfanSync\desktop\build\icon.png"
img.save(out, "PNG", optimize=True)
print(f"OK: {out} ({os.path.getsize(out)//1024} KB)", file=sys.stderr)
