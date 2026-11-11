import React from 'react';
import {useCurrentFrame} from 'remotion';
import {COR, tinta, W, DIVISA} from './estilo';

// Apresentador PROVISÓRIO (desenhado) no lugar da gravação real da câmera.
// boca = abertura 0..1 (volume da voz); gesto = 0..1 braço levantado.
export const Apresentador: React.FC<{boca: number; gesto: number}> = ({boca, gesto}) => {
  const f = useCurrentFrame();
  const piscando = f % 96 > 90;
  const bob = Math.sin(f / 9) * 3 + boca * 6;
  const cx = W / 2;
  const cy = 330 - bob;
  const ab = Math.max(0.08, boca);
  const braco = -20 - gesto * 95; // ângulo do antebraço

  return (
    <svg width={W} height={DIVISA} viewBox={`0 0 ${W} ${DIVISA}`}>
      {/* estante ao fundo */}
      <g opacity={0.55}>
        <path d="M 90 250 L 330 250 M 90 420 L 330 420" {...tinta} strokeWidth={4} />
        {[0, 1, 2, 3, 4].map((i) => (
          <rect key={i} x={105 + i * 42} y={170 + (i % 2) * 14} width={32} height={80 - (i % 2) * 14}
            fill={[COR.teal, COR.laranja, COR.mostarda, COR.jeans, COR.salvia][i]} {...tinta} strokeWidth={3} />
        ))}
        {[0, 1, 2].map((i) => (
          <rect key={i} x={120 + i * 52} y={350} width={40} height={70}
            fill={[COR.salvia, COR.vermelho, COR.tealClaro][i]} {...tinta} strokeWidth={3} />
        ))}
        <path d="M 790 200 q 50 -60 100 0 q 20 60 -50 80 q -70 -20 -50 -80 z" fill={COR.salvia} {...tinta} strokeWidth={3} />
        <path d="M 800 290 L 880 290 L 865 400 L 815 400 Z" fill={COR.laranja} {...tinta} strokeWidth={3} />
      </g>

      {/* corpo / blazer */}
      <g transform={`translate(0 ${-bob * 0.4})`}>
        <path d={`M ${cx - 230} 790 Q ${cx - 220} 520 ${cx - 70} 490 L ${cx + 70} 490 Q ${cx + 220} 520 ${cx + 230} 790 Z`}
          fill={COR.teal} {...tinta} />
        <path d={`M ${cx - 70} 490 L ${cx} 600 L ${cx + 70} 490 Z`} fill="#F7F3EA" {...tinta} strokeWidth={4} />
        <path d={`M ${cx - 70} 490 L ${cx - 30} 640 M ${cx + 70} 490 L ${cx + 30} 640`} {...tinta} strokeWidth={4} fill="none" />
        <path d={`M ${cx} 520 L ${cx - 16} 560 L ${cx} 640 L ${cx + 16} 560 Z`} fill={COR.laranja} {...tinta} strokeWidth={3.5} />
        {/* braço esquerdo (do espectador: direita) com gesto */}
        <g transform={`translate(${cx + 175} 600)`}>
          <path d="M 0 0 L 40 120" {...tinta} strokeWidth={46} stroke={COR.tinta} />
          <path d="M 0 0 L 40 120" strokeWidth={36} stroke={COR.teal} strokeLinecap="round" />
          <g transform={`translate(40 120) rotate(${braco})`}>
            <path d="M 0 0 L -10 -130" strokeWidth={42} stroke={COR.tinta} strokeLinecap="round" />
            <path d="M 0 0 L -10 -130" strokeWidth={32} stroke={COR.teal} strokeLinecap="round" />
            <circle cx={-12} cy={-158} r={26} fill={COR.pele} {...tinta} strokeWidth={4} />
            <path d="M -12 -180 L -14 -210" {...tinta} strokeWidth={13} stroke={COR.tinta} />
            <path d="M -12 -180 L -14 -208" strokeWidth={7} stroke={COR.pele} strokeLinecap="round" />
          </g>
        </g>
      </g>

      {/* pescoço + cabeça */}
      <path d={`M ${cx - 32} ${cy + 110} L ${cx - 32} ${cy + 170} L ${cx + 32} ${cy + 170} L ${cx + 32} ${cy + 110}`}
        fill={COR.pele} {...tinta} strokeWidth={4} />
      <ellipse cx={cx} cy={cy} rx={118} ry={132} fill={COR.pele} {...tinta} />
      {/* orelhas */}
      <ellipse cx={cx - 120} cy={cy + 10} rx={16} ry={26} fill={COR.pele} {...tinta} strokeWidth={4} />
      <ellipse cx={cx + 120} cy={cy + 10} rx={16} ry={26} fill={COR.pele} {...tinta} strokeWidth={4} />
      {/* cabelo */}
      <path d={`M ${cx - 122} ${cy - 10} Q ${cx - 140} ${cy - 150} ${cx - 20} ${cy - 145} Q ${cx + 60} ${cy - 175} ${cx + 110} ${cy - 110}
        Q ${cx + 135} ${cy - 70} ${cx + 120} ${cy - 20} Q ${cx + 90} ${cy - 80} ${cx + 20} ${cy - 85} Q ${cx - 60} ${cy - 60} ${cx - 122} ${cy - 10} Z`}
        fill={COR.tinta} />
      {/* óculos */}
      {[-1, 1].map((s) => (
        <g key={s}>
          <circle cx={cx + s * 50} cy={cy + 8} r={38} fill="#FFFFFF" fillOpacity={0.35} {...tinta} strokeWidth={4.5} />
          {piscando ? (
            <path d={`M ${cx + s * 50 - 16} ${cy + 10} Q ${cx + s * 50} ${cy + 18} ${cx + s * 50 + 16} ${cy + 10}`} {...tinta} strokeWidth={4} fill="none" />
          ) : (
            <circle cx={cx + s * 50 + 3} cy={cy + 10} r={9} fill={COR.tinta} />
          )}
          <path d={`M ${cx + s * 50 - 22} ${cy - 44 - boca * 6} q 22 -10 44 0`} {...tinta} strokeWidth={5} fill="none" />
        </g>
      ))}
      <path d={`M ${cx - 12} ${cy + 8} L ${cx + 12} ${cy + 8}`} {...tinta} strokeWidth={4} />
      {/* nariz */}
      <path d={`M ${cx + 4} ${cy + 30} q 14 22 -6 30`} {...tinta} strokeWidth={4} fill="none" />
      {/* boca */}
      <ellipse cx={cx} cy={cy + 88} rx={30 + ab * 6} ry={4 + ab * 22} fill={COR.vermelho} {...tinta} strokeWidth={4.5} />
      <path d={`M ${cx - 16} ${cy + 88 - ab * 18} L ${cx + 16} ${cy + 88 - ab * 18}`} stroke="#FFF" strokeWidth={ab > 0.3 ? 6 : 0} strokeLinecap="round" />
      {/* bochechas */}
      <circle cx={cx - 82} cy={cy + 62} r={16} fill={COR.laranja} opacity={0.35} />
      <circle cx={cx + 82} cy={cy + 62} r={16} fill={COR.laranja} opacity={0.35} />
    </svg>
  );
};
