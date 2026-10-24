import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';

// Poeira e areia no ar, deterministas (mesmo resultado em cada render).
export const Particulas: React.FC<{quantidade?: number; cor?: string}> = ({quantidade = 60, cor = '#EDE6D6'}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {Array.from({length: quantidade}, (_, i) => {
        const x = random(`px${i}`) * 1080;
        const vel = 0.3 + random(`pv${i}`) * 0.9;
        const y = (random(`py${i}`) * 1920 - frame * vel + 1920 * 4) % 1920;
        const r = 1 + random(`pr${i}`) * 2.5;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x + Math.sin((frame + i * 20) / 40) * 12,
              top: y,
              width: r * 2,
              height: r * 2,
              borderRadius: '50%',
              background: cor,
              opacity: 0.15 + random(`po${i}`) * 0.35,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};
