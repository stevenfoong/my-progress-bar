# Config reference

The config is a JSON file passed with `--config`. Missing keys use the defaults below.
Positions are in **1920×1080 reference pixels**; the script rescales them to the real video size.

| Key | Default | Meaning |
|---|---|---|
| `line_y` | `1042` | Top row of the line the characters stand on (feet land on `line_y + 1`). |
| `line_thickness` | `4` | Rows of the line (for dimming and for drawing it in `showcase`/`frame`). |
| `line_x` | `[98, 1820]` | Left and right end of the line. |
| `dim_line` | `true` | Dim and dash the not-yet-travelled part of the line. Set `false` if the video has no line. |
| `line_color` / `dim_color` / `dash_color` | gold / `#464460` / `#68688a` | Line colours. |
| `x_start` / `x_end` | `165` / `1700` | Hero position at the start and at the end of the video. |
| `house_x` / `castle_x` | `72` / `1850` | Centres of the start and end buildings. |
| `scale` | `3` | Sprite pixel size at 1080p (the hero is about 81 px tall). Use 2 for a smaller bar. |
| `interval` | `60` | Seconds between milestones. |
| `min_end_gap` | `10` | Drop a milestone closer than this many seconds to the end. |
| `story` | `null` | Item names in milestone order. `null` means automatic. |
| `milestones` | `null` | Exact list such as `[{"time": 95, "item": "goblin"}, …]`. Overrides `interval` and `story`. |
| `background` | `#232a45` | Background colour for `showcase` and `frame`. |

CLI flags override the config: `--story a,b,c`, `--interval`, `--scale`, `--line-y`, `--no-dim`.

## Items

| Item | Kind | Animation |
|---|---|---|
| `signpost` | prop | static |
| `camp` | prop | flickering fire, 4 frames |
| `warning_sign` | prop | static (skull and red marks) |
| `goblin` | enemy | club bob, 2 frames |
| `slime` | enemy | squash-and-bounce, 6 frames |
| `dragon` | enemy (boss) | wing flap, 4 frames |
| `mage` | partner | idle, 2 frames, plus walk, 8 frames |
| `knight` | partner | idle, 2 frames, plus walk, 8 frames |

Always present: `house` (start), `castle` (end), `hero` (walk, 8 frames), plus `puff` (5 frames) and `coin` (2 frames) after an enemy is defeated.

## Adding a sprite

1. In `scripts/sprites.py`, write `def thing(f): img = canvas(w, h); ...; return outline(img)`.
   Draw fills only: `outline()` adds the dark 1-px border. Stay within about 30 native px of height.
   Use the palette in `C` so it matches the rest.
2. Register its frames in `build_all()` (for example `s[f'thing_{f}'] = thing(f)`).
3. Add it to `ITEMS` in `scripts/progressbar.py` with a kind (`prop`, `enemy` or `partner`), its frame names and the
   seconds per frame `dt`. A partner needs `<name>_walk_0..7` and `<name>_idle_0..1` frames drawn on the 32×36 character canvas.
4. Check it with `python3 progressbar.py frame --duration 300 --time 100 --story thing --out t.png`.
