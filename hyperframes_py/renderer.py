"""
Renderer module for HyperFrames Python framework.
Drives headless rendering to MP4 and opens live previews.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from .composition import Composition

def render_to_mp4(
    composition: Composition,
    output_path: str = "renders/output.mp4",
    quality: str = "standard",
    fps: Optional[int] = None,
    work_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Exports composition and renders to MP4 using the HyperFrames rendering engine.
    """
    target_mp4 = Path(output_path).resolve()
    target_mp4.parent.mkdir(parents=True, exist_ok=True)
    
    if work_dir is None:
        work_dir = str(target_mp4.parent / f".tmp_{composition.comp_id}")
    
    comp_dir = Path(work_dir)
    comp_dir.mkdir(parents=True, exist_ok=True)
    
    composition.export(str(comp_dir))
    
    cmd = [
        "npx", "hyperframes", "render",
        str(comp_dir),
        "-o", str(target_mp4),
        "--quality", quality
    ]
    if fps:
        cmd.extend(["--fps", str(fps)])

    # Add environment variables to ensure non-interactive headless render
    env = os.environ.copy()
    env["CI"] = "1"
    env["HYPERFRAMES_NON_INTERACTIVE"] = "1"

    print(f"🎬 HyperFrames rendering '{composition.comp_id}' -> {target_mp4}...")
    
    # Run subprocess feeding empty stdin so it does not block on ratings
    process = subprocess.run(
        cmd,
        cwd=os.getcwd(),
        env=env,
        input="\n",
        capture_output=True,
        text=True
    )
    
    success = process.returncode == 0 and target_mp4.exists()
    size_bytes = target_mp4.stat().st_size if success else 0
    
    return {
        "success": success,
        "output_file": str(target_mp4),
        "size_bytes": size_bytes,
        "size_mb": round(size_bytes / (1024 * 1024), 2),
        "duration": composition.duration,
        "stdout": process.stdout,
        "stderr": process.stderr,
        "returncode": process.returncode
    }

def preview_composition(composition: Composition, port: int = 4000) -> None:
    """Exports composition and starts HyperFrames preview studio."""
    comp_dir = Path(f".preview_{composition.comp_id}")
    comp_dir.mkdir(parents=True, exist_ok=True)
    composition.export(str(comp_dir))
    
    cmd = ["npx", "hyperframes", "preview", str(comp_dir), "--port", str(port)]
    print(f"🚀 Launching HyperFrames preview on port {port}...")
    subprocess.Popen(cmd)
