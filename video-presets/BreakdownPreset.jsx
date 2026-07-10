/**
 * BreakdownPreset.jsx — "Breakdown": listicle/steps vertical (1080x1920, 30fps)
 *
 * Structure (24s): Hook (0-74) → 5 steps x 105f each with a progress rail and
 * alternating visual treatments (stat / chart / plain punch) → CTA (599-719).
 * Data-driven: pass 5 steps with {title, body, visual}.
 * visual: {type:'stat', value, suffix, label} | {type:'bars', data} | {type:'none'}
 */

const React = require('react');
const { Sequence, useCurrentFrame } = require('remotion');
const K = require('./ArchitectKit');

const STEP_DUR = 105;
const TOTAL_FRAMES = 75 + 5 * STEP_DUR + 120; // 720

const DEFAULTS = {
  brandKey: 'agent-architects',
  hook: { kicker: 'THE BREAKDOWN', headline: '5 AI moves that PRINT time', accents: ['5', 'PRINT'] },
  steps: [
    { title: 'Give your AI a memory', body: 'Stop re-explaining your business every chat. Feed it context once — it compounds forever.', visual: { type: 'stat', value: 15, suffix: ' hrs', label: 'saved per week, average' } },
    { title: 'Automate your content', body: 'A week of posts in your voice, from one prompt. Review, tweak, schedule.', visual: { type: 'bars', data: [ { label: 'Manual', value: 6, suffix: 'h' }, { label: 'With AI', value: 1, suffix: 'h', highlight: true } ] } },
    { title: 'Monitor your market', body: 'Free feeds + a free model = a ranked morning brief about your niche. Every day.', visual: { type: 'stat', value: 0, prefix: '$', label: 'monthly cost. Yes, zero.' } },
    { title: 'Deploy it 24/7', body: 'Move it to a free cloud server. It works while your laptop is closed.', visual: { type: 'stat', value: 24, suffix: '/7', label: 'always on, always working' } },
    { title: 'Put it in your pocket', body: 'Text it. Voice-note it. Your whole system answers from your phone.', visual: { type: 'none' } },
  ],
  cta: { headline: 'Build ALL of this in 7 DAYS', sub: 'The 7-Day Agent Architect Challenge — beginner-friendly, everything free', button: 'Join the Challenge' },
};

function StepVisual({ visual, brand }) {
  if (!visual || visual.type === 'none') return null;
  if (visual.type === 'stat') {
    return <K.BigStat value={visual.value} prefix={visual.prefix || ''} suffix={visual.suffix || ''} label={visual.label} start={34} size={150} brand={brand} />;
  }
  if (visual.type === 'bars') {
    return (
      <K.Panel start={30}>
        <K.BarChart data={visual.data} start={36} height={360} brand={brand} />
      </K.Panel>
    );
  }
  return null;
}

function BreakdownPreset(props) {
  const p = { ...DEFAULTS, ...props };
  const brand = K.BRANDS[p.brandKey] || K.BRANDS['agent-architects'];
  const frame = useCurrentFrame();
  const bgVariants = ['grid', 'particles', 'beams', 'grid', 'particles'];

  return (
    <div style={{ position: 'absolute', inset: 0, background: K.C.bg }}>
      {/* HOOK */}
      <Sequence from={0} durationInFrames={75}>
        <K.EnergyBg brand={brand} variant="beams" />
        <K.SafeArea justify="center" gap={30}>
          <K.Kicker start={2} brand={brand}>{p.hook.kicker}</K.Kicker>
          <K.WordPop text={p.hook.headline} start={6} per={4} size={100} accentWords={p.hook.accents} brand={brand} />
        </K.SafeArea>
      </Sequence>

      {/* STEPS */}
      {p.steps.map((step, i) => {
        const from = 75 + i * STEP_DUR;
        return (
          <Sequence key={i} from={from} durationInFrames={STEP_DUR}>
            <K.EnergyBg brand={brand} variant={bgVariants[i % bgVariants.length]} />
            <K.WhipIn from={i % 2 ? 'left' : 'right'}>
              <K.SafeArea justify="flex-start" gap={36}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 30 }}>
                  <K.ChapterChip n={i + 1} start={2} brand={brand} />
                  <K.ProgressRail total={p.steps.length} current={i} brand={brand} />
                </div>
                <K.WordPop text={step.title} start={8} size={82} brand={brand} accentWords={[]} />
                <K.Panel start={20}>
                  <span style={{ fontFamily: K.fontFamily, fontSize: 42, fontWeight: 600, color: K.C.dim, lineHeight: 1.45 }}>{step.body}</span>
                </K.Panel>
                <StepVisual visual={step.visual} brand={brand} />
              </K.SafeArea>
            </K.WhipIn>
          </Sequence>
        );
      })}

      {/* CTA */}
      <Sequence from={75 + 5 * STEP_DUR} durationInFrames={120}>
        <K.EnergyBg brand={brand} variant="particles" />
        <K.SafeArea justify="center">
          <K.CTAEnd headline={p.cta.headline} sub={p.cta.sub} button={p.cta.button} start={4} brand={brand} />
        </K.SafeArea>
      </Sequence>

      {/* scene-boundary effects */}
      {Array.from({ length: 6 }).map((_, i) => {
        const at = 75 + i * STEP_DUR;
        return (
          <React.Fragment key={at}>
            <K.FlashCut at={at} brand={brand} />
            <K.FlareSweep at={at + 2} brand={brand} />
          </React.Fragment>
        );
      })}
      <div style={{ position: 'absolute', top: 0, left: 0, height: 10, width: `${(frame / TOTAL_FRAMES) * 100}%`, background: `linear-gradient(90deg, ${brand.primary}, ${brand.light})`, zIndex: 50 }} />
    </div>
  );
}

module.exports = BreakdownPreset;
module.exports.TOTAL_FRAMES = TOTAL_FRAMES;
