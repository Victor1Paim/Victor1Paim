import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {paleta} from '../../series/ano-zero/paleta';

// Névoa baixa que deriva devagar (maresia).
export const Nevoa: React.FC<{intensidade?: number}> = ({intensidade = 0.35}) => {
  const frame = useCurrentFrame();
  const desvio = Math.sin(frame / 90) * 80;
  return (
    <AbsoluteFill style={{pointerEvents: 'none', opacity: intensidade}}>
      <div
        style={{
          position: 'absolute',
          left: -300 + desvio,
          right: -300 - desvio,
          bottom: 200,
          height: 900,
          background: `radial-gradient(ellipse 50% 50% at 50% 60%, ${paleta.nevoa}, transparent 70%)`,
          filter: 'blur(40px)',
        }}
      />
    </AbsoluteFill>
  );
};
