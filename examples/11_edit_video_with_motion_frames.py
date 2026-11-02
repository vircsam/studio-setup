"""
Example 11: Edit Video With Motion Frames
Demonstrates loading raw video footage and overlaying motion frames:
  - Base Video Track 0 synchronized frame-by-frame
  - Camera punch-in zoom on subject (Huashu Design)
  - Handwriting callout animation (Tegaki)
  - Glassmorphic lower-third explainer card (Student Kit)
  - Animated stat badges & progress indicators
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hyperframes_py import Composition, CameraRig, HandwritingText, render_to_mp4

def create_video_edit_composition(user_video_path: str = "renders/test.mp4"):
    # 1. Initialize Composition matching video aspect ratio
    comp = Composition(
        comp_id="video_edit_demo",
        width=1280,
        height=720,
        duration=4.5,
        title="Edited Video with Motion Frames"
    )

    # 2. Add Base Video Track (Place your MP4 here!)
    # Can be a relative path or local file URL
    comp.add_video_background(
        video_path=user_video_path,
        opacity=0.85,
        filter="contrast(1.05) brightness(0.95)"
    )

    # 3. Add 3D Camera Rig over the footage (subtle zoom punch-in)
    cam = CameraRig("video-cam", width=1280, height=720)
    cam.push_in(target_selector=".stage", scale=1.12, duration=2.0, at=0.4, ease="power2.out")
    comp.set_camera_rig(cam)

    # 4. Add Tegaki Handwriting Callout over the video
    hw = HandwritingText(
        text="Dynamic Motion Frame",
        element_id="vid-callout",
        font_size=54,
        color="#38bdf8",
        x=100,
        y=120
    )
    hw.set_timing(duration=1.8, start_time=0.5)

    comp.add_style(hw.render_css())
    comp.add_style("""
        /* Glassmorphic Lower-Third Card */
        .motion-lower-third {
          position: absolute;
          left: 80px;
          bottom: 60px;
          width: 650px;
          background: rgba(15, 23, 42, 0.85);
          border: 1px solid rgba(56, 189, 248, 0.35);
          backdrop-filter: blur(16px);
          border-radius: 20px;
          padding: 26px 32px;
          box-shadow: 0 20px 40px rgba(0,0,0,0.6);
          display: flex;
          align-items: center;
          gap: 20px;
          z-index: 10;
        }
        .lower-icon {
          width: 54px;
          height: 54px;
          border-radius: 12px;
          background: rgba(56, 189, 248, 0.2);
          color: #38bdf8;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 26px;
          flex-shrink: 0;
        }
        .lower-title {
          font-size: 22px;
          font-weight: 700;
          color: #ffffff;
          margin-bottom: 4px;
        }
        .lower-sub {
          font-size: 14px;
          color: #94a3b8;
          line-height: 1.4;
        }

        /* Top-Right Badge */
        .live-badge {
          position: absolute;
          right: 60px;
          top: 60px;
          background: rgba(16, 185, 129, 0.2);
          border: 1px solid rgba(16, 185, 129, 0.4);
          color: #34d399;
          font-family: monospace;
          font-weight: 700;
          font-size: 14px;
          padding: 8px 16px;
          border-radius: 999px;
          display: flex;
          align-items: center;
          gap: 8px;
          z-index: 10;
        }
        .pulse-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #34d399;
          box-shadow: 0 0 10px #34d399;
        }
    """)

    # 5. Add Motion Frame Overlays to HTML
    comp.add_html(f"""
        <!-- Top Right Badge -->
        <div id="vid-badge" class="live-badge">
          <span class="pulse-dot"></span> HYPERFRAMES OVERLAY
        </div>

        <!-- Handwriting Callout -->
        {hw.render_html()}

        <!-- Lower Third Explainer Card -->
        <div id="vid-card" class="motion-lower-third">
          <div class="lower-icon">🎬</div>
          <div>
            <div class="lower-title">Raw Footage + Programmatic Motion</div>
            <div class="lower-sub">Frame-accurate deterministic timeline with zero drift.</div>
          </div>
        </div>
    """)

    # 6. Animate Overlays with GSAP
    comp.animate("""
        // Badge entry
        tl.from('#vid-badge', { opacity: 0, scale: 0.8, duration: 0.5, ease: 'back.out(2)' }, 0.2);
        
        // Lower Third card slide-in
        tl.from('#vid-card', {
          opacity: 0,
          y: 40,
          scale: 0.95,
          duration: 0.7,
          ease: 'power3.out'
        }, 0.8);
    """)
    comp.animate(hw.render_gsap())

    return comp

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Edit video with motion frames")
    parser.add_argument("--video", default="renders/test.mp4", help="Path to input video")
    parser.add_argument("--out", default="renders/edited_video_with_motion.mp4", help="Path to output MP4")
    args = parser.parse_args()

    comp = create_video_edit_composition(args.video)
    print(f"Editing '{args.video}' with motion frames -> {args.out}...")
    res = render_to_mp4(comp, output_path=args.out, quality="draft")
    print("Render complete:", res["output_file"], f"({res['size_mb']} MB)")
