"""
Example 05: Seek-Safe Camera Rig
Inspired by alchaincyf/huashu-design (camera-language.md & logarithmic duration budget).
Smooth push-in, parallax pan, and 3D orbit on UI elements.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hyperframes_py import Composition, CameraRig, render_to_mp4

def create_camera_demo():
    comp = Composition(
        comp_id="camera_demo",
        duration=5.0,
        background="#0b0f19",
        title="Huashu Seek-Safe Camera Rig"
    )

    cam = CameraRig("cam", width=1920, height=1080)
    # Budget-safe camera sequence: Push in -> Subtle 3D Orbit -> Settle
    cam.push_in(target_selector=".hero-card", scale=1.35, duration=2.2, at=0.5, ease="power2.out")
    cam.orbit(rot_x=8, rot_y=-14, duration=2.0, at=1.8, ease="sine.inOut")
    comp.set_camera_rig(cam)

    comp.add_style("""
        .cam-content {
          position: absolute;
          inset: 0;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .hero-card {
          width: 900px;
          height: 520px;
          background: linear-gradient(145deg, #1e293b, #0f172a);
          border: 1px solid rgba(56, 189, 248, 0.3);
          border-radius: 28px;
          padding: 60px;
          box-shadow: 0 30px 60px rgba(0,0,0,0.7), 0 0 40px rgba(56, 189, 248, 0.15);
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }
        .cam-badge {
          font-family: monospace;
          color: #38bdf8;
          font-size: 20px;
          letter-spacing: 3px;
        }
        .card-h1 {
          font-size: 58px;
          font-weight: 800;
          letter-spacing: -0.03em;
          color: #f8fafc;
          margin: 15px 0;
        }
        .card-meta {
          font-size: 24px;
          color: #94a3b8;
        }
        .card-stats {
          display: flex;
          gap: 40px;
          border-top: 1px solid #334155;
          padding-top: 25px;
        }
        .stat-item {
          font-size: 20px;
          color: #cbd5e1;
        }
        .stat-num {
          font-size: 32px;
          font-weight: 700;
          color: #38bdf8;
          display: block;
        }
    """)

    comp.add_html("""
        <div class="cam-content">
          <div class="hero-card">
            <div>
              <div class="cam-badge">HUASHU-DESIGN / 3D CAMERA RIG</div>
              <h1 class="card-h1">Seek-Safe Viewport Navigation</h1>
              <p class="card-meta">Logarithmic motion durations governed by viewer comfort budgets.</p>
            </div>
            <div class="card-stats">
              <div class="stat-item"><span class="stat-num">1.35x</span>Push-in Scale</div>
              <div class="stat-item"><span class="stat-num">1200px</span>Perspective Field</div>
              <div class="stat-item"><span class="stat-num">0 Drift</span>Deterministic Output</div>
            </div>
          </div>
        </div>
    """)

    return comp

if __name__ == "__main__":
    comp = create_camera_demo()
    out = "renders/05_camera_rig.mp4"
    print(f"Rendering Camera Rig demo to {out}...")
    res = render_to_mp4(comp, output_path=out, quality="draft")
    print("Result:", res)
