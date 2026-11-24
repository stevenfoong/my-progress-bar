# my-progress-bar

An animated **pixel-art journey progress bar** for videos, packaged as a Claude Code skill and plugin.

A hero in a purple cape walks from a village house to an evil castle in step with the video's time.
At every milestone (default: every minute) something happens: he passes a signpost and a camp,
defeats a goblin, a slime and finally a dragon, and gains a mage and a knight who follow him to the castle.

![sprites](docs/sprites.png)

![bar at 5:00](docs/bar-5min.png)

![walk cycle](docs/hero-walk.gif) · 30-second fast-forward demo: [docs/showcase-30s.mp4](docs/showcase-30s.mp4)

All sprites are drawn in code at their native size (about 30 px tall) and only scaled up by whole numbers, so they stay crisp at progress-bar size.

## Install

**As a plugin, in any project (Claude Code):**

```
/plugin install pixel-progress-bar --marketplace stevenfoong/my-progress-bar
```

On older versions, run `/plugin marketplace add stevenfoong/my-progress-bar` and then `/plugin install pixel-progress-bar@my-progress-bar`.

**In a session that has this repo:** Claude Code loads the skill from `.claude/skills/` automatically,
for example in a Claude Code on the web session with this repository attached.

Then just ask: *"add the pixel progress bar to video.mp4"*, *"make a 30-second showcase of the bar"*, or
*"export the progress bar as a transparent overlay for FilmCraft"*.

## Use without Claude

Requires Python 3, Pillow and ffmpeg.

```bash
S=skills/pixel-progress-bar/scripts
python3 $S/progressbar.py story --duration 501.8                       # milestone plan
python3 $S/progressbar.py detect video.mp4 --color '#d4ab58'           # find the line to walk on
python3 $S/progressbar.py still video.mp4 --time 5 125 300 --out chk.png
python3 $S/progressbar.py burn video.mp4 --out video-with-bar.mp4      # burned in, audio kept
python3 $S/progressbar.py overlay video.mp4 --out bar.mov              # ProRes 4444 with alpha, for editors
python3 $S/progressbar.py showcase --duration 501.8 --length 30 --out showcase.mp4
python3 $S/sprites.py sprites_out --scale 1 3 4                        # PNG and GIF sprites
```

Layout and story options (line position, scale, custom milestones) are described in
[skills/pixel-progress-bar/reference/config.md](skills/pixel-progress-bar/reference/config.md).

## Layout

```
.claude-plugin/          plugin + marketplace manifests
skills/pixel-progress-bar/
  SKILL.md               instructions Claude follows
  scripts/               progressbar.py, sprites.py
  presets/               magazine-1080p.json (layout of the original video template)
  reference/config.md    config keys, items, how to add sprites
.claude/skills/pixel-progress-bar -> ../../skills/pixel-progress-bar   (auto-load when working in this repo)
docs/                    previews
```

License: GPL-3.0.
