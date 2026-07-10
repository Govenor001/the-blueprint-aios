# Video Presets — Pulse & Breakdown

Two production-grade, high-energy vertical video templates (1080×1920, 30fps) built with Remotion. Data-driven: swap the props, keep the motion. Yours to keep and use for your own content — your AIOS can generate the data and render these on command.

Preview stills: `pulse_still.png`, `breakdown_still.png`.

## The two presets

**Pulse** (`PulsePreset.jsx`) — a news / insight clip. Hook → three data stories (bar chart, line chart, donut gauge) → CTA. For "here's what's happening and here's our take."

**Breakdown** (`BreakdownPreset.jsx`) — a listicle / steps clip. Hook → 5 numbered steps with a progress rail and mixed visuals → CTA. For "5 ways to…", "how to…", teaching content.

Both share `ArchitectKit.jsx` — the motion design system: kinetic word-by-word headlines, animated bar/line/donut charts, count-up stats, scene-boundary flashes and light sweeps, a scrolling ticker, and four brand palettes.

## Use it

Drop the three files into a Remotion project's `src/`, register the compositions, then:
```
npx remotion render src/index.jsx Pulse out/pulse.mp4
npx remotion render src/index.jsx Breakdown out/breakdown.mp4
```
Preview live with `npx remotion studio src/index.jsx`.

## Customize
Every preset takes props — pass your own `brandKey` (`agent-architects` / `novacall` / `swiftleads` / `automa8`, or add yours in `ArchitectKit.jsx`), headlines, chart data, and CTA. The animation timing stays; only your content changes.

## Rules baked in (so it always looks right)
- All animation from `useCurrentFrame()` — deterministic, re-renderable
- Two spring speeds: `snap` (punchy) for entrances, `glide` (no bounce) for panels/charts
- Every scene changes with a flash + whip, never a plain cut
- Safe zone respected (top 140 / bottom 160 / side 55)

MIT — build on it, ship it.
