import React from 'react';

// Personagem "cartoon" de cabeça grande: traço grosso, cores chapadas, rosto simples.
// Origem nos pés. Altura ~900 px na escala 1 (cabeça ~ 1/3 do corpo).

const TINTA = '#0A0C10';

export type BonecoProps = {
  x: number;
  y: number;
  escala?: number;
  pele?: string;
  camisa?: string;
  calca?: string;
  cabelo?: 'curto' | 'cacheado' | 'grisalho' | 'calvo';
  corCabelo?: string;
  bigode?: boolean;
  oculos?: boolean;
  cracha?: boolean;
  fitinha?: boolean;
  vestido?: boolean;
  sentado?: boolean;
  boca?: 'reta' | 'sorriso' | 'preocupado' | 'aberta';
  olhar?: number; // -1 esquerda, 0 frente, 1 direita
  piscar?: boolean;
  bracoE?: number; // graus (0 = pendurado)
  bracoD?: number;
  inclina?: number;
};

export const Boneco: React.FC<BonecoProps> = ({
  x, y, escala = 1, pele = '#C68B62', camisa = '#2F4F86', calca = '#1D2740', cabelo = 'curto', corCabelo = '#14100E',
  bigode, oculos, cracha, fitinha, vestido, sentado, boca = 'reta', olhar = 0, piscar, bracoE = 12, bracoD = -12, inclina = 0,
}) => {
  const traco = {stroke: TINTA, strokeWidth: 9, strokeLinejoin: 'round' as const, strokeLinecap: 'round' as const};
  const quadril = sentado ? -230 : -330;
  const braco = (lado: number, ang: number) => (
    <g transform={`translate(${lado * 108} ${quadril - 250}) rotate(${ang})`}>
      <path d={`M0,0 L${lado * 18},210`} stroke={TINTA} strokeWidth={66} strokeLinecap="round" />
      <path d={`M0,0 L${lado * 18},210`} stroke={camisa} strokeWidth={48} strokeLinecap="round" />
      {fitinha && lado === -1 ? <path d={`M${lado * 6},170 L${lado * 30},178`} stroke="#E0413A" strokeWidth={16} /> : null}
      <circle cx={lado * 20} cy={236} r={30} fill={pele} {...traco} />
    </g>
  );
  return (
    <g transform={`translate(${x} ${y}) scale(${escala}) rotate(${inclina})`}>
      {/* sombra no chão */}
      <ellipse cx={0} cy={6} rx={170} ry={22} fill="#000" opacity={0.35} />
      {/* pernas */}
      {sentado ? (
        <>
          <path d="M-70,-230 L60,-230 L60,-60" stroke={TINTA} strokeWidth={84} strokeLinejoin="round" fill="none" />
          <path d="M-70,-230 L60,-230 L60,-60" stroke={calca} strokeWidth={66} strokeLinejoin="round" fill="none" />
          <ellipse cx={92} cy={-30} rx={62} ry={30} fill="#E9E6DF" {...traco} />
        </>
      ) : (
        [-1, 1].map((l) => (
          <g key={l}>
            <path d={`M${l * 48},${quadril} L${l * 52},-40`} stroke={TINTA} strokeWidth={80} strokeLinecap="round" />
            <path d={`M${l * 48},${quadril} L${l * 52},-40`} stroke={vestido ? pele : calca} strokeWidth={62} strokeLinecap="round" />
            <ellipse cx={l * 62} cy={-22} rx={58} ry={28} fill="#E9E6DF" {...traco} />
          </g>
        ))
      )}
      {/* tronco */}
      {vestido ? (
        <path d={`M-100,${quadril - 270} Q0,${quadril - 290} 100,${quadril - 270} L150,${quadril + 70} Q0,${quadril + 95} -150,${quadril + 70} Z`} fill={camisa} {...traco} />
      ) : (
        <rect x={-118} y={quadril - 280} width={236} height={300} rx={46} fill={camisa} {...traco} />
      )}
      {cracha ? (
        <g transform={`translate(52 ${quadril - 210})`}>
          <rect x={-30} y={0} width={60} height={34} rx={5} fill="#EDE6D6" stroke={TINTA} strokeWidth={5} />
          <rect x={-22} y={12} width={44} height={6} fill="#2A3640" />
        </g>
      ) : null}
      {braco(-1, bracoE)}
      {braco(1, bracoD)}
      {/* cabeça */}
      <g transform={`translate(0 ${quadril - 300})`}>
        <circle cx={0} cy={-150} r={162} fill={pele} {...traco} />
        <path d="M-150,-90 Q0,10 150,-90 Q120,10 0,10 Q-120,10 -150,-90 Z" fill="#000" opacity={0.1} />
        {cabelo === 'curto' ? <path d="M-158,-170 Q-150,-318 0,-316 Q150,-318 158,-170 Q120,-236 0,-236 Q-120,-236 -158,-170 Z" fill={corCabelo} {...traco} /> : null}
        {cabelo === 'grisalho' ? <path d="M-158,-160 Q-150,-318 0,-316 Q150,-318 158,-160 Q130,-230 0,-232 Q-130,-230 -158,-160 Z" fill="#B9BEC4" {...traco} /> : null}
        {cabelo === 'cacheado'
          ? [-120, -70, -20, 30, 80, 125, -145, 150].map((cx, i) => (
              <circle key={i} cx={cx} cy={-270 + (i % 2) * 18 + (i > 5 ? 70 : 0)} r={46} fill={corCabelo} {...traco} strokeWidth={6} />
            ))
          : null}
        {/* olhos */}
        {piscar ? (
          <>
            <path d={`M${-62 + olhar * 16},-150 h40`} {...traco} />
            <path d={`M${22 + olhar * 16},-150 h40`} {...traco} />
          </>
        ) : (
          <>
            <ellipse cx={-42 + olhar * 16} cy={-150} rx={17} ry={26} fill={TINTA} />
            <ellipse cx={42 + olhar * 16} cy={-150} rx={17} ry={26} fill={TINTA} />
          </>
        )}
        {oculos ? (
          <g fill="none" stroke={TINTA} strokeWidth={7}>
            <circle cx={-42} cy={-150} r={40} />
            <circle cx={42} cy={-150} r={40} />
            <path d="M-2,-150 h4" />
          </g>
        ) : null}
        {bigode ? <path d="M-58,-78 Q-30,-104 0,-86 Q30,-104 58,-78 Q30,-70 0,-76 Q-30,-70 -58,-78 Z" fill="#E9E6DF" {...traco} strokeWidth={6} /> : null}
        {boca === 'reta' ? <path d="M-24,-60 h48" {...traco} /> : null}
        {boca === 'sorriso' ? <path d="M-34,-66 Q0,-34 34,-66" fill="none" {...traco} /> : null}
        {boca === 'preocupado' ? <path d="M-34,-50 Q0,-78 34,-50" fill="none" {...traco} /> : null}
        {boca === 'aberta' ? <ellipse cx={0} cy={-56} rx={24} ry={30} fill={TINTA} /> : null}
      </g>
    </g>
  );
};
