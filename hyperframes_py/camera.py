"""
Camera Rig module for HyperFrames.
Inspired by alchaincyf/huashu-design (3D seek-safe camera rig & camera language).
Implements budget-governed push-in, pull-out, smooth parallax pans, and orbits.
"""

from typing import List, Dict, Any, Tuple
import math

class CameraRig:
    def __init__(self, rig_id: str = "camera-rig", width: int = 1920, height: int = 1080):
        self.rig_id = rig_id
        self.width = width
        self.height = height
        self.shots: List[Dict[str, Any]] = []

    def calc_duration(self, zoom_delta: float, distance_normalized: float) -> float:
        """
        Calculates cinematic logarithmic duration following Huashu Camera Language rules:
        Duration scales smoothly with motion magnitude while respecting viewer comfort.
        """
        base = 1.6
        zoom_factor = math.log1p(abs(zoom_delta)) * 1.8
        pan_factor = distance_normalized * 2.2
        dur = base + zoom_factor + pan_factor
        return round(max(1.8, min(4.8, dur)), 2)

    def push_in(self, target_selector: str, scale: float = 1.45, duration: float = 2.4, at: float = 0.0, ease: str = "power2.out"):
        """
        Push in camera closer to focus on subject.
        Safe zoom bounds: 1.25x - 2.3x.
        """
        scale = max(1.15, min(2.5, scale))
        self.shots.append({
            "type": "push_in",
            "target": target_selector,
            "scale": scale,
            "duration": duration,
            "at": at,
            "ease": ease
        })
        return self

    def pull_out(self, scale: float = 1.0, duration: float = 2.0, at: float = 0.0, ease: str = "power2.inOut"):
        """Pull out to reveal wide scene or finish a sequence."""
        self.shots.append({
            "type": "pull_out",
            "scale": scale,
            "duration": duration,
            "at": at,
            "ease": ease
        })
        return self

    def pan(self, dx: float, dy: float, duration: float = 2.5, at: float = 0.0, ease: str = "power1.inOut"):
        """Smooth pan across coordinates."""
        self.shots.append({
            "type": "pan",
            "dx": dx,
            "dy": dy,
            "duration": duration,
            "at": at,
            "ease": ease
        })
        return self

    def orbit(self, rot_x: float = 12, rot_y: float = -18, duration: float = 3.2, at: float = 0.0, ease: str = "sine.inOut"):
        """3D subtle perspective orbit for hero shot depth."""
        self.shots.append({
            "type": "orbit",
            "rot_x": rot_x,
            "rot_y": rot_y,
            "duration": duration,
            "at": at,
            "ease": ease
        })
        return self

    def render_open_tag(self) -> str:
        return f'<div id="{self.rig_id}" class="camera-rig-container"><div id="{self.rig_id}-inner" class="camera-rig-inner">'

    def render_close_tag(self) -> str:
        return '</div></div>'

    def render_css(self) -> str:
        return f"""
    .camera-rig-container {{
      position: absolute;
      inset: 0;
      width: {self.width}px;
      height: {self.height}px;
      perspective: 1200px;
      transform-style: preserve-3d;
      overflow: hidden;
    }}
    .camera-rig-inner {{
      position: absolute;
      inset: 0;
      width: {self.width}px;
      height: {self.height}px;
      transform-origin: 50% 50%;
      will-change: transform;
    }}
"""

    def render_gsap(self) -> str:
        code_lines = []
        target = f"#{self.rig_id}-inner"
        for shot in self.shots:
            stype = shot["type"]
            dur = shot["duration"]
            at = shot["at"]
            ease = shot["ease"]

            if stype == "push_in":
                scale = shot["scale"]
                code_lines.append(f"tl.to('{target}', {{ scale: {scale}, ease: '{ease}', duration: {dur} }}, {at});")
            elif stype == "pull_out":
                scale = shot["scale"]
                code_lines.append(f"tl.to('{target}', {{ scale: {scale}, x: 0, y: 0, rotateX: 0, rotateY: 0, ease: '{ease}', duration: {dur} }}, {at});")
            elif stype == "pan":
                dx = shot["dx"]
                dy = shot["dy"]
                code_lines.append(f"tl.to('{target}', {{ x: {dx}, y: {dy}, ease: '{ease}', duration: {dur} }}, {at});")
            elif stype == "orbit":
                rx = shot["rot_x"]
                ry = shot["rot_y"]
                code_lines.append(f"tl.to('{target}', {{ rotateX: {rx}, rotateY: {ry}, ease: '{ease}', duration: {dur} }}, {at});")

        return "\n    ".join(code_lines)
