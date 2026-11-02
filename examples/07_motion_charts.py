"""
Example 07: HyperFrames Motion Library Charts
Inspired by nutllwhy/hyperframes-motion-library (23 templates, charts to explainers).
Parameter-driven growing bar chart with dynamic metrics.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hyperframes_py import Composition, BarChartGrow, render_to_mp4

def create_chart_demo():
    comp = Composition(
        comp_id="chart_demo",
        duration=4.5,
        background="#0a0f1d",
        title="Motion Library Data Visualization"
    )

    chart = BarChartGrow(
        chart_id="revenue-chart",
        title="Annual Recurring Revenue (ARR)",
        subtitle="Live Animated Bar Chart Growth Template"
    )
    chart.add_bar("Q1 2025", 28, max_val=100, color="#60a5fa", prefix="$", suffix="M")
    chart.add_bar("Q2 2025", 45, max_val=100, color="#38bdf8", prefix="$", suffix="M")
    chart.add_bar("Q3 2025", 68, max_val=100, color="#818cf8", prefix="$", suffix="M")
    chart.add_bar("Q4 2025", 94, max_val=100, color="#34d399", prefix="$", suffix="M")

    comp.add_style(chart.render_css())
    comp.add_html(chart.render_html())
    comp.animate(chart.render_gsap())

    return comp

if __name__ == "__main__":
    comp = create_chart_demo()
    out = "renders/07_motion_charts.mp4"
    print(f"Rendering Motion Charts demo to {out}...")
    res = render_to_mp4(comp, output_path=out, quality="draft")
    print("Result:", res)
