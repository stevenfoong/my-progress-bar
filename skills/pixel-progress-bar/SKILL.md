---
name: pixel-progress-bar
description: Add an animated pixel-art "journey" progress bar to a video. A hero in a purple cape walks from a village house to an evil castle in step with the video's time, and at each milestone (default every minute) he passes props, defeats enemies (goblin, slime, dragon boss) or gains partners (mage, knight) who follow him. Use when the user wants a progress bar, timeline or journey bar on a video, wants it burned in or as a transparent overlay for an editor (FilmCraft, Premiere and so on), wants a short fast-forward showcase clip of the bar, or wants the pixel sprites (hero, house, castle, goblin, slime, camp, signpost, warning sign, dragon, mage, knight) as PNG or GIF.
---

# Pixel progress bar

Everything is drawn in code at tiny native size (about 30 px tall) and scaled up
by whole numbers, so the sprites stay crisp when small. Do not swap in AI
images that have been scaled down: they turn to mush at progress-bar size.

Scripts (Python 3 + Pillow; rendering also needs `ffmpeg`/`ffprobe`):
- `scripts/progressbar.py`: the bar. Subcommands: `story`, `detect`, `still`, `burn`, `overlay`, `showcase`, `frame`.
- `scripts/sprites.py`: all sprites. `python3 sprites.py OUTDIR --scale 1 3 4` exports PNGs and GIF loops.
- `presets/magazine-1080p.json`: layout for the owner's 1080p "magazine" video template (gold border, line at y=1042). It matches the defaults.
- `reference/config.md`: every config key, the items and how to add new ones.

Below, `$SKILL` is the directory that holds this file.

## Workflow

1. **Probe and plan.** `python3 $SKILL/scripts/progressbar.py story --duration <seconds>` prints the
   milestone plan. The default is one item per full minute, dragon last; a mark within 10 s of the end is dropped.
   Agree on the story with the user if they care: `--story signpost,goblin,mage,...`, or exact
   times through `"milestones"` in a config.
2. **Find the line to walk on.** For the owner's template, use `--config $SKILL/presets/magazine-1080p.json`.
   For a new layout, run `progressbar.py detect VIDEO --color '#rrggbb'`. It prints `line_y`, `line_thickness` and `line_x`
   (in 1080p reference units) to put in a config JSON. If the video has no line, set `"dim_line": false`
   and pick `line_y` (the ground row) yourself.
3. **Preview before rendering.** `progressbar.py still VIDEO --config CFG --time 5 125 300 480 --out chk.png`
   writes `chk_<t>.png`. Look at them: feet on the line, nothing cut off at the edges, enemies sitting just past their minute mark.
4. **Render.**
   - Burned in: `progressbar.py burn VIDEO --config CFG --out out.mp4`. Keeps the audio, H.264 CRF 18.
   - Overlay for an editor: `progressbar.py overlay VIDEO --config CFG --out bar.mov`. ProRes 4444 with alpha,
     full frame by default, about 2.3 GB for 8 min at 1080p. `--strip` renders only the bar band (about 5× smaller) and prints the y to place it at.
     In FilmCraft: `file.import` it, then `timeline.place` it on V2 above the footage on V1.
   - Social clip: `progressbar.py showcase --duration <video seconds> --length 30 --out showcase.mp4`.
     The story is fast-forwarded, but the walking and effects play at normal speed. It includes a `mm:ss / mm:ss` timer (`--no-timer` to hide it).
5. **Verify.** Extract a few frames from the result (`ffmpeg -ss T -i out.mp4 -frames:v 1 f.png`) around milestones
   and look at them before reporting success. Check that the output duration matches the input.

Speed reference: 8:21 at 1080p25 burns in about 2.5 min on 4 vCPU. The ProRes overlay is slower, about 3× real time.
If the project says heavy work runs on a remote machine (for example a CLAUDE.md with EC2 rules), copy
`$SKILL/scripts`, the config and the video there. The machine needs only `python3`, `python3-pil` and `ffmpeg`.
Run the job under `nohup` or `tmux` and pull back only the result.

## Story rules (built in)

- **Props** (`signpost`, `camp`, `warning_sign`) sit at their mark; the party walks past them.
- **Enemies** (`goblin`, `slime`, `dragon`) are placed so the hero's sword touches them exactly at the mark. They blink for about 1 s,
  burst into a puff of smoke and leave a sparkling coin as a permanent marker.
- **Partners** (`mage`, `knight`) wait at their mark facing the hero. Once he passes, they walk behind him, one partner every 16 sprite pixels.
- The hero's position is linear in time. The part of the line not yet travelled is dimmed and dashed (`dim_line`).
- `auto_story(n)` keeps the story readable for any number of marks: it starts calm, puts the dragon last, and adds extra goblins and slimes for long videos.

## Gotchas

- Scale only by whole numbers (`scale` is the sprite pixel size at 1080p; it is rescaled for other heights).
- Keep the house and castle inside the frame. For a non-16:9 video, set `house_x`, `castle_x`, `x_start` and `x_end`.
- The script exits non-zero if ffmpeg fails. Still check the output frames: a missing overlay is easy to miss.
