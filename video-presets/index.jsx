// Entry point — registers the two shipped compositions.
// Presets are data-driven: pass props in Remotion Studio, or render with
// their built-in DEFAULTS to see the demo content.
const React = require('react');
const { Composition, registerRoot } = require('remotion');
const PulsePreset = require('./PulsePreset.jsx');
const BreakdownPreset = require('./BreakdownPreset.jsx');

const Root = () => (
  <>
    <Composition
      id="Pulse"
      component={PulsePreset}
      durationInFrames={PulsePreset.TOTAL_FRAMES}
      fps={30}
      width={1080}
      height={1920}
    />
    <Composition
      id="Breakdown"
      component={BreakdownPreset}
      durationInFrames={BreakdownPreset.TOTAL_FRAMES}
      fps={30}
      width={1080}
      height={1920}
    />
  </>
);

registerRoot(Root);
