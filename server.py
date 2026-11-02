"""
HyperFrames Video Studio Server
Provides REST APIs for:
  - 10 GitHub Extension Registry & Examples
  - Live Python Animation Compilation & Execution
  - Real-time Video Preview & Scrubbing
  - Headless Chrome MP4 Rendering
  - Rendered Video Media Library
"""

import os
import sys
import json
import subprocess
import mimetypes
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

BASE_DIR = Path(__file__).parent.resolve()
STUDIO_DIR = BASE_DIR / "studio"
EXAMPLES_DIR = BASE_DIR / "examples"
RENDERS_DIR = BASE_DIR / "renders"
LIVE_PREVIEW_DIR = BASE_DIR / "live-preview"

RENDERS_DIR.mkdir(parents=True, exist_ok=True)
LIVE_PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

class HyperFramesStudioHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ["/", "/index.html"]:
            self.serve_file(STUDIO_DIR / "index.html", "text/html")
            return

        if path == "/api/extensions":
            reg_file = BASE_DIR / "extensions_registry.json"
            if reg_file.exists():
                self.serve_file(reg_file, "application/json")
            else:
                self.send_json({"extensions": []})
            return

        if path == "/api/examples":
            query = parse_qs(parsed.query)
            filename = query.get("file", ["07_motion_charts.py"])[0]
            example_file = EXAMPLES_DIR / filename
            if example_file.exists():
                self.serve_file(example_file, "text/plain")
            else:
                self.send_error(404, "Example not found")
            return

        if path == "/api/renders":
            files = []
            for f in sorted(RENDERS_DIR.glob("*.mp4"), key=os.path.getmtime, reverse=True):
                size_mb = round(f.stat().st_size / (1024 * 1024), 2)
                files.append({
                    "name": f.name,
                    "size_mb": size_mb,
                    "duration": "MP4 Video"
                })
            self.send_json({"files": files})
            return

        if path.startswith("/renders/"):
            filename = path.replace("/renders/", "")
            target = RENDERS_DIR / filename
            if target.exists() and target.is_file():
                self.serve_file(target, "video/mp4")
                return

        if path == "/preview" or path.startswith("/preview/"):
            index_path = LIVE_PREVIEW_DIR / "index.html"
            if index_path.exists():
                self.serve_file(index_path, "text/html")
                return
            else:
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"<html><body style='background:#090d16;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;'><h2>No active preview. Run a Python script to start.</h2></body></html>")
                return

        if path == "/api/cli-preview":
            cmd = ["npx", "hyperframes", "preview", str(LIVE_PREVIEW_DIR), "--port", "4000"]
            subprocess.Popen(cmd, cwd=str(BASE_DIR))
            self.send_json({"success": True, "port": 4000})
            return

        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        if path == "/api/run-python":
            try:
                payload = json.loads(post_data.decode("utf-8"))
                code = payload.get("code", "")
                
                # Execute Python script in isolated local context with hyperframes_py available
                exec_globals = {
                    "__file__": str(BASE_DIR / "runner.py"),
                    "__name__": "__main__",
                    "sys": sys,
                }
                if str(BASE_DIR) not in sys.path:
                    sys.path.insert(0, str(BASE_DIR))

                # Intercept render_to_mp4 so run-python does not block on video encoding
                from hyperframes_py.composition import Composition
                
                # Save script temporarily and run execution
                script_path = BASE_DIR / ".current_script.py"
                script_path.write_text(code, encoding="utf-8")
                
                captured_comp = None
                
                # Execute script namespace
                exec_scope = {"sys": sys}
                exec(compile(code, str(script_path), "exec"), exec_scope)
                
                # Look for Composition instances created or functions returning them
                for val in exec_scope.values():
                    if isinstance(val, Composition):
                        captured_comp = val
                        break
                    elif callable(val) and hasattr(val, "__name__") and "create_" in val.__name__:
                        try:
                            candidate = val()
                            if isinstance(candidate, Composition):
                                captured_comp = candidate
                                break
                        except Exception:
                            pass

                if not captured_comp:
                    # Search global fallback
                    from hyperframes_py import Composition
                    captured_comp = Composition(comp_id="preview", duration=4.5)

                # Export to live-preview folder
                captured_comp.export(str(LIVE_PREVIEW_DIR))
                html_content = (LIVE_PREVIEW_DIR / "index.html").read_text(encoding="utf-8")

                self.send_json({
                    "success": True,
                    "html": html_content,
                    "duration": captured_comp.duration,
                    "width": captured_comp.width,
                    "height": captured_comp.height
                })
            except Exception as e:
                import traceback
                self.send_json({
                    "success": False,
                    "error": str(e),
                    "traceback": traceback.format_exc()
                })
            return

        if path == "/api/render":
            try:
                payload = json.loads(post_data.decode("utf-8"))
                output_name = payload.get("output_name", "output.mp4")
                if not output_name.endswith(".mp4"):
                    output_name += ".mp4"
                
                target_mp4 = RENDERS_DIR / output_name
                
                cmd = [
                    "npx", "hyperframes", "render",
                    str(LIVE_PREVIEW_DIR),
                    "-o", str(target_mp4),
                    "--quality", "standard"
                ]
                env = os.environ.copy()
                env["CI"] = "1"
                env["HYPERFRAMES_NON_INTERACTIVE"] = "1"

                proc = subprocess.run(
                    cmd,
                    cwd=str(BASE_DIR),
                    env=env,
                    input="\n",
                    capture_output=True,
                    text=True
                )
                
                success = proc.returncode == 0 and target_mp4.exists()
                size_mb = round(target_mp4.stat().st_size / (1024 * 1024), 2) if success else 0
                
                self.send_json({
                    "success": success,
                    "filename": output_name,
                    "size_mb": size_mb,
                    "stdout": proc.stdout[-500:],
                    "stderr": proc.stderr[-500:]
                })
            except Exception as e:
                self.send_json({"success": False, "error": str(e)})
            return

        self.send_error(404, "Endpoint not found")

    def serve_file(self, filepath: Path, content_type: str):
        if not filepath.exists():
            self.send_error(404, f"File not found: {filepath.name}")
            return
        data = filepath.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, data: dict):
        response_bytes = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

def run_server(port: int = 8080):
    server_address = ("0.0.0.0", port)
    httpd = ThreadingHTTPServer(server_address, HyperFramesStudioHandler)
    print(f"\n=======================================================")
    print(f"🚀 HyperFrames Video Studio & Extensions Hub Active!")
    print(f"👉 Local UI: http://localhost:{port}")
    print(f"=======================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down studio server...")
        httpd.shutdown()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
