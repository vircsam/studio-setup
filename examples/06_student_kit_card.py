"""
Example 06: HyperFrames Student Kit
Inspired by nateherkai/hyperframes-student-kit (herk-edit-kit).
Card templates, talking-head overlays, and silence cutting typography.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hyperframes_py import Composition, render_to_mp4

def create_student_kit_demo():
    # 9:16 vertical short format for modern video creator feeds
    comp = Composition(
        comp_id="student_kit_demo",
        width=1080,
        height=1920,
        duration=4.0,
        background="#0a0c10",
        title="Student Kit Short-Form Card"
    )

    comp.add_style("""
        .sk-wrap {
          position: absolute;
          inset: 0;
          display: flex;
          flex-direction: column;
          justify-content: flex-end;
          padding: 100px 70px 140px;
        }
        .sk-card {
          background: rgba(17, 24, 39, 0.88);
          border: 1px solid rgba(255, 255, 255, 0.15);
          backdrop-filter: blur(24px);
          border-radius: 32px;
          padding: 50px;
          box-shadow: 0 20px 50px rgba(0,0,0,0.6);
        }
        .sk-tag {
          font-family: monospace;
          color: #38bdf8;
          font-size: 24px;
          letter-spacing: 3px;
          font-weight: 700;
        }
        .sk-title {
          font-size: 64px;
          font-weight: 900;
          line-height: 1.1;
          letter-spacing: -0.03em;
          margin: 20px 0;
          color: #ffffff;
        }
        .sk-desc {
          font-size: 28px;
          line-height: 1.5;
          color: #94a3b8;
          margin: 0;
        }
        .sk-pill {
          display: inline-block;
          background: #38bdf822;
          color: #38bdf8;
          padding: 4px 14px;
          border-radius: 8px;
        }
    """)

    comp.add_html("""
        <div class="sk-wrap">
          <div id="sk-card" class="sk-card">
            <div class="sk-tag">HERK-EDIT-KIT // LESSON #04</div>
            <h2 class="sk-title">Trim Dead Air.<br>Keep <span class="sk-pill">Natural</span> Rhythm.</h2>
            <p class="sk-desc">Autonomous transcription alignment and synchronized visual title cards for AI video production.</p>
          </div>
        </div>
    """)

    comp.animate("""
        tl.from('#sk-card', {
          opacity: 0,
          y: 120,
          scale: 0.94,
          duration: 0.9,
          ease: 'power3.out'
        }, 0.3);
    """)

    return comp

if __name__ == "__main__":
    comp = create_student_kit_demo()
    out = "renders/06_student_kit.mp4"
    print(f"Rendering Student Kit demo to {out}...")
    res = render_to_mp4(comp, output_path=out, quality="draft")
    print("Result:", res)
