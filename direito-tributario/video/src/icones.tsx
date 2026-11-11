import React from 'react';
import {COR, MAO, tinta} from './estilo';

// Ícones desenhados (centro em 0,0, ~200px). Usar dentro de <svg> com transform.
type P = {x: number; y: number; s?: number; r?: number; children?: React.ReactNode};
export const G: React.FC<P> = ({x, y, s = 1, r = 0, children}) => (
  <g transform={`translate(${x} ${y}) rotate(${r}) scale(${s})`}>{children}</g>
);

export const Cofre: React.FC = () => (
  <g>
    <rect x={-150} y={-130} width={300} height={250} rx={18} fill={COR.cinza} {...tinta} />
    <rect x={-120} y={-100} width={240} height={190} rx={10} fill={COR.papelEscuro} {...tinta} strokeWidth={4} />
    <circle cx={0} cy={-5} r={48} fill={COR.mostarda} {...tinta} strokeWidth={4.5} />
    {[0, 60, 120, 180, 240, 300].map((a) => (
      <path key={a} d={`M 0 -5 L ${Math.cos((a * Math.PI) / 180) * 40} ${-5 + Math.sin((a * Math.PI) / 180) * 40}`} {...tinta} strokeWidth={4} />
    ))}
    <rect x={-60} y={-160} width={120} height={22} rx={6} fill={COR.tinta} />
    <rect x={-130} y={120} width={40} height={24} fill={COR.tinta} />
    <rect x={90} y={120} width={40} height={24} fill={COR.tinta} />
  </g>
);

export const Carteira: React.FC = () => (
  <g>
    <rect x={-90} y={-60} width={180} height={125} rx={18} fill={COR.laranja} {...tinta} />
    <path d="M -70 -60 L -40 -95 L 70 -95 L 80 -60" fill="#F7F3EA" {...tinta} strokeWidth={4} />
    <text x={10} y={-66} textAnchor="middle" fontFamily={MAO} fontSize={34} fill={COR.teal}>$</text>
    <rect x={30} y={-15} width={70} height={45} rx={10} fill={COR.mostarda} {...tinta} strokeWidth={4} />
    <circle cx={60} cy={8} r={7} fill={COR.tinta} />
  </g>
);

export const Sacola: React.FC = () => (
  <g>
    <path d="M -45 -50 Q -45 -110 0 -110 Q 45 -110 45 -50" fill="none" {...tinta} strokeWidth={8} />
    <path d="M -85 -55 L 85 -55 L 100 80 L -100 80 Z" fill={COR.jeans} {...tinta} />
    <path d="M -55 0 L 55 0" stroke="#F7F3EA" strokeWidth={6} strokeLinecap="round" opacity={0.7} />
  </g>
);

export const Casa: React.FC<{cor?: string}> = ({cor = COR.laranja}) => (
  <g>
    <path d="M -120 -10 L 0 -120 L 120 -10" fill={COR.vermelho} {...tinta} />
    <rect x={-95} y={-25} width={190} height={145} fill={cor} {...tinta} />
    <rect x={-25} y={40} width={50} height={80} fill={COR.tinta} opacity={0.85} />
    <rect x={-80} y={5} width={40} height={38} fill="#F7F3EA" {...tinta} strokeWidth={4} />
    <rect x={40} y={5} width={40} height={38} fill="#F7F3EA" {...tinta} strokeWidth={4} />
    <rect x={60} y={-105} width={26} height={50} fill={COR.cinza} {...tinta} strokeWidth={4} />
  </g>
);

export const Lixeira: React.FC = () => (
  <g>
    <path d="M -38 -40 L 38 -40 L 30 55 L -30 55 Z" fill={COR.salvia} {...tinta} strokeWidth={4.5} />
    <rect x={-46} y={-55} width={92} height={16} rx={6} fill={COR.teal} {...tinta} strokeWidth={4} />
    <path d="M -12 -20 L -10 40 M 12 -20 L 10 40" {...tinta} strokeWidth={3.5} />
  </g>
);

export const Caminhao: React.FC<{roda?: number}> = ({roda = 0}) => (
  <g>
    <rect x={-170} y={-110} width={230} height={150} rx={14} fill={COR.salvia} {...tinta} />
    <path d="M 60 -70 L 130 -70 L 170 -20 L 170 40 L 60 40 Z" fill={COR.teal} {...tinta} />
    <path d="M 80 -55 L 125 -55 L 150 -22 L 80 -22 Z" fill="#F7F3EA" {...tinta} strokeWidth={4} />
    <path d="M -140 -70 L 30 -70 M -140 -30 L 30 -30" stroke={COR.tinta} strokeWidth={4} opacity={0.4} />
    {[-110, 110].map((x) => (
      <g key={x} transform={`translate(${x} 45) rotate(${roda})`}>
        <circle r={34} fill={COR.tinta} />
        <circle r={14} fill={COR.cinza} />
        <path d="M -14 0 L 14 0" stroke={COR.tinta} strokeWidth={4} />
      </g>
    ))}
  </g>
);

export const Loja: React.FC = () => (
  <g>
    <rect x={-150} y={-60} width={300} height={190} fill={COR.papelEscuro} {...tinta} />
    <path d="M -170 -60 L -150 -130 L 150 -130 L 170 -60 Z" fill={COR.laranja} {...tinta} />
    {[-110, -40, 30, 100].map((x, i) => (
      <path key={x} d={`M ${x} -130 L ${x - 10} -60`} stroke={i % 2 ? COR.tinta : '#F7F3EA'} strokeWidth={4} opacity={0.6} />
    ))}
    <rect x={-120} y={-30} width={130} height={90} fill={COR.tealClaro} {...tinta} strokeWidth={4} />
    <rect x={40} y={-10} width={80} height={140} fill={COR.teal} {...tinta} strokeWidth={4} />
  </g>
);

export const Lupa: React.FC = () => (
  <g>
    <path d="M 55 55 L 130 130" {...tinta} strokeWidth={22} />
    <path d="M 55 55 L 130 130" stroke={COR.laranja} strokeWidth={13} strokeLinecap="round" />
    <circle r={80} fill="#FFFFFF" fillOpacity={0.35} {...tinta} strokeWidth={10} />
  </g>
);

export const Cone: React.FC = () => (
  <g>
    <path d="M -20 -90 L 20 -90 L 55 60 L -55 60 Z" fill={COR.laranja} {...tinta} />
    <path d="M -32 -30 L 32 -30 L 38 0 L -38 0 Z" fill="#F7F3EA" />
    <rect x={-80} y={55} width={160} height={24} rx={6} fill={COR.laranja} {...tinta} strokeWidth={4.5} />
  </g>
);

export const Marcador: React.FC = () => (
  <g>
    <path d="M -70 -100 L 70 -100 L 70 110 L 0 60 L -70 110 Z" fill={COR.vermelho} {...tinta} />
    <path d="M -28 -10 L -6 14 L 34 -36" stroke="#F7F3EA" strokeWidth={12} strokeLinecap="round" strokeLinejoin="round" fill="none" />
  </g>
);

export const Seta: React.FC<{d: string; p: number; cor?: string}> = ({d, p, cor = COR.tinta}) => (
  <path d={d} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} stroke={cor} strokeWidth={6}
    strokeLinecap="round" fill="none" markerEnd={p > 0.95 ? 'url(#ponta)' : undefined} />
);

export const DefsSeta: React.FC = () => (
  <defs>
    <marker id="ponta" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10" fill="none" stroke={COR.tinta} strokeWidth={2} strokeLinecap="round" />
    </marker>
  </defs>
);
