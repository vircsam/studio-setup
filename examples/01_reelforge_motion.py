"""
Example 01: ReelForge Motion Fragments
Render-tested typography and scene choreography.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hyperframes_py import Composition, Scene, render_to_mp4

def create_reelforge_demo():
    comp = Composition(
        comp_id="reelforge_demo",
        duration=4.0,
        background="#0a0a0c",
        title="ReelForge Motion Fragment"
    )

    comp.add_style("""
        .rf-container {
          position: absolute;
          inset: 0;
          display: flex;
          flex-direction: column;
          justify-content: center;
          padding: 120px 160px;
        }
        .rf-tag {
          font-family: monospace;
          color: #f43f5e;
          font-size: 26px;
          letter-spacing: 4px;
          font-weight: 700;
        }
        .rf-hero {
          font-size: 96px;
          font-weight: 900;
          line-height: 1.05;
          letter-spacing: -0.04em;
          margin: 30px 0;
          background: linear-gradient(135deg, #ffffff 30%, #94a3b8);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        .rf-sub {
          font-size: 32px;
          color: #94a3b8;
          max-width: 900px;
        }
        .rf-badge {
          display: inline-flex;
          align-items: center;
          gap: 12px;
          background: #18181b;
          border: 1px solid #27272a;
          padding: 14px 28px;
          border-radius: 999px;
          font-size: 22px;
          color: #e4e4e7;
          width: fit-content;
          margin-top: 40px;
        }
    """)

    comp.add_html("""
        <div class="rf-container">
          <div id="rf-tag" class="rf-tag">REELFORGE / MOTION FRAGMENT #01</div>
          <h1 id="rf-hero" class="rf-hero">Render-Tested.<br>Deterministic Video.</h1>
          <p id="rf-sub" class="rf-sub">Automated multi-hook generation designed for coding agents.</p>
          <div id="rf-badge" class="rf-badge"><span>⚡</span> Verified Frame-by-Frame</div>
        </div>
    """)

    comp.animate("""
        tl.from('#rf-tag', { opacity: 0, y: -20, duration: 0.6, ease: 'power2.out' }, 0.2);
        tl.from('#rf-hero', { opacity: 0, y: 40, duration: 0.9, ease: 'power3.out' }, 0.4);
        tl.from('#rf-sub', { opacity: 0, y: 20, duration: 0.7, ease: 'power2.out' }, 0.8);
        tl.from('#rf-badge', { opacity: 0, scale: 0.85, duration: 0.6, ease: 'back.out(1.8)' }, 1.2);
    """)

    return comp

if __name__ == "__main__":
    comp = create_reelforge_demo()
    out = "renders/01_reelforge.mp4"
    print(f"Rendering ReelForge demo to {out}...")
    res = render_to_mp4(comp, output_path=out, quality="draft")
    print("Result:", res)
