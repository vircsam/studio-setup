"""
Example 03: Animated Diagrams That Draw Themselves
Self-assembling microservices architecture inspired by omkamal/animated-diagrams-skill.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hyperframes_py import Composition, AnimatedDiagram, render_to_mp4

def create_diagram_demo():
    comp = Composition(
        comp_id="diagram_demo",
        duration=4.5,
        background="#090d16",
        title="Animated Diagram Pipeline"
    )

    diagram = AnimatedDiagram("pipeline")
    diagram.add_node("agent", "AI Coding Agent", "Claude Code / Codex", 240, 480, icon="🤖", color="#38bdf8")
    diagram.add_node("engine", "HyperFrames Engine", "HTML + GSAP Timelines", 680, 480, icon="⚡", color="#a855f7")
    diagram.add_node("chrome", "Headless Chrome", "Deterministic Capture", 1120, 360, icon="🌐", color="#ec4899")
    diagram.add_node("mp4", "MP4 Video Artifact", "H.264 / AAC Encoding", 1120, 600, icon="🎬", color="#10b981")

    diagram.add_link("agent", "engine", "Generates Code")
    diagram.add_link("engine", "chrome", "Direct Frame Seeks")
    diagram.add_link("engine", "mp4", "Stitches Render")

    comp.add_style(diagram.render_css())
    comp.add_style("""
        .diagram-eyebrow {
          position: absolute;
          left: 240px;
          top: 180px;
          font-family: monospace;
          color: #38bdf8;
          font-size: 24px;
          letter-spacing: 4px;
        }
        .diagram-title {
          position: absolute;
          left: 240px;
          top: 220px;
          font-size: 56px;
          font-weight: 800;
          letter-spacing: -0.02em;
          color: #f8fafc;
          margin: 0;
        }
    """)

    comp.add_html(f"""
        <div id="diag-eye" class="diagram-eyebrow">ANIMATED DIAGRAMS SKILL / ARCHITECTURE</div>
        <h1 id="diag-h1" class="diagram-title">Diagrams That Draw Themselves</h1>
        {diagram.render_html()}
    """)

    comp.animate("""
        tl.from('#diag-eye', { opacity: 0, y: -10, duration: 0.5, ease: 'power2.out' }, 0.1);
        tl.from('#diag-h1', { opacity: 0, y: 20, duration: 0.7, ease: 'power3.out' }, 0.2);
    """)
    comp.animate(diagram.render_gsap())

    return comp

if __name__ == "__main__":
    comp = create_diagram_demo()
    out = "renders/03_animated_diagram.mp4"
    print(f"Rendering Diagram demo to {out}...")
    res = render_to_mp4(comp, output_path=out, quality="draft")
    print("Result:", res)
