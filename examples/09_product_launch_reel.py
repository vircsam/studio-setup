"""
Example 09: Product Launch Motion Reel
Inspired by AbubakrChan/product-launch-motion (cursor path, continuous motion, cue checks).
Dribbble-level product launch trailer with dynamic cursor choreography.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hyperframes_py import Composition, CursorChoreography, render_to_mp4

def create_product_launch_demo():
    comp = Composition(
        comp_id="product_launch_demo",
        duration=5.0,
        background="#0a0a0c",
        title="Product Launch Trailer"
    )

    cursor = CursorChoreography("hero-cursor")
    # Cursor starts offscreen, moves to primary CTA button, clicks, and moves away
    cursor.move_to(x=600, y=450, duration=1.2, at=0.5, click=False)
    cursor.move_to(x=960, y=560, duration=0.8, at=1.8, click=True)
    cursor.move_to(x=1300, y=620, duration=1.0, at=3.0, click=False)

    comp.add_style(cursor.render_css())
    comp.add_style("""
        .pl-wrapper {
          position: absolute;
          inset: 0;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          text-align: center;
        }
        .pl-eyebrow {
          font-family: monospace;
          color: #38bdf8;
          font-size: 22px;
          letter-spacing: 4px;
          margin-bottom: 20px;
        }
        .pl-headline {
          font-size: 88px;
          font-weight: 900;
          letter-spacing: -0.04em;
          color: #ffffff;
          margin: 0 0 24px 0;
          line-height: 1.05;
        }
        .pl-headline span {
          background: linear-gradient(135deg, #38bdf8, #818cf8);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        .pl-cta-btn {
          margin-top: 40px;
          background: #ffffff;
          color: #090d16;
          font-size: 24px;
          font-weight: 700;
          padding: 22px 56px;
          border-radius: 999px;
          box-shadow: 0 10px 40px rgba(56, 189, 248, 0.4);
          cursor: pointer;
          transform-origin: 50% 50%;
        }
        /* Film grain overlay */
        .film-grain {
          position: absolute;
          inset: 0;
          opacity: 0.05;
          pointer-events: none;
          background-image: radial-gradient(#fff 1px, transparent 1px);
          background-size: 4px 4px;
        }
    """)

    comp.add_html(f"""
        <div class="film-grain"></div>
        <div class="pl-wrapper">
          <div id="pl-eye" class="pl-eyebrow">PRODUCT LAUNCH MOTION / CONTINUOUS FLOW</div>
          <h1 id="pl-h1" class="pl-headline">Turn Code Into <span>Cinematic Motion</span></h1>
          <div id="pl-btn" class="pl-cta-btn">Start Creating Now →</div>
        </div>
        {cursor.render_html()}
    """)

    comp.animate("""
        tl.from('#pl-eye', { opacity: 0, y: -20, duration: 0.6, ease: 'power2.out' }, 0.2);
        tl.from('#pl-h1', { opacity: 0, y: 40, duration: 0.9, ease: 'power3.out' }, 0.4);
        tl.from('#pl-btn', { opacity: 0, scale: 0.8, duration: 0.6, ease: 'back.out(2)' }, 0.8);
        
        // Button press reactive effect on cursor click at 2.6s
        tl.to('#pl-btn', { scale: 0.94, duration: 0.1, yoyo: true, repeat: 1, ease: 'power2.in' }, 2.6);
        tl.to('#pl-btn', { boxShadow: '0 0 60px rgba(56, 189, 248, 0.8)', duration: 0.3, yoyo: true, repeat: 1 }, 2.6);
    """)
    comp.animate(cursor.render_gsap())

    return comp

if __name__ == "__main__":
    comp = create_product_launch_demo()
    out = "renders/09_product_launch.mp4"
    print(f"Rendering Product Launch demo to {out}...")
    res = render_to_mp4(comp, output_path=out, quality="draft")
    print("Result:", res)
