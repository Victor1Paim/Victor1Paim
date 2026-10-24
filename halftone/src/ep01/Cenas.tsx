import React from 'react';
import {paleta} from '../../series/ano-zero/paleta';
import {fontes} from '../theme/fontes';
import {ruido} from '../motion/tempo';

// Cenários do Ep. 1 em vetor chapado: calçadão de ondas, beira-mar em retícula,
// barreira da avenida. Mundo de 1080×1920; a câmera recorta.

const Ceu: React.FC<{tom?: string}> = ({tom = '#0D1628'}) => (
  <>
    <defs>
      <linearGradient id="ceu-ep" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#05070B" />
        <stop offset="1" stopColor={tom} />
      </linearGradient>
    </defs>
    <rect x={-800} y={-400} width={2680} height={1500} fill="url(#ceu-ep)" />
  </>
);

const Predios: React.FC<{y: number; semente: number; cor?: string}> = ({y, semente, cor = '#101826'}) => (
  <g>
    {Array.from({length: 16}, (_, i) => {
      const h = 220 + ((i * 97 + semente * 31) % 260);
      const x = -400 + i * 120;
      return (
        <g key={i}>
          <rect x={x} y={y - h} width={104} height={h} fill={cor} />
          {Array.from({length: Math.floor(h / 30)}, (_, r) =>
            [0, 1, 2].map((c) =>
              ruido(semente * 100 + i * 17 + r * 3 + c) > 0 ? (
                <rect key={`${r}-${c}`} x={x + 14 + c * 30} y={y - h + 14 + r * 30} width={14} height={14} fill="#E8C27A" opacity={0.55} />
              ) : null,
            ),
          )}
        </g>
      );
    })}
  </g>
);

const Poste: React.FC<{x: number; y: number}> = ({x, y}) => (
  <g>
    <circle cx={x} cy={y - 520} r={160} fill="#F2B544" opacity={0.12} />
    <rect x={x - 8} y={y - 520} width={16} height={520} fill="#2A2F38" />
    <rect x={x - 40} y={y - 540} width={80} height={24} rx={8} fill="#F2C27A" />
  </g>
);

const Palmeira: React.FC<{x: number; y: number}> = ({x, y}) => (
  <g>
    <path d={`M${x},${y} Q${x + 20},${y - 260} ${x - 10},${y - 520}`} stroke="#1B140E" strokeWidth={26} fill="none" />
    {[-60, -20, 20, 60, 110, -110].map((a, i) => (
      <path key={i} d={`M${x - 10},${y - 520} q${Math.cos((a * Math.PI) / 180) * 160},${-40 + Math.abs(a) * 0.9} ${Math.cos((a * Math.PI) / 180) * 260},${80 + Math.abs(a)}`} stroke="#0F1A12" strokeWidth={22} fill="none" strokeLinecap="round" />
    ))}
  </g>
);

// Calçadão de Copacabana: ondas pretas e brancas em faixas.
export const Calcadao: React.FC<{t: number}> = () => (
  <g>
    <Ceu />
    <Predios y={980} semente={3} />
    <rect x={-800} y={980} width={2680} height={1000} fill="#D9D4C7" />
    {Array.from({length: 12}, (_, r) => {
      const y0 = 1000 + r * 80;
      const amp = 18 + r * 3;
      let d = `M-800,${y0}`;
      for (let x = -800; x <= 1900; x += 60) d += ` Q${x + 30},${y0 + (Math.floor(x / 60) % 2 ? amp : -amp)} ${x + 60},${y0}`;
      return <path key={r} d={`${d} L1900,${y0 + 40} L-800,${y0 + 40} Z`} fill="#1A1C20" />;
    })}
    <Poste x={120} y={1020} />
    <Poste x={900} y={1020} />
    <Palmeira x={-120} y={1000} />
    <Palmeira x={1240} y={1000} />
  </g>
);

// Beira-mar: ondas em retícula, balsas apagadas, flores e velas na areia (oferendas, com respeito).
export const BeiraMar: React.FC<{t: number}> = ({t}) => (
  <g>
    <Ceu tom="#0B1424" />
    <rect x={-800} y={760} width={2680} height={420} fill="#0E1A24" />
    {Array.from({length: 10}, (_, r) =>
      Array.from({length: 60}, (_, c) => {
        const x = -800 + c * 46 + (r % 2) * 23 + Math.sin(t * 0.9 + c * 0.35 + r) * 6;
        return <circle key={`${r}-${c}`} cx={x} cy={790 + r * 38} r={2 + r * 0.9} fill="#5E7FA6" opacity={0.22 + r * 0.05} />;
      }),
    )}
    <rect x={-300} y={772} width={110} height={10} fill="#1C2533" />
    <rect x={560} y={776} width={90} height={8} fill="#1C2533" />
    <path d={`M-800,1180 Q0,${1150 + Math.sin(t * 1.2) * 14} 1880,1180 L1880,2100 L-800,2100 Z`} fill="#3A2C1E" />
    {[[-60, 1300], [200, 1360], [420, 1290], [760, 1340], [980, 1400]].map(([x, y], i) => (
      <g key={i}>
        <circle cx={x} cy={y} r={14} fill="#F4F2EC" />
        <circle cx={x + 18} cy={y + 6} r={12} fill="#F4F2EC" />
        <rect x={x - 40} y={y - 6} width={8} height={22} fill="#EDE6D6" />
        <circle cx={x - 36} cy={y - 14} r={6} fill="#F2B544" opacity={0.6 + Math.sin(t * 7 + i) * 0.3} />
      </g>
    ))}
  </g>
);

// Barreira da avenida: grades metálicas, asfalto, prédios com reflexo.
export const Barreira: React.FC<{t: number}> = () => (
  <g>
    <Ceu />
    <Predios y={1000} semente={7} cor="#121A28" />
    <rect x={-800} y={1000} width={2680} height={1000} fill="#1C1F25" />
    {[0, 1, 2, 3].map((k) => (
      <rect key={k} x={-600 + k * 640} y={1120} width={240} height={10} fill="#EDE6D6" opacity={0.35} />
    ))}
    {Array.from({length: 9}, (_, i) => (
      <g key={i} transform={`translate(${-500 + i * 260} 1250)`}>
        <rect x={0} y={-200} width={230} height={14} fill="#8A949C" />
        <rect x={0} y={-40} width={230} height={14} fill="#8A949C" />
        {Array.from({length: 8}, (_, k) => (
          <rect key={k} x={8 + k * 28} y={-200} width={6} height={170} fill="#6F7882" />
        ))}
        <path d="M10,-26 L-20,20 M220,-26 L250,20" stroke="#6F7882" strokeWidth={10} />
      </g>
    ))}
  </g>
);

// Mão de perto (gancho): a mão vazia da Bia; a fitinha do Caio some entre silhuetas.
export const CloseMao: React.FC<{u: number}> = ({u}) => {
  const some = Math.min(1, u / 1.3);
  return (
    <g>
      <rect x={-200} y={-200} width={1480} height={2320} fill="#120F0B" />
      {Array.from({length: 9}, (_, i) => (
        <g key={i} transform={`translate(${-120 + i * 170 + Math.sin(u * 2 + i) * 20} ${1050 + (i % 2) * 90}) scale(1.6)`} opacity={0.55}>
          <path d="M-110,0 Q-110,-150 0,-160 Q110,-150 110,0 L110,600 L-110,600 Z" fill="#2B2620" />
          <circle cx={0} cy={-215} r={62} fill="#2B2620" />
        </g>
      ))}
      {/* pulso do Caio com a fitinha, escapando para a direita */}
      <g transform={`translate(${430 + some * 830} ${1000 - some * 60}) rotate(${-8 + some * 10})`} opacity={1 - Math.max(0, some - 0.75) * 4}>
        <rect x={-40} y={-50} width={420} height={110} rx={50} fill="#7A4E33" stroke="#0A0C10" strokeWidth={10} />
        <rect x={10} y={-56} width={34} height={122} fill={paleta.perigo} stroke="#0A0C10" strokeWidth={6} />
        <circle cx={-40} cy={5} r={66} fill="#7A4E33" stroke="#0A0C10" strokeWidth={10} />
      </g>
      {/* mão aberta da Bia, vazia */}
      <g transform="translate(260 1180) rotate(-18)">
        <rect x={-60} y={0} width={150} height={700} rx={60} fill="#8A5A3C" stroke="#0A0C10" strokeWidth={10} />
        <ellipse cx={20} cy={-40} rx={150} ry={130} fill="#8A5A3C" stroke="#0A0C10" strokeWidth={10} />
        {[-90, -30, 30, 90].map((dx, i) => (
          <rect key={i} x={dx - 4 + 20} y={-220 + Math.abs(dx) * 0.4} width={52} height={170} rx={26} fill="#8A5A3C" stroke="#0A0C10" strokeWidth={9} />
        ))}
        <rect x={150} y={-90} width={52} height={140} rx={26} fill="#8A5A3C" stroke="#0A0C10" strokeWidth={9} transform="rotate(40 176 -20)" />
      </g>
    </g>
  );
};

// Tela de celular (inserto): chamada de vídeo do Caio, 23:05.
export const TelaChamada: React.FC<{u: number; toques: number[]}> = ({u, toques}) => {
  const vibra = toques.some((tc) => u >= tc && u < tc + 0.9) ? Math.sin(u * 90) * 6 : 0;
  return (
    <g>
      <rect x={-200} y={-200} width={1480} height={2320} fill="#0A0907" />
      <g transform={`translate(${190 + vibra} 360)`}>
        <rect x={0} y={0} width={700} height={1300} rx={70} fill="#0D1016" stroke="#2A3443" strokeWidth={10} />
        <rect x={30} y={40} width={640} height={1220} rx={46} fill="#141B26" />
        <text x={350} y={150} textAnchor="middle" fontFamily={fontes.mono} fontSize={44} fill="#8A949C">
          23:05
        </text>
        <text x={350} y={360} textAnchor="middle" fontFamily={fontes.mono} fontSize={34} letterSpacing={6} fill={paleta.sessoes.caio}>
          CHAMADA DE VÍDEO
        </text>
        <circle cx={350} cy={600} r={150} fill="#22324A" stroke={paleta.sessoes.caio} strokeWidth={8} />
        <text x={350} y={640} textAnchor="middle" fontFamily={fontes.marca} fontSize={120} fill="#EDE6D6">
          C
        </text>
        <text x={350} y={860} textAnchor="middle" fontFamily={fontes.marca} fontSize={110} fill="#EDE6D6">
          CAIO
        </text>
        <circle cx={190} cy={1110} r={66} fill={paleta.perigo} />
        <circle cx={510} cy={1110} r={66} fill={paleta.sessoes.davi} />
      </g>
    </g>
  );
};
