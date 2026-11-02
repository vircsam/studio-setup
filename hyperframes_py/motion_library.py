"""
Motion Library module for HyperFrames.
Inspired by nutllwhy/hyperframes-motion-library (23 templates, charts to explainers).
Provides parameter-driven data visualizations: Bar charts, counters, growth graphs.
"""

from typing import List, Dict, Any, Tuple
import html

class BarChartGrow:
    def __init__(self, chart_id: str = "chart-grow", title: str = "Quarterly Revenue Growth", subtitle: str = "Deterministic HyperFrames Render"):
        self.chart_id = chart_id
        self.title = title
        self.subtitle = subtitle
        self.bars: List[Dict[str, Any]] = []
        self.start_time: float = 0.5
        self.duration: float = 2.5

    def add_bar(self, label: str, value: float, max_val: float = 100.0, color: str = "#38bdf8", prefix: str = "", suffix: str = "%"):
        self.bars.append({
            "label": label,
            "value": value,
            "max": max_val,
            "color": color,
            "prefix": prefix,
            "suffix": suffix
        })
        return self

    def render_html(self) -> str:
        bars_html = []
        for i, b in enumerate(self.bars):
            height_pct = round((b["value"] / b["max"]) * 100, 1)
            bars_html.append(f"""
        <div class="chart-col">
          <div class="col-bar-track">
            <div id="bar-fill-{i}" class="col-bar-fill" style="background: linear-gradient(180deg, {b['color']}, {b['color']}88);" data-h="{height_pct}%">
              <span id="bar-val-{i}" class="bar-val-badge">{b['prefix']}{b['value']}{b['suffix']}</span>
            </div>
          </div>
          <div class="col-label">{html.escape(b['label'])}</div>
        </div>
""")

        return f"""
    <div id="{self.chart_id}" class="chart-wrapper">
      <div class="chart-header">
        <h2 class="chart-title">{html.escape(self.title)}</h2>
        <p class="chart-subtitle">{html.escape(self.subtitle)}</p>
      </div>
      <div class="chart-canvas">
        {"".join(bars_html)}
      </div>
    </div>
"""

    def render_css(self) -> str:
        return """
    .chart-wrapper {
      position: absolute;
      left: 160px;
      top: 140px;
      width: 1600px;
      height: 780px;
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid rgba(56, 189, 248, 0.2);
      border-radius: 24px;
      padding: 60px 80px;
      backdrop-filter: blur(20px);
      box-shadow: 0 20px 50px rgba(0,0,0,0.6);
      display: flex;
      flex-direction: column;
    }
    .chart-header {
      margin-bottom: 40px;
    }
    .chart-title {
      font-size: 48px;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin: 0 0 10px 0;
      color: #f8fafc;
    }
    .chart-subtitle {
      font-size: 22px;
      color: #94a3b8;
      margin: 0;
    }
    .chart-canvas {
      flex: 1;
      display: flex;
      align-items: flex-end;
      gap: 40px;
      border-bottom: 2px solid #334155;
      padding-bottom: 20px;
    }
    .chart-col {
      flex: 1;
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-end;
    }
    .col-bar-track {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: flex-end;
      justify-content: center;
    }
    .col-bar-fill {
      width: 80px;
      height: 0%;
      border-radius: 12px 12px 0 0;
      position: relative;
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
    }
    .bar-val-badge {
      position: absolute;
      top: -45px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 20px;
      font-weight: 700;
      color: #f8fafc;
      white-space: nowrap;
      opacity: 0;
    }
    .col-label {
      margin-top: 18px;
      font-size: 20px;
      font-weight: 600;
      color: #cbd5e1;
    }
"""

    def render_gsap(self) -> str:
        lines = [f"""
    // Chart container fade & rise
    tl.from('#{self.chart_id}', {{
      opacity: 0,
      y: 40,
      duration: 0.8,
      ease: 'power3.out'
    }}, {self.start_time});
"""]
        t = self.start_time + 0.3
        for i, b in enumerate(self.bars):
            height_pct = round((b["value"] / b["max"]) * 100, 1)
            lines.append(f"""
    // Bar #{i} grow
    tl.to('#bar-fill-{i}', {{
      height: '{height_pct}%',
      duration: 1.2,
      ease: 'elastic.out(1, 0.75)'
    }}, {round(t, 2)});
    
    tl.to('#bar-val-{i}', {{
      opacity: 1,
      y: -5,
      duration: 0.5,
      ease: 'power2.out'
    }}, {round(t + 0.3, 2)});
""")
            t += 0.15

        return "\n".join(lines)


class MetricCounter:
    def __init__(self, element_id: str, label: str, target_val: int, prefix: str = "", suffix: str = "", x: int = 200, y: int = 200):
        self.element_id = element_id
        self.label = label
        self.target_val = target_val
        self.prefix = prefix
        self.suffix = suffix
        self.x = x
        self.y = y

    def render_html(self) -> str:
        return f"""
    <div id="{self.element_id}" class="metric-counter-box" style="left:{self.x}px; top:{self.y}px;">
      <div id="{self.element_id}-val" class="metric-num">0</div>
      <div class="metric-label">{html.escape(self.label)}</div>
    </div>
"""

    def render_css(self) -> str:
        return """
    .metric-counter-box {
      position: absolute;
      background: #0f172a;
      border: 1px solid #334155;
      padding: 30px 45px;
      border-radius: 20px;
      text-align: center;
      min-width: 280px;
    }
    .metric-num {
      font-size: 64px;
      font-weight: 800;
      color: #38bdf8;
      font-family: monospace;
    }
    .metric-label {
      font-size: 20px;
      color: #94a3b8;
      margin-top: 8px;
    }
"""

    def render_gsap(self, at: float = 0.5, duration: float = 2.0) -> str:
        return f"""
    // Metric counter count-up
    {{
      let obj = {{ val: 0 }};
      tl.to(obj, {{
        val: {self.target_val},
        duration: {duration},
        ease: 'power3.out',
        onUpdate: function() {{
          const el = document.getElementById('{self.element_id}-val');
          if (el) el.innerText = '{self.prefix}' + Math.round(obj.val).toLocaleString() + '{self.suffix}';
        }}
      }}, {at});
    }}
"""
