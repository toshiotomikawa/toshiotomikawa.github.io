"""Generate crimson and white favicon assets from source artwork."""
import base64
from collections import deque
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SRC_PATH = Path(r"C:\Users\Zen\Downloads\letter-t-.png")

CRIMSON = np.array([188.0, 0.0, 45.0])  # #bc002d
WHITE = np.array([255.0, 255.0, 255.0])    # #ffffff


def build_favicons():
    im = Image.open(SRC_PATH).convert("RGBA")
    w, h = im.size
    orig_alpha = np.array(im)[:, :, 3].astype(float)

    # Flood fill from corners at alpha < 250 to classify the outer corner region
    is_outer = np.zeros((h, w), dtype=bool)
    q = deque([(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)])
    for x, y in list(q):
        is_outer[y, x] = True

    while q:
        x, y = q.popleft()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not is_outer[ny, nx]:
                if orig_alpha[ny, nx] < 250:
                    is_outer[ny, nx] = True
                    q.append((nx, ny))

    out_rgba = np.zeros((h, w, 4), dtype=np.uint8)

    for y in range(h):
        for x in range(w):
            a = orig_alpha[y, x]
            if is_outer[y, x]:
                out_rgba[y, x, 0:3] = CRIMSON.astype(np.uint8)
                out_rgba[y, x, 3] = int(round(a))
            else:
                t_weight = (255.0 - a) / 255.0
                color = t_weight * WHITE + (1.0 - t_weight) * CRIMSON
                out_rgba[y, x, 0:3] = np.clip(np.round(color), 0, 255).astype(np.uint8)
                out_rgba[y, x, 3] = 255

    master = Image.fromarray(out_rgba, "RGBA")

    # 1. Master 512x512 PNG
    master.save(ASSETS / "favicon.png", "PNG", optimize=True)

    # 2. 32x32 standard tab favicon
    fav32 = master.resize((32, 32), Image.Resampling.LANCZOS)
    fav32.save(ASSETS / "favicon-32x32.png", "PNG", optimize=True)

    # 3. 192x192 Android / PWA favicon
    fav192 = master.resize((192, 192), Image.Resampling.LANCZOS)
    fav192.save(ASSETS / "favicon-192x192.png", "PNG", optimize=True)

    # 4. 180x180 Apple touch icon
    fav180 = master.resize((180, 180), Image.Resampling.LANCZOS)
    fav180.save(ASSETS / "apple-touch-icon.png", "PNG", optimize=True)

    # 5. Multi-resolution ICO (16, 32, 48)
    master.save(
        ASSETS / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )

    # 6. SVG favicon with embedded high-resolution master
    png_bytes = (ASSETS / "favicon.png").read_bytes()
    b64_png = base64.b64encode(png_bytes).decode("ascii")
    svg_content = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">\n'
        f'  <image width="{w}" height="{h}" href="data:image/png;base64,{b64_png}"/>\n'
        f'</svg>\n'
    )
    (ASSETS / "favicon.svg").write_text(svg_content, encoding="utf-8")

    print("Generated all favicon variants in assets/ successfully.")


if __name__ == "__main__":
    build_favicons()
