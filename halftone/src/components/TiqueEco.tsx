import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';

// Tique seco da cabeça do eco ao travar num som: um tranco no ritmo, que some em 4 quadros.
export const TiqueEco: React.FC<{bpm?: number; children: React.ReactNode}> = ({bpm = 100, children}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const batida = (60 / bpm) * fps;
  const fase = frame % batida;
  const n = Math.floor(frame / batida);
  const forca = fase < 4 ? 1 - fase / 4 : 0;
  const lado = n % 2 ? 1 : -1;
  return (
    <AbsoluteFill style={{transform: `rotate(${lado * 2.2 * forca}deg) translateX(${lado * 10 * forca}px)`, transformOrigin: '50% 75%'}}>
      {children}
    </AbsoluteFill>
  );
};
