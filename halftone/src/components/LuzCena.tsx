import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';
import type {TipoLuz} from '../tipos';

// Postes de sódio, telas, flashes vermelhos, palco e tremulação.
export const LuzCena: React.FC<{tipo: TipoLuz; tremulacao?: boolean}> = ({tipo, tremulacao}) => {
  const frame = useCurrentFrame();
  const tremor = tremulacao ? (random(`luz-${Math.floor(frame / 2)}`) > 0.93 ? 0.45 : 0.92 + random(`l${frame}`) * 0.08) : 1;
  if (tipo === 'nenhuma') return null;
  const camadas: Record<Exclude<TipoLuz, 'nenhuma'>, React.CSSProperties> = {
    'poste-sodio': {background: 'radial-gradient(ellipse 70% 45% at 70% 8%, rgba(255,170,70,0.38), transparent 70%)', mixBlendMode: 'screen'},
    'tela-celular': {background: 'radial-gradient(ellipse 45% 30% at 50% 45%, rgba(170,205,255,0.28), transparent 70%)', mixBlendMode: 'screen'},
    'flash-vermelho': {background: 'rgba(224,65,58,0.28)', mixBlendMode: 'screen', opacity: frame % 20 < 3 ? 1 : 0.15},
    palco: {background: 'radial-gradient(ellipse 90% 40% at 50% 0%, rgba(255,225,170,0.35), transparent 75%)', mixBlendMode: 'screen'},
    fluorescente: {background: 'rgba(200,235,255,0.10)', mixBlendMode: 'screen'},
  };
  return <AbsoluteFill style={{...camadas[tipo], opacity: (camadas[tipo].opacity as number | undefined ?? 1) * tremor, pointerEvents: 'none'}} />;
};
