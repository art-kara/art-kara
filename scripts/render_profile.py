#!/usr/bin/env python3
"""Write the profile README. Edit profile.json, then run this script."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = json.loads((ROOT / 'profile.json').read_text())
links = ' · '.join(f'[{label}]({url})' for label,url in p['links'])
highlights = '\n'.join(f'- {s}' for s in p['highlights'])
projects = '\n'.join(f'| **[{name}]({url})** | {description} |' for name,url,description in p['projects'])
stack = ' · '.join(f'`{item}`' for item in p['stack'])
(ROOT / 'README.md').write_text(f'''<img align="left" width="210" height="210" src="https://raw.githubusercontent.com/art-kara/art-kara/main/assets/builder-dark.gif?v=2#gh-dark-mode-only" alt="A little 3D robot in sunglasses, turning and waving.">
<img align="left" width="210" height="210" src="https://raw.githubusercontent.com/art-kara/art-kara/main/assets/builder-light.gif?v=2#gh-light-mode-only" alt="A little 3D robot in sunglasses, turning and waving.">

### {p['name']}

{p['intro']}

{p['current']}

{links}

<br clear="all">

#### A few highlights

{highlights}

#### Things I've worked on

| Project | Work |
| :--- | :--- |
{projects}

{stack}

<!-- Content: profile.json → python3 scripts/render_profile.py -->
<!-- Animation: python3 scripts/render_robot.py (numpy + Pillow) -->
''')
print('Wrote README.md')
