import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {paleta} from '../../series/ano-zero/paleta';

// Anéis vermelhos saindo de tudo que faz um padrão de som (bíblia, seção 9.4).
export const AneisSom: React.FC<{x?: number; y?: number; bpm?: number; tamanho?: number}> = ({
  x = 0.5,
  y = 0.45,
  bpm = 100,
  tamanho = 420,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const batida = (60 / bpm) * fps;
  const vida = batida * 2.2;
  const aneis = [];
  for (let n = Math.floor((frame - vida) / batida); n <= Math.floor(frame / batida); n++) {
    if (n < 0) continue;
    const idade = frame - n * batida;
    if (idade < 0 || idade > vida) continue;
    const p = idade / vida;
    aneis.push(
      <div
        key={n}
        style={{
          position: 'absolute',
          left: x * 1080 - (tamanho * p) / 2,
          top: y * 1920 - (tamanho * p) / 2,
          width: tamanho * p,
          height: tamanho * p,
          borderRadius: '50%',
          border: `${Math.max(1, 7 * (1 - p))}px solid ${paleta.perigo}`,
          opacity: (1 - p) * 0.9,
        }}
      />,
    );
  }
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div
        style={{
          position: 'absolute',
          left: x * 1080 - 9,
          top: y * 1920 - 9,
          width: 18,
          height: 18,
          borderRadius: '50%',
          background: paleta.perigo,
        }}
      />
      {aneis}
    </AbsoluteFill>
  );
};
