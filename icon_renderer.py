from PIL import Image, ImageDraw, ImageFont

_FONT = None


def _font(size: int):
    global _FONT
    if _FONT is None or _FONT.size != size:
        try:
            _FONT = ImageFont.truetype("segoeuib.ttf", size)
        except OSError:
            _FONT = ImageFont.load_default()
    return _FONT


CANVAS = 48


def render(percent: int, charging: bool, has_battery: bool) -> Image.Image:
    img = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if not has_battery:
        text = "--"
    elif percent >= 100:
        text = "F"
    else:
        text = str(percent)

    color = (0, 0, 0, 255)
    size = 34 if len(text) >= 2 else 44
    font = _font(size)

    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    w, h = right - left, bottom - top
    draw.text(((CANVAS - w) / 2 - left, (CANVAS - h) / 2 - top),
              text, font=font, fill=color)
    return img
