#!/usr/bin/env python3
"""
HyperFrames Super-Simple Video Editor CLI
Add motion frames, handwriting, camera zooms, and cards to any video with one command.

Usage:
  python3 edit.py my_video.mp4
  python3 edit.py my_video.mp4 --text "Welcome to my video" --zoom --handwriting
  python3 edit.py my_video.mp4 --card "Key Takeaway" "Trim dead air and keep rhythm"
"""

import os
import sys
import argparse
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from hyperframes_py import Composition, CameraRig, HandwritingText, BarChartGrow, render_to_mp4

def edit_video(
    video_path: str,
    output_path: str = None,
    text: str = None,
    handwriting: bool = False,
    zoom: bool = False,
    card_title: str = None,
    card_sub: str = None,
    chart: bool = False,
    duration: float = None
):
    video_file = Path(video_path).resolve()
    if not video_file.exists():
        print(f"❌ Error: Video file not found: {video_path}")
        print("👉 Please provide a valid path to an MP4 video, e.g.:")
        print("   python3 edit.py renders/test.mp4")
        return False

    # Probe duration if not given using ffprobe
    if duration is None:
        try:
            import subprocess
            cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(video_file)]
            dur_str = subprocess.check_output(cmd, text=True).strip()
            duration = min(float(dur_str), 15.0) # Cap at 15s for quick preview/render
        except Exception:
            duration = 5.0

    print(f"\n=======================================================")
    print(f"🎬 Editing Video: {video_file.name} ({duration}s)")
    print(f"=======================================================")

    # 1. Create Composition
    comp = Composition(
        comp_id="user_video_edit",
        width=1280,
        height=720,
        duration=duration,
        title=f"Edited: {video_file.stem}"
    )

    # 2. Add Base Video (Track 0)
    comp.add_video_background(str(video_file), opacity=0.92, filter="contrast(1.04)")

    # 3. Add 3D Camera Rig if requested
    if zoom:
        print("  ✓ Adding Huashu 3D Camera Zoom punch-in")
        cam = CameraRig("cam", width=1280, height=720)
        cam.push_in(target_selector=".stage", scale=1.14, duration=2.0, at=0.4)
        comp.set_camera_rig(cam)

    # 4. Add Handwriting if requested
    if handwriting and text:
        print(f"  ✓ Adding Tegaki Handwriting: '{text}'")
        hw = HandwritingText(text=text, element_id="hw-callout", font_size=52, color="#38bdf8", x=80, y=100)
        hw.set_timing(duration=2.0, start_time=0.5)
        comp.add_style(hw.render_css())
        comp.add_html(hw.render_html())
        comp.animate(hw.render_gsap())
    elif text:
        # Standard sleek title
        print(f"  ✓ Adding Title Overlay: '{text}'")
        comp.add_style("""
            .top-title {
              position: absolute;
              left: 80px;
              top: 80px;
              font-size: 48px;
              font-weight: 800;
              color: #ffffff;
              text-shadow: 0 4px 20px rgba(0,0,0,0.8);
              letter-spacing: -0.02em;
            }
        """)
        comp.add_html(f'<h1 id="top-title" class="top-title">{text}</h1>')
        comp.animate("tl.from('#top-title', { opacity: 0, y: -20, duration: 0.8, ease: 'power2.out' }, 0.4);")

    # 5. Add Motion Card if requested
    if card_title:
        print(f"  ✓ Adding Student Kit Explainer Card: '{card_title}'")
        sub_text = card_sub or "Enhanced with HyperFrames motion frames"
        comp.add_style("""
            .explainer-card {
              position: absolute;
              left: 80px;
              bottom: 60px;
              background: rgba(15, 23, 42, 0.90);
              border: 1px solid rgba(56, 189, 248, 0.4);
              backdrop-filter: blur(20px);
              border-radius: 20px;
              padding: 24px 32px;
              color: #ffffff;
              box-shadow: 0 20px 40px rgba(0,0,0,0.6);
              z-index: 10;
              max-width: 600px;
            }
            .card-tag { font-family: monospace; font-size: 13px; color: #38bdf8; font-weight: 700; margin-bottom: 6px; }
            .card-h { font-size: 24px; font-weight: 800; margin-bottom: 4px; }
            .card-p { font-size: 15px; color: #94a3b8; line-height: 1.4; margin: 0; }
        """)
        comp.add_html(f"""
            <div id="explainer-card" class="explainer-card">
              <div class="card-tag">HYPERFRAMES // MOTION FRAME</div>
              <div class="card-h">{card_title}</div>
              <div class="card-p">{sub_text}</div>
            </div>
        """)
        comp.animate("tl.from('#explainer-card', { opacity: 0, y: 50, duration: 0.8, ease: 'back.out(1.5)' }, 0.8);")

    # 6. Add Growing Chart if requested
    if chart:
        print("  ✓ Adding Motion Library Data Chart")
        chart_comp = BarChartGrow(title="Growth Metric", subtitle="Synchronized with video playback")
        chart_comp.add_bar("Start", 35, color="#60a5fa", suffix="%")
        chart_comp.add_bar("Midway", 65, color="#818cf8", suffix="%")
        chart_comp.add_bar("Final", 95, color="#34d399", suffix="%")
        comp.add_style(chart_comp.render_css())
        comp.add_html(chart_comp.render_html())
        comp.animate(chart_comp.render_gsap())

    # Set output destination
    if output_path is None:
        output_path = f"renders/{video_file.stem}_edited.mp4"

    out_file = Path(output_path).resolve()
    print(f"\n🚀 Rendering final video to: {out_file}...")
    res = render_to_mp4(comp, output_path=str(out_file), quality="standard")
    
    if res["success"]:
        print(f"\n🎉 SUCCESS! Your edited video is ready:")
        print(f"👉 File: {res['output_file']} ({res['size_mb']} MB)")
        print(f"👉 You can also preview it in the web studio: http://localhost:8080")
        return True
    else:
        print(f"❌ Render encountered an error: {res.get('stderr') or res.get('error')}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HyperFrames Video Editor: Overlay motion frames on any video")
    parser.add_argument("video", nargs="?", default="renders/test.mp4", help="Path to your raw video file")
    parser.add_argument("--out", "-o", help="Output MP4 path (default: renders/<video>_edited.mp4)")
    parser.add_argument("--text", "-t", default="HyperFrames Motion Frame", help="Title text overlay")
    parser.add_argument("--handwriting", "-hw", action="store_true", default=True, help="Use Tegaki handwriting style")
    parser.add_argument("--zoom", "-z", action="store_true", default=True, help="Use Huashu 3D camera zoom punch-in")
    parser.add_argument("--card", nargs=2, metavar=("TITLE", "SUBTITLE"), default=["Key Takeaway", "AI-assisted video editing with deterministic motion"], help="Add Student Kit lower-third card")
    parser.add_argument("--chart", action="store_true", help="Add animated growing bar chart")
    parser.add_argument("--duration", "-d", type=float, help="Video duration in seconds")

    args = parser.parse_args()
    card_title, card_sub = args.card if args.card else (None, None)

    edit_video(
        video_path=args.video,
        output_path=args.out,
        text=args.text,
        handwriting=args.handwriting,
        zoom=args.zoom,
        card_title=card_title,
        card_sub=card_sub,
        chart=args.chart,
        duration=args.duration
    )
