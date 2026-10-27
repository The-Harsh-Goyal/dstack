#!/usr/bin/env python3
"""Convert "an already-written visual-draft HTML" straight into an editable PPTX, without requiring the HTML to meet any hard constraints.

Division of labor with html2pptx.js (don't mix them; see the decision table at the top of references/editable-pptx.md):

  html2pptx.js          HTML not written yet → write it to the 4 hard constraints; the exported text box structure is cleanest
  this script           HTML already written and visually driven (flex / centering / bare text / background images)
                        → convert directly with zero rework; it's also the only route when you must inherit the client's official template masters

Why it can sidestep those 4 hard constraints: what it reads is not the source but the getBoundingClientRect
**after the browser has rendered**. The browser has already turned flex, centering and auto-wrapping into absolute coordinates,
so patterns like "bare text inside a div" or "using flex" simply aren't a problem.

Four kinds of elements map to four kinds of PowerPoint objects:
  text  → text box (split into paragraphs at <br>, one box per paragraph, each with its own runs and line height)
  shape → rectangle / rounded rectangle (card backgrounds, color bars, dividers, inline decorative blocks)
  img   → picture (CSS corner radius is baked into the alpha channel)
  svg   → picture captured as PNG (a chart broken into hundreds of rectangles can't be edited anyway; keeping it as an image is more practical)

Usage:
    python3 pptx_from_rendered.py deck.html -o deck.pptx
    python3 pptx_from_rendered.py deck.html -o deck.pptx \\
        --template client-template.pptx --layout "Content" --skip-class logo

Dependencies: playwright (with chromium), python-pptx, Pillow
"""
import argparse, asyncio, json, os, re, sys

from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

EMU_PER_PT = 12700

# ─────────────────────────────────────────────────────────────
# 1. Measure in the browser: break the rendered result into an element list
# ─────────────────────────────────────────────────────────────

JS = r"""
(selector) => {
  const INLINE = ['em','b','i','strong','span','small','br','sup','sub','a','code','mark'];
  const px = v => parseFloat(v) || 0;

  // Split a run of nodes into runs (one run per stretch of consecutive same-styled text).
  //
  // ⚠️ HTML whitespace collapsing must be done here. Line breaks and indentation in the source become real text nodes,
  // which the browser collapses under white-space:normal (consecutive whitespace → one space, leading and trailing dropped),
  // but PPTX has no such rule. Carried over as is, that \n is a real line break in PowerPoint
  // and pushes the whole following content down a line, on top of other elements.
  const runsOf = (root, op) => {
    const out = [];
    let atLineStart = true, pendingSpace = false;
    const push = (node, styleEl) => {
      let t = node.textContent;
      if (!t) return;
      t = t.replace(/\s+/g, ' ');
      if (t === ' ') { if (!atLineStart) pendingSpace = true; return; }
      if (atLineStart) t = t.replace(/^ /, '');
      if (pendingSpace && !t.startsWith(' ')) t = ' ' + t;
      pendingSpace = false;
      if (!t) return;
      atLineStart = false;
      const cs = getComputedStyle(styleEl);
      // text-transform changes only rendering, not textContent, so apply it ourselves; otherwise uppercase labels revert to the source casing
      const tt = cs.textTransform;
      if (tt === 'uppercase') t = t.toUpperCase();
      else if (tt === 'lowercase') t = t.toLowerCase();
      else if (tt === 'capitalize') t = t.replace(/(^|\s)(\S)/g, (_, a, b) => a + b.toUpperCase());
      out.push({
        t, op, fs: px(cs.fontSize), fw: cs.fontWeight, color: cs.color,
        ls: cs.letterSpacing === 'normal' ? 0 : px(cs.letterSpacing),
        italic: cs.fontStyle === 'italic',
        under: cs.textDecorationLine.includes('underline'),
      });
    };
    const walk = (node, styleEl) => {
      for (const n of node.childNodes) {
        if (n.nodeType === 3) push(n, styleEl);
        else if (n.tagName && n.tagName.toLowerCase() === 'br') {
          out.push({br: true}); atLineStart = true; pendingSpace = false;
        } else if (n.nodeType === 1) walk(n, n);
      }
    };
    walk(root, root);
    for (let i = out.length - 1; i >= 0 && !out[i].br; i--) {
      if (out[i].t) { out[i].t = out[i].t.replace(/ $/, ''); break; }
    }
    return out.filter(r => r.br || r.t);
  };

  // Measure the position and line count occupied by a group of nodes.
  // Line count can't come from de-duplicating each rect's top: runs of different sizes on the same line (a 132px number next to
  // a 62px caption) share a baseline but their top edges differ a lot, and would be counted as two lines. Cluster by overlapping y ranges instead.
  const measure = (nodes) => {
    const rng = document.createRange();
    rng.setStartBefore(nodes[0]);
    rng.setEndAfter(nodes[nodes.length - 1]);
    const bb = rng.getBoundingClientRect();
    const rects = [...rng.getClientRects()]
                    .filter(q => q.width > 0.5 && q.height > 0.5)
                    .sort((a, b) => a.top - b.top);
    const rows = [];
    for (const q of rects) {
      const last = rows[rows.length - 1];
      if (last && q.top < last.bottom - 2) last.bottom = Math.max(last.bottom, q.bottom);
      else rows.push({top: q.top, bottom: q.bottom});
    }
    return {bb, lines: Math.max(1, rows.length)};
  };

  const pages = [...document.querySelectorAll(selector)];
  return pages.map((pg) => {
    const pb = pg.getBoundingClientRect();
    const out = [];
    let svgSeq = 0;

    // A group of adjacent nodes → one text element. own=true means this is "bare text between block-level children",
    // so its position must use the text's own bounding box, not the container's x/w (otherwise it would cover the icon next to it).
    const emitText = (el, cs, base, g, op, own) => {
      const nodes = g.filter(n => n.nodeType !== 3 || n.textContent.trim());
      if (!nodes.length) return;
      const {bb, lines} = measure(nodes);
      if (!bb.height) return;
      const tmp = document.createElement('div');
      for (const n of g) tmp.appendChild(n.cloneNode(true));
      tmp.style.cssText = 'position:absolute;visibility:hidden';
      el.appendChild(tmp);
      const rs = runsOf(tmp, op);
      tmp.remove();
      if (!rs.length) return;
      const fsMax = Math.max(px(cs.fontSize), ...rs.filter(r => !r.br).map(r => r.fs));
      out.push({
        tag: base.tag, cls: base.cls, kind: 'text',
        // x/w come from the container: a centered paragraph needs the container width to stay centered;
        // using the paragraph's own shrunk width makes it drift left or right after a font change.
        x: own ? bb.left - pb.left : base.x, w: own ? bb.width : base.w,
        y: bb.top - pb.top, h: bb.height,
        fs: px(cs.fontSize), fsMax, fw: cs.fontWeight, color: cs.color,
        ls: cs.letterSpacing === 'normal' ? 0 : px(cs.letterSpacing),
        ta: own ? 'left' : cs.textAlign,
        lhEff: bb.height / lines, lines,
        wrap: lines > 1,
        runs: rs,
      });
    };

    // op: the cumulative product of opacity along the ancestor chain (CSS opacity applies to the whole subtree)
    const walk = (el, parentOp = 1) => {
      const cs = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      const tag = el.tagName.toLowerCase();
      const op = parentOp * (parseFloat(cs.opacity) || 0);
      if (cs.display === 'none' || cs.visibility === 'hidden' || op === 0) return;

      const cls = (typeof el.className === 'string' ? el.className : '');
      const base = {tag, cls, x: r.left - pb.left, y: r.top - pb.top, w: r.width, h: r.height};

      if (tag === 'img') {
        out.push({...base, kind: 'img', src: el.getAttribute('src'),
                  radius: px(cs.borderRadius), shadow: cs.boxShadow});
        return;
      }
      if (tag === 'svg' || tag === 'canvas') {
        out.push({...base, kind: 'svg', seq: svgSeq++, tagName: tag});
        return;
      }

      const hasText = el.innerText && el.innerText.trim().length > 0;
      const onlyInline = [...el.children].every(c => INLINE.includes(c.tagName.toLowerCase()));

      const bg = cs.backgroundColor;
      const painted = (bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent');
      const bdw = px(cs.borderTopWidth);
      if (painted || bdw > 0) {          // background/border emit a rectangle first, drawn beneath the text
        out.push({...base, kind: 'shape', bg, bdw, bdc: cs.borderTopColor, op,
                  radius: px(cs.borderRadius), shadow: cs.boxShadow, rot: 0});
      }

      if (hasText && onlyInline) {
        // Split into paragraphs at <br>, each paragraph gets its own text box.
        //
        // Why not one box for the whole block: PowerPoint line spacing is paragraph-level, and visual drafts often put lines of different sizes
        // in the same div. Applying one line spacing to the whole block stretches the small lines and squashes the large one;
        // in testing, adjacent lines ended up stacked on top of each other. Split up, each paragraph uses its own actual line height and they don't affect each other.
        const groups = [[]];
        for (const n of el.childNodes) {
          if (n.nodeType === 1 && n.tagName.toLowerCase() === 'br') groups.push([]);
          else groups[groups.length - 1].push(n);
        }
        for (const g of groups) emitText(el, cs, base, g, op, false);

        // Purely decorative inline color blocks (strike-through bars over the text, highlight bars) must not be swallowed along with the text;
        // emit them as separate shapes, drawn above the text.
        for (const c of el.children) {
          const ccs = getComputedStyle(c);
          const cbg = ccs.backgroundColor;
          if (c.textContent.trim() === '' &&
              cbg !== 'rgba(0, 0, 0, 0)' && cbg !== 'transparent') {
            const cr = c.getBoundingClientRect();
            let rot = 0;
            const m = ccs.transform.match(/matrix\(([^)]+)\)/);
            if (m) {
              const [a, b] = m[1].split(',').map(parseFloat);
              rot = Math.round(Math.atan2(b, a) * 180 / Math.PI * 10) / 10;
            }
            out.push({tag: c.tagName.toLowerCase(), cls: '', kind: 'shape',
                      x: cr.left - pb.left, y: cr.top - pb.top, w: cr.width, h: cr.height,
                      bg: cbg, bdw: px(ccs.borderTopWidth), bdc: ccs.borderTopColor,
                      radius: px(ccs.borderRadius), shadow: ccs.boxShadow, rot});
          }
        }
        return;
      }
      // Mixed content: both non-inline children (svg/div…) and bare text. el.children can't see text nodes,
      // so walk childNodes, otherwise bare text gets silently dropped (issue #56).
      let run = [];
      const flush = () => { emitText(el, cs, base, run, op, true); run = []; };
      for (const n of el.childNodes) {
        if (n.nodeType === 3) run.push(n);
        else if (n.nodeType === 1) { flush(); walk(n, op); }
      }
      flush();
    };

    for (const c of pg.children) walk(c);
    // ref: the innerText the browser rendered itself. It doesn't pass through any of the extraction logic above,
    // and is the only independent reference when checking for dropped text (text-transform already applied).
    // svg/canvas are captured whole as images and their text never goes into text boxes, so hide them before comparing.
    const hid = [...pg.querySelectorAll('svg,canvas')].map(n => [n, n.style.display]);
    hid.forEach(([n]) => { n.style.display = 'none'; });
    const ref = pg.innerText;
    hid.forEach(([n, d]) => { n.style.display = d; });
    return {w: pb.width, h: pb.height, els: out, ref};
  });
}
"""


async def render(html, selector, asset_dir, scale):
    from playwright.async_api import async_playwright
    os.makedirs(asset_dir, exist_ok=True)
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(viewport={"width": 1920, "height": 1080},
                               device_scale_factor=scale)
        await pg.goto("file://" + os.path.abspath(html))
        await pg.wait_for_timeout(2500)
        pages = await pg.evaluate(JS, selector)
        for pi, page in enumerate(pages):          # SVG / canvas captured separately as PNG
            for e in page["els"]:
                if e["kind"] == "svg":
                    name = f"p{pi+1:02d}_{e['tagName']}{e['seq']}.png"
                    await pg.locator(selector).nth(pi).locator(e["tagName"]).nth(e["seq"]) \
                            .screenshot(path=os.path.join(asset_dir, name), omit_background=True)
                    e["file"] = os.path.join(asset_dir, name)
        await br.close()
    return pages


# ─────────────────────────────────────────────────────────────
# 2. Translate into PowerPoint objects
# ─────────────────────────────────────────────────────────────

ALIGN = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "start": PP_ALIGN.LEFT,
         "right": PP_ALIGN.RIGHT, "end": PP_ALIGN.RIGHT, "justify": PP_ALIGN.JUSTIFY}


def parse_color(css):
    """'rgb(r,g,b)' / 'rgba(r,g,b,a)' → (RGBColor, alpha)."""
    m = re.findall(r"[\d.]+", css or "")
    if len(m) < 3:
        return None, 0.0
    r, g, b = (int(float(v)) for v in m[:3])
    return RGBColor(r, g, b), (float(m[3]) if len(m) > 3 else 1.0)


def _alpha(clr_el, alpha):
    a = clr_el.makeelement(qn("a:alpha"), {})
    a.set("val", str(int(alpha * 100000)))
    clr_el.append(a)


class Builder:
    def __init__(self, cfg):
        self.cfg = cfg
        self.round_dir = os.path.join(cfg.asset_dir, "_round")

    # ── Text ──────────────────────────────────────────────
    def set_run_font(self, run, r):
        f = run.font
        f.size = Pt(r["fs"] * self.k)
        fw = str(r["fw"])
        f.bold = int(fw) >= 600 if fw.isdigit() else fw in ("bold", "bolder")
        f.italic = r.get("italic", False)
        f.underline = r.get("under", False)
        f.name = self.cfg.font_latin           # only latin is set; Chinese needs to be specified separately
        col, alpha = parse_color(r["color"])
        if col:
            f.color.rgb = col
        rPr = run._r.get_or_add_rPr()
        for tag, val in (("a:ea", self.cfg.font_ea), ("a:cs", self.cfg.font_latin)):
            el = rPr.find(qn(tag))
            if el is None:
                el = rPr.makeelement(qn(tag), {})
                rPr.append(el)
            el.set("typeface", val)
        if r.get("ls"):
            rPr.set("spc", str(int(round(r["ls"] * self.k * 100))))   # unit: 1/100 pt
        alpha *= r.get("op", 1)              # CSS opacity multiplied along the ancestor chain
        if col and alpha < 1:
            solid = rPr.find(qn("a:solidFill"))
            if solid is not None and solid.find(qn("a:srgbClr")) is not None:
                _alpha(solid.find(qn("a:srgbClr")), alpha)

    def add_text(self, slide, e):
        """One paragraph → one text box.

        Leave slack in the width: in visual drafts these boxes are often flex shrink-wrapped, exactly as wide as the text;
        moved to PowerPoint, the slightest difference in font metrics pushes the last character to the next line.
        For paragraphs that are single-line anyway, turn off word wrap so they can't possibly wrap.
        """
        k = self.k
        wrap = e.get("wrap", True)
        fs = e.get("fsMax") or e["fs"]     # the container's size is often a small inherited value; size the slack by the largest text
        pad = (fs * 0.25) if wrap else max(12.0, fs * 0.8)
        x, w = e["x"], e["w"] + pad
        ta = e.get("ta")
        if ta in ("center",):
            x -= pad / 2                   # a centered box widens on both sides, so the visual center stays put
        elif ta in ("right", "end"):
            x -= pad

        box = slide.shapes.add_textbox(Pt(x * k), Pt(e["y"] * k), Pt(w * k), Pt(e["h"] * k))
        tf = box.text_frame
        tf.word_wrap = wrap
        tf.auto_size = None
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        paras = [[]]
        for r in e["runs"]:
            paras.append([]) if r.get("br") else paras[-1].append(r)
        paras = [p for p in paras if p] or [[]]

        for i, runs in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = ALIGN.get(ta, PP_ALIGN.LEFT)
            # Set line spacing only on boxes where "this paragraph wraps by itself". Not on single-line paragraphs: the measured line box is taller
            # than the real line spacing (that's the font's line box, not the CSS line-height); using it as exact spacing pushes the whole text down;
            # for a single line, let PowerPoint lay it out naturally by font size, so the text hugs the top of the box and the position is most accurate.
            if e.get("lines", 1) > 1 and e.get("lhEff"):
                p.line_spacing = Pt(e["lhEff"] * k)
            for r in runs:
                run = p.add_run()
                run.text = r["t"]
                self.set_run_font(run, r)
        return box

    # ── Shapes ──────────────────────────────────────────────
    def add_shape(self, slide, e):
        k = self.k
        rounded = e.get("radius", 0) >= 4
        shp = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
            Pt(e["x"] * k), Pt(e["y"] * k), Pt(e["w"] * k), Pt(e["h"] * k))
        shp.shadow.inherit = False
        op = e.get("op", 1)                # CSS opacity multiplied along the ancestor chain
        col, alpha = parse_color(e.get("bg"))
        alpha *= op
        if col and alpha > 0:
            shp.fill.solid()
            shp.fill.fore_color.rgb = col
            if alpha < 1:
                sf = shp.fill._xPr.find(qn("a:solidFill"))
                _alpha(sf.find(qn("a:srgbClr")), alpha)
        else:
            shp.fill.background()

        bcol, balpha = parse_color(e.get("bdc"))
        balpha *= op
        if e.get("bdw", 0) > 0 and bcol and balpha > 0:
            shp.line.color.rgb = bcol
            if balpha < 1:
                ln = shp.line._get_or_add_ln().find(qn("a:solidFill"))
                _alpha(ln.find(qn("a:srgbClr")), balpha)
            shp.line.width = Pt(e["bdw"] * k)
        else:
            shp.line.fill.background()

        if e.get("rot"):
            shp.rotation = -e["rot"]       # in CSS counterclockwise is negative, in PowerPoint clockwise is positive
        if rounded and e["w"] and e["h"]:
            # PowerPoint corner radius is "a percentage of the short side"; convert back to a CSS px radius
            shp.adjustments[0] = min(0.5, e["radius"] / min(e["w"], e["h"]))
        return shp

    # ── Pictures ──────────────────────────────────────────────
    def round_corners(self, path, radius_px, box_w):
        """PowerPoint pictures have no corner radius, so bake it into the PNG's alpha channel."""
        os.makedirs(self.round_dir, exist_ok=True)
        out = os.path.join(self.round_dir, f"{abs(hash((path, radius_px, box_w))) % 10**10}.png")
        if os.path.exists(out):
            return out
        im = Image.open(path).convert("RGBA")
        scale = im.width / box_w if box_w else 1
        r = int(min(radius_px * scale, min(im.size) / 2))
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width - 1, im.height - 1],
                                               radius=r, fill=255)
        im.putalpha(mask)
        im.save(out)
        return out

    def add_img(self, slide, e):
        k = self.k
        src = e.get("file") or e["src"]
        if not src or src.startswith("data:"):
            return None
        path = src if os.path.isabs(src) else os.path.normpath(os.path.join(self.html_dir, src))
        if not os.path.exists(path):
            print(f"   ⚠️ Image not found {src}")
            return None
        if e.get("radius", 0) >= 2:
            path = self.round_corners(path, e["radius"], e["w"])
        pic = slide.shapes.add_picture(path, Pt(e["x"] * k), Pt(e["y"] * k),
                                       Pt(e["w"] * k), Pt(e["h"] * k))
        # box-shadow: rgba(...) 0 0 0 Npx in visual drafts is usually a hard border; translate it into a picture border
        m = re.match(r"rgba?\(([^)]+)\)\s+0px\s+0px\s+0px\s+([\d.]+)px", e.get("shadow") or "")
        if m:
            col, alpha = parse_color("rgba(" + m.group(1) + ")")
            if col and alpha > 0:
                pic.line.color.rgb = col
                pic.line.width = Pt(float(m.group(2)) * k)
        return pic

    # ── Assembly ──────────────────────────────────────────────
    def run(self, pages):
        cfg = self.cfg
        self.html_dir = os.path.dirname(os.path.abspath(cfg.html))

        if cfg.template:
            prs = Presentation(cfg.template)
            strip_slides(prs)                       # delete the template's sample slides; leave masters/layouts untouched
        else:
            prs = Presentation()
            pw, ph = pages[0]["w"], pages[0]["h"]
            prs.slide_width, prs.slide_height = Pt(pw), Pt(ph)   # 1 CSS px = 1 pt

        # Ratio of HTML canvas width → slide width. A 1920px canvas with 26.667in (=1920pt) gives exactly 1.0.
        self.k = (prs.slide_width / EMU_PER_PT) / pages[0]["w"]

        if cfg.layout:
            layout = next((l for l in prs.slide_layouts if l.name == cfg.layout), None)
            if layout is None:
                names = " / ".join(l.name for l in prs.slide_layouts)
                sys.exit(f"❌ The template has no layout '{cfg.layout}'. Options: {names}")
            killed = unblock_layout(layout, prs.slide_width, prs.slide_height)
        else:
            layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
            killed = []

        n_text = n_shape = n_img = 0
        for page in pages:
            slide = prs.slides.add_slide(layout)
            for sh in list(slide.shapes):           # empty placeholders brought by the layout don't stay on the slide
                sh._element.getparent().remove(sh._element)
            if cfg.bg:
                set_bg(slide, cfg.bg)
            for e in page["els"]:
                if cfg.skip_class and cfg.skip_class in (e.get("cls") or "").split():
                    continue
                if e["kind"] == "shape":
                    self.add_shape(slide, e); n_shape += 1
                elif e["kind"] == "text":
                    self.add_text(slide, e); n_text += 1
                else:
                    if self.add_img(slide, e) is not None:
                        n_img += 1

        prs.save(cfg.out)
        mb = os.path.getsize(cfg.out) / 1024 / 1024
        print(f"✅ {len(prs.slides)} slides → {os.path.basename(cfg.out)} ({mb:.1f}MB)")
        print(f"   text boxes {n_text} · shapes {n_shape} · pictures {n_img}"
              + (f" · layout masks cleared {killed}" if killed else ""))
        print(f"   canvas {prs.slide_width/914400:.3f}×{prs.slide_height/914400:.3f} inch"
              f" (scale {self.k:.4f})")


# ─────────────────────────────────────────────────────────────
# 2.5 Dropped-text check (reference = the browser's rendered innerText)
# ─────────────────────────────────────────────────────────────

def _norm(t):
    # Strip all whitespace and normalize case: innerText already has text-transform applied, while PPTX carries the legacy of source casing
    return re.sub(r"\s+", "", t or "").lower()


def verify_text(refs, pptx_path):
    """Page-by-page comparison: fragments present in the rendered innerText (refs[i]) but missing from the text boxes of PPTX slide i.

    Returns [[missing fragment, ...], ...], one list per slide; all empty = no dropped text.
    The reference must be independent of the extraction logic: compare against the --dump-json list and text dropped during extraction is missing on both sides,
    so it is bound to go undetected.
    """
    import difflib
    prs = Presentation(pptx_path)
    res = []
    for ref, slide in zip(refs, prs.slides):
        got = _norm("".join(sh.text_frame.text for sh in slide.shapes if sh.has_text_frame))
        want = _norm(ref)
        sm = difflib.SequenceMatcher(None, want, got, autojunk=False)
        res.append([want[i1:i2] for tag, i1, i2, _, _ in sm.get_opcodes()
                    if tag in ("delete", "replace")])
    return res


def report_missing(missing):
    n = sum(len(m) for m in missing)
    if not n:
        print("🔍 Dropped-text check: all rendered page text is in the PPTX, no text dropped")
        return
    print(f"⚠️ Dropped-text check: {n} pieces of text are visible in the browser but missing from the PPTX (compared with whitespace removed)")
    for pi, segs in enumerate(missing):
        for sg in segs:
            print(f"   slide {pi+1} missing: {sg[:60]}{'…' if len(sg) > 60 else ''}")
    print("   (elements skipped by --skip-class show up here, which is expected; investigate the rest)")


# ─────────────────────────────────────────────────────────────
# 3. Three small template surgeries
# ─────────────────────────────────────────────────────────────

def strip_slides(prs):
    """Delete the template's sample slides; masters, layouts, theme and palette stay untouched."""
    lst = prs.slides._sldIdLst
    for sld in list(lst):
        prs.part.drop_rel(sld.rId)
        lst.remove(sld)


def unblock_layout(layout, W, H):
    """Delete solid rectangles in a layout that cover the full screen.

    Some official templates have a full-screen rectangle in the layout with the same color and size as the layout background (a redundant mask).
    Left in place, anything placed beneath it on the slide is hidden; deleting it doesn't change how the layout looks.
    """
    killed = []
    for sp in list(layout.shapes):
        full = (sp.left == 0 and sp.top == 0 and sp.width and sp.height
                and sp.width >= W and sp.height >= H)
        if full and b"<a:solidFill>" in sp._element.xml.encode():
            sp._element.getparent().remove(sp._element)
            killed.append(sp.name)
    return killed


def set_bg(slide, rgb_hex):
    bg = slide._element.makeelement(qn("p:bg"), {})
    pr = slide._element.makeelement(qn("p:bgPr"), {})
    fill = slide._element.makeelement(qn("a:solidFill"), {})
    clr = slide._element.makeelement(qn("a:srgbClr"), {"val": rgb_hex.lstrip("#").upper()})
    fill.append(clr); pr.append(fill)
    pr.append(slide._element.makeelement(qn("a:effectLst"), {}))
    bg.append(pr)
    slide._element.find(qn("p:cSld")).insert(0, bg)


# ─────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Visual-draft HTML → editable PPTX (reads rendered coordinates, doesn't modify the HTML)")
    ap.add_argument("html")
    ap.add_argument("-o", "--out", required=True, help="output .pptx")
    ap.add_argument("--selector", default=".slide, .s, section",
                    help="CSS selector for each slide (default '.slide, .s, section')")
    ap.add_argument("--template", help="use this .pptx as the base, inheriting its masters/layouts/theme/palette")
    ap.add_argument("--layout", help="layout name applied to every slide (use with --template)")
    ap.add_argument("--skip-class", help="skip elements with this class, e.g. pass logo when the layout provides the logo")
    ap.add_argument("--font-latin", default="Microsoft YaHei", help="Latin font name")
    ap.add_argument("--font-ea", default="微软雅黑", help="East Asian font name")
    ap.add_argument("--bg", help="background color for every slide, e.g. 05070B; if omitted, the layout background is used")
    ap.add_argument("--asset-dir", help="where SVG/rounded images are written (default: _pptx_assets/ next to the output)")
    ap.add_argument("--scale", type=int, default=3, help="SVG capture scale (default 3)")
    ap.add_argument("--dump-json", help="write out the measured element list, for troubleshooting")
    cfg = ap.parse_args()

    cfg.out = os.path.abspath(cfg.out)
    cfg.asset_dir = cfg.asset_dir or os.path.join(os.path.dirname(cfg.out), "_pptx_assets")
    if cfg.layout and not cfg.template:
        sys.exit("❌ --layout must be used together with --template")

    pages = asyncio.run(render(cfg.html, cfg.selector, cfg.asset_dir, cfg.scale))
    if not pages:
        sys.exit(f"❌ Selector '{cfg.selector}' didn't match a single slide")
    if cfg.dump_json:
        json.dump(pages, open(cfg.dump_json, "w"), ensure_ascii=False, indent=1)

    kinds = {}
    for p in pages:
        for e in p["els"]:
            kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
    print(f"📐 Measured {len(pages)} slides  {kinds}")
    Builder(cfg).run(pages)
    report_missing(verify_text([p["ref"] for p in pages], cfg.out))


if __name__ == "__main__":
    main()
