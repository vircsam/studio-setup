"""
Composition module for HyperFrames.
Builds HTML, CSS, and GSAP timeline structure compliant with HyperFrames standards.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

class Scene:
    def __init__(self, scene_id: str, start: float, duration: float, name: str = ""):
        self.scene_id = scene_id
        self.start = start
        self.duration = duration
        self.name = name or scene_id
        self.elements_html: List[str] = []
        self.styles: List[str] = []
        self.gsap_lines: List[str] = []

    def add_html(self, html: str):
        self.elements_html.append(html)
        return self

    def add_style(self, css: str):
        self.styles.append(css)
        return self

    def animate(self, code: str):
        """Append GSAP animation command (e.g., tl.from('#title', {...}))"""
        self.gsap_lines.append(code)
        return self

class Composition:
    """
    Main HyperFrames composition manager.
    Produces deterministic HTML with GSAP timelines that HyperFrames renders to MP4.
    """
    def __init__(
        self,
        comp_id: str = "main",
        width: int = 1920,
        height: int = 1080,
        fps: int = 30,
        duration: float = 6.0,
        background: str = "#090d16",
        title: str = "HyperFrames Composition"
    ):
        self.comp_id = comp_id
        self.width = width
        self.height = height
        self.fps = fps
        self.duration = duration
        self.background = background
        self.title = title
        
        self.scenes: List[Scene] = []
        self.custom_styles: List[str] = []
        self.custom_scripts: List[str] = []
        self.custom_html: List[str] = []
        self.timeline_actions: List[str] = []
        self.camera_rig: Optional[Any] = None
        self.soundtrack: Optional[Any] = None
        self.video_source: Optional[str] = None
        self.video_opacity: float = 1.0
        self.video_filter: str = ""

    def add_video_background(self, video_path: str, opacity: float = 1.0, filter: str = "") -> "Composition":
        """
        Adds base video footage as track 0.
        All motion cards, typography, handwriting, and camera rigs animate on top!
        """
        self.video_source = video_path
        self.video_opacity = opacity
        self.video_filter = filter
        return self

    def add_scene(self, scene: Scene) -> "Composition":
        self.scenes.append(scene)
        return self

    def add_style(self, css: str) -> "Composition":
        self.custom_styles.append(css)
        return self

    def add_script(self, js: str) -> "Composition":
        self.custom_scripts.append(js)
        return self

    def add_html(self, html: str) -> "Composition":
        self.custom_html.append(html)
        return self

    def animate(self, gsap_code: str) -> "Composition":
        self.timeline_actions.append(gsap_code)
        return self

    def set_camera_rig(self, rig: Any) -> "Composition":
        self.camera_rig = rig
        return self

    def set_soundtrack(self, soundtrack: Any) -> "Composition":
        self.soundtrack = soundtrack
        return self

    def compile_html(self) -> str:
        """Generates pixel-perfect HyperFrames-compatible HTML."""
        combined_styles = "\n".join(self.custom_styles)
        combined_body = "\n".join(self.custom_html)
        
        # Scenes HTML
        for scene in self.scenes:
            combined_styles += "\n" + "\n".join(scene.styles)
            scene_content = "\n".join(scene.elements_html)
            combined_body += f"""
    <!-- Scene: {scene.name} -->
    <div id="{scene.scene_id}" class="scene" data-track-index="1" data-start="{scene.start}" data-duration="{scene.duration}">
      {scene_content}
    </div>
"""

        # GSAP Timeline Script
        combined_gsap = "\n    ".join(self.timeline_actions)
        for scene in self.scenes:
            for g in scene.gsap_lines:
                combined_gsap += f"\n    // Scene {scene.scene_id}\n    {g}"

        # Camera Rig integration if present
        camera_rig_html_open = ""
        camera_rig_html_close = ""
        if self.camera_rig:
            camera_rig_html_open = self.camera_rig.render_open_tag()
            camera_rig_html_close = self.camera_rig.render_close_tag()
            combined_styles += "\n" + self.camera_rig.render_css()
            combined_gsap += "\n" + self.camera_rig.render_gsap()

        # Sound cues if present
        sound_html = ""
        if self.soundtrack:
            sound_html = self.soundtrack.render_audio_tags()
            combined_gsap += "\n" + self.soundtrack.render_gsap()

        # Base Video Track if present
        video_html = ""
        video_sync_js = ""
        if self.video_source:
            filter_style = f"filter: {self.video_filter};" if self.video_filter else ""
            video_html = f"""
    <!-- Base Video Track 0 -->
    <div id="base-video-track" class="video-stage" data-track-index="0" data-start="0" data-duration="{self.duration}">
      <video id="base-video" src="{self.video_source}" playsinline muted style="width:100%;height:100%;object-fit:cover;opacity:{self.video_opacity};{filter_style}"></video>
    </div>
"""
            video_sync_js = """
    // Deterministic Video Frame Seeking Synchronization
    const baseVid = document.getElementById('base-video');
    if (baseVid) {
      tl.eventCallback('onUpdate', function() {
        if (baseVid.readyState >= 1) {
          const t = tl.time();
          if (Math.abs(baseVid.currentTime - t) > 0.04) {
            baseVid.currentTime = t;
          }
        }
      });
    }
"""

        html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width={self.width}, height={self.height}">
  <title>{self.title}</title>
  <!-- GSAP Engine -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}
    html, body {{
      margin: 0;
      padding: 0;
      width: {self.width}px;
      height: {self.height}px;
      overflow: hidden;
      background: {self.background};
      color: #f1f5f9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
    }}
    .stage {{
      position: relative;
      width: {self.width}px;
      height: {self.height}px;
      overflow: hidden;
      transform-origin: 0 0;
    }}
    .video-stage {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: 0;
    }}
    .scene {{
      position: absolute;
      inset: 0;
      width: {self.width}px;
      height: {self.height}px;
      z-index: 1;
    }}
    {combined_styles}
  </style>
</head>
<body>
  <div id="{self.comp_id}"
       class="stage"
       data-composition-id="{self.comp_id}"
       data-start="0"
       data-duration="{self.duration}"
       data-width="{self.width}"
       data-height="{self.height}">
    
    {video_html}
    {camera_rig_html_open}
    {combined_body}
    {camera_rig_html_close}
    {sound_html}
  </div>

  <script>
    // HyperFrames deterministic timeline
    const tl = gsap.timeline({{ paused: true }});
    
    // Animate composition
    {combined_gsap}
    
    {video_sync_js}

    // Register timeline with HyperFrames renderer hook
    window.__timelines = window.__timelines || {{}};
    window.__timelines['{self.comp_id}'] = tl;
    window.__hyperframes_ready = true;
  </script>
</body>
</html>"""
        return html

    def export(self, output_dir: str = ".") -> Path:
        """Writes index.html and hyperframes.json to output directory."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        
        # Handle local video assets
        if self.video_source:
            src_path = Path(self.video_source)
            if src_path.exists():
                assets_dir = out / "assets"
                assets_dir.mkdir(parents=True, exist_ok=True)
                dest = assets_dir / src_path.name
                if not dest.exists():
                    import shutil
                    shutil.copy2(src_path, dest)
                original_src = self.video_source
                self.video_source = f"assets/{src_path.name}"
                html_text = self.compile_html()
                self.video_source = original_src
            else:
                html_text = self.compile_html()
        else:
            html_text = self.compile_html()

        index_file = out / "index.html"
        index_file.write_text(html_text, encoding="utf-8")
        
        hf_config = {
            "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
            "fps": self.fps,
            "width": self.width,
            "height": self.height,
            "duration": self.duration
        }
        (out / "hyperframes.json").write_text(json.dumps(hf_config, indent=2), encoding="utf-8")
        return index_file
