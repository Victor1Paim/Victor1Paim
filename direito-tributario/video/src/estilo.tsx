import React from 'react';
import {AbsoluteFill, Easing, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {loadFont} from '@remotion/fonts';

// Fonte local (Patrick Hand, OFL): o Chromium do render não confia no proxy para baixar do Google Fonts.
export const MAO = 'Patrick Hand';
loadFont({family: MAO, url: staticFile('fontes/PatrickHand-latin.woff2')});
loadFont({family: MAO, url: staticFile('fontes/PatrickHand-latinext.woff2'), unicodeRange: 'U+0100-024F, U+1E00-1EFF'});

// Paleta: papel + nanquim + cores apagadas (teal e laranja vêm da identidade do PDF).
export const COR = {
  papel: '#ECE8DC',
  papelEscuro: '#E2DCCB',
  tinta: '#2E2925',
  teal: '#3F8A86',
  tealClaro: '#9CC5BF',
  laranja: '#DE8A55',
  mostarda: '#D9B45A',
  jeans: '#7189AB',
  salvia: '#A9BC97',
  vermelho: '#A3303F',
  pele: '#F1D7BF',
  cinza: '#B9B2A3',
};

export const FPS = 30;
export const W = 1080;
export const H = 1920;
export const DIVISA = 768; // 40% da altura para o apresentador

export const suave = Easing.bezier(0.33, 0, 0.2, 1);
export const mola = Easing.bezier(0.34, 1.56, 0.64, 1);

export const entre = (f: number, ini: number, dur: number, de = 0, ate = 1, ease = suave) =>
  interpolate(f, [ini, ini + dur], [de, ate], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});

// Traço "fervendo" (boil) como em animação desenhada à mão: o ruído muda a cada 4 quadros (~8 desenhos/s).
export const FiltrosTraco: React.FC = () => {
  const f = useCurrentFrame();
  const seed = Math.floor(f / 4) % 6;
  return (
    <svg width={0} height={0} style={{position: 'absolute'}}>
      <defs>
        <filter id="boil" x="-5%" y="-5%" width="110%" height="110%">
          <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves={2} seed={seed} result="r" />
          <feDisplacementMap in="SourceGraphic" in2="r" scale={5} xChannelSelector="R" yChannelSelector="G" />
        </filter>
        <filter id="grao">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={seed} />
          <feColorMatrix values="0 0 0 0 0.3  0 0 0 0 0.25  0 0 0 0 0.2  0 0 0 0.10 0" />
        </filter>
        <filter id="lapis">
          <feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves={1} seed={seed} result="n" />
          <feDisplacementMap in="SourceGraphic" in2="n" scale={2.5} />
        </filter>
      </defs>
    </svg>
  );
};

export const Papel: React.FC<{tom?: string}> = ({tom = COR.papel}) => (
  <AbsoluteFill style={{background: tom}}>
    <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
      <rect width={W} height={H} filter="url(#grao)" />
    </svg>
    <AbsoluteFill
      style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(80,60,30,0.16) 100%)'}}
    />
  </AbsoluteFill>
);

// Camada de desenho: tudo dentro "ferve" levemente.
export const Desenho: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
  <AbsoluteFill style={{filter: 'url(#boil)', ...style}}>{children}</AbsoluteFill>
);

export const tinta = {stroke: COR.tinta, strokeWidth: 5, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const};

// Caminho que se "desenha" (progresso 0→1).
export const Traco: React.FC<{d: string; p: number; cor?: string; largura?: number; fill?: string}> = ({
  d,
  p,
  cor = COR.tinta,
  largura = 5,
  fill = 'none',
}) => (
  <path
    d={d}
    pathLength={1}
    strokeDasharray={1}
    strokeDashoffset={1 - p}
    stroke={cor}
    strokeWidth={largura}
    strokeLinecap="round"
    strokeLinejoin="round"
    fill={fill}
  />
);

// Texto manuscrito em caixa alta.
export const Escrito: React.FC<{
  children: React.ReactNode;
  tam?: number;
  cor?: string;
  style?: React.CSSProperties;
}> = ({children, tam = 64, cor = COR.tinta, style}) => (
  <div
    style={{
      fontFamily: MAO,
      fontSize: tam,
      color: cor,
      textTransform: 'uppercase',
      letterSpacing: tam * 0.04,
      lineHeight: 1.05,
      textAlign: 'center',
      ...style,
    }}
  >
    {children}
  </div>
);

// Moeda desenhada.
export const Moeda: React.FC<{x: number; y: number; r?: number; s?: number}> = ({x, y, r = 34, s = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <circle r={r} fill={COR.mostarda} {...tinta} strokeWidth={4.5} />
    <circle r={r * 0.68} fill="none" stroke={COR.tinta} strokeWidth={2.5} opacity={0.6} />
    <text
      y={r * 0.36}
      textAnchor="middle"
      fontFamily={MAO}
      fontSize={r * 1.05}
      fill={COR.tinta}
    >
      $
    </text>
  </g>
);
