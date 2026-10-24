import React from 'react';
import {paleta} from '../../series/ano-zero/paleta';
import {fontes} from '../theme/fontes';
import {pulso, ruido, TL} from './tempo';

// Copacabana à noite em vetor: céu, prédios com janelas em pontos, mar em retícula,
// palco com telão e caixas de som, areia. Luzes do palco pulsam com a batida.

const PREDIOS = Array.from({length: 9}, (_, i) => ({x: 640 + i * 62, w: 54, h: 260 + ((i * 97) % 230)}));

export const Cenario: React.FC<{t: number; hora: string; faltam: string}> = ({t, hora, faltam}) => {
  const p = pulso(t);
  return (
    <g>
      <defs>
        <linearGradient id="ceu" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#05070B" />
          <stop offset="0.55" stopColor="#0B1424" />
          <stop offset="1" stopColor="#14223A" />
        </linearGradient>
        <linearGradient id="areia" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#3A2A1C" />
          <stop offset="1" stopColor="#120D09" />
        </linearGradient>
        <radialGradient id="brilho-palco" cx="0.5" cy="0.5" r="0.5">
          <stop offset="0" stopColor="#FFD9A0" stopOpacity="0.55" />
          <stop offset="1" stopColor="#FFD9A0" stopOpacity="0" />
        </radialGradient>
      </defs>
      <rect x={-600} y={-200} width={2280} height={1300} fill="url(#ceu)" />
      {/* prédios da orla, janelas em pontos */}
      {PREDIOS.map((b, i) => (
        <g key={i}>
          <rect x={b.x} y={900 - b.h} width={b.w} height={b.h} fill="#0D1522" />
          {Array.from({length: Math.floor(b.h / 26)}, (_, r) =>
            [0, 1, 2].map((c) =>
              ruido(i * 50 + r * 3 + c) > -0.15 ? (
                <circle key={`${r}-${c}`} cx={b.x + 12 + c * 15} cy={900 - b.h + 16 + r * 26} r={3.2} fill="#F2C27A" opacity={0.35 + (ruido(i + r + c * 7) + 0.5) * 0.5} />
              ) : null,
            ),
          )}
        </g>
      ))}
      {/* mar em retícula: pontos crescem para perto */}
      {Array.from({length: 7}, (_, r) =>
        Array.from({length: 46}, (_, c) => {
          const y = 870 + r * 12;
          const x = -300 + c * 38 + (r % 2) * 19 + Math.sin(t * 0.8 + c * 0.4 + r) * 4;
          return <circle key={`${r}-${c}`} cx={x} cy={y} r={1.6 + r * 0.55} fill="#5E7FA6" opacity={0.25 + r * 0.06} />;
        }),
      )}
      {/* balsas apagadas no horizonte */}
      <rect x={-120} y={858} width={90} height={8} fill="#1C2533" />
      <rect x={300} y={860} width={70} height={6} fill="#1C2533" />
      {/* areia */}
      <rect x={-600} y={950} width={2280} height={1300} fill="url(#areia)" />
      {/* palco: treliça, telão, caixas de som */}
      <ellipse cx={330} cy={640} rx={420 + p * 40} ry={300} fill="url(#brilho-palco)" opacity={0.45 + p * 0.5} />
      <g stroke="#7E8794" strokeWidth={6} fill="none">
        <path d="M60,1000 L60,420 L600,420 L600,1000" />
        <path d="M60,470 L600,470" />
        {Array.from({length: 12}, (_, i) => (
          <path key={i} d={`M${60 + i * 45},420 L${105 + i * 45},470`} />
        ))}
      </g>
      <rect x={150} y={500} width={360} height={220} rx={6} fill="#0A1018" stroke="#2A3640" strokeWidth={6} />
      <text x={330} y={600} textAnchor="middle" fontFamily={fontes.mono} fontSize={64} fill="#EDE6D6" opacity={0.55}>
        {hora}
      </text>
      <text x={330} y={660} textAnchor="middle" fontFamily={fontes.mono} fontSize={28} letterSpacing={6} fill={paleta.perigo} opacity={0.6}>
        {faltam}
      </text>
      {[90, 570].map((x) => (
        <g key={x}>
          <rect x={x - 50} y={740} width={100} height={260} rx={6} fill="#0B0E13" stroke="#2A3640" strokeWidth={4} />
          <circle cx={x} cy={820} r={30 + p * 6} fill="#151A22" stroke="#3A4452" strokeWidth={4} />
          <circle cx={x} cy={920} r={38 + p * 8} fill="#151A22" stroke="#3A4452" strokeWidth={4} />
        </g>
      ))}
      {/* feixes de luz do palco no ritmo */}
      {[150, 330, 510].map((x, i) => (
        <path key={x} d={`M${x},430 L${x - 160 + i * 40},1000 L${x + 120 + i * 40},1000 Z`} fill="#FFE2B0" opacity={0.05 + p * 0.12} />
      ))}
    </g>
  );
};

// Anéis vermelhos saindo das caixas de som em cada batida (a regra dos ecos).
export const AneisBatida: React.FC<{t: number; fontes: {x: number; y: number}[]; ate?: number}> = ({t, fontes: origens, ate = 99}) => {
  const vivos = TL.batidas.filter((b) => b <= t && t - b < 1.1 && b < ate);
  return (
    <g>
      {vivos.map((b) =>
        origens.map((o, k) => {
          const q = (t - b) / 1.1;
          return (
            <circle key={`${b}-${k}`} cx={o.x} cy={o.y} r={20 + q * 220} fill="none" stroke={paleta.perigo} strokeWidth={Math.max(1, 9 * (1 - q))} opacity={(1 - q) * 0.9} />
          );
        }),
      )}
    </g>
  );
};
