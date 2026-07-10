/**
 * ArchitectKit.jsx — The Agent Architects motion design kit (v2)
 *
 * The high-energy design system behind the Pulse and Breakdown presets.
 * Self-contained: ships with The Blueprint AIOS kit as a course giveaway.
 *
 * PRINCIPLES
 *   - Every frame from useCurrentFrame(); every interpolate clamped
 *   - Two spring speeds: SNAP (punchy overshoot) and GLIDE (damped, no bounce)
 *   - Scenes change with a flash + whip, never a plain cut
 *   - Charts are first-class: bars, lines, and gauges animate their data in
 *   - Safe zone (vertical 1080x1920): top 140 / bottom 160 / side 55
 */

const React = require('react');
const { useCurrentFrame, useVideoConfig, interpolate, spring } = require('remotion');

// ─── Font ────────────────────────────────────────────────────────────────────
let fontFamily = "'Inter', system-ui, sans-serif";
try {
  const inter = require('@remotion/google-fonts/Inter');
  inter.loadFont('normal', { weights: ['400', '600', '800', '900'] });
  fontFamily = inter.fontFamily;
} catch (_) {}
module.exports.fontFamily = fontFamily;

// ─── Palettes ────────────────────────────────────────────────────────────────
const BRANDS = {
  'agent-architects': { name: 'The Agent Architects', primary: '#7c3aed', light: '#a78bfa', dark: '#4c1d95' },
  'novacall':         { name: 'Novacall AI',          primary: '#0ea5e9', light: '#38bdf8', dark: '#1e3a8a' },
  'swiftleads':       { name: 'Swiftleads AI',        primary: '#db2777', light: '#f472b6', dark: '#9d174d' },
  'automa8':          { name: 'Automa8 AI',           primary: '#2563eb', light: '#60a5fa', dark: '#1e40af' },
};
module.exports.BRANDS = BRANDS;

const C = {
  bg: '#06060d', panel: 'rgba(255,255,255,0.045)', stroke: 'rgba(255,255,255,0.10)',
  text: '#f8fafc', dim: '#cbd5e1', muted: '#64748b',
  green: '#22c55e', red: '#ef4444', yellow: '#eab308', orange: '#f97316',
};
module.exports.C = C;

const SAFE = { top: 140, bottom: 160, side: 55 };
module.exports.SAFE = SAFE;

function rgb(hex) {
  const h = hex.replace('#', '');
  return `${parseInt(h.slice(0, 2), 16)},${parseInt(h.slice(2, 4), 16)},${parseInt(h.slice(4, 6), 16)}`;
}
module.exports.rgb = rgb;

// ─── Motion helpers ──────────────────────────────────────────────────────────
const cl = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };
module.exports.cl = cl;

// SNAP: punchy, slight overshoot — entrances, numbers, icons
function snap(frame, fps, delay = 0) {
  return spring({ frame: Math.max(0, frame - delay), fps, config: { damping: 14, mass: 0.8, stiffness: 130 } });
}
// GLIDE: fast but no bounce — panels, charts, camera moves
function glide(frame, fps, delay = 0) {
  return spring({ frame: Math.max(0, frame - delay), fps, config: { damping: 200 } });
}
module.exports.snap = snap;
module.exports.glide = glide;

// ─── FlashCut — brand flash at a scene boundary ─────────────────────────────
function FlashCut({ at, brand = BRANDS['agent-architects'] }) {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [at - 2, at, at + 7], [0, 0.85, 0], cl);
  if (o <= 0.01) return null;
  return <div style={{ position: 'absolute', inset: 0, background: `radial-gradient(circle at 50% 42%, rgba(${rgb(brand.light)},${o}) 0%, rgba(${rgb(brand.primary)},${o * 0.55}) 45%, transparent 78%)`, zIndex: 40 }} />;
}
module.exports.FlashCut = FlashCut;

// ─── WhipIn — scene enters with a fast horizontal whip + settle ─────────────
function WhipIn({ children, start = 0, from = 'right' }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const g = glide(frame, fps, start);
  const dir = from === 'right' ? 1 : -1;
  const x = interpolate(g, [0, 1], [dir * 110, 0], cl);
  return (
    <div style={{ position: 'absolute', inset: 0, transform: `translateX(${x}px) scale(${interpolate(g, [0, 1], [1.04, 1], cl)})`, opacity: interpolate(g, [0, 0.35, 1], [0, 1, 1], cl), willChange: 'transform' }}>
      {children}
    </div>
  );
}
module.exports.WhipIn = WhipIn;

// ─── FlareSweep — diagonal light streak (fire at transitions) ────────────────
function FlareSweep({ at, dur = 18, brand = BRANDS['agent-architects'] }) {
  const frame = useCurrentFrame();
  if (frame < at || frame > at + dur) return null;
  const p = (frame - at) / dur;
  const x = interpolate(p, [0, 1], [-70, 115]);
  return (
    <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', zIndex: 30, pointerEvents: 'none' }}>
      <div style={{
        position: 'absolute', top: '-25%', left: `${x}%`, width: '34%', height: '150%',
        transform: 'rotate(16deg)',
        background: `linear-gradient(90deg, transparent, rgba(${rgb(brand.light)},${0.28 * Math.sin(p * Math.PI)}), transparent)`,
      }} />
    </div>
  );
}
module.exports.FlareSweep = FlareSweep;

// ─── EnergyBg — animated background, three variants for scene variety ───────
const Grid = React.memo(function Grid({ o }) {
  return <div style={{
    position: 'absolute', inset: 0, opacity: o,
    backgroundImage: 'linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px)',
    backgroundSize: '72px 72px',
  }} />;
});

function EnergyBg({ brand = BRANDS['agent-architects'], variant = 'beams' }) {
  const frame = useCurrentFrame();
  const t = frame / 90;
  const p = rgb(brand.primary), d = rgb(brand.dark);
  return (
    <div style={{ position: 'absolute', inset: 0, background: C.bg, overflow: 'hidden' }}>
      {/* drifting glows — all variants */}
      <div style={{ position: 'absolute', width: 900, height: 900, borderRadius: '50%', top: -320 + Math.sin(t) * 26, left: -240 + Math.cos(t * 0.8) * 22, background: `radial-gradient(circle, rgba(${p},${0.16 + 0.05 * Math.sin(t)}) 0%, transparent 70%)` }} />
      <div style={{ position: 'absolute', width: 700, height: 700, borderRadius: '50%', bottom: -220 - Math.sin(t * 0.7) * 20, right: -180, background: `radial-gradient(circle, rgba(${d},${0.11 + 0.04 * Math.cos(t + 1.6)}) 0%, transparent 70%)` }} />
      {variant === 'grid' && <Grid o={0.8} />}
      {variant === 'beams' && [0, 1, 2].map((i) => (
        <div key={i} style={{
          position: 'absolute', top: '-30%', height: '160%', width: 3,
          left: `${((t * 9 + i * 33) % 130) - 15}%`,
          transform: 'rotate(14deg)',
          background: `linear-gradient(180deg, transparent, rgba(${p},0.20), transparent)`,
        }} />
      ))}
      {variant === 'particles' && Array.from({ length: 14 }).map((_, i) => {
        const seed = i * 137.5;
        const y = ((seed + frame * (0.55 + (i % 4) * 0.22)) % 2100) - 90;
        const x = (seed * 7.3) % 1080;
        return <div key={i} style={{ position: 'absolute', left: x, top: 1920 - y, width: 5 + (i % 3) * 3, height: 5 + (i % 3) * 3, borderRadius: '50%', background: `rgba(${p},${0.14 + (i % 3) * 0.1})` }} />;
      })}
      {/* vignette */}
      <div style={{ position: 'absolute', inset: 0, background: 'radial-gradient(ellipse at 50% 45%, transparent 55%, rgba(0,0,0,0.5) 100%)' }} />
    </div>
  );
}
module.exports.EnergyBg = EnergyBg;

// ─── WordPop — kinetic headline, word by word with overshoot ────────────────
function WordPop({ text, start = 0, per = 4, size = 92, weight = 900, color = C.text, accentWords = [], brand = BRANDS['agent-architects'], align = 'left' }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = String(text).split(' ');
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0 22px', justifyContent: align === 'center' ? 'center' : 'flex-start' }}>
      {words.map((w, i) => {
        const s = snap(frame, fps, start + i * per);
        const accent = accentWords.includes(w.replace(/[^\w%$]/g, ''));
        return (
          <span key={i} style={{
            fontFamily, fontSize: size, fontWeight: weight, lineHeight: 1.04, letterSpacing: '-0.03em',
            display: 'inline-block',
            opacity: s,
            transform: `translateY(${interpolate(s, [0, 1], [46, 0], cl)}px) rotate(${interpolate(s, [0, 1], [i % 2 ? 3 : -3, 0], cl)}deg)`,
            ...(accent ? {
              background: `linear-gradient(120deg, ${brand.primary}, ${brand.light})`,
              WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
            } : { color }),
          }}>{w}</span>
        );
      })}
    </div>
  );
}
module.exports.WordPop = WordPop;

// ─── Kicker — small uppercase tag with underline sweep ──────────────────────
function Kicker({ children, start = 0, brand = BRANDS['agent-architects'] }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = glide(frame, fps, start);
  return (
    <div style={{ alignSelf: 'flex-start', opacity: s, transform: `translateY(${interpolate(s, [0, 1], [18, 0], cl)}px)` }}>
      <span style={{ fontFamily, fontSize: 30, fontWeight: 800, letterSpacing: '0.16em', textTransform: 'uppercase', color: brand.light }}>{children}</span>
      <div style={{ height: 4, marginTop: 8, width: `${interpolate(s, [0, 1], [0, 100], cl)}%`, background: `linear-gradient(90deg, ${brand.primary}, transparent)`, borderRadius: 2 }} />
    </div>
  );
}
module.exports.Kicker = Kicker;

// ─── PunchList — bullets that punch in fast ─────────────────────────────────
function PunchList({ items, start = 0, per = 7, size = 40, brand = BRANDS['agent-architects'] }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div>
      {items.map((it, i) => {
        const s = snap(frame, fps, start + i * per);
        return (
          <div key={i} style={{ display: 'flex', gap: 18, alignItems: 'flex-start', marginBottom: 20, opacity: s, transform: `translateX(${interpolate(s, [0, 1], [-46, 0], cl)}px)` }}>
            <div style={{ width: 14, height: 14, marginTop: size * 0.45, borderRadius: 4, background: brand.primary, transform: `rotate(45deg) scale(${s})`, flexShrink: 0 }} />
            <span style={{ fontFamily, fontSize: size, fontWeight: 600, color: C.dim, lineHeight: 1.35 }}>{it}</span>
          </div>
        );
      })}
    </div>
  );
}
module.exports.PunchList = PunchList;

// ─── BigStat — hero number with count-up + underline sweep ──────────────────
function BigStat({ value, prefix = '', suffix = '', label, start = 0, dur = 26, size = 190, brand = BRANDS['agent-architects'] }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = snap(frame, fps, start);
  const v = interpolate(frame, [start, start + dur], [0, value], cl);
  const shown = value % 1 === 0 ? Math.round(v).toLocaleString() : v.toFixed(1);
  return (
    <div style={{ opacity: s, transform: `scale(${interpolate(s, [0, 1], [0.7, 1], cl)})` }}>
      <div style={{ fontFamily, fontSize: size, fontWeight: 900, letterSpacing: '-0.04em', lineHeight: 1, background: `linear-gradient(120deg, ${brand.light}, ${brand.primary})`, WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
        {prefix}{shown}{suffix}
      </div>
      <div style={{ height: 6, marginTop: 14, width: `${interpolate(frame, [start + 6, start + dur + 8], [0, 100], cl)}%`, background: `linear-gradient(90deg, ${brand.primary}, transparent)`, borderRadius: 3 }} />
      {label && <div style={{ fontFamily, fontSize: 36, fontWeight: 600, color: C.dim, marginTop: 16 }}>{label}</div>}
    </div>
  );
}
module.exports.BigStat = BigStat;

// ─── BarChart — staggered growing bars with count-up labels ─────────────────
function BarChart({ data, start = 0, per = 6, height = 520, brand = BRANDS['agent-architects'] }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const max = Math.max(...data.map((d) => d.value));
  return (
    <div style={{ display: 'flex', alignItems: 'flex-end', gap: 30, height, width: '100%' }}>
      {data.map((d, i) => {
        const g = glide(frame, fps, start + i * per);
        const h = interpolate(g, [0, 1], [0, (d.value / max) * (height - 120)], cl);
        const v = Math.round(interpolate(frame, [start + i * per, start + i * per + 22], [0, d.value], cl));
        const hot = d.highlight;
        return (
          <div key={i} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-end', height: '100%' }}>
            <div style={{ fontFamily, fontSize: 42, fontWeight: 900, color: hot ? brand.light : C.text, marginBottom: 10, opacity: g }}>{d.prefix || ''}{v}{d.suffix || ''}</div>
            <div style={{
              width: '100%', height: h, borderRadius: '14px 14px 6px 6px',
              background: hot ? `linear-gradient(180deg, ${brand.light}, ${brand.primary})` : `linear-gradient(180deg, rgba(${rgb(brand.primary)},0.55), rgba(${rgb(brand.dark)},0.45))`,
              boxShadow: hot ? `0 0 44px rgba(${rgb(brand.primary)},0.45)` : 'none',
            }} />
            <div style={{ fontFamily, fontSize: 30, fontWeight: 600, color: C.muted, marginTop: 14, opacity: g, textAlign: 'center' }}>{d.label}</div>
          </div>
        );
      })}
    </div>
  );
}
module.exports.BarChart = BarChart;

// ─── LineChart — SVG path draw with pulsing head dot + area fill ────────────
function LineChart({ points, start = 0, dur = 40, w = 960, h = 480, brand = BRANDS['agent-architects'], yLabel }) {
  const frame = useCurrentFrame();
  const max = Math.max(...points), min = Math.min(...points);
  const span = max - min || 1;
  const px = (i) => 30 + (i / (points.length - 1)) * (w - 60);
  const py = (v) => h - 60 - ((v - min) / span) * (h - 130);
  const path = points.map((v, i) => `${i ? 'L' : 'M'} ${px(i)} ${py(v)}`).join(' ');
  const p = interpolate(frame, [start, start + dur], [0, 1], cl);
  const totalLen = w * 1.6; // safe overestimate for dashoffset draw
  const headIdx = Math.min(points.length - 1, Math.floor(p * (points.length - 1)));
  const pulse = 1 + 0.35 * Math.sin(frame / 4);
  return (
    <svg width={w} height={h} style={{ overflow: 'visible' }}>
      {[0.25, 0.5, 0.75].map((g, i) => (
        <line key={i} x1={30} x2={w - 30} y1={h - 60 - g * (h - 130)} y2={h - 60 - g * (h - 130)} stroke="rgba(255,255,255,0.07)" strokeWidth="1.5" />
      ))}
      <path d={`${path} L ${px(points.length - 1)} ${h - 60} L ${px(0)} ${h - 60} Z`} fill={`rgba(${rgb(brand.primary)},${0.16 * p})`} />
      <path d={path} fill="none" stroke={brand.light} strokeWidth="7" strokeLinecap="round"
        strokeDasharray={totalLen} strokeDashoffset={totalLen * (1 - p)} />
      {p > 0.02 && <circle cx={px(headIdx)} cy={py(points[headIdx])} r={13 * pulse} fill={brand.light} opacity={0.95} />}
      {yLabel && <text x={30} y={34} fill={C.muted} fontFamily={fontFamily} fontSize="28" fontWeight="600">{yLabel}</text>}
    </svg>
  );
}
module.exports.LineChart = LineChart;

// ─── DonutGauge — arc sweep to a percentage with center counter ─────────────
function DonutGauge({ pct, start = 0, dur = 34, size = 430, label, brand = BRANDS['agent-architects'] }) {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [start, start + dur], [0, pct], cl);
  const r = size / 2 - 30;
  const circ = 2 * Math.PI * r;
  return (
    <div style={{ position: 'relative', width: size, height: size }}>
      <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="30" />
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={`url(#gaugeGrad)`} strokeWidth="30" strokeLinecap="round"
          strokeDasharray={circ} strokeDashoffset={circ * (1 - p / 100)} />
        <defs>
          <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor={brand.primary} />
            <stop offset="100%" stopColor={brand.light} />
          </linearGradient>
        </defs>
      </svg>
      <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <span style={{ fontFamily, fontSize: size * 0.24, fontWeight: 900, color: C.text }}>{Math.round(p)}%</span>
        {label && <span style={{ fontFamily, fontSize: 30, fontWeight: 600, color: C.muted, marginTop: 6, textAlign: 'center', maxWidth: size * 0.7 }}>{label}</span>}
      </div>
    </div>
  );
}
module.exports.DonutGauge = DonutGauge;

// ─── ProgressRail — step indicator for listicles ─────────────────────────────
function ProgressRail({ total, current, brand = BRANDS['agent-architects'] }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
      {Array.from({ length: total }).map((_, i) => {
        const active = i === current;
        const done = i < current;
        const s = active ? snap(frame, fps, 2) : 1;
        return (
          <div key={i} style={{
            height: 12, borderRadius: 6,
            width: active ? interpolate(s, [0, 1], [26, 74], cl) : 26,
            background: active ? `linear-gradient(90deg, ${brand.primary}, ${brand.light})` : done ? `rgba(${rgb(brand.primary)},0.65)` : 'rgba(255,255,255,0.14)',
          }} />
        );
      })}
    </div>
  );
}
module.exports.ProgressRail = ProgressRail;

// ─── ChapterChip — big numbered badge that punches in ────────────────────────
function ChapterChip({ n, start = 0, brand = BRANDS['agent-architects'] }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = snap(frame, fps, start);
  return (
    <div style={{
      width: 120, height: 120, borderRadius: 32, display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: `linear-gradient(135deg, ${brand.primary}, ${brand.dark})`,
      boxShadow: `0 0 60px rgba(${rgb(brand.primary)},0.5)`,
      opacity: s, transform: `scale(${interpolate(s, [0, 1], [0.4, 1], cl)}) rotate(${interpolate(s, [0, 1], [-14, 0], cl)}deg)`,
    }}>
      <span style={{ fontFamily, fontSize: 64, fontWeight: 900, color: '#fff' }}>{n}</span>
    </div>
  );
}
module.exports.ChapterChip = ChapterChip;

// ─── TickerStrip — scrolling text strip ──────────────────────────────────────
function TickerStrip({ items, y = 1770, speed = 3.2, brand = BRANDS['agent-architects'] }) {
  const frame = useCurrentFrame();
  const text = items.join('   •   ') + '   •   ';
  const x = -((frame * speed) % 2400);
  return (
    <div style={{ position: 'absolute', top: y, left: 0, right: 0, overflow: 'hidden', borderTop: `1px solid ${C.stroke}`, borderBottom: `1px solid ${C.stroke}`, background: 'rgba(0,0,0,0.35)', padding: '14px 0' }}>
      <div style={{ whiteSpace: 'nowrap', transform: `translateX(${x}px)` }}>
        {[0, 1, 2].map((k) => (
          <span key={k} style={{ fontFamily, fontSize: 28, fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', color: brand.light, opacity: 0.85 }}>{text}</span>
        ))}
      </div>
    </div>
  );
}
module.exports.TickerStrip = TickerStrip;

// ─── Panel — glass card that glides up ───────────────────────────────────────
function Panel({ children, start = 0, style = {} }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const g = glide(frame, fps, start);
  return (
    <div style={{
      background: C.panel, border: `1.5px solid ${C.stroke}`, borderRadius: 28, padding: '42px 46px',
      opacity: g, transform: `translateY(${interpolate(g, [0, 1], [60, 0], cl)}px)`,
      ...style,
    }}>
      {children}
    </div>
  );
}
module.exports.Panel = Panel;

// ─── SafeArea ────────────────────────────────────────────────────────────────
function SafeArea({ children, justify = 'flex-start', gap = 0 }) {
  return (
    <div style={{ position: 'absolute', top: SAFE.top, bottom: SAFE.bottom, left: SAFE.side, right: SAFE.side, display: 'flex', flexDirection: 'column', justifyContent: justify, gap }}>
      {children}
    </div>
  );
}
module.exports.SafeArea = SafeArea;

// ─── CTAEnd — end card with pulsing button ───────────────────────────────────
function CTAEnd({ headline, sub, button, start = 0, brand = BRANDS['agent-architects'] }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = snap(frame, fps, start);
  const pulse = 1 + 0.03 * Math.sin((frame - start) / 5);
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', gap: 34 }}>
      <WordPop text={headline} start={start} size={86} align="center" accentWords={headline.split(' ').filter((w) => w === w.toUpperCase() && w.length > 2)} brand={brand} />
      <div style={{ fontFamily, fontSize: 40, fontWeight: 600, color: C.dim, opacity: s, maxWidth: 850, lineHeight: 1.4 }}>{sub}</div>
      <div style={{
        padding: '26px 66px', borderRadius: 999, marginTop: 10,
        background: `linear-gradient(120deg, ${brand.primary}, ${brand.light})`,
        boxShadow: `0 0 70px rgba(${rgb(brand.primary)},0.55)`,
        opacity: s, transform: `scale(${s * pulse})`,
      }}>
        <span style={{ fontFamily, fontSize: 44, fontWeight: 900, color: '#fff' }}>{button}</span>
      </div>
    </div>
  );
}
module.exports.CTAEnd = CTAEnd;
