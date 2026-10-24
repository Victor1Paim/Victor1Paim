import React from 'react';
import {AbsoluteFill, interpolate, random, useCurrentFrame, useVideoConfig} from 'remotion';
import {marca} from '../../marca/marca';
import {fontes} from '../theme/fontes';

// "REBOBINA • 23:15 • OUTRO PONTO DE VISTA" — só quando traz informação nova.
export const Rebobina: React.FC<{hora: string}> = ({hora}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const op = interpolate(frame, [0, 4, durationInFrames - 5, durationInFrames], [0, 1, 1, 0], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: marca.cores.preto, opacity: op, alignItems: 'center', justifyContent: 'center'}}>
      {Array.from({length: 7}, (_, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: ((random(`rb${i}`) * 1920 + frame * 60 * (i + 1)) % 1920),
            height: 3 + random(`rh${i}`) * 8,
            background: marca.cores.papel,
            opacity: 0.08,
          }}
        />
      ))}
      <div style={{display: 'flex', alignItems: 'center', gap: 24, fontFamily: fontes.mono, color: marca.cores.papel}}>
        <span style={{fontSize: 64, letterSpacing: -12}}>◀◀</span>
        <span style={{fontSize: 56, letterSpacing: 8}}>REBOBINA</span>
      </div>
      <div style={{marginTop: 24, fontFamily: fontes.mono, fontSize: 34, letterSpacing: 6, color: marca.cores.cinza}}>
        {hora} • OUTRO PONTO DE VISTA
      </div>
    </AbsoluteFill>
  );
};
