from PIL import Image, ImageDraw
import io
def create_palette_image(palette):
    W, H, TEXT_H = 220, 220, 70
    img = Image.new("RGB", (W * len(palette), H + TEXT_H), "#1a1a1a")
    draw = ImageDraw.Draw(img)
    for i, color in enumerate(palette):
        x = i * W
        r, g, b = color["rgb"]
        draw.rectangle([x, 0, x + W, H], fill=(r, g, b))
        draw.text((x + 8, H + 8),  color["name"], fill="white")
        draw.text((x + 8, H + 28), color["hex"],  fill="#c9a84c")
        draw.text((x + 8, H + 48), f"RGB {r},{g},{b}", fill="#888")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()