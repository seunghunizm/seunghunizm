"""Generates the light/dark SVG assets used by README.md.

Run from the repo root:  python assets/build.py
"""
from pathlib import Path

OUT = Path(__file__).parent / "v2"  # bump the folder when assets change, so GitHub drops cached images
W = 830  # GitHub README content width

SERIF = "'Iowan Old Style','Charter','Georgia','Times New Roman',serif"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif"

THEMES = {
    "light": dict(
        panel="#FAFAF8", card="#FFFFFF", muted="#F3F2EE",
        line="rgba(20,20,20,0.08)", line2="rgba(20,20,20,0.18)",
        ink="#141414", body="#4A4A46", meta="#7A7871", faint="#B8B6AE",
        pill="#141414", pill_ink="#FFFFFF", chip="#FFFFFF", chip_ink="#141414",
        mark="rgba(20,20,20,0.05)",
    ),
    "dark": dict(
        panel="#151B23", card="#0D1117", muted="#1C232D",
        line="rgba(240,246,252,0.10)", line2="rgba(240,246,252,0.24)",
        ink="#F2F1ED", body="#B9B7B0", meta="#8D8B85", faint="#4B525C",
        pill="#F2F1ED", pill_ink="#0D1117", chip="#0D1117", chip_ink="#F2F1ED",
        mark="rgba(240,246,252,0.07)",
    ),
}

BASE_CSS = f"""
.serif{{font-family:{SERIF}}}
.sans{{font-family:{SANS}}}
.eyebrow{{font-family:{SANS};font-size:11px;font-weight:600;letter-spacing:2.6px}}
.rise{{opacity:0;animation:rise .9s cubic-bezier(.2,.7,.2,1) forwards}}
@keyframes rise{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;opacity:1!important;stroke-dashoffset:0!important}}}}
"""


def svg(w, h, title, body, extra_css=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{title}">\n'
        f"<title>{title}</title>\n<style>{BASE_CSS}{extra_css}</style>\n{body}\n</svg>\n"
    )


def delay(s):
    return f'style="animation-delay:{s}s"'


# ---------------------------------------------------------------- header
def header(t):
    h = 300
    # A design-tool selection frame that draws itself around the name.
    bx, by, bw, bh = 52, 96, 516, 96
    per = 2 * (bw + bh)
    handles = "".join(
        f'<rect class="handle" x="{x-4}" y="{y-4}" width="8" height="8" fill="{t["card"]}" '
        f'stroke="{t["ink"]}" stroke-width="1.2" style="animation-delay:{1.25 + i*0.06:.2f}s"/>'
        for i, (x, y) in enumerate([(bx, by), (bx + bw, by), (bx + bw, by + bh), (bx, by + bh)])
    )
    css = (
        f".frame{{stroke-dasharray:{per};stroke-dashoffset:{per};animation:draw 1.1s cubic-bezier(.6,0,.2,1) .45s forwards}}"
        "@keyframes draw{to{stroke-dashoffset:0}}"
        ".handle{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .35s cubic-bezier(.2,.9,.3,1.4) forwards}"
        "@keyframes pop{from{opacity:0;transform:scale(.2)}to{opacity:1;transform:scale(1)}}"
        ".caret{animation:blink 1.1s steps(1) 2s infinite;opacity:0}"
        "@keyframes blink{0%{opacity:1}50%{opacity:0}}"
        ".dim{opacity:0;animation:fadein .6s ease 1.5s forwards}"
        "@keyframes fadein{to{opacity:1}}"
    )
    body = f"""
<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="28" fill="{t['panel']}" stroke="{t['line']}"/>

<g class="rise" {delay(0.05)}>
  <circle cx="56" cy="58" r="3.5" fill="{t['ink']}"/>
  <text x="68" y="62" class="eyebrow" fill="{t['meta']}">SEUNGHUNIZM</text>
</g>
<text x="{W-52}" y="62" text-anchor="end" class="eyebrow rise" {delay(0.1)} fill="{t['faint']}">UI / UX · FRONT-END</text>

<rect class="frame" x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="none" stroke="{t['line2']}" stroke-width="1"/>
{handles}
<g class="dim">
  <rect x="{bx}" y="{by-26}" width="66" height="18" rx="4" fill="{t['ink']}"/>
  <text x="{bx+33}" y="{by-13}" text-anchor="middle" class="sans" font-size="10.5" font-weight="600" fill="{t['card']}">516 × 96</text>
</g>
<text x="70" y="164" class="serif rise" {delay(0.15)} font-size="62" font-weight="700" fill="{t['ink']}" letter-spacing="-1.2">Seung Hun Lee</text>

<text x="54" y="240" class="sans rise" {delay(0.3)} font-size="21" fill="{t['body']}">UI/UX Designer <tspan fill="{t['faint']}">&amp;</tspan> Front-end Developer</text>
<rect class="caret" x="424" y="222" width="2" height="23" fill="{t['ink']}"/>
"""
    return svg(W, h, "Seung Hun Lee — UI/UX Designer &amp; Front-end Developer", body, css)


# ---------------------------------------------------------------- section label
def label(t, num, text):
    h = 44
    body = f"""
<text x="0" y="28" class="sans" font-size="13" font-weight="600" fill="{t['meta']}" letter-spacing="1">{num}</text>
<line x1="30" y1="23.5" x2="58" y2="23.5" stroke="{t['line2']}"/>
<text x="70" y="28" class="eyebrow" fill="{t['ink']}" font-size="12">{text}</text>
<line x1="{70 + len(text) * 10.2 + 18:.0f}" y1="23.5" x2="{W}" y2="23.5" stroke="{t['line']}"/>
"""
    return svg(W, h, text.title(), body)


# ---------------------------------------------------------------- focus cards
def wrap(lines, x, y, size, fill, lh):
    return "".join(
        f'<text x="{x}" y="{y + i * lh}" class="sans" font-size="{size}" fill="{fill}">{ln}</text>'
        for i, ln in enumerate(lines)
    )


def focus(t):
    h = 268
    gap = 14
    lw = 452
    rw = W - lw - gap
    sh = (h - gap) / 2
    rx = lw + gap

    def chips(x, y):
        out, cx = [], x
        for word in ("Layout", "Typography", "Motion", "Prototyping"):
            w = len(word) * 7.4 + 26
            out.append(f'<rect x="{cx}" y="{y}" width="{w:.0f}" height="28" rx="14" fill="{t["muted"]}"/>'
                       f'<text x="{cx + w/2:.0f}" y="{y+18.5}" text-anchor="middle" class="sans" font-size="12.5" fill="{t["body"]}">{word}</text>')
            cx += w + 8
        return "".join(out)

    def card(x, y, w, hh, num, title, lines, big=False, d=0.0):
        tsize = 30 if big else 21
        body_y = y + (128 if big else 104)
        return f"""
<g class="rise" {delay(d)}>
  <rect x="{x+0.5}" y="{y+0.5}" width="{w-1}" height="{hh-1}" rx="20" fill="{t['card']}" stroke="{t['line']}"/>
  <rect x="{x+24}" y="{y+24}" width="34" height="22" rx="11" fill="{t['ink'] if big else t['muted']}"/>
  <text x="{x+41}" y="{y+39.5}" text-anchor="middle" class="sans" font-size="11" font-weight="700" fill="{t['card'] if big else t['meta']}">{num}</text>
  <text x="{x+24}" y="{y + (96 if big else 80)}" class="serif" font-size="{tsize}" font-weight="700" fill="{t['ink']}" letter-spacing="-.3">{title}</text>
  {wrap(lines, x + 24, body_y, 15 if big else 14, t['body'], 22 if big else 20)}
  {chips(x + 24, y + hh - 50) if big else ""}
</g>"""

    body = (
        card(0, 0, lw, h, "01", "Interface design",
             ["Clean layouts, considered type, and",
              "motion that feels quiet and deliberate —",
              "from the first sketch to the shipped pixel."], big=True, d=0.05)
        + card(rx, 0, rw, sh, "02", "Front-end engineering",
               ["Semantic HTML, modern CSS, JS / TS &amp; React."], d=0.18)
        + card(rx, sh + gap, rw, sh, "03", "Engineering depth",
               ["C / C++, graphics, ML and systems groundwork."], d=0.3)
    )
    return svg(W, h, "Focus areas", body)


# ---------------------------------------------------------------- contact pill
def pill(t):
    w, h = 214, 52
    body = f"""
<rect x="0" y="0" width="{w}" height="{h}" rx="26" fill="{t['pill']}"/>
<text x="26" y="31.5" class="sans" font-size="15" font-weight="600" fill="{t['pill_ink']}">Get in touch</text>
<circle cx="{w-27}" cy="26" r="17" fill="{t['chip']}"/>
<path d="M{w-33} 32 L{w-21} 20 M{w-30} 20 L{w-21} 20 L{w-21} 29" stroke="{t['chip_ink']}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
"""
    return svg(w, h, "Get in touch", body)


# ---------------------------------------------------------------- footer
def footer(t):
    h = 210
    body = f"""
<defs><clipPath id="c"><rect x="0" y="0" width="{W}" height="{h}"/></clipPath></defs>
<line x1="0" y1="0.5" x2="{W}" y2="0.5" stroke="{t['line']}"/>
<text x="0" y="38" class="eyebrow" fill="{t['faint']}">© 2026 SEUNG HUN LEE</text>
<text x="{W}" y="38" text-anchor="end" class="eyebrow" fill="{t['faint']}">UI / UX · FRONT-END</text>
<g clip-path="url(#c)">
  <text x="{W/2}" y="214" text-anchor="middle" class="serif" font-size="132" font-weight="700" fill="{t['mark']}" letter-spacing="-3" textLength="{W+20}" lengthAdjust="spacingAndGlyphs">SEUNGHUNIZM</text>
</g>
"""
    return svg(W, h, "Footer", body)


def main():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    sections = [("01", "FOCUS"), ("02", "STACK"), ("03", "CONTACT")]
    for name, t in THEMES.items():
        files = {
            f"header-{name}.svg": header(t),
            f"focus-{name}.svg": focus(t),
            f"contact-{name}.svg": pill(t),
            f"footer-{name}.svg": footer(t),
        }
        for num, text in sections:
            files[f"label-{text.lower()}-{name}.svg"] = label(t, num, text)
        for fn, content in files.items():
            (OUT / fn).write_text(content, encoding="utf-8", newline="\n")
            print("wrote", fn)


if __name__ == "__main__":
    main()
