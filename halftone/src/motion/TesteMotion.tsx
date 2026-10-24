import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {marca} from '../../marca/marca';
import {paleta} from '../../series/ano-zero/paleta';
import {CTAFinal} from '../components/CTAFinal';
import {HalftoneApresenta} from '../components/HalftoneApresenta';
import {faltamMin, Relogio} from '../components/Relogio';
import {Reticula} from '../components/Reticula';
import {SeloFiccao} from '../components/SeloFiccao';
import {AneisBatida, Cenario} from './Cenario';
import {LegendaKaraoke} from './LegendaKaraoke';
import {FILEIRAS_FRENTE, FILEIRAS_FUNDO, Multidao} from './Multidao';
import {Pessoa} from './Pessoa';
import {EV, indiceBatida, pulso, rampa, ruido, TL} from './tempo';

// Ano Zero · teste motion: o início da infecção, contado em motion graphics vetorial.
// Um mundo só; a câmera viaja por ele. Toda ação cai na palavra que a narra.

const L = Object.fromEntries(TL.linhas.map((l) => [l.id, l]));
const fimDe = (id: string) => L[id].inicio + L[id].duracao;

// posições no mundo (pés)
const HOMEM = {x: 330, y: 1240, s: 0.62};
const AMBULANTE = {x: 160, y: 1250, s: 0.6};
const RAFA = {x: 760, y: 1262, s: 0.64};
const BIA = {x: 900, y: 1270, s: 0.66};
const CAIO = {x: 1015, y: 1276, s: 0.66};

type Chave = [number, number, number, number]; // t, cx, cy, zoom
const CAMERA: Chave[] = [
  [0, 330, 850, 2.4],
  [3.6, 330, 870, 2.6],
  [3.61, 540, 900, 1.0],
  [11.8, 600, 960, 1.12],
  [12.8, 880, 990, 1.55],
  [19.1, 880, 990, 1.62],
  [19.9, 360, 970, 1.55],
  [EV.dedos - 0.05, 350, 960, 1.75],
  [EV.dedos + 0.4, 285, 1060, 3.1],
  [EV.dedos + 2.0, 290, 1060, 3.2],
  [EV.dedos + 2.7, 300, 980, 1.5],
  [L.a01.inicio, 260, 990, 1.55],
  [EV.somCorta, 400, 1010, 1.45],
  [EV.parouRespirar + 1.6, 540, 1170, 1.85],
  [L.b02.inicio - 0.01, 540, 1170, 1.85],
  [L.b02.inicio, 900, 1010, 1.9],
  [fimDe('b02') + 0.2, 900, 1010, 1.95],
  [fimDe('b02') + 0.21, 540, 1160, 1.7],
  [EV.levanta, 450, 1050, 1.5],
  [L.r02.inicio, 560, 1000, 1.35],
  [EV.ataque, 600, 990, 1.45],
  [EV.fuga - 0.01, 600, 990, 1.45],
  [EV.fuga, 540, 960, 1.05],
  [EV.fuga + 4, 820, 1010, 1.35],
  [EV.cta, 900, 1020, 1.5],
];

const camera = (t: number) => {
  let i = 0;
  while (i < CAMERA.length - 2 && t >= CAMERA[i + 1][0]) i++;
  const [t0, x0, y0, z0] = CAMERA[i];
  const [t1, x1, y1, z1] = CAMERA[i + 1];
  const k = rampa(t, t0, t1);
  return {x: x0 + (x1 - x0) * k, y: y0 + (y1 - y0) * k, z: z0 + (z1 - z0) * k};
};

const hora = (t: number) => (t < EV.ganchoFim ? '23:04' : t < L.n02.inicio ? '23:00' : t < EV.ataque ? '23:01' : '23:02');

// O homem do crachá: dança, febre do ritmo, cai, silêncio, levanta em rajadas como eco, ataca.
const poseHomem = (t: number) => {
  const p = pulso(t);
  const gancho = t < EV.ganchoFim;
  const tremor = t >= EV.tremorInicio && t < EV.parouRespirar ? ruido(Math.floor(t * 24)) * 7 : 0;
  let corpo = 0;
  let x = HOMEM.x + tremor;
  const queda = EV.somCorta + 0.35;
  if (t >= queda && t < EV.levanta) corpo = 90 * rampa(t, queda, queda + 0.4);
  if (t >= EV.levanta) {
    // levanta em três trancos, um por batida
    const b0 = indiceBatida(EV.levanta);
    const n = Math.min(3, indiceBatida(t) - b0 + 1);
    corpo = [90, 58, 24, 0][n] ?? 0;
  }
  const eco = gancho || t >= EV.batidaVolta;
  const tique = eco && (gancho || t >= EV.levanta) ? (indiceBatida(t) % 2 ? 1 : -1) * 7 * Math.min(1, p * 2) : 0;
  let inclina = eco ? 24 + tique : Math.sin(t * 6) * 3 * p;
  if (t >= EV.viraCabeca) inclina = -30 + tique;
  if (t >= EV.ataque) x = HOMEM.x + (RAFA.x - 90 - HOMEM.x) * rampa(t, EV.ataque, EV.ataque + 0.25);
  const dedos = t >= EV.tremorInicio && t < EV.somCorta ? (indiceBatida(t) % 2 ? 22 : 4) : 8;
  return {
    x: gancho ? HOMEM.x : x,
    corpo,
    eco,
    inclina,
    bracoE: eco ? 28 + tique : dedos + (t < EV.tremorInicio ? -p * 30 : 0),
    bracoD: eco ? -40 - tique : -8 - (t < EV.tremorInicio ? -p * 30 : 0),
  };
};

export const TesteMotion: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const cam = camera(t);
  const p = pulso(t);
  const h = poseHomem(t);
  const fuga = t >= EV.fuga ? rampa(t, EV.fuga, EV.fuga + 3.5) : 0;
  const silencio = t >= EV.somCorta && t < EV.batidaVolta;
  const depoisAtaque = t >= EV.fuga;
  const flash = t >= EV.ataque + 0.08 && t < EV.ataque + 0.25;
  const preto = t >= EV.ataque + 0.25 && t < EV.fuga;
  const bia = {
    bracoD: t >= L.b02.inicio && t < fimDe('b02') + 0.3 ? -150 : t >= L.b03.inicio && t < EV.fuga ? -110 : -8 - p * 25,
    bracoE: 8 + p * 20,
  };
  const rafa = {
    bracoD: t >= L.r02.inicio && t < EV.ataque ? -70 : -8 - p * 35,
    bracoE: t < EV.somCorta ? 8 + p * 35 : 10,
  };

  return (
    <AbsoluteFill style={{background: marca.cores.preto}}>
      <AbsoluteFill style={{transform: `translate(${540 - cam.x * cam.z}px, ${900 - cam.y * cam.z}px) scale(${cam.z})`, transformOrigin: '0 0'}}>
        <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{overflow: 'visible'}}>
          <Cenario t={t} hora={hora(t)} faltam={`FALTAM ${faltamMin(hora(t))} MIN`} />
          <Multidao t={t} fileiras={FILEIRAS_FUNDO} fuga={fuga} centroFuga={HOMEM.x} agito={silencio ? 0 : 1} />
          <AneisBatida t={t} fontes={[{x: 90, y: 870}, {x: 570, y: 870}]} ate={EV.cta} />
          {!depoisAtaque ? (
            <>
              <Pessoa id="amb" x={AMBULANTE.x} y={AMBULANTE.y - (silencio ? 0 : p * 6)} escala={AMBULANTE.s} pele="#6B4630" acessorios={['isopor']} bracoE={silencio ? 30 : 10} />
              <Pessoa id="caio" x={CAIO.x} y={CAIO.y - p * 10} escala={CAIO.s} pele="#7A4E33" de="costas" acessorios={['cacheado', 'fitinha']} bracoE={10 + p * 25} bracoD={-10 - p * 25} recorte="#7FB8D6" />
              <Pessoa id="rafa" x={RAFA.x} y={RAFA.y - (silencio ? 0 : p * 12)} escala={RAFA.s} pele="#C79A7A" cabelo="#5A3B22" acessorios={['oculos']} bracoE={rafa.bracoE} bracoD={rafa.bracoD} />
            </>
          ) : null}
          <Pessoa id="bia" x={depoisAtaque ? 540 : BIA.x} y={(depoisAtaque ? 1290 : BIA.y) - (silencio || depoisAtaque ? 0 : p * 8)} escala={BIA.s} pele="#8A5A3C" acessorios={['rabo']} saia bracoE={bia.bracoE} bracoD={bia.bracoD} inclinaCabeca={depoisAtaque ? Math.sin((t - EV.fuga) * 1.6) * 14 : 0} />
          {!depoisAtaque ? (
            <Pessoa id="homem" x={h.x} y={HOMEM.y} escala={HOMEM.s} pele="#B08A6E" cabelo="#3B2E26" acessorios={['cracha']} corpo={h.corpo} eco={h.eco} inclinaCabeca={h.inclina} bracoE={h.bracoE} bracoD={h.bracoD} />
          ) : null}
          <Multidao t={t} fileiras={FILEIRAS_FRENTE} fuga={fuga} centroFuga={HOMEM.x} agito={silencio ? 0 : 1} />
        </svg>
      </AbsoluteFill>

      {flash ? <AbsoluteFill style={{background: paleta.perigo, opacity: 0.85}} /> : null}
      {preto ? <AbsoluteFill style={{background: marca.cores.preto}} /> : null}
      {silencio ? <AbsoluteFill style={{background: '#000', opacity: 0.18}} /> : null}

      <Reticula opacidade={0.11} />
      <LegendaKaraoke t={t} />
      {t < EV.cta ? <Relogio hora={hora(t)} corSessao={paleta.sessoes.bia} /> : null}

      <Sequence from={Math.round(EV.ganchoFim * fps)} durationInFrames={Math.round((EV.apresentaFim - EV.ganchoFim) * fps)} name="Halftone apresenta">
        <HalftoneApresenta serie="Ano Zero" temporada="T1 · A Virada" />
      </Sequence>
      <Sequence from={Math.round(EV.cta * fps)} name="CTA">
        <CTAFinal texto="Estreia 04/12 · 20h" serie="Ano Zero · teste" nota="SÉRIE DE FICÇÃO · HALFTONE" />
      </Sequence>
      <SeloFiccao texto="DIA 1 · DA INFECÇÃO" />

      <Audio src={staticFile(TL.trilha)} volume={0.55} />
      {TL.linhas.map((l) => (
        <Sequence key={l.id} from={Math.round(l.inicio * fps)} layout="none" name={`voz ${l.id}`}>
          <Audio src={staticFile(l.arquivo)} volume={1} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const DURACAO_TESTE_MOTION = Math.ceil(TL.duracao * 30);
