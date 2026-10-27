#!/usr/bin/env python3
"""cover.py: covers and single social images at exact pixel sizes (dstack). Fully local.

  render   HTML -> PNG at exactly the preset size (viewport = size, device scale 1)
  upscale  small raster (e.g. a 1024x576 generation) -> preset size with ffmpeg lanczos,
           cover-cropped (default) or contained/padded; optional light sharpening
  check    raster checks for a finished cover: exact size, aspect, flat image, metadata,
           and a safe-area overlay PNG to look at (design_lint.py is HTML-only)

Presets (WxH): x-article 2500x1000 (X article header), x-infeed 1600x900 (in-feed 16:9),
og 1200x630, yt-thumb 1280x720, square 1080x1080, portrait 1080x1350. Or --size WxH.

Usage:
  python3 scripts/cover.py render cover.html --preset x-article -o final/cover-2500x1000.png
  python3 scripts/cover.py upscale gen-1024x576.png --preset x-article -o hero-2500x1000.png [--gravity top] [--fit contain] [--sharpen]
  python3 scripts/cover.py check final/cover-2500x1000.png --preset x-article [--safe 0.08]
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PRESETS = {'x-article': (2500, 1000), 'x-infeed': (1600, 900), 'og': (1200, 630), 'yt-thumb': (1280, 720),
           'square': (1080, 1080), 'portrait': (1080, 1350)}


def size_of(a):
    if a.size:
        w, h = a.size.lower().split('x')
        return int(w), int(h)
    if a.preset:
        return PRESETS[a.preset]
    sys.exit('Give --preset (' + ', '.join(PRESETS) + ') or --size WxH')


def strip_metadata(path):
    """Re-save the pixels into a fresh PNG with no text/EXIF chunks."""
    from PIL import Image
    im = Image.open(path)
    clean = Image.frombytes(im.mode, im.size, im.tobytes())
    clean.save(path, format='PNG', optimize=True)


def cmd_render(a):
    from playwright.sync_api import sync_playwright
    w, h = size_of(a)
    src = Path(a.html).resolve()
    if not src.exists():
        sys.exit(f'Not found: {src}')
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg.goto(src.as_uri(), wait_until='load', timeout=60000)
        try:
            pg.wait_for_load_state('networkidle', timeout=8000)
        except Exception:
            pass
        pg.evaluate('document.fonts && document.fonts.ready')
        pg.wait_for_timeout(a.wait)
        pg.screenshot(path=str(out), clip={'x': 0, 'y': 0, 'width': w, 'height': h})
        b.close()
    strip_metadata(out)
    return verify(out, w, h)


def cmd_upscale(a):
    if not shutil.which('ffmpeg'):
        sys.exit('ffmpeg is required for upscale')
    w, h = size_of(a)
    src = Path(a.image)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    gx = {'center': '(iw-ow)/2', 'left': '0', 'right': 'iw-ow'}.get(a.gravity, '(iw-ow)/2')
    gy = {'center': '(ih-oh)/2', 'top': '0', 'bottom': 'ih-oh'}.get(a.gravity, '(ih-oh)/2')
    if a.fit == 'cover':
        vf = f'scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h}:{gx}:{gy}'
    else:
        vf = (f'scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,'
              f'pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color={a.pad}')
    if a.sharpen:
        vf += ',unsharp=5:5:0.6:5:5:0.0'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-vf', vf, '-frames:v', '1', str(out)], check=True)
    from PIL import Image
    sw, sh = Image.open(src).size
    factor = max(w / sw, h / sh) if a.fit == 'cover' else min(w / sw, h / sh)
    print(f'Upscaled {sw}x{sh} -> {w}x{h} ({a.fit}, x{factor:.2f}, lanczos{" + unsharp" if a.sharpen else ""})')
    if factor > 2.5:
        print(f'  note: x{factor:.1f} is a big jump; expect softness. Fine for feed size, check at 100% before print use')
    strip_metadata(out)
    return verify(out, w, h)


def verify(path, w, h):
    from PIL import Image
    im = Image.open(path)
    ok = im.size == (w, h)
    print(f'{"✓" if ok else "✗"} {path}: {im.size[0]}x{im.size[1]} (want {w}x{h})')
    return 0 if ok else 1


def cmd_check(a):
    from PIL import Image, ImageDraw, ImageStat
    w, h = size_of(a)
    path = Path(a.image)
    im = Image.open(path)
    bad = 0
    if im.size != (w, h):
        print(f'🔴 size {im.size[0]}x{im.size[1]}, want {w}x{h}')
        bad += 1
    else:
        print(f'✓ size {w}x{h}')
    meta = {k: v for k, v in im.info.items() if k not in ('dpi', 'gamma', 'transparency', 'srgb', 'icc_profile')}
    exif = im.getexif()
    if meta or len(exif):
        print(f'🟡 metadata present ({", ".join(list(meta)[:5]) or "EXIF"}); re-save with cover.py upscale/render or strip it')
    else:
        print('✓ no metadata chunks')
    stat = ImageStat.Stat(im.convert('L'))
    if stat.stddev[0] < 4:
        print('🔴 image is almost one flat tone')
        bad += 1
    m = a.safe
    ov = im.convert('RGB').copy()
    d = ImageDraw.Draw(ov)
    x0, y0, x1, y1 = int(im.size[0] * m), int(im.size[1] * m), int(im.size[0] * (1 - m)), int(im.size[1] * (1 - m))
    for k in range(3):
        d.rectangle([x0 - k, y0 - k, x1 + k, y1 + k], outline=(255, 0, 180))
    ov_path = path.with_name(path.stem + '-safe.png')
    ov.save(ov_path)
    print(f'Safe area {int(m * 100)}% ({x0}-{x1} x {y0}-{y1}) overlay → {ov_path} : look at it; key elements and any text belong inside the box')
    print('Raster covers are not checked for type size or contrast; if there is text, check it by eye at feed size (about 600 px wide).')
    return 1 if bad else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('render', 'upscale', 'check'):
        sp = sub.add_parser(name)
        sp.add_argument('html' if name == 'render' else 'image')
        sp.add_argument('--preset', choices=sorted(PRESETS))
        sp.add_argument('--size', help='WxH, overrides --preset')
        if name != 'check':
            sp.add_argument('-o', '--out', required=True)
        if name == 'render':
            sp.add_argument('--wait', type=int, default=300, help='ms to wait after load (default 300)')
        if name == 'upscale':
            sp.add_argument('--fit', choices=['cover', 'contain'], default='cover')
            sp.add_argument('--gravity', choices=['center', 'top', 'bottom', 'left', 'right'], default='center')
            sp.add_argument('--pad', default='black', help='pad colour for --fit contain')
            sp.add_argument('--sharpen', action='store_true')
        if name == 'check':
            sp.add_argument('--safe', type=float, default=0.08, help='safe-area margin as a fraction (default 0.08)')
    a = ap.parse_args(argv)
    return {'render': cmd_render, 'upscale': cmd_upscale, 'check': cmd_check}[a.cmd](a)


if __name__ == '__main__':
    sys.exit(main())
