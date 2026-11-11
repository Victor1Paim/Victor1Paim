import React from 'react';
import {
  AbsoluteFill, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing,
} from 'remotion';
import {loadFont} from '@remotion/fonts';

// Fontes locais em public/fonts (o renderizador não depende de internet).
const anton = 'Anton';
const inter = 'Inter';
loadFont({family: anton, url: staticFile('fonts/anton.woff2')});
loadFont({family: inter, url: staticFile('fonts/inter-600.woff2'), weight: '600'});
loadFont({family: inter, url: staticFile('fonts/inter-800.woff2'), weight: '800'});

const ROSA = '#ff4fa3';
const AMARELO = '#ffd23f';
const VIDEO_TOPO = 400;
const VIDEO_ALTURA = 1080;

type Legenda = {inicio: number; fim: number; texto: string};
type PalavraFonte = {texto: string; inicio: number; fim: number};
export type Dados = {
  video: string; duracao: number; gancho: string[]; destaque: string; cabecalho: string; selo: string;
  credito: string; canal: string; chamadaFinal: string; inicioFinal: number; legendas: Legenda[]; destaques: string[];
  palavras?: PalavraFonte[];
  cartoes?: Cartao[];
};
type Cartao = {inicio: number; fim: number; grande: string; pequeno: string};

// Divide cada frase em palavras com tempo proporcional ao tamanho, e agrupa de 2 a 4 palavras por tela.
type Palavra = {texto: string; inicio: number; fim: number};
const agrupar = (palavras: Palavra[]): Palavra[][] => {
  const grupos: Palavra[][] = [];
  let atual: Palavra[] = [];
  palavras.forEach((w, i) => {
    atual.push(w);
    const fimDeFrase = /[.?!,]$/.test(w.texto);
    const pausa = palavras[i + 1] && palavras[i + 1].inicio - w.fim > 0.35;
    const proxima = palavras[i + 1]?.texto.length ?? 0;
    const largo = atual.reduce((n, x) => n + x.texto.length + 1, 0) + proxima > 17;
    if (atual.length >= 4 || largo || ((fimDeFrase || pausa) && atual.length >= 1)) {
      grupos.push(atual);
      atual = [];
    }
  });
  if (atual.length) grupos.push(atual);
  return grupos;
};

const quebrar = (l: Legenda): Palavra[][] => {
  const ps = l.texto.split(' ');
  const pesos = ps.map((p) => p.length + 2);
  const total = pesos.reduce((a, b) => a + b, 0);
  let t = l.inicio;
  const palavras = ps.map((p, i) => {
    const d = ((l.fim - l.inicio) * pesos[i]) / total;
    const w = {texto: p, inicio: t, fim: t + d};
    t += d;
    return w;
  });
  const grupos: Palavra[][] = [];
  let atual: Palavra[] = [];
  palavras.forEach((w) => {
    atual.push(w);
    const fimDeFrase = /[.?!,]$/.test(w.texto);
    if (atual.length >= 4 || (fimDeFrase && atual.length >= 2)) {
      grupos.push(atual);
      atual = [];
    }
  });
  if (atual.length) grupos.push(atual);
  return grupos;
};

const Legendas: React.FC<{dados: Dados}> = ({dados}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  // Com tempo real de cada palavra (transcrição), usa direto; senão, distribui pelas frases.
  const grupos = dados.palavras?.length ? agrupar(dados.palavras) : dados.legendas.flatMap(quebrar);
  const g = grupos.find((gr, i) => {
    const fim = Math.min(gr[gr.length - 1].fim + 0.25, grupos[i + 1]?.[0].inicio ?? Infinity);
    return t >= gr[0].inicio && t < fim;
  });
  if (!g) return null;
  const entrada = spring({frame: frame - Math.round(g[0].inicio * fps), fps, config: {damping: 14, mass: 0.6}});
  return (
    <div style={{
      position: 'absolute', top: VIDEO_TOPO + VIDEO_ALTURA + 50, left: 60, right: 60, textAlign: 'center',
      transform: `scale(${interpolate(entrada, [0, 1], [0.85, 1])})`, opacity: entrada,
    }}>
      {g.map((w, i) => {
        const falando = t >= w.inicio && t < w.fim + 0.05;
        const limpa = w.texto.replace(/[.,!?]/g, '').toLowerCase();
        const destaque = dados.destaques.some((d) => d.replace(/[.,!?]/g, '').toLowerCase() === limpa);
        return (
          <span key={i} style={{
            fontFamily: anton, fontSize: 92, lineHeight: 1.15, textTransform: 'uppercase', margin: '0 12px',
            display: 'inline-block', color: destaque ? AMARELO : '#fff',
            WebkitTextStroke: '10px #000', paintOrder: 'stroke fill',
            textShadow: '0 8px 0 rgba(0,0,0,0.6)',
            transform: falando ? 'scale(1.12) translateY(-4px)' : 'scale(1)',
            background: falando ? ROSA : 'transparent', borderRadius: 14, padding: '0 10px',
          }}>{w.texto}</span>
        );
      })}
    </div>
  );
};

const Gancho: React.FC<{dados: Dados}> = ({dados}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  // 0 a 3,5 s: gancho grande. Depois encolhe para um cabeçalho fixo.
  const recolher = interpolate(frame, [3.2 * fps, 3.8 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  return (
    <>
      <div style={{position: 'absolute', top: 120, left: 40, right: 40, textAlign: 'center', opacity: 1 - recolher, transform: `translateY(${-60 * recolher}px)`}}>
        {dados.gancho.map((linha, i) => {
          const s = spring({frame: frame - i * 6, fps, config: {damping: 12}});
          const partes = linha.split(dados.destaque);
          return (
            <div key={i} style={{
              fontFamily: anton, fontSize: 118, lineHeight: 1.05, color: '#fff', WebkitTextStroke: '12px #000', paintOrder: 'stroke fill',
              transform: `translateY(${interpolate(s, [0, 1], [80, 0])}px) scale(${interpolate(s, [0, 1], [0.7, 1])})`, opacity: s,
            }}>
              {partes.map((p, j) => (
                <React.Fragment key={j}>
                  {p}
                  {j < partes.length - 1 && <span style={{color: AMARELO}}>{dados.destaque}</span>}
                </React.Fragment>
              ))}
            </div>
          );
        })}
      </div>
      <div style={{
        position: 'absolute', top: 250, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: recolher,
        transform: `translateY(${40 * (1 - recolher)}px)`,
      }}>
        <div style={{fontFamily: inter, fontWeight: 800, fontSize: 46, color: '#fff', background: 'rgba(0,0,0,0.55)', padding: '14px 30px', borderRadius: 999, border: `3px solid ${ROSA}`}}>
          {dados.cabecalho}
        </div>
      </div>
    </>
  );
};

const Selo: React.FC<{texto: string}> = ({texto}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - 20, fps, config: {damping: 10}});
  const pulso = 1 + 0.04 * Math.sin(frame / 8);
  return (
    <div style={{
      position: 'absolute', top: VIDEO_TOPO - 34, right: 40, transform: `rotate(-4deg) scale(${s * pulso})`,
      fontFamily: anton, fontSize: 54, color: '#000', background: AMARELO, padding: '6px 22px', borderRadius: 10, boxShadow: '0 8px 0 #000',
    }}>{texto}</div>
  );
};

const Credito: React.FC<{texto: string; canal: string}> = ({texto, canal}) => (
  <div style={{position: 'absolute', bottom: 150, left: 0, right: 0, textAlign: 'center', fontFamily: inter, fontWeight: 600, fontSize: 32, color: 'rgba(255,255,255,0.8)'}}>
    {texto} · {canal}
  </div>
);

const Final: React.FC<{dados: Dados}> = ({dados}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const inicio = Math.round(dados.inicioFinal * fps);
  const s = spring({frame: frame - inicio, fps, config: {damping: 13}});
  if (frame < inicio) return null;
  return (
    <AbsoluteFill style={{background: `rgba(0,0,0,${0.55 * s})`, alignItems: 'center', justifyContent: 'center'}}>
      <div style={{transform: `scale(${interpolate(s, [0, 1], [0.6, 1])})`, opacity: s, textAlign: 'center', padding: 60}}>
        <div style={{fontFamily: anton, fontSize: 104, lineHeight: 1.05, color: '#fff', WebkitTextStroke: '10px #000', paintOrder: 'stroke fill'}}>
          {dados.chamadaFinal.toUpperCase()}
        </div>
        <div style={{marginTop: 40, display: 'inline-block', fontFamily: inter, fontWeight: 800, fontSize: 56, color: '#000', background: AMARELO, padding: '14px 40px', borderRadius: 999}}>
          {dados.canal}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Cartão de informação (número grande + linha de apoio) no centro do quadro.
const Cartoes: React.FC<{cartoes: Cartao[]}> = ({cartoes}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const c = cartoes.find((x) => t >= x.inicio && t < x.fim);
  if (!c) return null;
  const s = spring({frame: frame - Math.round(c.inicio * fps), fps, config: {damping: 12, mass: 0.7}});
  const saida = interpolate(t, [c.fim - 0.25, c.fim], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', top: 640, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: saida}}>
      <div style={{
        transform: `scale(${interpolate(s, [0, 1], [0.6, 1])}) rotate(${interpolate(s, [0, 1], [-6, -2])}deg)`, opacity: s,
        background: 'rgba(13,7,24,0.82)', border: `6px solid ${AMARELO}`, borderRadius: 34, padding: '34px 56px', textAlign: 'center',
        boxShadow: '0 14px 0 #000', maxWidth: 940,
      }}>
        <div style={{fontFamily: anton, fontSize: 150, lineHeight: 1, color: AMARELO, WebkitTextStroke: '8px #000', paintOrder: 'stroke fill'}}>{c.grande}</div>
        <div style={{fontFamily: inter, fontWeight: 800, fontSize: 46, color: '#fff', marginTop: 14, textTransform: 'uppercase'}}>{c.pequeno}</div>
      </div>
    </div>
  );
};

export const Corte: React.FC<{dados: Dados}> = ({dados}) => (
  <AbsoluteFill style={{backgroundColor: '#000'}}>
    <OffthreadVideo src={staticFile(dados.video)} />
    <Gancho dados={dados} />
    <Selo texto={dados.selo} />
    {dados.cartoes && <Cartoes cartoes={dados.cartoes} />}
    <Legendas dados={dados} />
    <Credito texto={dados.credito} canal={dados.canal} />
    <Final dados={dados} />
  </AbsoluteFill>
);
