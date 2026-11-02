"""
SaaS and Product Launch Motion module for HyperFrames.
Inspired by:
  - tugrawork-creator/saas-motion-kit (six styles: Minimal, Bento, Kinetic, Elegant, Neo-brutalist, Playful)
  - AbubakrChan/product-launch-motion (cursor path, film grain, continuous spring physics)
"""

from typing import List, Dict, Any, Optional
import html

class CursorChoreography:
    """Simulates realistic cursor movement, clicks, and interactions."""
    def __init__(self, cursor_id: str = "main-cursor"):
        self.cursor_id = cursor_id
        self.waypoints: List[Dict[str, Any]] = []

    def move_to(self, x: int, y: int, duration: float = 1.0, at: float = 0.0, click: bool = False):
        self.waypoints.append({
            "x": x,
            "y": y,
            "duration": duration,
            "at": at,
            "click": click
        })
        return self

    def render_html(self) -> str:
        return f"""
    <div id="{self.cursor_id}" class="pro-cursor">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M5.65376 12.3673H5.46026L5.31717 12.4976L0.500002 16.8829L0.500002 1.19841L11.7841 12.3673H5.65376Z" fill="#38bdf8" stroke="#ffffff" stroke-width="1.5"/>
      </svg>
      <div id="{self.cursor_id}-click-ripple" class="cursor-ripple"></div>
    </div>
"""

    def render_css(self) -> str:
        return f"""
    .pro-cursor {{
      position: absolute;
      left: 100px;
      top: 100px;
      z-index: 9999;
      pointer-events: none;
      filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));
    }}
    .cursor-ripple {{
      position: absolute;
      top: 2px;
      left: 2px;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      border: 2px solid #38bdf8;
      transform: scale(0);
      opacity: 0;
    }}
"""

    def render_gsap(self) -> str:
        lines = []
        target = f"#{self.cursor_id}"
        ripple = f"#{self.cursor_id}-click-ripple"
        for wp in self.waypoints:
            lines.append(f"""
    tl.to('{target}', {{
      x: {wp['x']},
      y: {wp['y']},
      duration: {wp['duration']},
      ease: 'power2.inOut'
    }}, {wp['at']});
""")
            if wp.get("click"):
                click_time = wp["at"] + wp["duration"]
                lines.append(f"""
    // Cursor click action
    tl.to('{target}', {{ scale: 0.85, duration: 0.1, yoyo: true, repeat: 1, ease: 'power2.in' }}, {click_time});
    tl.to('{ripple}', {{ opacity: 1, scale: 1.8, duration: 0.45, ease: 'power2.out' }}, {click_time});
    tl.to('{ripple}', {{ opacity: 0, duration: 0.2 }}, {click_time + 0.3});
""")
        return "\n".join(lines)


class SaaSCard:
    """Pre-styled SaaS feature cards with Bento and Neo-brutalist themes."""
    def __init__(self, card_id: str, title: str, description: str, tag: str = "FEATURE", icon: str = "🚀", width: int = 480, height: int = 320, x: int = 200, y: int = 200, style: str = "bento"):
        self.card_id = card_id
        self.title = title
        self.description = description
        self.tag = tag
        self.icon = icon
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.style = style

    def render_html(self) -> str:
        return f"""
    <div id="{self.card_id}" class="saas-card saas-{self.style}" style="left:{self.x}px; top:{self.y}px; width:{self.width}px; height:{self.height}px;">
      <div class="saas-card-tag">{html.escape(self.tag)}</div>
      <div class="saas-card-icon">{self.icon}</div>
      <h3 class="saas-card-title">{html.escape(self.title)}</h3>
      <p class="saas-card-desc">{html.escape(self.description)}</p>
    </div>
"""

    def render_css(self) -> str:
        return """
    .saas-card {
      position: absolute;
      border-radius: 20px;
      padding: 36px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    .saas-bento {
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95));
      border: 1px solid rgba(255,255,255,0.12);
      backdrop-filter: blur(16px);
    }
    .saas-kinetic {
      background: #0f172a;
      border: 2px solid #38bdf8;
      box-shadow: 0 0 30px rgba(56, 189, 248, 0.25);
    }
    .saas-card-tag {
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 2px;
      color: #38bdf8;
      margin-bottom: 12px;
      font-family: monospace;
    }
    .saas-card-icon {
      font-size: 40px;
      margin-bottom: 18px;
    }
    .saas-card-title {
      font-size: 28px;
      font-weight: 700;
      color: #f8fafc;
      margin: 0 0 10px 0;
    }
    .saas-card-desc {
      font-size: 16px;
      color: #94a3b8;
      line-height: 1.5;
      margin: 0;
    }
"""

    def render_gsap(self, at: float = 0.5, duration: float = 0.8) -> str:
        return f"""
    tl.from('#{self.card_id}', {{
      opacity: 0,
      y: 60,
      scale: 0.9,
      duration: {duration},
      ease: 'back.out(1.6)'
    }}, {at});
"""


class BentoGrid:
    """Layout helper that arranges cards in a Bento grid pattern."""
    def __init__(self, grid_id: str = "bento-grid", x: int = 160, y: int = 140):
        self.grid_id = grid_id
        self.x = x
        self.y = y
        self.cards: List[SaaSCard] = []

    def add_card(self, card: SaaSCard):
        self.cards.append(card)
        return self

    def render_html(self) -> str:
        return "".join([c.render_html() for c in self.cards])

    def render_css(self) -> str:
        if self.cards:
            return self.cards[0].render_css()
        return ""

    def render_gsap(self, start_time: float = 0.5, stagger: float = 0.15) -> str:
        selectors = [f"#{c.card_id}" for c in self.cards]
        joined = "', '".join(selectors)
        return f"""
    tl.from(['{joined}'], {{
      opacity: 0,
      y: 50,
      scale: 0.92,
      duration: 0.85,
      stagger: {stagger},
      ease: 'back.out(1.4)'
    }}, {start_time});
"""
