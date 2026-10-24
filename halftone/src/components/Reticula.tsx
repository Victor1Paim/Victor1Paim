import React from 'react';
import {AbsoluteFill} from 'remotion';

// Textura de pontos do canal, sutil, por cima das cenas (no lugar do grão de filme).
export const Reticula: React.FC<{opacidade?: number; passo?: number; angulo?: number}> = ({
  opacidade = 0.09,
  passo = 7,
  angulo = 45,
}) => {
  const id = React.useId().replace(/:/g, '');
  return (
    <AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'overlay', opacity: opacidade}}>
      <svg width="100%" height="100%">
        <defs>
          <pattern id={id} width={passo} height={passo} patternUnits="userSpaceOnUse" patternTransform={`rotate(${angulo})`}>
            <circle cx={passo / 2} cy={passo / 2} r={passo * 0.32} fill="#000" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill={`url(#${id})`} />
      </svg>
    </AbsoluteFill>
  );
};
