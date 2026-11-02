"""
Animated Diagrams module for HyperFrames.
Inspired by omkamal/animated-diagrams-skill (diagrams that draw themselves).
Renders architecture layouts, data flowcharts, and self-drawing connector pipelines.
"""

from typing import List, Dict, Any, Optional
import html

class DiagramNode:
    def __init__(self, node_id: str, label: str, sub: str, x: int, y: int, icon: str = "⚡", color: str = "#38bdf8"):
        self.node_id = node_id
        self.label = label
        self.sub = sub
        self.x = x
        self.y = y
        self.icon = icon
        self.color = color

class DiagramLink:
    def __init__(self, from_node: str, to_node: str, label: str = "", style: str = "curved"):
        self.from_node = from_node
        self.to_node = to_node
        self.label = label
        self.style = style

class AnimatedDiagram:
    def __init__(self, diagram_id: str = "arch-diagram"):
        self.diagram_id = diagram_id
        self.nodes: Dict[str, DiagramNode] = {}
        self.links: List[DiagramLink] = []
        self.start_time: float = 0.5
        self.duration: float = 4.0

    def add_node(self, node_id: str, label: str, sub: str, x: int, y: int, icon: str = "⚡", color: str = "#38bdf8") -> "AnimatedDiagram":
        self.nodes[node_id] = DiagramNode(node_id, label, sub, x, y, icon, color)
        return self

    def add_link(self, from_node: str, to_node: str, label: str = "") -> "AnimatedDiagram":
        self.links.append(DiagramLink(from_node, to_node, label))
        return self

    def render_html(self) -> str:
        nodes_html = []
        for n in self.nodes.values():
            nodes_html.append(f"""
        <div id="node-{n.node_id}" class="diagram-node" style="left: {n.x}px; top: {n.y}px; border-color: {n.color};">
          <div class="node-icon" style="background: {n.color}22; color: {n.color};">{n.icon}</div>
          <div class="node-body">
            <div class="node-title">{html.escape(n.label)}</div>
            <div class="node-sub">{html.escape(n.sub)}</div>
          </div>
        </div>
""")

        links_svg_paths = []
        for i, link in enumerate(self.links):
            if link.from_node in self.nodes and link.to_node in self.nodes:
                n1 = self.nodes[link.from_node]
                n2 = self.nodes[link.to_node]
                
                # Calculate connection coordinates (center to center)
                x1 = n1.x + 220
                y1 = n1.y + 45
                x2 = n2.x
                y2 = n2.y + 45
                
                cx1 = x1 + (x2 - x1) * 0.5
                cy1 = y1
                cx2 = x1 + (x2 - x1) * 0.5
                cy2 = y2
                
                path_d = f"M {x1} {y1} C {cx1} {cy1}, {cx2} {cy2}, {x2} {y2}"
                links_svg_paths.append(f"""
          <path id="link-path-{i}" class="diagram-link-path" d="{path_d}" />
          <!-- Animated pulse particle -->
          <circle id="link-pulse-{i}" class="diagram-pulse" r="5" fill="#38bdf8" />
""")

        return f"""
    <div id="{self.diagram_id}" class="animated-diagram-container">
      <svg class="diagram-svg-canvas" width="1920" height="1080">
        {"".join(links_svg_paths)}
      </svg>
      {"".join(nodes_html)}
    </div>
"""

    def render_css(self) -> str:
        return """
    .animated-diagram-container {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
    }
    .diagram-svg-canvas {
      position: absolute;
      inset: 0;
      overflow: visible;
    }
    .diagram-link-path {
      fill: none;
      stroke: #3b82f6;
      stroke-width: 3;
      stroke-linecap: round;
      stroke-dasharray: 800;
      stroke-dashoffset: 800;
      opacity: 0.7;
    }
    .diagram-pulse {
      opacity: 0;
    }
    .diagram-node {
      position: absolute;
      width: 220px;
      height: 90px;
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 14px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 15px -3px rgba(56, 189, 248, 0.2);
      display: flex;
      align-items: center;
      padding: 14px 18px;
      gap: 14px;
      opacity: 0;
      transform: scale(0.85);
    }
    .node-icon {
      width: 44px;
      height: 44px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      flex-shrink: 0;
    }
    .node-title {
      font-size: 16px;
      font-weight: 700;
      color: #f8fafc;
      letter-spacing: -0.01em;
    }
    .node-sub {
      font-size: 12px;
      color: #94a3b8;
      margin-top: 2px;
      font-family: monospace;
    }
"""

    def render_gsap(self) -> str:
        lines = []
        t = self.start_time
        
        # Staggered nodes entry
        node_selectors = [f"#node-{k}" for k in self.nodes.keys()]
        if node_selectors:
            joined = "', '".join(node_selectors)
            lines.append(f"""
    // Self-drawing diagram nodes entry
    tl.to(['{joined}'], {{
      opacity: 1,
      scale: 1,
      y: 0,
      duration: 0.65,
      stagger: 0.22,
      ease: 'back.out(1.5)'
    }}, {t});
""")
            t += 0.22 * len(node_selectors) + 0.2

        # Drawing links
        for i in range(len(self.links)):
            lines.append(f"""
    // Draw connector link #{i}
    tl.to('#link-path-{i}', {{
      strokeDashoffset: 0,
      duration: 0.8,
      ease: 'power2.out'
    }}, {round(t, 2)});
""")
            t += 0.35

        return "\n".join(lines)
