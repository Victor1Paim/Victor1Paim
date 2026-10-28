---
name: claude-animation-base
description: >
  Animate a hand-painted 2D character (brush strokes, boiling linework, paper texture) in p5.js +
  p5.brush and render it to MP4 headlessly. Starter kit with a character rig (views, emotions, eyes,
  mouths, hats, dances), timeline with brush-wipe transitions, camera, light and paper helpers, plus
  the animation rules and workflow guide. Use when the user wants a painterly character animation or
  a recurring mascot/guide character in videos, or wants to swap the character or add emotions and
  costumes. Not for photoreal or 3D work.
---

# Claude Animation Base

A small kit for painterly character animation, by John Heibel (github.com/JohnHeibel/ClaudeAnimationBase, MIT).
The bundled character is Clawd; the rig is meant to be changed: swap the character, add emotions or costumes,
or feed it reference images (for example the channel's own avatar).

## What is here

| Path | What |
|---|---|
| `ANIMATION_GUIDE.md` | The rules, workflow and full API. **Read it first, completely.** |
| `kit/src/` | `clawd.js` (character), `core.js` (painting, timing, motion, camera, light, paper), `timeline.js` (shots, loops, brush-wipe), `config.js` (length, tempo), `sheets.js` (model sheets), `scenes/demo.js` (example) |
| `kit/render.mjs` | Headless renderer: contact sheets, frame strips, crops, stills, MP4 |
| `kit/studio.html` | Open in Chrome to scrub the timeline (`?loop=emotions`, `?loop=views` for model sheets) |
| `kit/gpu_probe.mjs` | Shows which renderer a set of Chrome flags gets |
| `references/emotions.jpg`, `references/views.jpg` | Model sheets: the 31 emotions; the five views, motion helpers and hats |

## How to make a video

1. Copy `kit/` into a new folder under the project's `producoes/`, then `npm install` there.
2. Read `ANIMATION_GUIDE.md`. It says to storyboard first, build shot by shot, render contact sheets to check your
   own work, and write `out/video.mp4`.
3. Put the new scene in `src/scenes/` (the demo is an example). Set length and tempo in `src/config.js`.
4. Check: `node render.mjs --sheet=0,1,2,3,4,5 --out=out/sheet.jpg`. Full render: `node render.mjs --clip --out=out/video.mp4`.
5. Linux without GPU: add `--soft-gl`. Watercolour fills are slow in software, so ask for flat or brush fills instead.
   Chrome path: `--chrome=<path>` or `CHROME_PATH` (cloud container: `/opt/pw-browsers/chromium`).

## Notes for this repo

- Output is 16:9 by default. For TikTok, Reels and Shorts change the canvas to 1080×1920 in `src/config.js`/`core.js`
  and re-check the framing of every shot.
- The guide says "no text" inside the painted film. Captions and titles are added afterwards in the editing step (Remotion).
- The animation is deterministic per frame, so scenes can be re-rendered shot by shot.
- Licence MIT, copyright John Heibel (`LICENSE.origem`).
