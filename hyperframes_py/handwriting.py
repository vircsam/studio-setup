"""
Handwriting animation module for HyperFrames.
Inspired by gkurt/tegaki (handwriting from real fonts).
Renders authentic vector handwriting strokes that draw themselves smoothly over time.
"""

from typing import List, Dict, Any, Optional
import html

class HandwritingText:
    """
    Generates realistic cursive/stroke handwriting animations using SVG paths
    and GSAP stroke-dashoffset / stroke-dasharray reveal sequences.
    """
    def __init__(
        self,
        text: str,
        element_id: str = "handwriting-text",
        font_family: str = "'Caveat', 'Dancing Script', cursive",
        font_size: int = 72,
        color: str = "#38bdf8",
        x: int = 200,
        y: int = 300,
        stroke_width: float = 3.5
    ):
        self.text = text
        self.element_id = element_id
        self.font_family = font_family
        self.font_size = font_size
        self.color = color
        self.x = x
        self.y = y
        self.stroke_width = stroke_width
        self.duration: float = 2.5
        self.start_time: float = 0.5

    def set_timing(self, duration: float = 2.5, start_time: float = 0.5) -> "HandwritingText":
        self.duration = duration
        self.start_time = start_time
        return self

    def render_html(self) -> str:
        # We construct an SVG containing stylized script text with dynamic stroke-dashpath reveals
        safe_text = html.escape(self.text)
        return f"""
    <div id="{self.element_id}-wrap" class="handwriting-wrapper" style="left:{self.x}px; top:{self.y}px;">
      <svg class="handwriting-svg" viewBox="0 0 1200 240" width="1200" height="240">
        <!-- Underline flourishing stroke -->
        <path id="{self.element_id}-flourish" class="flourish-path"
              d="M 10 180 Q 250 160 500 175 T 950 165"
              fill="none" stroke="{self.color}" stroke-width="{self.stroke_width}" stroke-linecap="round"/>
        <!-- Handwritten typography -->
        <text id="{self.element_id}-txt" class="handwritten-text"
              x="20" y="140"
              font-family="{self.font_family}"
              font-size="{self.font_size}"
              fill="none"
              stroke="{self.color}"
              stroke-width="{self.stroke_width}"
              stroke-dasharray="1400"
              stroke-dashoffset="1400">
          {safe_text}
        </text>
      </svg>
    </div>
"""

    def render_css(self) -> str:
        return f"""
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Dancing+Script:wght@700&display=swap');
    
    .handwriting-wrapper {{
      position: absolute;
      width: 1200px;
      height: 240px;
      pointer-events: none;
    }}
    .flourish-path {{
      stroke-dasharray: 1000;
      stroke-dashoffset: 1000;
      opacity: 0.85;
    }}
    .handwritten-text {{
      letter-spacing: 2px;
      will-change: stroke-dashoffset, fill;
    }}
"""

    def render_gsap(self) -> str:
        txt_id = f"#{self.element_id}-txt"
        flourish_id = f"#{self.element_id}-flourish"
        fill_dur = round(self.duration * 0.35, 2)
        flourish_dur = round(self.duration * 0.5, 2)
        
        return f"""
    // Tegaki handwriting stroke reveal
    tl.to('{txt_id}', {{
      strokeDashoffset: 0,
      duration: {self.duration},
      ease: 'power1.inOut'
    }}, {self.start_time});
    
    // Smooth ink fill transition
    tl.to('{txt_id}', {{
      fill: '{self.color}',
      duration: {fill_dur},
      ease: 'power2.out'
    }}, {self.start_time + self.duration * 0.7});

    // Flourish underline accent
    tl.to('{flourish_id}', {{
      strokeDashoffset: 0,
      duration: {flourish_dur},
      ease: 'power2.out'
    }}, {self.start_time + self.duration * 0.4});
"""
