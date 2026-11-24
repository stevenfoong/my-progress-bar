---
name: pixel-progress-bar
description: Add an animated pixel-art "journey" progress bar to a video. A hero in a purple cape walks from a village house to an evil castle in step with the video's time, and at each milestone (every 1, 2, 3, 5 or 10 minutes, at most 10 milestones) he passes places, defeats enemies or gains partners who follow him, ending with a dragon boss. The library has 22 components. Use when the user wants a progress bar, timeline or journey bar on a video, wants it burned in or as a transparent overlay for an editor (FilmCraft, Premiere and so on), wants a short fast-forward showcase clip of the bar, or wants the pixel sprites as PNG or GIF.
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

## Components (22)

| Kind | Early third | Middle third | Late third |
|---|---|---|---|
| **Places** (party walks past) | signpost, well, windmill, cart | bridge, camp, chest (opens as the party passes) | haunted_tree, warning_sign |
| **Enemies** (defeated at the mark) | slime, bat | goblin, mushroom, wolf | skeleton, ghost |
| **Partners** (join and follow) | mage, knight, archer, cat, dog: any third except the very start | | |
| **Fixed** | `house` at the start, `dragon` at the last milestone, `castle` at the end | | |

## Choosing the story (you decide)

Rules: **dragon always last**; **warning_sign just before it** (when there are 5 or more milestones);
**at most 3 partners**, joining in the middle stretch; a **camp** around the middle (6 or more milestones);
roughly **half of the other slots are fights, never two fights in a row**; **no item used twice**;
places and enemies come from the tier that matches their third of the video.

Milestone spacing is automatic: the smallest of **1, 2, 3, 5, 10, 15, 20, 30 or 60 min** that gives
**10 or fewer** milestones. A mark within 10 s of the end is dropped. Override with `--interval SECONDS`.

1. `progressbar.py story --video VIDEO` (or `--duration S`) prints the automatic pick. It is seeded from the
   duration, so it is the same every run; `--seed N` re-rolls it.
2. **Make it fit the video when you can.** For example, a spooky topic → ghost, haunted_tree, skeleton;
   a cosy topic → cat, dog, camp, windmill; a money or treasure topic → chest, cart. Pass exactly as many
   items as there are milestones, following the rules: `--story well,bat,cat,camp,...,warning_sign,dragon`.
   Otherwise keep the automatic pick.
3. Save the final plan with `story ... --save plan.json` and pass `--plan plan.json` to every later
   command (`still`, `burn`, `overlay`, `showcase`), so the preview and the final render match. Keep
   `plan.json` next to the output video so the video can be re-rendered exactly.
4. Tell the user the plan as a short timeline (`01:00 well · 02:00 bat · …`) before the long render.

## Workflow

1. **Plan:** see "Choosing the story" above.
2. **Find the line to walk on.** For the owner's template, use `--config $SKILL/presets/magazine-1080p.json`.
   For a new layout, run `progressbar.py detect VIDEO --color '#rrggbb'`. It prints `line_y`, `line_thickness` and `line_x`
   (in 1080p reference units) to put in a config JSON. If the video has no line, set `"dim_line": false`
   and pick `line_y` (the ground row) yourself.
3. **Preview before rendering.** `progressbar.py still VIDEO --config CFG --plan plan.json --time 5 125 300 480 --out chk.png`
   writes `chk_<t>.png`. Look at them: feet on the line, nothing cut off at the edges, enemies sitting just past their minute mark.
4. **Render.**
   - Burned in: `progressbar.py burn VIDEO --config CFG --plan plan.json --out out.mp4`. Keeps the audio, H.264 CRF 18.
   - Overlay for an editor: `progressbar.py overlay VIDEO --config CFG --plan plan.json --out bar.mov`. ProRes 4444 with alpha,
     full frame by default, about 2.3 GB for 8 min at 1080p. `--strip` renders only the bar band (about 5× smaller) and prints the y to place it at.
     In FilmCraft: `file.import` it, then `timeline.place` it on V2 above the footage on V1.
   - Social clip: `progressbar.py showcase --duration <video seconds> --plan plan.json --length 30 --out showcase.mp4`.
     The story is fast-forwarded, but the walking and effects play at normal speed. It includes a `mm:ss / mm:ss` timer (`--no-timer` to hide it).
5. **Verify.** Extract a few frames from the result (`ffmpeg -ss T -i out.mp4 -frames:v 1 f.png`) around milestones
   and look at them before reporting success. Check that the output duration matches the input.

Speed reference: 8:21 at 1080p25 burns in about 2.5 min on 4 vCPU. The ProRes overlay is slower, about 3× real time.
If the project says heavy work runs on a remote machine (for example a CLAUDE.md with EC2 rules), copy
`$SKILL/scripts`, the config and the video there. The machine needs only `python3`, `python3-pil` and `ffmpeg`.
Run the job under `nohup` or `tmux` and pull back only the result.

## What happens on screen

- **Places** sit at their mark; the party walks past them. The chest opens once the hero reaches it.
- **Enemies** are placed so the hero's sword touches them exactly at the mark. They blink for about 1 s,
  burst into a puff of smoke and leave a sparkling coin as a permanent marker. The bat and ghost float.
- **Partners** wait at their mark facing the hero. Once he passes, they walk behind him, spaced by body length.
- The hero's position is linear in time. The part of the line not yet travelled is dimmed and dashed (`dim_line`).
- **New components:** if the user wants something not in the library, draw it in `scripts/sprites.py` following
  `reference/config.md` → "Adding a sprite". Show the user a preview, then offer to commit it back to the skill's repo
  (stevenfoong/my-progress-bar) so other devices get it. An installed plugin's copy is a cache and gets overwritten on update.

## Gotchas

- Scale only by whole numbers (`scale` is the sprite pixel size at 1080p; it is rescaled for other heights).
- Keep the house and castle inside the frame. For a non-16:9 video, set `house_x`, `castle_x`, `x_start` and `x_end`.
- The script exits non-zero if ffmpeg fails. Still check the output frames: a missing overlay is easy to miss.
