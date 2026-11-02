"""
HyperFrames Python Animation Framework (hyperframes_py)
Deterministic HTML & GSAP video generation powered by Python.
Integrates with 10 industry-standard motion extensions:
  01. ReelForge (motion fragments)
  02. Tegaki (handwriting animation)
  03. Animated Diagrams (diagrams that draw themselves)
  04. Design Engineering (sound derived from motion)
  05. Huashu Design (seek-safe camera rig)
  06. Student Kit (card templates & speech pacing)
  07. Motion Library (23 chart & explainer templates)
  08. SaaS Motion Kit (6-style promotional design)
  09. Product Launch Motion (cursor choreography & film look)
  10. OpenAI / HeyGen Codex Skills
"""

from .composition import Composition, Scene
from .camera import CameraRig
from .handwriting import HandwritingText
from .diagrams import AnimatedDiagram, DiagramNode, DiagramLink
from .sound import SoundTrack, SoundCue
from .motion_library import BarChartGrow, MetricCounter
from .saas import SaaSCard, CursorChoreography, BentoGrid
from .renderer import render_to_mp4, preview_composition

__version__ = "1.0.0"

__all__ = [
    "Composition",
    "Scene",
    "CameraRig",
    "HandwritingText",
    "AnimatedDiagram",
    "DiagramNode",
    "DiagramLink",
    "SoundTrack",
    "SoundCue",
    "BarChartGrow",
    "MetricCounter",
    "SaaSCard",
    "CursorChoreography",
    "BentoGrid",
    "render_to_mp4",
    "preview_composition",
]
