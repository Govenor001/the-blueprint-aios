/**
 * PulsePreset.jsx — "Pulse": high-energy news/insight vertical (1080x1920, 30fps)
 *
 * Structure (23s):
 *   Hook (0-74)         cold open, kinetic headline, flash in
 *   Story 1 (75-239)    headline + punch list + BAR CHART
 *   Story 2 (240-404)   headline + LINE CHART + big stat
 *   Story 3 (405-569)   headline + DONUT GAUGE + takeaway panel
 *   CTA (570-689)       end card, pulsing button, ticker throughout
 *
 * Fully data-driven via props — swap `brand` and the content, keep the motion.
 */

const React = require('react');
const { useCurrentFrame, Sequence } = require('remotion');
const K = require('./ArchitectKit');

const TOTAL_FRAMES = 690;

const DEFAULTS = {
  brandKey: 'agent-architects',
  ticker: ['AI moves fast', 'Here is our take', 'The Agent Architects'],
  hook: { kicker: 'THE PULSE', headline: 'AI just changed the game AGAIN', accents: ['AI', 'AGAIN'] },
  story1: {
    kicker: 'STORY 01', headline: 'Everyone is switching',
    points: ['Adoption doubled in 6 months', 'Costs collapsed 10x', 'The winners automate first'],
    chart: [
      { label: '2024', value: 18, suffix: '%' },
      { label: '2025', value: 41, suffix: '%' },
      { label: '2026', value: 87, suffix: '%', highlight: true },
    ],
  },
  story2: {
    kicker: 'STORY 02', headline: 'The cost curve is collapsing',
    line: [92, 84, 71, 55, 38, 24, 12], yLabel: 'Cost per task ($)',
    stat: { value: 10, suffix: 'x', label: 'cheaper than 18 months ago' },
  },
  story3: {
    kicker: 'STORY 03', headline: 'Most are still not ready',
    gauge: { pct: 73, label: 'of businesses have no AI system' },
    takeaway: 'The gap is the opportunity. The ones who build now own the next five years.',
  },
  cta: { headline: 'Stop doing it MANUALLY', sub: 'Join 1,000+ founders automating their business', button: 'The Agent Architects' },
};

function PulsePreset(props) {
  const p = { ...DEFAULTS, ...props };
  const brand = K.BRANDS[p.brandKey] || K.BRANDS['agent-architects'];
  const frame = useCurrentFrame();

  return (
    <div style={{ position: 'absolute', inset: 0, background: K.C.bg }}>
      {/* HOOK */}
      <Sequence from={0} durationInFrames={75}>
        <K.EnergyBg brand={brand} variant="beams" />
        <K.SafeArea justify="center" gap={30}>
          <K.Kicker start={2} brand={brand}>{p.hook.kicker}</K.Kicker>
          <K.WordPop text={p.hook.headline} start={6} per={4} size={104} accentWords={p.hook.accents} brand={brand} />
        </K.SafeArea>
      </Sequence>

      {/* STORY 1 — bar chart */}
      <Sequence from={75} durationInFrames={165}>
        <K.EnergyBg brand={brand} variant="grid" />
        <K.WhipIn from="right">
          <K.SafeArea justify="flex-start" gap={34}>
            <K.Kicker start={2} brand={brand}>{p.story1.kicker}</K.Kicker>
            <K.WordPop text={p.story1.headline} start={4} size={84} brand={brand} accentWords={[]} />
            <K.PunchList items={p.story1.points} start={16} brand={brand} />
            <K.Panel start={34} style={{ marginTop: 8 }}>
              <K.BarChart data={p.story1.chart} start={40} brand={brand} height={480} />
            </K.Panel>
          </K.SafeArea>
        </K.WhipIn>
      </Sequence>

      {/* STORY 2 — line chart + big stat */}
      <Sequence from={240} durationInFrames={165}>
        <K.EnergyBg brand={brand} variant="particles" />
        <K.WhipIn from="left">
          <K.SafeArea justify="flex-start" gap={38}>
            <K.Kicker start={2} brand={brand}>{p.story2.kicker}</K.Kicker>
            <K.WordPop text={p.story2.headline} start={4} size={84} brand={brand} accentWords={[]} />
            <K.Panel start={18}>
              <K.LineChart points={p.story2.line} start={26} w={880} h={440} brand={brand} yLabel={p.story2.yLabel} />
            </K.Panel>
            <K.BigStat value={p.story2.stat.value} suffix={p.story2.stat.suffix} label={p.story2.stat.label} start={70} size={170} brand={brand} />
          </K.SafeArea>
        </K.WhipIn>
      </Sequence>

      {/* STORY 3 — gauge + takeaway */}
      <Sequence from={405} durationInFrames={165}>
        <K.EnergyBg brand={brand} variant="beams" />
        <K.WhipIn from="right">
          <K.SafeArea justify="flex-start" gap={40}>
            <K.Kicker start={2} brand={brand}>{p.story3.kicker}</K.Kicker>
            <K.WordPop text={p.story3.headline} start={4} size={84} brand={brand} accentWords={[]} />
            <div style={{ display: 'flex', justifyContent: 'center', marginTop: 10 }}>
              <K.DonutGauge pct={p.story3.gauge.pct} label={p.story3.gauge.label} start={20} brand={brand} />
            </div>
            <K.Panel start={62}>
              <span style={{ fontFamily: K.fontFamily, fontSize: 42, fontWeight: 600, color: K.C.text, lineHeight: 1.45 }}>{p.story3.takeaway}</span>
            </K.Panel>
          </K.SafeArea>
        </K.WhipIn>
      </Sequence>

      {/* CTA */}
      <Sequence from={570} durationInFrames={120}>
        <K.EnergyBg brand={brand} variant="particles" />
        <K.SafeArea justify="center">
          <K.CTAEnd headline={p.cta.headline} sub={p.cta.sub} button={p.cta.button} start={4} brand={brand} />
        </K.SafeArea>
      </Sequence>

      {/* Global overlays: ticker + scene-boundary flashes and flares */}
      <K.TickerStrip items={p.ticker} brand={brand} />
      {[75, 240, 405, 570].map((at) => (
        <React.Fragment key={at}>
          <K.FlashCut at={at} brand={brand} />
          <K.FlareSweep at={at + 2} brand={brand} />
        </React.Fragment>
      ))}
      {/* progress bar along the very top */}
      <div style={{ position: 'absolute', top: 0, left: 0, height: 10, width: `${(frame / TOTAL_FRAMES) * 100}%`, background: `linear-gradient(90deg, ${brand.primary}, ${brand.light})`, zIndex: 50 }} />
    </div>
  );
}

module.exports = PulsePreset;
module.exports.TOTAL_FRAMES = TOTAL_FRAMES;
