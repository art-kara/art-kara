#!/usr/bin/env python3
"""Render the profile card with Python's standard library.

Edit profile.json or assets/portrait.txt, then run python3 scripts/render_profile.py.
The generated SVGs contain no scripts, remote resources, or embedded photographs.
"""

from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT / "profile.json").read_text())
PORTRAIT = (ROOT / "assets/portrait.txt").read_text().splitlines()

THEMES = {
    "dark": {
        "canvas": "#0b111c", "panel": "#101c2d", "line": "#263750",
        "text": "#e8f1ff", "muted": "#99abc5", "accent": "#73b7ff",
        "portrait": "#c4e0ff", "positive": "#7dd3ad", "faint": "#537190",
    },
    "light": {
        "canvas": "#f9fbff", "panel": "#edf4fd", "line": "#c7d8ee",
        "text": "#142a46", "muted": "#526c8c", "accent": "#1f65bc",
        "portrait": "#244a78", "positive": "#257357", "faint": "#7c96b4",
    },
}


def render(theme):
    c = THEMES[theme]
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="720" viewBox="0 0 1120 720" role="img" aria-labelledby="title desc">
  <title id="title">{escape(PROFILE['name'])} — @{escape(PROFILE['handle'])}</title>
  <desc id="desc">Founder, full-stack engineer, and product builder. Building Runtools AI and Sendblue. An ASCII portrait with work, tools, and milestones.</desc>
  <defs>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{c['accent']}" stroke-width="0.5" opacity="0.055"/></pattern>
    <clipPath id="portrait-clip"><rect x="36" y="130" width="350" height="364" rx="4"/></clipPath>
    <style>
      text {{ font-family: "DejaVu Sans Mono", "SFMono-Regular", Consolas, "Liberation Mono", monospace; }}
      .micro {{ font-size: 11px; letter-spacing: 1px; }}
      .body {{ font-size: 15px; }}
      .prompt {{ font-size: 14px; font-weight: 600; }}
      .name {{ font-family: "DejaVu Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; font-size: 37px; font-weight: 700; letter-spacing: -1px; }}
      .ascii {{ font-size: 9px; white-space: pre; font-weight: 500; }}
    </style>
  </defs>
  <rect x="8" y="8" width="1104" height="704" rx="16" fill="{c['canvas']}" stroke="{c['line']}"/>
  <rect x="8" y="8" width="1104" height="704" rx="16" fill="url(#grid)"/>
  <path d="M9 58H1111" stroke="{c['line']}"/>
  <circle cx="33" cy="33" r="5" fill="#ef7b79"/>
  <circle cx="52" cy="33" r="5" fill="#e5bd68"/>
  <circle cx="71" cy="33" r="5" fill="#78c6a3"/>
  <text x="97" y="37" class="micro" fill="{c['muted']}">~/people/{escape(PROFILE['handle'])}</text>
  <text x="1086" y="37" text-anchor="end" class="micro" fill="{c['muted']}">PROFILE / 01</text>
  <rect x="24" y="78" width="378" height="542" rx="10" fill="{c['panel']}" stroke="{c['line']}"/>
  <text x="43" y="108" class="micro" fill="{c['accent']}">PORTRAIT.TXT</text>
  <text x="382" y="108" text-anchor="end" class="micro" fill="{c['muted']}">64 × 36</text>
  <g clip-path="url(#portrait-clip)" fill="{c['portrait']}" class="ascii" xml:space="preserve">''']
    for i, row in enumerate(PORTRAIT):
        parts.append(f'<text x="40" y="{145 + i * 9.5:.1f}">{escape(row)}</text>')
    parts.append(f'''</g>
  <path d="M43 511H383" stroke="{c['line']}"/>
  <text x="43" y="543" class="prompt" fill="{c['accent']}">$ human --full-stack</text>
  <text x="43" y="571" class="body" fill="{c['muted']}">Curiosity in. Products out.</text>
  <circle cx="47" cy="596" r="3" fill="{c['positive']}"/>
  <text x="59" y="600" class="micro" fill="{c['muted']}">ALWAYS BUILDING</text>

  <text x="438" y="103" class="prompt" fill="{c['accent']}">art@kara:~$ whoami</text>
  <text x="438" y="150" class="name" fill="{c['text']}">{escape(PROFILE['name'])}</text>
  <text x="438" y="180" font-size="13" fill="{c['muted']}">{escape(PROFILE['headline'])}</text>
  <path d="M438 199H1084" stroke="{c['line']}"/>
  <text x="438" y="229" class="body" fill="{c['text']}">{escape(PROFILE['intro'][0])}</text>
  <text x="438" y="252" class="body" fill="{c['muted']}">{escape(PROFILE['intro'][1])}</text>
  <text x="438" y="293" class="prompt" fill="{c['accent']}">$ cat work.log</text>''')
    for i, (label, value) in enumerate(PROFILE['work']):
        y = 326 + i * 29
        parts.append(f'<text x="438" y="{y}" class="body" fill="{c["muted"]}">{escape(label)}</text>')
        parts.append(f'<text x="552" y="{y}" class="body" fill="{c["faint"]}">→</text>')
        parts.append(f'<text x="583" y="{y}" font-size="14" fill="{c["text"]}">{escape(value)}</text>')
    parts.append(f'<text x="438" y="455" class="prompt" fill="{c["accent"]}">$ stack --whatever-it-takes</text>')
    x = 438
    for label in PROFILE['stack']:
        width = len(label) * 8 + 24
        parts.append(f'<rect x="{x}" y="470" width="{width}" height="32" rx="5" fill="{c["panel"]}" stroke="{c["line"]}"/>')
        parts.append(f'<text x="{x + width / 2}" y="491" text-anchor="middle" font-size="13" fill="{c["text"]}">{escape(label)}</text>')
        x += width + 9
    parts.append(f'<text x="438" y="544" class="prompt" fill="{c["accent"]}">$ cat principles.md</text>')
    for i, (label, x) in enumerate(zip(PROFILE['principles'], [438, 632, 877])):
        parts.append(f'<text x="{x}" y="579" font-size="12" fill="{c["muted"]}"><tspan fill="{c["accent"]}">0{i + 1}</tspan> {escape(label)}</text>')
    parts.append(f'<path d="M438 610H1084" stroke="{c["line"]}"/>')
    parts.append(f'<text x="438" y="641" font-size="13" fill="{c["accent"]}">artkara.co</text>')
    parts.append(f'<text x="1084" y="641" text-anchor="end" font-size="13" fill="{c["muted"]}">@artkara_</text>')
    parts.append(f'<path d="M24 659H1096" stroke="{c["line"]}"/>')
    for (number, label), x in zip(PROFILE['milestones'], [44, 400, 756]):
        parts.append(f'<text x="{x}" y="691" font-size="20" font-weight="700" fill="{c["text"]}">{escape(number)}</text>')
        parts.append(f'<text x="{x + 106}" y="689" font-size="10" letter-spacing="0.5" fill="{c["muted"]}">{escape(label)}</text>')
    parts.append('</svg>\n')
    return '\n'.join(parts)


for theme in THEMES:
    (ROOT / f'{theme}_mode.svg').write_text(render(theme))

alt = 'Artur Karapetian — founder, full-stack engineer, and product builder. Building Runtools AI and Sendblue.'
links = ' &nbsp;·&nbsp; '.join(f'<a href="{escape(url, quote=True)}">{escape(label)}</a>' for label, url in PROFILE['links'])
(ROOT / 'README.md').write_text(f'''<a href="{PROFILE['website']}">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/art-kara/art-kara/main/dark_mode.svg">
    <img src="https://raw.githubusercontent.com/art-kara/art-kara/main/light_mode.svg" width="100%" alt="{alt}">
  </picture>
</a>

<p align="center">
  {links}
</p>

<!-- Edit profile.json, then run python3 scripts/render_profile.py. -->
''')
print('Rendered README.md, dark_mode.svg, light_mode.svg')
