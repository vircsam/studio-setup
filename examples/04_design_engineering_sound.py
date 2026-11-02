"""
Example 04: Sound Derived From Motion
Inspired by AgentsORG/design-engineering (sound-sheet.mjs).
Element size -> Pitch, Element X -> Pan, Impact -> Audio Transient.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hyperframes_py import Composition, SoundTrack, render_to_mp4

def create_sound_demo():
    comp = Composition(
        comp_id="sound_demo",
        duration=4.5,
        background="#f4f3ee",
        title="Sound Derived From Motion"
    )

    sound = SoundTrack()
    # Contact frame sounds derived from layout geometry
    sound.add_cue("heavy_card_drop", at=0.6, cue_type="thud", size_px=800, x_pos=480)
    sound.add_cue("light_toggle_click", at=1.6, cue_type="click", size_px=120, x_pos=960)
    sound.add_cue("confirm_button", at=2.4, cue_type="click", size_px=180, x_pos=1440)
    comp.set_soundtrack(sound)

    comp.add_style("""
        body { color: #0f1013 !important; }
        .snd-container {
          position: absolute;
          inset: 0;
          padding: 140px 180px;
          display: flex;
          flex-direction: column;
        }
        .snd-eyebrow {
          font-family: monospace;
          color: #0068d6;
          font-size: 24px;
          letter-spacing: 3px;
        }
        .snd-hero {
          font-size: 84px;
          font-weight: 800;
          letter-spacing: -0.03em;
          margin: 15px 0 40px;
          color: #0f1013;
        }
        .snd-cards {
          display: flex;
          gap: 32px;
          margin-top: 40px;
        }
        .snd-card {
          flex: 1;
          background: #ffffff;
          border-radius: 20px;
          padding: 36px;
          box-shadow: 0 10px 30px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.05);
          border: 1px solid rgba(15,16,19,0.08);
          opacity: 0;
          transform: translateY(40px);
        }
        .snd-card-tag {
          font-family: monospace;
          font-size: 16px;
          color: #0068d6;
          font-weight: 700;
        }
        .snd-card-val {
          font-size: 38px;
          font-weight: 800;
          margin: 16px 0 8px;
        }
        .snd-card-desc {
          font-size: 18px;
          color: #52525b;
        }
    """)

    comp.add_html("""
        <div class="snd-container">
          <div id="snd-tag" class="snd-eyebrow">DESIGN-ENGINEERING / SOUND MOTION</div>
          <h1 id="snd-h1" class="snd-hero">Sound, derived from motion.</h1>
          
          <div class="snd-cards">
            <div id="card-1" class="snd-card">
              <div class="snd-card-tag">SIZE → PITCH</div>
              <div class="snd-card-val">86 Hz Thud</div>
              <div class="snd-card-desc">Large mass produces resonant bass impact.</div>
            </div>
            <div id="card-2" class="snd-card">
              <div class="snd-card-tag">COORDINATE → STEREO</div>
              <div class="snd-card-val">Center Click</div>
              <div class="snd-card-desc">Horizontal X position maps to spatial acoustic field.</div>
            </div>
            <div id="card-3" class="snd-card">
              <div class="snd-card-tag">CONTACT FRAME</div>
              <div class="snd-card-val">Transient Sync</div>
              <div class="snd-card-desc">Zero drift between visual velocity stop and attack.</div>
            </div>
          </div>
        </div>
    """)

    comp.animate("""
        tl.from('#snd-tag', { opacity: 0, y: -10, duration: 0.5, ease: 'power2.out' }, 0.1);
        tl.from('#snd-h1', { opacity: 0, y: 30, duration: 0.8, ease: 'power3.out' }, 0.2);
        
        // Card 1 impact synced with audio transient at 0.6s
        tl.to('#card-1', { opacity: 1, y: 0, duration: 0.5, ease: 'back.out(1.5)' }, 0.6);
        
        // Card 2 impact at 1.6s
        tl.to('#card-2', { opacity: 1, y: 0, duration: 0.5, ease: 'back.out(1.5)' }, 1.6);
        
        // Card 3 impact at 2.4s
        tl.to('#card-3', { opacity: 1, y: 0, duration: 0.5, ease: 'back.out(1.5)' }, 2.4);
    """)

    return comp

if __name__ == "__main__":
    comp = create_sound_demo()
    out = "renders/04_sound_motion.mp4"
    print(f"Rendering Sound demo to {out}...")
    res = render_to_mp4(comp, output_path=out, quality="draft")
    print("Result:", res)
