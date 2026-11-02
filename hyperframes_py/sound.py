"""
Sound Derived from Motion module for HyperFrames.
Inspired by AgentsORG/design-engineering (sound-sheet.mjs & sound-from-motion).
Derives acoustic properties from geometric motion:
  - Element size -> Pitch (bigger = lower frequency thud, smaller = crisp click)
  - Element X position -> Stereo pan (-1.0 to +1.0)
  - Contact frame -> Transient impact
Synthesizes zero-dependency procedural audio directly inside the browser using Web Audio API.
"""

from typing import List, Dict, Any, Optional

class SoundCue:
    def __init__(self, name: str, at: float, cue_type: str = "click", frequency: float = 440.0, volume: float = 0.5, pan: float = 0.0):
        self.name = name
        self.at = at
        self.cue_type = cue_type  # 'thud', 'click', 'tick', 'swoosh'
        self.frequency = frequency
        self.volume = volume
        self.pan = pan

class SoundTrack:
    def __init__(self):
        self.cues: List[SoundCue] = []

    def add_cue(self, name: str, at: float, cue_type: str = "click", size_px: float = 100.0, x_pos: float = 960.0, width: float = 1920.0):
        """
        Derives sound properties from physical motion parameters:
        - Size translates to base frequency (100px -> 600Hz, 800px -> 80Hz)
        - Screen X position translates to stereo pan (-1.0 to 1.0)
        """
        # Pitch derived from size
        norm_size = min(max(size_px / 1000.0, 0.05), 1.0)
        freq = 80.0 + (1.0 - norm_size) * 750.0
        
        # Stereo pan from X coordinate
        pan = (x_pos / width) * 2.0 - 1.0
        pan = max(-1.0, min(1.0, pan))
        
        cue = SoundCue(name=name, at=at, cue_type=cue_type, frequency=round(freq, 1), pan=round(pan, 2))
        self.cues.append(cue)
        return self

    def render_audio_tags(self) -> str:
        # Generates procedural WebAudio synthesis engine
        return f"""
    <!-- Procedural Motion Sound Synthesis Engine -->
    <script>
      (function() {{
        let audioCtx = null;
        function getAudioContext() {{
          if (!audioCtx) {{
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            audioCtx = new AudioContext();
          }}
          return audioCtx;
        }}
        
        window.playProceduralSound = function(type, freq, pan, vol) {{
          try {{
            const ctx = getAudioContext();
            if (ctx.state === 'suspended') ctx.resume();
            
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            const panner = ctx.createStereoPanner ? ctx.createStereoPanner() : null;
            
            osc.frequency.setValueAtTime(freq || 440, ctx.currentTime);
            
            if (type === 'thud') {{
              osc.type = 'triangle';
              osc.frequency.exponentialRampToValueAtTime(30, ctx.currentTime + 0.18);
              gain.gain.setValueAtTime(vol || 0.6, ctx.currentTime);
              gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.22);
            }} else if (type === 'click') {{
              osc.type = 'sine';
              osc.frequency.exponentialRampToValueAtTime(freq * 0.4, ctx.currentTime + 0.04);
              gain.gain.setValueAtTime(vol || 0.4, ctx.currentTime);
              gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.06);
            }} else if (type === 'tick') {{
              osc.type = 'highpass';
              gain.gain.setValueAtTime(0.2, ctx.currentTime);
              gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.03);
            }} else {{
              osc.type = 'sine';
              gain.gain.setValueAtTime(vol || 0.3, ctx.currentTime);
              gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.15);
            }}
            
            if (panner) {{
              panner.pan.setValueAtTime(pan || 0, ctx.currentTime);
              osc.connect(gain);
              gain.connect(panner);
              panner.connect(ctx.destination);
            }} else {{
              osc.connect(gain);
              gain.connect(ctx.destination);
            }}
            
            osc.start();
            osc.stop(ctx.currentTime + 0.25);
          }} catch (e) {{
            // Safe fallback if audio is muted or headless
          }}
        }};
      }})();
    </script>
"""

    def render_gsap(self) -> str:
        lines = []
        for cue in self.cues:
            lines.append(f"""
    // Sound cue derived from motion: {cue.name} ({cue.cue_type} @ {cue.frequency}Hz, pan={cue.pan})
    tl.call(() => {{
      if (window.playProceduralSound) {{
        window.playProceduralSound('{cue.cue_type}', {cue.frequency}, {cue.pan}, {cue.volume});
      }}
    }}, null, {cue.at});
""")
        return "\n".join(lines)
