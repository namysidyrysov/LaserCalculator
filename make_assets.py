"""Готовит файлы логотипа из logo.png. Запускается один раз."""

from PIL import Image, ImageFilter

SIZES = [256, 128, 64, 48, 32, 24, 16]

src = Image.open("logo.png").convert("RGBA")

# Промежуточный размер: огромный файл сначала уменьшаем до 512
base = src.resize((512, 512), Image.LANCZOS)

# Логотип для меню
src.resize((140, 140), Image.LANCZOS).save("logo_menu.png")

# Каждый размер иконки готовим отдельно, с лёгкой резкостью
frames = []
for s in SIZES:
    im = base.resize((s, s), Image.LANCZOS)
    if s <= 64:
        percent = 120 if s >= 32 else 160
        im = im.filter(ImageFilter.UnsharpMask(radius=0.6, percent=percent,
                                               threshold=0))
    frames.append(im)

frames[0].save("icon.ico", format="ICO",
               sizes=[(s, s) for s in SIZES],
               append_images=frames[1:])

print("Готово: logo_menu.png и icon.ico")