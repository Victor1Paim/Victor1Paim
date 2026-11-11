import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {COR, DIVISA, Desenho, FiltrosTraco, H, Papel, W, entre, suave} from './estilo';
import {Bloco, montarLinha, quando, volumeEm} from './linha';
import {Legenda} from './Legenda';
import {PROJETOS} from './projetos';

const TRANS = 14; // quadros da passagem entre cenas
const LEGENDA_Y = 1585;

// Altura do painel do apresentador: 100% (apresentador), 40% (dividida), 0 (motion).
const ALTURA = {apresentador: H, dividida: DIVISA, motion: 0};
const divisaEm = (blocos: Bloco[], f: number) => {
  let d = ALTURA[blocos[0].modo];
  for (const b of blocos) {
    if (f < b.de) break;
    const alvo = ALTURA[b.modo];
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

export const Video: React.FC<{id: string}> = ({id}) => {
  const f = useCurrentFrame();
  const {falas, cenas: CENAS, Apresentador, gestos} = PROJETOS[id];
  const {blocos} = montarLinha(falas);
  const divisa = divisaEm(blocos, f);
  const atual = [...blocos].reverse().find((b) => f >= b.de) ?? blocos[0];
  const rel = f - atual.de;
  // gesto do apresentador nas palavras de ênfase
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
            if (b.modo === 'apresentador') return null;
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
        <AbsoluteFill style={{height: Math.max(divisa, DIVISA), transform: `translateY(${Math.min(0, divisa - DIVISA)}px)`, overflow: 'hidden'}}>
          <AbsoluteFill style={{background: COR.papelEscuro}} />
          <Apresentador boca={atual.modo !== 'motion' ? volumeEm(atual, rel) : 0} gesto={gesto} alt={Math.max(divisa, DIVISA)} />
          <svg width={W} height={H} style={{position: 'absolute', inset: 0, filter: 'url(#boil)'}}>
            <path d={`M 0 ${Math.max(divisa, DIVISA) - 4} l 1080 -2`} stroke={COR.tinta} strokeWidth={7} fill="none" />
          </svg>
        </AbsoluteFill>
      )}
      {/* cenas sobrepostas ao apresentador em tela cheia */}
      <Desenho>
        {blocos.map((b) => {
          if (b.modo !== 'apresentador') return null;
          const Cena = CENAS[b.id];
          return (
            <Sequence key={b.id} from={b.de} durationInFrames={b.quadros + TRANS}>
              <Cena b={b} />
            </Sequence>
          );
        })}
      </Desenho>
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
