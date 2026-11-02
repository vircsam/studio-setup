"""
Example 10: HeyGen Official HyperFrames Skills for Codex
Inspired by openai/plugins (HeyGen's official HyperFrames skills for Codex).
Demonstrates autonomous multi-track AI agent prompt-to-video workflow.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hyperframes_py import Composition, MetricCounter, render_to_mp4

def create_codex_demo():
    comp = Composition(
        comp_id="codex_heygen_demo",
        duration=4.5,
        background="#0b0f17",
        title="Codex HeyGen Official Skills"
    )

    counter1 = MetricCounter("fps-counter", "Deterministic Framerate", 60, suffix=" FPS", x=240, y=520)
    counter2 = MetricCounter("speed-counter", "Render Speed Acceleration", 8, suffix="x GPU", x=680, y=520)
    counter3 = MetricCounter("drift-counter", "Timeline Drift", 0, suffix=" ms", x=1120, y=520)

    comp.add_style(counter1.render_css())
    comp.add_style("""
        .codex-banner {
          position: absolute;
          left: 240px;
          top: 140px;
        }
        .codex-pill {
          display: inline-flex;
          align-items: center;
          gap: 10px;
          background: rgba(16, 185, 129, 0.15);
          border: 1px solid rgba(16, 185, 129, 0.3);
          color: #10b981;
          padding: 8px 18px;
          border-radius: 999px;
          font-family: monospace;
          font-size: 18px;
          font-weight: 700;
        }
        .codex-h1 {
          font-size: 68px;
          font-weight: 900;
          letter-spacing: -0.03em;
          color: #ffffff;
          margin: 20px 0 10px 0;
        }
        .codex-sub {
          font-size: 26px;
          color: #94a3b8;
          max-width: 1000px;
          margin: 0;
        }
    """)

    comp.add_html(f"""
        <div class="codex-banner">
          <div id="codex-tag" class="codex-pill">● OPENAI CODEX & HEYGEN OFFICIAL PLUGIN</div>
          <h1 id="codex-h1" class="codex-h1">Agent-Native HTML Video Engine</h1>
          <p id="codex-sub" class="codex-sub">Empowering autonomous AI coding agents to script, test, and render cinematic MP4 videos entirely in code.</p>
        </div>
        {counter1.render_html()}
        {counter2.render_html()}
        {counter3.render_html()}
    """)

    comp.animate("""
        tl.from('#codex-tag', { opacity: 0, y: -10, duration: 0.5, ease: 'power2.out' }, 0.1);
        tl.from('#codex-h1', { opacity: 0, y: 30, duration: 0.8, ease: 'power3.out' }, 0.2);
        tl.from('#codex-sub', { opacity: 0, y: 15, duration: 0.6, ease: 'power2.out' }, 0.5);
        
        tl.from(['#fps-counter', '#speed-counter', '#drift-counter'], {
          opacity: 0,
          y: 40,
          duration: 0.7,
          stagger: 0.15,
          ease: 'back.out(1.5)'
        }, 0.8);
    """)

    comp.animate(counter1.render_gsap(at=1.1, duration=1.8))
    comp.animate(counter2.render_gsap(at=1.3, duration=1.6))
    comp.animate(counter3.render_gsap(at=1.5, duration=1.4))

    return comp

if __name__ == "__main__":
    comp = create_codex_demo()
    out = "renders/10_codex_heygen.mp4"
    print(f"Rendering Codex demo to {out}...")
    res = render_to_mp4(comp, output_path=out, quality="draft")
    print("Result:", res)
