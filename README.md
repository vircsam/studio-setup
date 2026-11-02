# HyperFrames Video Studio & 10 Extension Ecosystem

An agent-native, deterministic HTML/CSS/GSAP-to-MP4 video production suite powered by **HeyGen's HyperFrames**, integrated with **10 elite open-source motion extensions**, featuring a **pure Python animation framework** (`hyperframes_py`) and a modern **web-based Studio Interface**.

---

## 🚀 Quick Start

### 1. Launch the HyperFrames Studio Web Interface
Start the visual editor, preview canvas, and extension hub:
```bash
python3 server.py 8080
# or
npm run studio
```
Then open: **`http://localhost:8080`**

### 2. Run Python Animations & Render to MP4
Generate and render any of the pre-built animations directly from Python:
```bash
# Example: 07 Motion Library (Bar chart growth & counters)
python3 examples/07_motion_charts.py

# Example: 02 Tegaki (Vector handwriting animation)
python3 examples/02_tegaki_handwriting.py

# Example: 09 Product Launch (Continuous flow, film grain & cursor choreography)
python3 examples/09_product_launch_reel.py
```
Rendered videos will appear in `./renders/*.mp4`.

---

## 📦 The 10 Extensions Ecosystem

All 10 companion repositories are cloned and indexed in `./extensions/`:

| # | Repository | Core Capability | Python Example |
|---|---|---|---|
| **01** | [`gongnyang/reelforge`](https://github.com/gongnyang/reelforge) | Render-tested motion fragments, multi-hook generation, automated audio ducking | `examples/01_reelforge_motion.py` |
| **02** | [`gkurt/tegaki`](https://github.com/gkurt/tegaki) | Handwriting animation from real fonts via SVG stroke orders and dashoffset | `examples/02_tegaki_handwriting.py` |
| **03** | [`omkamal/animated-diagrams-skill`](https://github.com/omkamal/animated-diagrams-skill) | Diagrams that draw themselves, auto-wiring SVG bezier connectors, pulsing data | `examples/03_animated_diagram.py` |
| **04** | [`AgentsORG/design-engineering`](https://github.com/AgentsORG/design-engineering) | Sound derived from motion (size → pitch, position → pan, contact frame sync) | `examples/04_design_engineering_sound.py` |
| **05** | [`alchaincyf/huashu-design`](https://github.com/alchaincyf/huashu-design) | Seek-safe 3D camera rig governed by logarithmic durations & comfort budgets | `examples/05_huashu_camera_rig.py` |
| **06** | [`nateherkai/hyperframes-student-kit`](https://github.com/nateherkai/hyperframes-student-kit) | Card templates, 9:16 vertical shorts, transcript-aligned dead air cutting | `examples/06_student_kit_card.py` |
| **07** | [`nutllwhy/hyperframes-motion-library`](https://github.com/nutllwhy/hyperframes-motion-library) | 23 production-ready templates: bar chart growth, metrics count-up, explainers | `examples/07_motion_charts.py` |
| **08** | [`tugrawork-creator/saas-motion-kit`](https://github.com/tugrawork-creator/saas-motion-kit) | Six distinct styles (Bento, Minimal, Kinetic, Neo-brutalist, Elegant, Playful) | `examples/08_saas_showcase.py` |
| **09** | [`AbubakrChan/product-launch-motion`](https://github.com/AbubakrChan/product-launch-motion) | Continuous motion flow ("never cut"), cursor paths, click ripples, film grain | `examples/09_product_launch_reel.py` |
| **10** | [`openai/plugins`](https://github.com/openai/plugins) | Official HeyGen HyperFrames Codex skills for autonomous coding agents | `examples/10_codex_heygen_skill.py` |

---

## 🐍 Python Animation Framework (`hyperframes_py`)

Author deterministic video compositions in pure Python:

```python
from hyperframes_py import Composition, BarChartGrow, CameraRig, render_to_mp4

# 1. Create Composition
comp = Composition(comp_id="promo", duration=4.5, background="#0a0f1d")

# 2. Add Seek-Safe Camera Rig
cam = CameraRig("cam")
cam.push_in(target_selector=".chart-wrapper", scale=1.35, duration=2.2, at=0.5)
comp.set_camera_rig(cam)

# 3. Add Motion Components
chart = BarChartGrow(title="Revenue Growth (ARR)")
chart.add_bar("Q1", 30, color="#60a5fa", prefix="$", suffix="M")
chart.add_bar("Q2", 55, color="#38bdf8", prefix="$", suffix="M")
chart.add_bar("Q3", 85, color="#34d399", prefix="$", suffix="M")

comp.add_style(chart.render_css())
comp.add_html(chart.render_html())
comp.animate(chart.render_gsap())

# 4. Render directly to MP4 via Headless Chrome
result = render_to_mp4(comp, output_path="renders/promo.mp4", quality="medium")
print("Rendered:", result["output_file"], result["size_mb"], "MB")
```

---

## 🖥️ Studio Web Interface Features

1. **Extensions Hub**: Direct access to all 10 repositories, their documentation, templates, and one-click code presets.
2. **Interactive Video Canvas**: Frame-accurate scrubber, real-time playback, loop, frame stepping, and timecode tracker.
3. **Python Animation Editor**: In-browser live editor with one-click **"Run Python Animation"** execution.
4. **Compiled Inspector**: Toggle between Python source and compiled HyperFrames HTML/CSS/GSAP.
5. **Render Engine**: One-click MP4 export using local Headless Chrome with hardware acceleration.
6. **Video Gallery**: Instant preview, playback, and download of all exported MP4 files.

---

## 📂 Project Structure

```
hyper-frame/
├── extensions/                 # 10 cloned companion repositories & skills
│   ├── reelforge/
│   ├── tegaki/
│   ├── animated-diagrams-skill/
│   ├── design-engineering/
│   ├── huashu-design/
│   ├── hyperframes-student-kit/
│   ├── hyperframes-motion-library/
│   ├── saas-motion-kit/
│   ├── product-launch-motion/
│   └── plugins/
├── hyperframes_py/             # Python animation SDK
│   ├── composition.py          # Stage, scenes, timeline manager
│   ├── camera.py               # Huashu seek-safe 3D camera rig
│   ├── handwriting.py          # Tegaki vector handwriting engine
│   ├── diagrams.py             # Self-drawing architecture diagrams
│   ├── sound.py                # Sound derived from motion synthesizer
│   ├── saas.py                 # Bento grids, SaaS cards, cursor pathing
│   ├── motion_library.py       # Bar charts, counter metrics
│   └── renderer.py             # MP4 render runner & preview server
├── examples/                   # 10 Python runnable demos
│   ├── 01_reelforge_motion.py
│   ├── 02_tegaki_handwriting.py
│   ├── 03_animated_diagram.py
│   ├── 04_design_engineering_sound.py
│   ├── 05_huashu_camera_rig.py
│   ├── 06_student_kit_card.py
│   ├── 07_motion_charts.py
│   ├── 08_saas_showcase.py
│   ├── 09_product_launch_reel.py
│   └── 10_codex_heygen_skill.py
├── studio/                     # Web UI frontend
│   └── index.html
├── renders/                    # Rendered MP4 video outputs
├── extensions_registry.json    # Metadata registry of all 10 extensions
├── server.py                   # Python Studio server (Port 8080)
└── package.json
```
