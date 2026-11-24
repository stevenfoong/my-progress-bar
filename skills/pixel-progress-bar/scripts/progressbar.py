#!/usr/bin/env python3
"""Pixel-art "journey" progress bar for videos.

A hero walks from a village house to an evil castle in step with the video's
time. At every milestone (default: every minute) something happens on the way:
props to pass, enemies that are defeated, partners who join the party.

Subcommands (all need Pillow; everything except `frame` and `story` also needs ffmpeg/ffprobe):
  story     print the milestone plan for a duration (no rendering)
  detect    find a horizontal line (e.g. a yellow border) in a video frame -> config values
  still     composite the bar over the video at one time -> PNG (check layout before rendering)
  burn      render the bar into the video -> MP4 (keeps audio)
  overlay   render the bar alone with transparency -> ProRes 4444 .mov (for an editor such as FilmCraft)
  showcase  fast-forward of the bar alone on a plain background -> MP4 (for social posts)
  frame     render one standalone bar frame -> PNG (no video needed)

Layout values in the config are in 1920x1080 reference pixels and are scaled to
the real video size. See ../reference/config.md for every key.
"""
import argparse, json, math, os, subprocess, sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sprites as SPR

# ---------------------------------------------------------------- config
DEFAULTS = {
    "line_y": 1042,            # top row of the line the characters walk on
    "line_thickness": 4,
    "line_x": [98, 1820],      # extent of the line (for dimming the untravelled part)
    "dim_line": True,          # dim + dash the part of the line not travelled yet
    "line_color": "#d4ab58",   # used by `showcase`/`frame` to draw the line, and by `detect`
    "dim_color": "#464460",
    "dash_color": "#68688a",
    "x_start": 165,            # hero position at t=0
    "x_end": 1700,             # hero position at the end
    "house_x": 72,
    "castle_x": 1850,
    "scale": 3,                # sprite pixel size at 1080p
    "interval": 60,            # seconds between milestones
    "min_end_gap": 10,         # drop a milestone closer than this to the end
    "story": None,             # list of item names, or null for the automatic story
    "milestones": None,        # explicit [{"time": s, "item": name}], overrides interval/story
    "background": "#232a45",   # showcase / frame background
}

ITEMS = {
    "signpost":     {"kind": "prop", "frames": ["signpost"]},
    "warning_sign": {"kind": "prop", "frames": ["warning_sign"]},
    "camp":         {"kind": "prop", "frames": [f"camp_{i}" for i in range(4)], "dt": 0.18},
    "goblin":       {"kind": "enemy", "frames": ["goblin_0", "goblin_1"], "dt": 0.35},
    "slime":        {"kind": "enemy", "frames": [f"slime_{i}" for i in (0, 0, 0, 0, 1, 2, 3, 4, 5, 0, 0, 0)], "dt": 0.12},
    "dragon":       {"kind": "enemy", "frames": [f"dragon_{i}" for i in range(4)], "dt": 0.18},
    "mage":         {"kind": "partner"},
    "knight":       {"kind": "partner"},
}
DEFAULT_STORY = ["signpost", "goblin", "mage", "slime", "camp", "knight", "warning_sign", "dragon"]


def auto_story(n):
    """Pick n items that still read as a story: start calm, dragon last."""
    if n <= 0: return []
    if n == 1: return ["dragon"]
    base = DEFAULT_STORY
    if n <= len(base):
        idx = [round(i * (len(base) - 1) / (n - 1)) for i in range(n)]
        return [base[i] for i in idx]
    extra = ["goblin", "slime"] * n
    return base[:-1] + extra[: n - len(base)] + ["dragon"]


def hexc(s):
    s = s.lstrip("#"); return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def load_config(path, overrides):
    cfg = dict(DEFAULTS)
    if path:
        with open(path) as f: cfg.update(json.load(f))
    cfg.update({k: v for k, v in overrides.items() if v is not None})
    return cfg


# ---------------------------------------------------------------- the bar
class Bar:
    def __init__(self, cfg, duration, width=1920, height=1080, fps=25):
        self.cfg, self.T, self.W, self.H, self.fps = cfg, float(duration), width, height, fps
        kx, ky = width / 1920, height / 1080
        self.S = max(1, round(cfg["scale"] * ky))
        S = self.S
        self.line_y = round(cfg["line_y"] * ky)
        self.ground_abs = self.line_y + 1                     # feet rest on the line
        above, below = 61 * S, min(height - self.ground_abs, 13 * S)
        self.y0 = max(0, self.ground_abs - above) // 2 * 2
        self.h = min(height - self.y0, (self.ground_abs - self.y0 + below + 1) // 2 * 2)
        self.ground = self.ground_abs - self.y0
        self.thick = max(1, round(cfg["line_thickness"] * ky))
        self.lx = [round(v * kx) for v in cfg["line_x"]]
        self.xs, self.xe = cfg["x_start"] * kx, cfg["x_end"] * kx
        self.house_x, self.castle_x = cfg["house_x"] * kx, cfg["castle_x"] * kx
        self.native = SPR.build_all()
        self.cache = {}
        self.hero_front = 10 * S
        self.milestones = self._plan()

    # ---- plan
    def _plan(self):
        c = self.cfg
        if c.get("milestones"):
            ms = [(float(m["time"]), m["item"]) for m in c["milestones"]]
        else:
            times, t = [], c["interval"]
            while t <= self.T - c["min_end_gap"]: times.append(t); t += c["interval"]
            story = c.get("story") or auto_story(len(times))
            ms = list(zip(times, story))
        for _, it in ms:
            if it not in ITEMS: raise SystemExit(f"unknown item {it!r}; choose from {sorted(ITEMS)}")
        out, nth = [], 0
        for tm, it in sorted(ms):
            m = {"time": tm, "item": it, "kind": ITEMS[it]["kind"], "x": self.X(tm)}
            if m["kind"] == "enemy":
                _, bb = self.spr(ITEMS[it]["frames"][0])
                m["x"] = m["x"] + self.hero_front + (bb[2] - bb[0]) / 2 * self.S - 2 * self.S
            if m["kind"] == "partner":
                nth += 1; m["offset"] = 16 * self.S * nth
            out.append(m)
        return out

    def X(self, t):
        return self.xs + (self.xe - self.xs) * min(max(t, 0), self.T) / self.T

    def spr(self, name):
        if name not in self.cache:
            im = self.native[name]
            self.cache[name] = (im.resize((im.width * self.S, im.height * self.S), Image.NEAREST), im.getbbox())
        return self.cache[name]

    def put(self, c, name, cx, anchor_x=None, ground_row=None):
        im, bb = self.spr(name)
        ax = (anchor_x if anchor_x is not None else (bb[0] + bb[2]) / 2) * self.S
        gr = (ground_row if ground_row is not None else bb[3]) * self.S
        c.alpha_composite(im, (int(cx - ax), int(self.ground - gr)))

    # ---- one frame
    def frame(self, t, bg=None, a=None, speed=1.0):
        """t = story time (video seconds); a = animation clock; speed = story s per real s."""
        a = t if a is None else a
        S, c = self.S, (bg.copy() if bg else Image.new("RGBA", (self.W, self.h), (0, 0, 0, 0)))
        d = ImageDraw.Draw(c)
        hx = self.X(t)
        if self.cfg["dim_line"]:
            y0 = self.line_y - self.y0; y1 = y0 + self.thick - 1; la, lb = self.lx
            if hx < lb:
                d.rectangle([max(la, int(hx)), y0, lb, y1], fill=hexc(self.cfg["dim_color"]))
                step = 14 * S // 3
                for x in range(int(hx) + 2 * S, lb, step):
                    d.rectangle([x, y0 + 1, min(lb, x + 5 * S // 3), max(y0 + 1, y1 - 1)], fill=hexc(self.cfg["dash_color"]))
        self.put(c, "house", self.house_x)
        self.put(c, "castle", self.castle_x)
        wf = int(a / 0.12 + 1e-6) % 8
        partners = []
        for m in self.milestones:
            it, kind, tm, x = m["item"], m["kind"], m["time"], m["x"]
            spec = ITEMS[it]
            if kind == "prop":
                fr = spec["frames"]; self.put(c, fr[int(a / spec.get("dt", 1)) % len(fr)], x)
            elif kind == "enemy":
                fr = spec["frames"]; g = self.spr(fr[0])[1][3]
                if t < tm:
                    if t > tm - 1.0 * speed and int(a * 25) % 4 < 2: continue     # hit flash
                    self.put(c, fr[int(a / spec["dt"]) % len(fr)], x, ground_row=g)
                else:
                    k = int((t - tm) / (0.1 * speed))
                    if k < 5: self.put(c, f"puff_{k}", x, ground_row=20)
                    else: self.put(c, f"coin_{int(a / 0.5) % 2}", x)
            else:
                partners.append(m)
        for m in reversed(partners):
            name, off = m["item"], m["offset"]
            if hx - off >= m["x"]:
                self.put(c, f"{name}_walk_{(wf + 3 * (off // (16 * S))) % 8}", hx - off, 14, 34)
            else:
                self.put(c, f"{name}_idle_{int(a / 0.5) % 2}", m["x"], 17, 34)
        self.put(c, f"hero_walk_{wf}", hx, 14, 34)
        return c

    def base_strip(self):
        """Plain background with the line drawn (for standalone renders)."""
        bg = Image.new("RGBA", (self.W, self.h), hexc(self.cfg["background"]))
        y0 = self.line_y - self.y0
        ImageDraw.Draw(bg).rectangle([self.lx[0], y0, self.lx[1], y0 + self.thick - 1], fill=hexc(self.cfg["line_color"]))
        return bg


# ---------------------------------------------------------------- video helpers
def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate:format=duration", "-of", "json", path],
                       capture_output=True, text=True, check=True)
    j = json.loads(r.stdout); s = j["streams"][0]
    n, dd = s["r_frame_rate"].split("/")
    return float(j["format"]["duration"]), int(s["width"]), int(s["height"]), float(n) / float(dd)


def grab(path, t, w, h):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1",
                        "-f", "rawvideo", "-pix_fmt", "rgba", "pipe:1"], capture_output=True, check=True)
    return Image.frombytes("RGBA", (w, h), r.stdout)


def stream_frames(bar, n, write):
    for i in range(n):
        write(bar.frame(i / bar.fps).tobytes())


def run_pipe(bar, n, ffargs):
    p = subprocess.Popen(ffargs, stdin=subprocess.PIPE)
    try:
        stream_frames(bar, n, p.stdin.write)
    finally:
        p.stdin.close()
    if p.wait() != 0: raise SystemExit("ffmpeg failed")


def raw_in(bar):
    return ["-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{bar.W}x{bar.h}", "-r", str(bar.fps), "-i", "pipe:0"]


# ---------------------------------------------------------------- commands
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, video=True):
        if video: p.add_argument("video")
        p.add_argument("--config", help="JSON config (see reference/config.md)")
        p.add_argument("--story", help="comma-separated items in milestone order")
        p.add_argument("--interval", type=float)
        p.add_argument("--scale", type=int)
        p.add_argument("--line-y", type=int, dest="line_y")
        p.add_argument("--no-dim", action="store_const", const=False, dest="dim_line")

    p = sub.add_parser("story", help="print the milestone plan"); common(p, video=False)
    p.add_argument("--duration", type=float, required=True)
    p = sub.add_parser("detect", help="find the line to walk on")
    p.add_argument("video"); p.add_argument("--time", type=float, default=30)
    p.add_argument("--color", default="#d4ab58"); p.add_argument("--tolerance", type=int, default=45)
    p = sub.add_parser("still", help="preview frame(s) over the video"); common(p)
    p.add_argument("--time", type=float, nargs="+", required=True); p.add_argument("--out", required=True)
    p = sub.add_parser("burn", help="render the bar into the video"); common(p)
    p.add_argument("--out", required=True); p.add_argument("--crf", type=int, default=18)
    p.add_argument("--preset", default="medium")
    p = sub.add_parser("overlay", help="transparent ProRes 4444 overlay"); common(p)
    p.add_argument("--out", required=True)
    p.add_argument("--strip", action="store_true", help="only the bar strip, not full frame (prints its y)")
    p = sub.add_parser("showcase", help="fast-forward of the bar alone"); common(p, video=False)
    p.add_argument("--duration", type=float, required=True, help="story length in seconds (e.g. the video's)")
    p.add_argument("--length", type=float, default=30); p.add_argument("--out", required=True)
    p.add_argument("--fps", type=int, default=25); p.add_argument("--no-timer", action="store_true")
    p = sub.add_parser("frame", help="one standalone bar frame"); common(p, video=False)
    p.add_argument("--duration", type=float, required=True); p.add_argument("--time", type=float, required=True)
    p.add_argument("--out", required=True)
    a = ap.parse_args()

    if a.cmd == "detect":
        return detect(a)
    ov = {k: getattr(a, k, None) for k in ("interval", "scale", "line_y", "dim_line")}
    if getattr(a, "story", None): ov["story"] = [s.strip() for s in a.story.split(",")]
    cfg = load_config(a.config, ov)

    if a.cmd in ("story", "showcase", "frame"):
        bar = Bar(cfg, a.duration, fps=getattr(a, "fps", 25))
    else:
        T, W, H, fps = probe(a.video)
        bar = Bar(cfg, T, W, H, fps)
        print(f"video {W}x{H} {fps:g}fps {T:.1f}s; strip y={bar.y0} h={bar.h} scale={bar.S}", file=sys.stderr)

    if a.cmd == "story":
        for m in bar.milestones:
            print(f"{int(m['time'] // 60):02d}:{int(m['time'] % 60):02d}  {m['item']:<13} {m['kind']:<8} x={m['x']:.0f}")
    elif a.cmd == "still":
        root, ext = os.path.splitext(a.out)
        for t in a.time:
            bg = grab(a.video, t, bar.W, bar.H)
            bg.paste(bar.frame(t, bg.crop((0, bar.y0, bar.W, bar.y0 + bar.h))), (0, bar.y0))
            out = a.out if len(a.time) == 1 else f"{root}_{t:g}{ext}"
            bg.save(out); print(out)
    elif a.cmd == "burn":
        n = math.ceil(bar.T * bar.fps) + 1
        run_pipe(bar, n, ["ffmpeg", "-y", "-v", "warning", "-stats", "-i", a.video, *raw_in(bar),
                          "-filter_complex", f"[0:v][1:v]overlay=0:{bar.y0}:eof_action=pass:format=auto,format=yuv420p[v]",
                          "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf),
                          "-c:a", "copy", "-movflags", "+faststart", a.out])
    elif a.cmd == "overlay":
        n = math.ceil(bar.T * bar.fps)
        vf = [] if a.strip else ["-vf", f"pad={bar.W}:{bar.H}:0:{bar.y0}:color=black@0"]
        run_pipe(bar, n, ["ffmpeg", "-y", "-v", "warning", "-stats", *raw_in(bar), *vf,
                          "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", a.out])
        if a.strip: print(f"strip overlay: place at x=0 y={bar.y0}")
    elif a.cmd == "frame":
        bar.frame(a.time, bar.base_strip()).save(a.out)
    elif a.cmd == "showcase":
        showcase(a, bar)


def showcase(a, bar):
    intro, outro = 0.8, 2.0
    speed = bar.T / (a.length - intro - outro)
    W, H = bar.W, bar.H
    sy = (H - bar.h) // 2
    base = bar.base_strip()
    font = None
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/Library/Fonts/Arial Bold.ttf",
              "C:/Windows/Fonts/arialbd.ttf"):
        if os.path.exists(f): font = ImageFont.truetype(f, 40); break
    font = font or ImageFont.load_default()
    fmt = lambda s: f"{int(s) // 60:02d}:{int(s) % 60:02d}"
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "warning", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(a.fps), "-i", "pipe:0", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                          "-tune", "animation", "-pix_fmt", "yuv420p", "-movflags", "+faststart", a.out],
                         stdin=subprocess.PIPE)
    for i in range(int(a.length * a.fps)):
        ra = i / a.fps
        t = min(max(0.0, (ra - intro) * speed), bar.T)
        c = Image.new("RGBA", (W, H), hexc(bar.cfg["background"]))
        c.paste(bar.frame(t, base, a=ra, speed=speed), (0, sy))
        if not a.no_timer:
            ImageDraw.Draw(c).text((W - 110, sy + 20), f"{fmt(t)} / {fmt(bar.T)}", font=font,
                                   fill=(214, 200, 160, 255), anchor="ra")
        p.stdin.write(c.convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() != 0: raise SystemExit("ffmpeg failed")


def detect(a):
    T, W, H, _ = probe(a.video)
    im = grab(a.video, min(a.time, T / 2), W, H).convert("RGB")
    tc = hexc(a.color)[:3]; px = im.load()
    rows = []
    for y in range(int(H * 0.6), H):
        xs = [x for x in range(W) if all(abs(px[x, y][i] - tc[i]) <= a.tolerance for i in range(3))]
        if xs: rows.append((len(xs), y, xs[0], xs[-1]))
    if not rows: raise SystemExit("no line of that colour in the lower 40% of the frame; try --color / --tolerance / --time")
    best = max(rows)
    band = sorted(r[1] for r in rows if r[0] >= best[0] * 0.6 and abs(r[1] - best[1]) <= 8)
    ky, kx = 1080 / H, 1920 / W
    sugg = {"line_y": round(band[0] * ky), "line_thickness": max(1, round((band[-1] - band[0] + 1) * ky)),
            "line_x": [round(best[2] * kx), round(best[3] * kx)]}
    print(f"longest run: {best[0]}px at y={best[1]} x={best[2]}..{best[3]} (video pixels)", file=sys.stderr)
    print(json.dumps(sugg))


if __name__ == "__main__":
    main()
