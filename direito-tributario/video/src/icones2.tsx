import React from 'react';
import {COR, MAO, tinta} from './estilo';
import {Caminhao, Carteira, Casa, Cofre, Cone, Lixeira, Loja, Lupa, Marcador, Sacola} from './icones';

// Mais ícones desenhados (centro 0,0; cabem num quadrado de ~240px).
const papel = '#F7F3EA';

export const Calendario: React.FC = () => (
  <g>
    <rect x={-100} y={-90} width={200} height={190} rx={14} fill={papel} {...tinta} />
    <rect x={-100} y={-90} width={200} height={52} rx={14} fill={COR.vermelho} {...tinta} />
    <path d="M -55 -110 L -55 -70 M 55 -110 L 55 -70" {...tinta} strokeWidth={10} />
    {[0, 1, 2].map((r) => [0, 1, 2, 3].map((c) => (
      <rect key={`${r}${c}`} x={-78 + c * 42} y={-20 + r * 38} width={28} height={24} rx={4}
        fill={r === 2 && c === 2 ? COR.laranja : COR.cinza} opacity={r === 2 && c === 2 ? 1 : 0.6} />
    )))}
  </g>
);

export const Documento: React.FC<{titulo?: string}> = ({titulo}) => (
  <g>
    <path d="M -85 -115 L 50 -115 L 90 -75 L 90 115 L -85 115 Z" fill={papel} {...tinta} />
    <path d="M 50 -115 L 50 -75 L 90 -75" fill={COR.cinza} {...tinta} strokeWidth={4} />
    {titulo && <text y={-60} textAnchor="middle" fontFamily={MAO} fontSize={34} fill={COR.teal}>{titulo}</text>}
    {[0, 1, 2, 3, 4].map((i) => (
      <path key={i} d={`M -60 ${-25 + i * 28} L ${i === 4 ? 10 : 62} ${-25 + i * 28}`} stroke={COR.cinza} strokeWidth={8} strokeLinecap="round" />
    ))}
  </g>
);

export const Cupom: React.FC = () => (
  <g>
    <path d="M -75 -120 L 75 -120 L 75 105 L 55 120 L 35 105 L 15 120 L -5 105 L -25 120 L -45 105 L -65 120 L -75 105 Z" fill={papel} {...tinta} />
    {[0, 1, 2, 3].map((i) => (
      <path key={i} d={`M -50 ${-80 + i * 32} L 50 ${-80 + i * 32}`} stroke={COR.cinza} strokeWidth={7} strokeLinecap="round" />
    ))}
    <rect x={-55} y={45} width={110} height={34} rx={6} fill={COR.mostarda} {...tinta} strokeWidth={4} />
  </g>
);

export const Carro: React.FC = () => (
  <g>
    <path d="M -130 20 L -110 -30 Q -95 -70 -50 -70 L 45 -70 Q 85 -70 105 -30 L 130 20 L 130 60 L -130 60 Z" fill={COR.jeans} {...tinta} />
    <path d="M -80 -30 L -60 -58 L -5 -58 L -5 -30 Z M 15 -30 L 15 -58 L 60 -58 L 85 -30 Z" fill={papel} {...tinta} strokeWidth={4} />
    {[-75, 75].map((x) => (
      <g key={x}><circle cx={x} cy={62} r={30} fill={COR.tinta} /><circle cx={x} cy={62} r={12} fill={COR.cinza} /></g>
    ))}
  </g>
);

export const Alerta: React.FC = () => (
  <g>
    <path d="M 0 -120 L 120 95 L -120 95 Z" fill={COR.mostarda} {...tinta} strokeWidth={7} />
    <path d="M 0 -45 L 0 25" {...tinta} strokeWidth={18} />
    <circle cx={0} cy={60} r={11} fill={COR.tinta} />
  </g>
);

export const Check: React.FC = () => (
  <g>
    <circle r={105} fill={COR.salvia} {...tinta} strokeWidth={7} />
    <path d="M -50 0 L -12 38 L 55 -40" stroke={COR.tinta} strokeWidth={20} strokeLinecap="round" strokeLinejoin="round" fill="none" />
  </g>
);

export const Xis: React.FC = () => (
  <g>
    <circle r={105} fill={COR.laranja} {...tinta} strokeWidth={7} />
    <path d="M -45 -45 L 45 45 M 45 -45 L -45 45" stroke={COR.tinta} strokeWidth={20} strokeLinecap="round" />
  </g>
);

export const Grafico: React.FC = () => (
  <g>
    <path d="M -110 -110 L -110 100 L 115 100" {...tinta} strokeWidth={7} fill="none" />
    {[[-80, 60, COR.tealClaro], [-25, 110, COR.mostarda], [30, 160, COR.laranja]].map(([x, h, c], i) => (
      <rect key={i} x={x as number} y={100 - (h as number)} width={42} height={h as number} fill={c as string} {...tinta} strokeWidth={5} />
    ))}
    <path d="M -90 10 L -10 -40 L 40 -20 L 105 -95" stroke={COR.vermelho} strokeWidth={8} strokeLinecap="round" fill="none" />
  </g>
);

export const Balanca: React.FC = () => (
  <g>
    <path d="M 0 -100 L 0 100 M -70 100 L 70 100 M -110 -70 L 110 -70" {...tinta} strokeWidth={10} />
    {[-1, 1].map((s) => (
      <g key={s}>
        <path d={`M ${s * 110} -70 L ${s * 110 - 45} 10 M ${s * 110} -70 L ${s * 110 + 45} 10`} {...tinta} strokeWidth={4} />
        <path d={`M ${s * 110 - 60} 10 Q ${s * 110} 55 ${s * 110 + 60} 10 Z`} fill={COR.mostarda} {...tinta} strokeWidth={5} />
      </g>
    ))}
    <circle cx={0} cy={-100} r={14} fill={COR.laranja} {...tinta} strokeWidth={4} />
  </g>
);

export const Celular: React.FC<{texto?: string}> = ({texto = 'PIX'}) => (
  <g>
    <rect x={-70} y={-125} width={140} height={250} rx={22} fill={COR.tinta} />
    <rect x={-58} y={-100} width={116} height={190} rx={8} fill={COR.tealClaro} />
    <path d="M 0 -60 L 38 -22 L 0 16 L -38 -22 Z" fill={COR.teal} {...tinta} strokeWidth={4} />
    <text y={70} textAnchor="middle" fontFamily={MAO} fontSize={40} fill={COR.tinta}>{texto}</text>
  </g>
);

export const Predio: React.FC = () => (
  <g>
    <rect x={-80} y={-120} width={160} height={235} fill={COR.cinza} {...tinta} />
    {[0, 1, 2, 3].map((r) => [0, 1, 2].map((c) => (
      <rect key={`${r}${c}`} x={-58 + c * 45} y={-98 + r * 45} width={26} height={28} fill={papel} {...tinta} strokeWidth={3} />
    )))}
    <rect x={-20} y={75} width={40} height={40} fill={COR.teal} {...tinta} strokeWidth={4} />
  </g>
);

export const Livro: React.FC = () => (
  <g>
    <path d="M 0 -70 Q -60 -105 -120 -80 L -120 85 Q -60 60 0 95 Q 60 60 120 85 L 120 -80 Q 60 -105 0 -70 Z" fill={papel} {...tinta} />
    <path d="M 0 -70 L 0 95" {...tinta} strokeWidth={5} />
    <path d="M -95 -40 Q -50 -60 -20 -42 M -95 -5 Q -50 -25 -20 -7 M 20 -42 Q 50 -60 95 -40" stroke={COR.cinza} strokeWidth={6} fill="none" strokeLinecap="round" />
  </g>
);

export const Saude: React.FC = () => (
  <g>
    <rect x={-105} y={-105} width={210} height={210} rx={30} fill={papel} {...tinta} />
    <path d="M -25 -70 L 25 -70 L 25 -25 L 70 -25 L 70 25 L 25 25 L 25 70 L -25 70 L -25 25 L -70 25 L -70 -25 L -25 -25 Z" fill={COR.vermelho} {...tinta} strokeWidth={5} />
  </g>
);

export const Relogio: React.FC = () => (
  <g>
    <circle r={105} fill={papel} {...tinta} strokeWidth={7} />
    {[0, 1, 2, 3].map((i) => (
      <path key={i} d={`M 0 -92 L 0 -78`} transform={`rotate(${i * 90})`} {...tinta} strokeWidth={6} />
    ))}
    <path d="M 0 0 L 0 -60 M 0 0 L 42 20" {...tinta} strokeWidth={9} />
    <circle r={9} fill={COR.vermelho} />
  </g>
);

export const Lampada: React.FC = () => (
  <g>
    <path d="M -45 50 Q -95 0 -80 -55 Q -60 -120 0 -120 Q 60 -120 80 -55 Q 95 0 45 50 Z" fill={COR.mostarda} {...tinta} />
    <rect x={-42} y={50} width={84} height={50} rx={8} fill={COR.cinza} {...tinta} strokeWidth={5} />
    <path d="M -20 -20 Q 0 10 20 -20" stroke={COR.tinta} strokeWidth={5} fill="none" />
    {[-1, 1].map((s) => <path key={s} d={`M ${s * 120} -80 L ${s * 145} -100 M ${s * 125} -20 L ${s * 155} -20`} {...tinta} strokeWidth={6} />)}
  </g>
);

export const Cafe: React.FC = () => (
  <g>
    <path d="M -85 -40 L 75 -40 L 60 80 Q 0 100 -70 80 Z" fill={papel} {...tinta} />
    <path d="M 72 -15 Q 125 -15 115 30 Q 105 60 63 55" fill="none" {...tinta} strokeWidth={8} />
    <path d="M -80 -40 L 70 -40 L 66 -10 L -76 -10 Z" fill="#7A4E2D" />
    {[-30, 10, 50].map((x) => <path key={x} d={`M ${x} -60 q -15 -25 0 -45 q 15 -20 0 -40`} stroke={COR.cinza} strokeWidth={6} fill="none" strokeLinecap="round" />)}
    <rect x={-110} y={88} width={210} height={16} rx={8} fill={COR.mostarda} {...tinta} strokeWidth={4} />
  </g>
);

export const Moedas: React.FC = () => (
  <g>
    {[[-50, 40], [10, 50], [60, 30], [-20, -5], [35, -15], [5, -55]].map(([x, y], i) => (
      <g key={i} transform={`translate(${x} ${y})`}>
        <circle r={42} fill={COR.mostarda} {...tinta} strokeWidth={5} />
        <text y={15} textAnchor="middle" fontFamily={MAO} fontSize={44} fill={COR.tinta}>$</text>
      </g>
    ))}
  </g>
);

// Registro: nome usado no elementos.json → desenho + escala para caber em ~240px.
export const ICONES: Record<string, {el: React.ReactNode; s: number}> = {
  cofre: {el: <Cofre />, s: 0.75},
  carteira: {el: <Carteira />, s: 1.15},
  sacola: {el: <Sacola />, s: 1.15},
  casa: {el: <Casa />, s: 1},
  lixeira: {el: <Lixeira />, s: 1.9},
  caminhao: {el: <Caminhao />, s: 0.65},
  loja: {el: <Loja />, s: 0.75},
  lupa: {el: <Lupa />, s: 0.95},
  cone: {el: <Cone />, s: 1.2},
  marcador: {el: <Marcador />, s: 1},
  calendario: {el: <Calendario />, s: 1},
  documento: {el: <Documento />, s: 1},
  declaracao: {el: <Documento titulo="IR" />, s: 1},
  nota: {el: <Cupom />, s: 1},
  carro: {el: <Carro />, s: 0.85},
  alerta: {el: <Alerta />, s: 0.95},
  check: {el: <Check />, s: 1},
  xis: {el: <Xis />, s: 1},
  grafico: {el: <Grafico />, s: 1},
  balanca: {el: <Balanca />, s: 1},
  pix: {el: <Celular />, s: 0.95},
  celular: {el: <Celular texto="" />, s: 0.95},
  empresa: {el: <Predio />, s: 1},
  livro: {el: <Livro />, s: 1},
  saude: {el: <Saude />, s: 1},
  relogio: {el: <Relogio />, s: 1},
  dica: {el: <Lampada />, s: 0.95},
  cafe: {el: <Cafe />, s: 1},
  moedas: {el: <Moedas />, s: 1.3},
};
