import React from 'react';
import {marca} from '../../marca/marca';

import {PONTO_VERMELHO, pontosSimbolo, raioVermelho} from '../../marca/simbolo';

// Avatar da marca. `revelar` (0–1) acende os pontos de baixo para cima, para animações.
export const SimboloHalftone: React.FC<{
  tamanho: number;
  simplificado?: boolean;
  revelar?: number;
  corPonto?: string;
  corVermelho?: string;
}> = ({tamanho, simplificado, revelar = 1, corPonto = marca.cores.papel, corVermelho = marca.cores.vermelho}) => {
  const pontos = React.useMemo(() => pontosSimbolo(simplificado), [simplificado]);
  return (
    <svg width={tamanho} height={tamanho} viewBox="-1.1 -1.1 2.2 2.2">
      {pontos.map((p, i) => {
        const k = Math.min(1, Math.max(0, (revelar * 1.4 - (1 - p.ordem) * 0.4) / 1));
        return k > 0 ? <circle key={i} cx={p.x} cy={p.y} r={p.r * k} fill={corPonto} /> : null;
      })}
      <circle cx={PONTO_VERMELHO.x} cy={PONTO_VERMELHO.y} r={raioVermelho(simplificado)} fill={corVermelho} opacity={revelar > 0.6 ? 1 : 0} />
    </svg>
  );
};
