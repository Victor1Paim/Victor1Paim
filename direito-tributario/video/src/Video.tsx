import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {COR, DIVISA, Desenho, FiltrosTraco, H, Papel, W, entre, suave} from './estilo';
import {Bloco, Fala, montarLinha, quando, volumeEm} from './linha';
import {Apresentador} from './Apresentador';
import {Legenda} from './Legenda';
import {CenaFecho, CenaGancho, CenaImposto, CenaMelhoria, CenaTaxa, CenaTres} from './Cenas';

const CENAS: Record<string, React.FC<{b: Bloco}>> = {
  '01_gancho': CenaGancho,
  '02_tres': CenaTres,
  '03_imposto': CenaImposto,
  '04_taxa': CenaTaxa,
  '05_melhoria': CenaMelhoria,
  '06_fecho': CenaFecho,
};

const TRANS = 14; // quadros da passagem entre cenas
const LEGENDA_Y = 1585;

// Altura do painel do apresentador ao longo do vídeo: 40% na tela dividida, 0 no motion.
const divisaEm = (blocos: Bloco[], f: number) => {
  let d = blocos[0].modo === 'dividida' ? DIVISA : 0;
  for (const b of blocos) {
    if (f < b.de) break;
    const alvo = b.modo === 'dividida' ? DIVISA : 0;
    d = interpolate(f, [b.de, b.de + TRANS + 4], [d, alvo], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: suave});
  }
  return d;
};

// Cena com entrada pela direita e saída pela esquerda (câmera "anda" no papel).
const Passagem: React.FC<{b: Bloco; ultimo: boolean; children: React.ReactNode}> = ({b, ultimo, children}) => {
  const f = useCurrentFrame();
  const entra = (1 - entre(f, 0, TRANS)) * W;
  const sai = ultimo ? 0 : -entre(f, b.quadros, TRANS) * W;
  return <AbsoluteFill style={{transform: `translateX(${entra + sai}px)`}}>{children}</AbsoluteFill>;
};

export const Video: React.FC<{falas: Fala[]}> = ({falas}) => {
  const f = useCurrentFrame();
  const {blocos} = montarLinha(falas);
  const divisa = divisaEm(blocos, f);
  const atual = [...blocos].reverse().find((b) => f >= b.de) ?? blocos[0];
  const rel = f - atual.de;
  // gesto do apresentador nas palavras de ênfase
  const gestos: Record<string, string[]> = {'01_gancho': ['imposto?', 'não.'], '06_fecho': ['então:', 'salva']};
  const gesto = Math.max(0, ...(gestos[atual.id] ?? []).map((p) => {
    const t = quando(atual, p);
    return entre(rel, t - 6, 8) * (1 - entre(rel, t + 24, 10));
  }));

  return (
    <AbsoluteFill style={{background: COR.papel}}>
      <FiltrosTraco />
      <Papel />
      {/* conteúdo (explicação) */}
      <AbsoluteFill style={{clipPath: `inset(${divisa}px 0 0 0)`}}>
        <Desenho>
          {blocos.map((b, i) => {
            const Cena = CENAS[b.id];
            const ultimo = i === blocos.length - 1;
            return (
              <Sequence key={b.id} from={b.de} durationInFrames={b.quadros + (ultimo ? 0 : TRANS)}>
                <Passagem b={b} ultimo={ultimo}>
                  <AbsoluteFill style={{top: b.modo === 'dividida' ? DIVISA : 0}}>
                    <Cena b={b} />
                  </AbsoluteFill>
                </Passagem>
              </Sequence>
            );
          })}
        </Desenho>
      </AbsoluteFill>
      {/* painel do apresentador (desliza para cima quando o motion toma a tela) */}
      {divisa > 1 && (
        <AbsoluteFill style={{height: DIVISA, transform: `translateY(${divisa - DIVISA}px)`, overflow: 'hidden'}}>
          <AbsoluteFill style={{background: COR.papelEscuro}} />
          <Desenho>
            <Apresentador boca={atual.modo === 'dividida' ? volumeEm(atual, rel) : 0} gesto={gesto} />
          </Desenho>
          <svg width={W} height={DIVISA} style={{position: 'absolute', inset: 0, filter: 'url(#boil)'}}>
            <path d={`M 0 ${DIVISA - 4} Q 270 ${DIVISA - 10} 540 ${DIVISA - 3} T 1080 ${DIVISA - 5}`} stroke={COR.tinta} strokeWidth={7} fill="none" />
          </svg>
        </AbsoluteFill>
      )}
      {/* áudio + legendas */}
      {blocos.map((b) => (
        <Sequence key={b.id} from={b.de} durationInFrames={b.quadros}>
          <Audio src={staticFile(b.audio)} />
          <Legenda fala={b} y={LEGENDA_Y} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
