import React from 'react';
import {pulso, ruido} from './tempo';

// Multidão de branco em silhuetas (cabeça + ombros), em fileiras com profundidade.
// Balança na batida; para quando a música para; foge quando `fuga` > 0.

type Fileira = {y: number; escala: number; n: number; cor: string; semente: number};

export const FILEIRAS_FUNDO: Fileira[] = [
  {y: 1010, escala: 0.32, n: 30, cor: '#5D6470', semente: 1},
  {y: 1060, escala: 0.4, n: 24, cor: '#7C838E', semente: 2},
  {y: 1120, escala: 0.5, n: 19, cor: '#9EA3AA', semente: 3},
];
export const FILEIRAS_FRENTE: Fileira[] = [{y: 1720, escala: 1.25, n: 8, cor: '#1B2028', semente: 9}];

const Silhueta: React.FC<{x: number; y: number; s: number; cor: string}> = ({x, y, s, cor}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M-110,0 Q-110,-150 0,-160 Q110,-150 110,0 Z" fill={cor} />
    <circle cx={0} cy={-215} r={62} fill={cor} />
  </g>
);

export const Multidao: React.FC<{t: number; fileiras: Fileira[]; fuga?: number; centroFuga?: number; agito?: number}> = ({
  t, fileiras, fuga = 0, centroFuga = 400, agito = 1,
}) => {
  const p = pulso(t) * agito;
  return (
    <g>
      {fileiras.map((f) => {
        const passo = 1500 / f.n;
        return Array.from({length: f.n}, (_, i) => {
          const base = -260 + i * passo + ruido(f.semente * 100 + i) * passo * 0.6;
          const fase = ruido(f.semente * 7 + i) + 0.5;
          const dy = -p * 22 * f.escala * (0.6 + fase);
          const dir = base < centroFuga ? -1 : 1;
          const dx = fuga * dir * (500 + fase * 700) * f.escala;
          const corrida = fuga > 0 ? Math.abs(Math.sin(t * 9 + i)) * -14 * f.escala : 0;
          return <Silhueta key={`${f.semente}-${i}`} x={base + dx} y={f.y + dy + corrida} s={f.escala} cor={f.cor} />;
        });
      })}
    </g>
  );
};
