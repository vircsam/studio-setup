"""
Example 08: SaaS Motion Kit Showcase
Inspired by tugrawork-creator/saas-motion-kit (six styles: Minimal, Bento, Kinetic, Neo-brutalist, Elegant, Playful).
Demonstrating Bento style feature grid.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hyperframes_py import Composition, BentoGrid, SaaSCard, render_to_mp4

def create_saas_demo():
    comp = Composition(
        comp_id="saas_demo",
        duration=4.5,
        background="#090d16",
        title="SaaS Motion Kit Bento Grid"
    )

    grid = BentoGrid("bento-features")
    grid.add_card(SaaSCard("card-1", "AI Video Pipeline", "Write clean HTML, CSS, and GSAP. HyperFrames outputs deterministic MP4s.", tag="ARCHITECTURE", icon="⚡", width=480, height=340, x=180, y=260, style="bento"))
    grid.add_card(SaaSCard("card-2", "Six Motion Styles", "Curated tone matrices preventing creative repetition across product promos.", tag="VARIETY AUDIT", icon="🎨", width=480, height=340, x=700, y=260, style="bento"))
    grid.add_card(SaaSCard("card-3", "Headless Chrome", "Zero wall-clock drift, frame-accurate seeking, and flawless audio sync.", tag="CORE ENGINE", icon="🚀", width=480, height=340, x=1220, y=260, style="bento"))

    comp.add_style(grid.render_css())
    comp.add_style("""
        .saas-header {
          position: absolute;
          left: 180px;
          top: 110px;
        }
        .saas-tag {
          font-family: monospace;
          color: #38bdf8;
          font-size: 20px;
          letter-spacing: 3px;
          font-weight: 700;
        }
        .saas-title {
          font-size: 52px;
          font-weight: 800;
          letter-spacing: -0.02em;
          color: #ffffff;
          margin: 8px 0 0 0;
        }
    """)

    comp.add_html(f"""
        <div class="saas-header">
          <div id="saas-tag" class="saas-tag">SAAS-MOTION-KIT / BENTO STYLE</div>
          <h1 id="saas-title" class="saas-title">Built for Modern Product Launches</h1>
        </div>
        {grid.render_html()}
    """)

    comp.animate("""
        tl.from('#saas-tag', { opacity: 0, y: -10, duration: 0.5, ease: 'power2.out' }, 0.1);
        tl.from('#saas-title', { opacity: 0, y: 20, duration: 0.7, ease: 'power3.out' }, 0.2);
    """)
    comp.animate(grid.render_gsap(start_time=0.5, stagger=0.18))

    return comp

if __name__ == "__main__":
    comp = create_saas_demo()
    out = "renders/08_saas_showcase.mp4"
    print(f"Rendering SaaS Showcase demo to {out}...")
    res = render_to_mp4(comp, output_path=out, quality="draft")
    print("Result:", res)
