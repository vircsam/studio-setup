"""
Example 02: Tegaki Handwriting Animation
Generates handwriting effects from real fonts using SVG stroke-dash dynamics.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hyperframes_py import Composition, HandwritingText, render_to_mp4

def create_tegaki_demo():
    comp = Composition(
        comp_id="tegaki_demo",
        duration=4.5,
        background="#0f172a",
        title="Tegaki Handwriting Animation"
    )

    hw = HandwritingText(
        text="Handwriting from Real Fonts",
        element_id="hw-title",
        font_size=82,
        color="#38bdf8",
        x=220,
        y=380
    )
    hw.set_timing(duration=2.6, start_time=0.6)

    comp.add_style(hw.render_css())
    comp.add_style("""
        .header-sub {
          position: absolute;
          left: 240px;
          top: 310px;
          font-family: monospace;
          color: #94a3b8;
          font-size: 24px;
          letter-spacing: 3px;
        }
        .footer-note {
          position: absolute;
          left: 240px;
          top: 600px;
          font-size: 26px;
          color: #64748b;
        }
    """)

    comp.add_html(f"""
        <div id="tegaki-sub" class="header-sub">TEGAKI × HYPERFRAMES</div>
        {hw.render_html()}
        <div id="tegaki-foot" class="footer-note">Organic SVG stroke-order choreography with zero raster artifacts.</div>
    """)

    comp.animate("""
        tl.from('#tegaki-sub', { opacity: 0, y: -15, duration: 0.6, ease: 'power2.out' }, 0.2);
    """)
    comp.animate(hw.render_gsap())
    comp.animate("""
        tl.from('#tegaki-foot', { opacity: 0, y: 15, duration: 0.8, ease: 'power2.out' }, 2.8);
    """)

    return comp

if __name__ == "__main__":
    comp = create_tegaki_demo()
    out = "renders/02_tegaki_handwriting.mp4"
    print(f"Rendering Tegaki demo to {out}...")
    res = render_to_mp4(comp, output_path=out, quality="draft")
    print("Result:", res)
