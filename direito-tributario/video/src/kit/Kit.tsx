import React from 'react';
import {AbsoluteFill, CalculateMetadataFunction, OffthreadVideo, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {COR, FPS, FiltrosTraco, H, Papel, W, suave} from '../estilo';
import {Legenda} from '../Legenda';
import {Fala} from '../linha';
import {Cartao} from './Cartoes';
import {CamadaFlutuantes, FiltroAdesivo} from './Flutuantes';
import {Dados, Modo, Trecho} from './tipos';

// Vídeo do kit: gravação da apresentadora + elementos flutuantes + cartões em motion (tudo vindo do dados.json).
export type PropsKit = {nome: string; dados?: Dados};

const ALTURA: Record<Modo, number> = {ela: H, dividida: 960, motion: 0};
const TRANS = 14;
const LEGENDA_Y = 1585;

export const calcularKit: CalculateMetadataFunction<PropsKit> = async ({props}) => {
  let nome = props.nome;
  if (!nome) nome = (await (await fetch(staticFile('videos/ultimo.json'))).json()).nome;
  const dados: Dados = await (await fetch(staticFile(`videos/${nome}/dados.json`))).json();
  return {durationInFrames: Math.ceil(dados.duracao * FPS), props: {...props, nome, dados}};
};

const trechoEm = (ts: Trecho[], s: number) => [...ts].reverse().find((t) => s >= t.ini) ?? ts[0];

const alturaEm = (ts: Trecho[], f: number) => {
  let a = ALTURA[ts[0].modo];
  for (const t of ts) {
    const ini = t.ini * FPS;
    if (f < ini) break;
    a = interpolate(f, [ini, ini + TRANS + 4], [a, ALTURA[t.modo]], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: suave});
  }
  return a;
};

export const Kit: React.FC<PropsKit> = ({dados}) => {
  const f = useCurrentFrame();
  if (!dados) return null;
  const s = f / FPS;
  const ts = dados.trechos;
  const alt = alturaEm(ts, f);
  const painel = Math.max(alt, 960);
  const desloc = interpolate(alt, [960, H], [dados.enquadramentoDividida ?? -170, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  // zoom de ênfase
  const zoom = dados.elementos.filter((e) => e.tipo === 'zoom').reduce((z, e) => {
    const a = e.ini * FPS;
    const b = a + e.dur * FPS;
    return z + interpolate(f, [a, a + 5, b - 6, b], [0, 0.13, 0.13, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: suave});
  }, 0);
  const modoEm = (seg: number) => trechoEm(ts, seg).modo;

  return (
    <AbsoluteFill style={{background: COR.papel}}>
      <FiltrosTraco />
      <FiltroAdesivo />
      <Papel />
      {/* cartões de motion: tela cheia ou metade de baixo */}
      {ts.map((t, i) => {
        const a = Math.round(t.ini * FPS);
        const b = Math.round(t.fim * FPS);
        if (t.modo === 'ela' || f < a || f > b + TRANS) return null;
        return (
          <SaiDeLado key={i} de={a} ate={b}>
            <Cartao tr={t} area={t.modo === 'motion' ? {top: 120, h: 1400} : {top: 975, h: 580}} />
          </SaiDeLado>
        );
      })}
      {/* gravação: sempre tocando (a voz continua no motion); o painel sobe/encolhe conforme o modo */}
      <AbsoluteFill style={{height: painel, transform: `translateY(${Math.min(0, alt - 960)}px)`, overflow: 'hidden'}}>
        <AbsoluteFill style={{transform: `translateY(${desloc}px) scale(${1 + zoom})`, transformOrigin: '50% 35%'}}>
          <OffthreadVideo src={staticFile(dados.video)} style={{width: W, height: H}} />
        </AbsoluteFill>
        {alt < H - 2 && (
          <svg width={W} height={painel} style={{position: 'absolute', inset: 0, filter: 'url(#boil)'}}>
            <path d={`M 0 ${painel - 4} Q 270 ${painel - 10} 540 ${painel - 3} T 1080 ${painel - 5}`} stroke={COR.tinta} strokeWidth={8} fill="none" />
          </svg>
        )}
      </AbsoluteFill>
      <CamadaFlutuantes elementos={dados.elementos} modoEm={modoEm} />
      {dados.legenda && <Legenda fala={{palavras: dados.palavras} as unknown as Fala} y={LEGENDA_Y} />}
    </AbsoluteFill>
  );
};

// Os cartões usam o tempo ABSOLUTO do vídeo (os itens vêm em segundos do dados.json), por isso nada de <Sequence>.
const SaiDeLado: React.FC<{de: number; ate: number; children: React.ReactNode}> = ({de, ate, children}) => {
  const f = useCurrentFrame();
  const entra = interpolate(f, [de, de + TRANS], [W, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: suave});
  const sai = interpolate(f, [ate, ate + TRANS], [0, -W], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: suave});
  return <AbsoluteFill style={{transform: `translateX(${entra + sai}px)`}}>{children}</AbsoluteFill>;
};
