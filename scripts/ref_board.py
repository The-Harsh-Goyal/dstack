#!/usr/bin/env python3
"""Screenshot reference works into a reference board, so the agent has really "looked at" them before starting.

Write the words "reference Stripe Press" and the model produces its average impression of Stripe Press;
put a screenshot in front of it, and only then will it measure the grid, compare type sizes and pick colors.

Usage:
  python3 scripts/ref_board.py <url-or-image> [<url-or-image> …] --out refs/board.jpg [--full]

  URL: opened in a headless browser, captures the first screen (--full captures the whole page, up to 4000px tall)
  Image: a local path or image URL (.jpg/.png/.webp/.gif), placed directly on the board
  Each source is saved as its own image (board-1.jpg …, the board's name plus a number, so it won't overwrite screenshots you put in refs/ yourself), then one combined board is assembled.
  Sources that won't open, or whose screenshot is almost a single flat color (common with WebGL sites), are all listed, without interrupting the run.

Once you have the images, open the combined board with your image-viewing ability and write "what is being borrowed" as concrete rules (how many grid columns, the heading-to-body type size ratio,
main color share, image-text relationship), not "referenced its style".
"""

import argparse
import html
import sys
from pathlib import Path

IMG_EXT = ('.jpg', '.jpeg', '.png', '.webp', '.gif')


class BotChallenge(RuntimeError):
    """The site answered with a bot check (Cloudflare, captcha...). dstack does not try to get past these."""


CHALLENGE_TITLES = ('just a moment', 'attention required', 'verify you are human', 'access denied',
                    'are you a robot', 'security check', 'checking your browser', 'pardon our interruption')
CHALLENGE_MARKERS = ('challenges.cloudflare.com', 'cf-chl', 'challenge-running', 'cf_chl_opt', 'hcaptcha.com',
                     'g-recaptcha', 'px-captcha', 'datadome', '_incapsula_')


def check_challenge(page, response=None):
    headers = (response.headers if response else {}) or {}
    title = (page.title() or '').strip().lower()
    body = page.content()[:200000].lower()
    hit = headers.get('cf-mitigated') == 'challenge' or any(title.startswith(t) for t in CHALLENGE_TITLES) \
        or any(m in body for m in CHALLENGE_MARKERS)
    if hit:
        raise BotChallenge('the site showed a bot check (Cloudflare or captcha); dstack does not try to get past it. '
                           'Ask the user for a screenshot of the work, save it into refs/ and pass that file path instead, '
                           'or try a press page / direct image URL for the same work')


# Pop-up buttons, most privacy-preserving first (reject/necessary-only, then accept, then close).
DISMISS_TEXT = [r'reject all', r'reject', r'only necessary', r'necessary only', r'decline', r'refuse',
                r'continue without accepting', r'accept all', r'accept', r'i agree', r'agree', r'allow all',
                r'got it', r'ok', r'okay', r'no,? thanks', r'not now', r'maybe later', r'dismiss', r'close', r'×', r'✕']
DISMISS_SELECTORS = ['#onetrust-reject-all-handler', '#onetrust-accept-btn-handler', '#didomi-notice-agree-button',
                     '.fc-cta-consent', '.qc-cmp2-summary-buttons button', '[aria-label="Close" i]',
                     '[aria-label*="close" i]', '[aria-label*="dismiss" i]', '[data-testid*="close" i]']


def dismiss_popups(page, rounds=3):
    """Click away common cookie/consent banners and promo modals (main page and consent iframes).
    Plain clicks on visible buttons only; anything left covering most of the screen is reported, not hidden."""
    import re
    pat = re.compile(r'^\s*(' + '|'.join(DISMISS_TEXT) + r')\s*[.!]?\s*$', re.I)
    clicked = 0
    for _ in range(rounds):
        hit = False
        for frame in page.frames:
            try:
                for sel in DISMISS_SELECTORS:
                    loc = frame.locator(sel)
                    for i in range(min(loc.count(), 3)):
                        el = loc.nth(i)
                        if el.is_visible():
                            el.click(timeout=1500)
                            clicked += 1
                            hit = True
                            break
                    if hit:
                        break
                if not hit:
                    btns = frame.locator('button, [role=button], a[role=button], input[type=button], input[type=submit]')
                    best = None
                    for i in range(min(btns.count(), 200)):
                        el = btns.nth(i)
                        txt = (el.inner_text(timeout=500) if el.evaluate('e => e.tagName') != 'INPUT' else el.get_attribute('value')) or ''
                        if pat.match(txt) and el.is_visible():
                            rank = next(k for k, t in enumerate(DISMISS_TEXT) if re.fullmatch(t, txt.strip().rstrip('.!'), re.I))
                            if best is None or rank < best[0]:
                                best = (rank, el)
                    if best:
                        best[1].click(timeout=1500)
                        clicked += 1
                        hit = True
            except Exception:
                continue
            if hit:
                break
        if not hit:
            break
        page.wait_for_timeout(400)
    try:   # some banners leave the page scroll-locked
        page.evaluate("document.documentElement.style.overflow='';document.body&&(document.body.style.overflow='')")
    except Exception:
        pass
    return clicked


def shoot(page, src, out, full):
    if Path(src).exists():
        src = Path(src).resolve().as_uri()
    if src.lower().split('?')[0].endswith(IMG_EXT):
        page.set_viewport_size({'width': 1440, 'height': 900})
        r = page.goto(src, wait_until='load', timeout=30000)   # the browser opens the image directly and wraps it in an <img> itself
        if (r and not r.ok) or not page.evaluate('document.images[0] && document.images[0].naturalWidth'):
            raise RuntimeError(f'Image failed to load (HTTP {r.status if r else "?"})')
        page.locator('img').first.screenshot(path=str(out), type='jpeg', quality=82)
        return
    page.set_viewport_size({'width': 1440, 'height': 900})
    resp = page.goto(src, wait_until='domcontentloaded', timeout=30000)
    try:
        page.wait_for_load_state('networkidle', timeout=8000)
    except Exception:
        pass  # sites with long-lived connections never reach networkidle; the first screen is usually enough
    page.wait_for_timeout(800)
    check_challenge(page, resp)
    if dismiss_popups(page):
        page.wait_for_timeout(500)
    if full:
        h = min(page.evaluate('document.documentElement.scrollHeight'), 4000)
        page.set_viewport_size({'width': 1440, 'height': h})
        page.wait_for_timeout(400)
    page.screenshot(path=str(out), type='jpeg', quality=82)


def mostly_blank(path):
    """The screenshot is almost one color: WebGL sites are often black in a headless browser, and lazy-loaded pages are white.

    Criterion: fewer than 0.8% of pixels are clearly different (brightness difference >24) from the most common color. Measured: a WebGL black screen is about 0.4%,
    the emptiest minimal design (one number plus a row of thin lines) about 1.5%. Returns None when Pillow isn't installed, meaning it can't tell.
    """
    try:
        from PIL import Image
    except ImportError:
        return None
    from collections import Counter
    px = Image.open(path).convert('L').resize((360, 225)).tobytes()
    mode = Counter(px).most_common(1)[0][0]
    return sum(1 for v in px if abs(v - mode) > 24) / len(px) < 0.008


def board(page, shots, out):
    cells = ''.join(
        f'<figure><img src="{p.resolve().as_uri()}"><figcaption>{html.escape(s)}</figcaption></figure>'
        for p, s in shots)
    page.set_viewport_size({'width': 1500, 'height': 600})
    tmp = out.parent / '.board.html'
    tmp.write_text(f'''<!doctype html><meta charset="utf-8"><style>
body{{margin:0;padding:20px;background:#ddd;font:13px/1.3 -apple-system,"PingFang SC","Noto Sans SC",sans-serif}}
.g{{display:grid;grid-template-columns:repeat(2,720px);gap:16px;align-items:start}}
figure{{margin:0}} img{{width:720px;display:block;max-height:1100px;object-fit:cover;object-position:top}}
figcaption{{margin-top:4px;word-break:break-all;color:#333}}</style><div class="g">{cells}</div>''', encoding='utf-8')
    page.goto(tmp.resolve().as_uri(), wait_until='load', timeout=30000)   # local images can only be referenced from a file:// page
    page.screenshot(path=str(out), full_page=True, type='jpeg', quality=80)
    tmp.unlink()


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8')
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description='Screenshot reference works into a reference board')
    ap.add_argument('sources', nargs='+')
    ap.add_argument('--out', default='refs/board.jpg')
    ap.add_argument('--full', action='store_true', help='capture the whole web page (up to 4000px)')
    a = ap.parse_args(argv)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('Playwright is required: pip install playwright && python3 -m playwright install chromium')
        print('Without it: use WebSearch image results or ask the user for screenshots, save them into refs/ and open them directly with your image-viewing ability.')
        return 2
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    shots, failed, unchecked = [], [], False
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as e:
            print('Chromium failed to launch:', str(e).splitlines()[0])
            print('Install it: python3 -m playwright install chromium')
            return 2
        page = browser.new_page()
        for i, src in enumerate(a.sources, 1):
            one = out.with_name(f'{out.stem}-{i}.jpg')
            if Path(src).exists() and Path(src).resolve() == one.resolve():
                one = out.with_name(f'{out.stem}-{i}-shot.jpg')
            try:
                shoot(page, src, one, a.full)
                blank = mostly_blank(one)
                unchecked = unchecked or blank is None
                if blank:
                    failed.append(src)
                    print('✗', src, ': the screenshot is almost a single flat color (WebGL/3D site or lazy loading), so it\'s as good as not having looked')
                    continue
                shots.append((one, src))
                print('✓', one, '←', src)
            except Exception as e:
                failed.append(src)
                print('✗', src, ':', str(e).splitlines()[0])
        if shots:
            board(page, shots, out)
            print('Reference board →', out)
        elif out.exists():
            out.unlink()   # the old board from last time; if kept it would be taken for this run's
        browser.close()
    if unchecked:
        print('\nPillow isn\'t installed (pip install pillow), so there\'s no automatic check for flat-color screenshots: open each one and take a look before using it.')
    if failed:
        print('\nSources that wouldn\'t open (common causes: anti-scraping, login required, region restrictions). Try a press page or image URL for the same work, '
              'or ask the user for a screenshot. Don\'t pretend to have looked based on impressions.')
    return 0 if shots else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
