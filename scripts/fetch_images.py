#!/usr/bin/env python3
"""
Fetch real images (public domain / CC) from Wikimedia Commons, for dstack's "use real images for content-driven design" (Phase 3.5).

Why this script exists: content-driven design (parrots/coffee/Malaysia…) must use real images, not fudge it with CSS color blocks.
Having the model write image-fetching logic from scratch every time is slow and easy to trip over (forget to clear the proxy → TLS blows up / forget a compliant UA → 429). This locks it in; next time just change the keywords.

Usage:
  python3 scripts/fetch_images.py --query "Petronas Towers" "Langkawi beach" "George Town street" \
      --out project/assets/img --count 2 --width 1600

For each query, take the first count images, scale to width, download to out, and print a list (path | license | author | source page) for the honesty check.
If nothing can be fetched → exit code 1, with a prompt to use the Phase 3.5 three-level image fallback (Unsplash/Pexels → image generation → honest placeholder).
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request

# ① Clear the proxy: on this machine curl/urllib through the proxy blows up TLS (see memory feedback_gemini_proxy)
for _k in ("ALL_PROXY", "all_proxy", "HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy"):
    os.environ.pop(_k, None)

API = "https://commons.wikimedia.org/w/api.php"
# ② A compliant User-Agent is a hard requirement, otherwise Wikimedia returns 429
UA = "dstack-image-fetcher/0.1 (local design tool)"


def _api_get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def _safe(name):
    return re.sub(r"[^\w\-.]", "_", name)[:60]


def fetch(query, out, count, width):
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": query, "gsrnamespace": 6, "gsrlimit": count,
        "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": width,
    }
    try:
        data = _api_get(params)
    except Exception as e:
        print(f"[FAIL search] {query}: {e}", file=sys.stderr)
        return []
    pages = (data.get("query", {}) or {}).get("pages", {})
    got = []
    for p in list(pages.values())[:count]:
        ii = (p.get("imageinfo") or [{}])[0]
        thumb = ii.get("thumburl") or ii.get("url")
        if not thumb:
            continue
        meta = ii.get("extmetadata", {}) or {}
        lic = (meta.get("LicenseShortName", {}) or {}).get("value", "?")
        artist = re.sub("<[^>]+>", "", (meta.get("Artist", {}) or {}).get("value", "?")).strip()
        ext = os.path.splitext(thumb)[1].split("?")[0] or ".jpg"
        fn = _safe(query) + "_" + _safe(p.get("title", "img").replace("File:", ""))
        fn = os.path.splitext(fn)[0][:55] + ext
        path = os.path.join(out, fn)
        try:
            req = urllib.request.Request(thumb, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as f:
                f.write(r.read())
            got.append(path)
            print(f"[OK] {path}  | {lic} | {artist} | {ii.get('descriptionurl','')}")
        except Exception as e:
            print(f"[FAIL dl] {thumb}: {e}", file=sys.stderr)
    if not got:
        print(f"[EMPTY] nothing fetched for \"{query}\"; change the keywords, or use the Phase 3.5 fallback", file=sys.stderr)
    return got


def main():
    ap = argparse.ArgumentParser(description="Wikimedia Commons real image fetcher (dstack Phase 3.5)")
    ap.add_argument("--query", nargs="+", required=True, help="one or more English keywords (English gets more hits)")
    ap.add_argument("--out", required=True, help="output directory (suggested: project/assets/img)")
    ap.add_argument("--count", type=int, default=2, help="how many images per keyword (default 2)")
    ap.add_argument("--width", type=int, default=1600, help="scaled width in px (default 1600)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    allgot = []
    for q in a.query:
        allgot += fetch(q, a.out, a.count, a.width)
    print(f"\n=== Downloaded {len(allgot)} images to {a.out} ===")
    print("⚠️ Honesty check: would removing each image lose information? Does the license allow this use? Delete the ones that don't fit.")
    if not allgot:
        print("❌ Everything failed → use the Phase 3.5 three-level image fallback (Unsplash/Pexels → image generation → honest placeholder, doesn't block the flow)", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
