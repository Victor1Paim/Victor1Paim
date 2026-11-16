import React from 'react';
import {useCurrentFrame} from 'remotion';
import {COR, Escrito, FPS, Moeda, W, entre, mola} from '../estilo';
import {ICONES} from '../icones2';
import {Elemento, Modo} from './tipos';

// Onde cada "lugar" fica (centro), fora da área do rosto. dividida = só a parte de cima (0–960).
const LUGAR: Record<Modo, Record<string, [number, number]>> = {
  ela: {
    topo: [540, 250], 'esquerda-alto': [215, 520], 'direita-alto': [865, 520], esquerda: [195, 960],
    direita: [885, 960], 'esquerda-baixo': [235, 1330], 'direita-baixo': [845, 1330],
  },
  dividida: {
    topo: [540, 130], 'esquerda-alto': [190, 300], 'direita-alto': [890, 300], esquerda: [175, 560],
    direita: [905, 560], 'esquerda-baixo': [190, 760], 'direita-baixo': [890, 760],
  },
  motion: {},
};

const cor = (c?: string, padrao = COR.mostarda) => (c && (COR as Record<string, string>)[c]) || (c === 'papel' ? '#F7F3EA' : padrao);

// Filtro "adesivo": contorno branco + sombra, para o desenho ler bem sobre o vídeo.
export const FiltroAdesivo: React.FC = () => (
  <svg width={0} height={0} style={{position: 'absolute'}}>
    <defs>
      <filter id="adesivo" x="-20%" y="-20%" width="140%" height="140%">
        <feMorphology in="SourceAlpha" operator="dilate" radius={7} result="d" />
        <feFlood floodColor="#FBF8F1" />
        <feComposite in2="d" operator="in" result="borda" />
        <feGaussianBlur in="d" stdDeviation={7} result="b" />
        <feOffset in="b" dx={0} dy={8} result="bo" />
        <feFlood floodColor="#2E2925" floodOpacity={0.35} />
        <feComposite in2="bo" operator="in" result="sombra" />
        <feMerge>
          <feMergeNode in="sombra" />
          <feMergeNode in="borda" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
    </defs>
  </svg>
);

const IconeSvg: React.FC<{nome: string; tam: number}> = ({nome, tam}) => {
  const i = ICONES[nome] ?? ICONES.alerta;
  return (
    <svg width={tam} height={tam} viewBox="-150 -150 300 300" style={{overflow: 'visible'}}>
      <g transform={`scale(${i.s})`}>{i.el}</g>
    </svg>
  );
};

const Corpo: React.FC<{e: Elemento; k: number}> = ({e, k}) => {
  switch (e.tipo) {
    case 'icone':
      return <IconeSvg nome={e.icone ?? 'alerta'} tam={260 * k} />;
    case 'etiqueta':
      return (
        <div style={{display: 'flex', alignItems: 'center', gap: 10 * k, background: cor(e.cor), border: `5px solid ${COR.tinta}`,
          borderRadius: 16, padding: `${8 * k}px ${26 * k}px ${2 * k}px`, maxWidth: 430 * k}}>
          {e.icone && <IconeSvg nome={e.icone} tam={100 * k} />}
          <Escrito tam={60 * k} style={{textAlign: 'left'}}>{e.texto}</Escrito>
        </div>
      );
    case 'numero':
      return (
        <div style={{position: 'relative', padding: `0 ${20 * k}px`}}>
          <div style={{position: 'absolute', left: 0, right: 0, bottom: 18 * k, height: 44 * k, background: cor(e.cor), borderRadius: 10, opacity: 0.85}} />
          <Escrito tam={120 * k} style={{position: 'relative', whiteSpace: 'nowrap'}}>{e.texto}</Escrito>
        </div>
      );
    case 'carimbo':
      return (
        <div style={{border: `${9 * k}px solid ${cor(e.cor, COR.vermelho)}`, borderRadius: 18, padding: `${8 * k}px ${30 * k}px 0`,
          background: 'rgba(251,248,241,0.9)', transform: 'rotate(-10deg)'}}>
          <Escrito tam={96 * k} cor={cor(e.cor, COR.vermelho)} style={{whiteSpace: 'nowrap'}}>{e.texto}</Escrito>
        </div>
      );
    case 'pergunta':
      return <Escrito tam={300 * k} cor={cor(e.cor, COR.laranja)} style={{WebkitTextStroke: `6px ${COR.tinta}`}}>?</Escrito>;
    case 'seta': {
      const cima = e.direcao !== 'baixo';
      return (
        <div style={{display: 'flex', alignItems: 'center', gap: 8}}>
          <svg width={150 * k} height={220 * k} viewBox="-75 -110 150 220">
            <path d={cima ? 'M 0 90 L 0 -60 M -50 -20 L 0 -80 L 50 -20' : 'M 0 -90 L 0 60 M -50 20 L 0 80 L 50 20'}
              stroke={COR.tinta} strokeWidth={34} strokeLinecap="round" strokeLinejoin="round" fill="none" />
            <path d={cima ? 'M 0 90 L 0 -60 M -50 -20 L 0 -80 L 50 -20' : 'M 0 -90 L 0 60 M -50 20 L 0 80 L 50 20'}
              stroke={cima ? COR.salvia : COR.laranja} strokeWidth={20} strokeLinecap="round" strokeLinejoin="round" fill="none" />
          </svg>
          {e.texto && <Escrito tam={56 * k}>{e.texto}</Escrito>}
        </div>
      );
    }
    default:
      return null;
  }
};

// Um elemento: entra com mola, flutua, sai encolhendo.
const Flutuante: React.FC<{e: Elemento; modo: Modo; i: number}> = ({e, modo, i}) => {
  const f = useCurrentFrame();
  const ini = Math.round(e.ini * FPS);
  const fim = ini + Math.round(e.dur * FPS);
  if (f < ini || f > fim) return null;
  const [x, y] = LUGAR[modo][e.lugar ?? 'direita-alto'] ?? LUGAR[modo]['direita-alto'] ?? [540, 400];
  const k = modo === 'dividida' ? 0.75 : 1.05;
  const ent = entre(f, ini, 12, 0, 1, mola);
  const sai = 1 - entre(f, fim - 8, 8);
  const lado = x < W / 2 ? -1 : x > W / 2 ? 1 : 0;
  const bob = Math.sin((f - ini) / 17 + i) * 9;
  const giro = Math.sin((f - ini) / 26 + i * 2) * 2.2 + (lado || 1) * (i % 2 ? 2 : -2);
  // laterais ancoradas na margem (o elemento cresce para dentro da tela, nunca para fora)
  const pos: React.CSSProperties = lado < 0 ? {left: 36} : lado > 0 ? {right: 36} : {left: x};
  const tx = lado === 0 ? '-50%' : '0%';
  const origem = lado < 0 ? '0% 50%' : lado > 0 ? '100% 50%' : '50% 50%';
  return (
    <div style={{position: 'absolute', ...pos, top: y, transformOrigin: origem,
      transform: `translate(${tx}, -50%) translate(${lado * (1 - ent) * 140}px, ${bob}px) scale(${Math.max(0, ent) * (0.7 + 0.3 * sai)}) rotate(${giro}deg)`,
      opacity: sai, filter: 'url(#boil) url(#adesivo)'}}>
      <Corpo e={e} k={k} />
    </div>
  );
};

// Chuva de moedas saindo de baixo.
const Moedas: React.FC<{e: Elemento}> = ({e}) => {
  const f = useCurrentFrame();
  const ini = Math.round(e.ini * FPS);
  const t = (f - ini) / FPS;
  if (t < 0 || t > e.dur) return null;
  return (
    <svg width={W} height={1920} style={{position: 'absolute', inset: 0, filter: 'url(#adesivo)'}}>
      {Array.from({length: 9}).map((_, j) => {
        const ang = -Math.PI / 2 + (j - 4) * 0.19;
        const v = 1500 + (j % 3) * 260;
        const x = 540 + Math.cos(ang) * v * t;
        const y = 1700 + Math.sin(ang) * v * t + 0.5 * 3200 * t * t;
        return <Moeda key={j} x={x} y={y} r={44} s={1 - Math.max(0, t - e.dur + 0.3) * 3} />;
      })}
    </svg>
  );
};

export const CamadaFlutuantes: React.FC<{elementos: Elemento[]; modoEm: (s: number) => Modo}> = ({elementos, modoEm}) => (
  <>
    {elementos.map((e, i) =>
      e.tipo === 'zoom' ? null : e.tipo === 'moedas' ? (
        <Moedas key={i} e={e} />
      ) : (
        <Flutuante key={i} e={e} modo={modoEm(e.ini + 0.05)} i={i} />
      ),
    )}
  </>
);
