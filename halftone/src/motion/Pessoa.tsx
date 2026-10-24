import React from 'react';

// Personagem vetorial no estilo da Halftone: traço de nanquim, roupa branca de Réveillon,
// luz de recorte (sódio âmbar de um lado, noite azul do outro) e sombra em retícula.
// Origem nos pés. Altura ~760 px na escala 1.

export type Acessorio = 'rabo' | 'fitinha' | 'oculos' | 'cracha' | 'isopor' | 'cacheado' | 'grisalho';

export type PessoaProps = {
  id: string;
  x: number;
  y: number;
  escala?: number;
  pele?: string;
  roupa?: string;
  cabelo?: string;
  recorte?: string;
  acessorios?: Acessorio[];
  inclinaCabeca?: number;
  corpo?: number; // rotação do corpo inteiro (90 = deitado)
  bracoE?: number;
  bracoD?: number;
  saia?: boolean;
  de?: 'frente' | 'costas';
  eco?: boolean;
  opacidade?: number;
};

const TINTA = '#0A0C10';

export const Pessoa: React.FC<PessoaProps> = ({
  id, x, y, escala = 1, pele = '#8A5A3C', roupa = '#E6E0D2', cabelo = '#1A1412', recorte = '#F2B544',
  acessorios = [], inclinaCabeca = 0, corpo = 0, bracoE = 8, bracoD = -8, saia, de = 'frente', eco, opacidade = 1,
}) => {
  const tem = (a: Acessorio) => acessorios.includes(a);
  const corPele = eco ? '#8C918E' : pele;
  const traco = {stroke: TINTA, strokeWidth: 5, strokeLinejoin: 'round' as const};

  const braco = (lado: number, ang: number) => (
    <g key={lado} transform={`translate(${lado * 96} -548) rotate(${ang})`}>
      <path d="M-12,0 L12,8 L10,250 L-10,250 Z" fill={corPele} {...traco} />
      <circle cx={0} cy={262} r={19} fill={corPele} {...traco} />
      <path d="M-27,-14 Q0,-30 27,-14 L25,96 Q0,104 -25,96 Z" fill={roupa} {...traco} />
      {lado === -1 && tem('fitinha') ? <rect x={-14} y={214} width={28} height={13} fill="#E0413A" stroke={TINTA} strokeWidth={3} /> : null}
    </g>
  );

  const formas = (fill?: string) => {
    const f = (c: string) => fill ?? c;
    return (
      <>
        {/* pernas */}
        {[-1, 1].map((l) => (
          <g key={l}>
            <path d={`M${l * 46 - 20},-260 L${l * 46 + 20},-260 L${l * 36 + 14},-24 L${l * 36 - 14},-24 Z`} fill={f(corPele)} {...traco} />
            <ellipse cx={l * 38} cy={-14} rx={30} ry={15} fill={f('#F2F0EA')} {...traco} />
          </g>
        ))}
        {saia ? (
          <path d="M-86,-560 Q0,-575 86,-560 L132,-238 Q0,-212 -132,-238 Z" fill={f(roupa)} {...traco} />
        ) : (
          <path d="M-74,-342 Q0,-356 74,-342 L72,-226 L10,-226 L0,-268 L-10,-226 L-72,-226 Z" fill={f('#CFC7B6')} {...traco} />
        )}
        {/* tronco */}
        <path
          d="M-58,-598 Q-104,-596 -112,-552 L-94,-330 Q0,-316 94,-330 L112,-552 Q104,-596 58,-598 Q0,-568 -58,-598 Z"
          fill={f(roupa)}
          {...traco}
        />
        {/* pescoço e cabeça */}
        <g transform={`translate(0 -590) rotate(${inclinaCabeca})`}>
          <path d="M-20,8 L20,8 L18,-34 L-18,-34 Z" fill={f(corPele)} {...traco} />
          <ellipse cx={0} cy={-96} rx={60} ry={70} fill={f(corPele)} {...traco} />
        </g>
      </>
    );
  };

  return (
    <g transform={`translate(${x} ${y}) scale(${escala}) rotate(${corpo})`} opacity={opacidade}>
      <defs>
        <pattern id={`${id}-dots`} width={11} height={11} patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <circle cx={5.5} cy={5.5} r={3.3} fill="#0B1428" />
        </pattern>
        <linearGradient id={`${id}-grad`} x1="0" x2="1">
          <stop offset="0" stopColor="#000" />
          <stop offset="0.45" stopColor="#000" />
          <stop offset="1" stopColor="#fff" />
        </linearGradient>
        <mask id={`${id}-mask`} maskUnits="userSpaceOnUse" x={-200} y={-800} width={400} height={820}>
          <rect x={-200} y={-800} width={400} height={820} fill={`url(#${id}-grad)`} />
        </mask>
        <linearGradient id={`${id}-rim`} x1="0" x2="1">
          <stop offset="0" stopColor={recorte} stopOpacity="0.55" />
          <stop offset="0.3" stopColor={recorte} stopOpacity="0" />
        </linearGradient>
      </defs>
      {/* braços atrás quando de costas */}
      {de === 'costas' ? [braco(-1, bracoE), braco(1, bracoD)] : null}
      {formas()}
      {/* sombra em retícula e luz de recorte */}
      <g mask={`url(#${id}-mask)`} opacity={0.75}>{formas(`url(#${id}-dots)`)}</g>
      <g style={{mixBlendMode: 'screen'}}>{formas(`url(#${id}-rim)`)}</g>
      {eco ? (
        <>
          <ellipse cx={-34} cy={-450} rx={30} ry={18} fill="#5B4A36" opacity={0.6} />
          <ellipse cx={44} cy={-370} rx={22} ry={28} fill="#5B4A36" opacity={0.5} />
        </>
      ) : null}
      {tem('cracha') && de === 'frente' ? (
        <g transform="translate(34 -470)">
          <path d="M-36,-110 L0,0 M30,-112 L10,0" stroke="#2A3640" strokeWidth={4} fill="none" />
          <rect x={-16} y={0} width={42} height={56} rx={4} fill="#F4F6F8" {...traco} strokeWidth={3} />
          <rect x={-16} y={0} width={42} height={13} fill="#3F7FBF" />
        </g>
      ) : null}
      {tem('isopor') ? <rect x={78} y={-430} width={116} height={140} rx={10} fill="#3F86C9" {...traco} /> : null}
      {de === 'frente' ? [braco(-1, bracoE), braco(1, bracoD)] : null}
      {/* rosto e cabelo */}
      <g transform={`translate(0 -590) rotate(${inclinaCabeca})`}>
        {de === 'frente' ? (
          eco ? (
            <>
              <ellipse cx={-22} cy={-100} rx={11} ry={8} fill="#E3ECEF" stroke={TINTA} strokeWidth={3} />
              <ellipse cx={22} cy={-100} rx={11} ry={8} fill="#E3ECEF" stroke={TINTA} strokeWidth={3} />
              <path d="M-14,-56 Q0,-48 14,-56" stroke={TINTA} strokeWidth={5} fill="#2A1F18" />
            </>
          ) : (
            <>
              <path d="M-34,-116 L-12,-112 M12,-112 L34,-116" stroke={TINTA} strokeWidth={5} />
              <circle cx={-22} cy={-98} r={6} fill={TINTA} />
              <circle cx={22} cy={-98} r={6} fill={TINTA} />
              <path d="M-12,-60 Q0,-56 12,-60" stroke={TINTA} strokeWidth={4} fill="none" />
            </>
          )
        ) : null}
        {tem('cacheado')
          ? [-48, -22, 6, 32, 52, -58, 60].map((cx, i) => (
              <circle key={i} cx={cx} cy={-150 + (i % 2) * 12 + (i > 4 ? 40 : 0)} r={28} fill={cabelo} {...traco} strokeWidth={3} />
            ))
          : null}
        {tem('rabo') ? (
          <>
            <circle cx={0} cy={-188} r={40} fill={cabelo} {...traco} />
            <circle cx={32} cy={-212} r={26} fill={cabelo} {...traco} strokeWidth={3} />
            <circle cx={-28} cy={-218} r={22} fill={cabelo} {...traco} strokeWidth={3} />
            <path d="M-62,-110 Q-58,-172 0,-170 Q58,-172 62,-110 Q36,-146 0,-144 Q-36,-146 -62,-110 Z" fill={cabelo} {...traco} />
          </>
        ) : null}
        {tem('grisalho') ? <path d="M-62,-104 Q-58,-174 0,-170 Q58,-174 62,-104 Q40,-140 0,-138 Q-40,-140 -62,-104 Z" fill="#9AA0A6" {...traco} /> : null}
        {!tem('cacheado') && !tem('rabo') && !tem('grisalho') ? (
          <path d="M-62,-104 Q-58,-174 0,-170 Q58,-174 62,-104 Q40,-136 0,-134 Q-40,-136 -62,-104 Z" fill={cabelo} {...traco} />
        ) : null}
        {de === 'costas' && !tem('cacheado') ? <ellipse cx={0} cy={-110} rx={58} ry={56} fill={cabelo} /> : null}
        {tem('oculos') ? (
          <g transform="translate(0 -160)">
            <rect x={-58} y={-14} width={50} height={26} rx={12} fill="#F2B544" {...traco} strokeWidth={3} />
            <rect x={8} y={-14} width={50} height={26} rx={12} fill="#3DDC97" {...traco} strokeWidth={3} />
          </g>
        ) : null}
      </g>
    </g>
  );
};
