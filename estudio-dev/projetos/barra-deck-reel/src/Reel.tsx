import React from 'react';
import {
  AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, random, staticFile, useCurrentFrame,
} from 'remotion';
import { loadFont } from '@remotion/fonts';
import FONTES from './fontes.json';

// fontes locais (public/fontes) — baixadas por scripts/baixar_fontes.py
FONTES.forEach((f) => {
  loadFont({ family: f.family, url: staticFile(f.file), style: f.style, weight: f.weight, unicodeRange: f.unicodeRange });
});
const SERIF = 'Cormorant Garamond';
const SANS = 'Karla';

// Paleta da marca (logo Barra Deck)
const C = {
  cream: '#FCF3EC', copper: '#C0652F', copperInk: '#A04E1F', copperLight: '#F2B48A', peach: '#F7C9A5',
  brown: '#4C220E', espresso: '#2A1409', ink: '#3B1D0D',
};

const FPS = 30;
const s = (sec: number) => Math.round(sec * FPS);
const OFFSET = 0.4;                          // a narração começa em 0,4 s
const t = (sec: number) => s(sec + OFFSET);  // tempo da narração -> frame do vídeo
export const DURACAO = s(26.5);

const ease = Easing.bezier(0.16, 1, 0.3, 1);
const io = (f: number, a: number, b: number) =>
  interpolate(f, [a, b], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease });

/* ---------- camadas de motion graphics ---------- */

const Fundo: React.FC<{ src: string; dur: number; giro?: number; escuro?: number }> = ({ src, dur, giro = 2, escuro = 0.35 }) => {
  const f = useCurrentFrame();
  const z = interpolate(f, [0, dur], [1.08, 1.22]);
  const r = interpolate(f, [0, dur], [-giro / 2, giro / 2]);
  const y = interpolate(f, [0, dur], [20, -30]);
  return (
    <AbsoluteFill style={{ overflow: 'hidden' }}>
      <Img src={staticFile(src)} style={{ width: '100%', height: '100%', objectFit: 'cover', transform: `translateY(${y}px) scale(${z}) rotate(${r}deg)` }} />
      <AbsoluteFill style={{ background: `radial-gradient(60% 40% at 50% 46%, rgba(0,0,0,${escuro}), transparent 75%)` }} />
    </AbsoluteFill>
  );
};

const Brilhos: React.FC<{ cor?: string; n?: number; vel?: number }> = ({ cor = C.copperLight, n = 50, vel = 1 }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      {Array.from({ length: n }).map((_, i) => {
        const x = random(`x${i}`) * 1080;
        const v = (0.6 + random(`v${i}`) * 1.6) * vel;
        const y = ((random(`y${i}`) * 2100 + f * v * 2.4) % 2100) - 100;
        const r = 2 + random(`r${i}`) * 6;
        const tw = 0.5 + 0.5 * Math.sin(f / (6 + random(`t${i}`) * 8) + i);
        return <div key={i} style={{ position: 'absolute', left: x + Math.sin((f + i * 20) / 28) * 16, top: y, width: r, height: r, borderRadius: '50%', background: cor, opacity: (0.25 + random(`o${i}`) * 0.6) * tw, boxShadow: `0 0 ${r * 4}px ${cor}` }} />;
      })}
    </AbsoluteFill>
  );
};

// anéis concêntricos girando (SVG)
const Aneis: React.FC<{ cx?: number; cy?: number; raio?: number; cor?: string; entrada?: number }> = ({ cx = 540, cy = 860, raio = 360, cor = C.copperLight, entrada = 0 }) => {
  const f = useCurrentFrame();
  const p = io(f, entrada, entrada + 24);
  return (
    <svg width={1080} height={1920} style={{ position: 'absolute', inset: 0 }}>
      {[1, 0.78, 0.58].map((k, i) => {
        const r = raio * k;
        const circ = 2 * Math.PI * r;
        return (
          <circle key={i} cx={cx} cy={cy} r={r} fill="none" stroke={cor} strokeOpacity={0.55 - i * 0.12}
            strokeWidth={i === 0 ? 2 : 1.5} strokeDasharray={i === 1 ? '4 14' : `${circ * p} ${circ}`}
            transform={`rotate(${(i % 2 ? -1 : 1) * f * (0.6 + i * 0.3) - 90} ${cx} ${cy})`} />
        );
      })}
    </svg>
  );
};

// raios de estrela girando
const Raios: React.FC<{ cor?: string }> = ({ cor = C.copperLight }) => {
  const f = useCurrentFrame();
  const p = io(f, 0, 30);
  return (
    <svg width={1080} height={1920} style={{ position: 'absolute', inset: 0, opacity: 0.5 }}>
      <g transform={`rotate(${f * 0.4} 540 900)`}>
        {Array.from({ length: 24 }).map((_, i) => {
          const a = (i / 24) * Math.PI * 2;
          const r1 = 300, r2 = 300 + (i % 2 ? 260 : 420) * p;
          return <line key={i} x1={540 + Math.cos(a) * r1} y1={900 + Math.sin(a) * r1} x2={540 + Math.cos(a) * r2} y2={900 + Math.sin(a) * r2} stroke={cor} strokeWidth={i % 2 ? 1.5 : 3} strokeLinecap="round" strokeOpacity={i % 2 ? 0.5 : 0.85} />;
        })}
      </g>
    </svg>
  );
};

const Linha: React.FC<{ p: number; cor?: string; w?: number }> = ({ p, cor = C.copperLight, w = 380 }) => (
  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 18 }}>
    <div style={{ height: 2, width: (w / 2) * p, background: `linear-gradient(90deg, transparent, ${cor})` }} />
    <div style={{ color: cor, fontSize: 30, transform: `rotate(${(1 - p) * 180}deg) scale(${p})` }}>✦</div>
    <div style={{ height: 2, width: (w / 2) * p, background: `linear-gradient(270deg, transparent, ${cor})` }} />
  </div>
);

// palavra que entra no tempo exato da fala
const Pal: React.FC<{ em: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ em, children, style }) => {
  const f = useCurrentFrame();
  const p = io(f, em - 3, em + 9);
  return (
    <span style={{ display: 'inline-block', opacity: p, filter: `blur(${(1 - p) * 12}px)`, transform: `translateY(${(1 - p) * 40}px) scale(${0.85 + p * 0.15})`, ...style }}>
      {children}
    </span>
  );
};

/* ---------- cenas ---------- */
const INI = { abre: 0, casa: t(4.55), menu: t(7.6), data: t(12.9), ret: t(16.45), cta: t(20.3) };

const Abertura: React.FC = () => {
  const f = useCurrentFrame();
  const at = (sec: number) => t(sec) - INI.abre;
  const logo = io(f, 0, 18);
  return (
    <AbsoluteFill>
      <Fundo src="fundos/abertura.jpg" dur={INI.casa} />
      <Brilhos n={40} />
      <div style={{ position: 'absolute', top: 260, width: '100%', display: 'flex', justifyContent: 'center', opacity: logo, transform: `translateY(${(1 - logo) * -24}px)` }}>
        <Img src={staticFile('img/logo-claro.webp')} style={{ width: 250 }} />
      </div>
      <div style={{ position: 'absolute', top: 640, left: 70, right: 70, textAlign: 'center' }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 40, letterSpacing: 12, color: C.peach, textTransform: 'uppercase' }}>
          <Pal em={at(0)}>Olha</Pal> <Pal em={at(0.55)}>só</Pal>
        </div>
        <div style={{ height: 34 }} />
        <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: 128, lineHeight: 1.02, color: C.cream }}>
          <Pal em={at(1.6)}>A sua</Pal> <Pal em={at(1.96)}>ceia</Pal><br />
          <Pal em={at(2.22)}>de</Pal> <Pal em={at(2.4)} style={{ color: C.copperLight, fontStyle: 'italic', fontWeight: 500 }}>Natal</Pal>
        </div>
        <div style={{ height: 30 }} />
        <div style={{ fontFamily: SERIF, fontStyle: 'italic', fontWeight: 500, fontSize: 84, color: C.peach }}>
          <Pal em={at(2.76)}>já tem</Pal> <Pal em={at(3.49)}>endereço</Pal>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Casa: React.FC = () => {
  const f = useCurrentFrame();
  const at = (sec: number) => t(sec) - INI.casa;
  const logo = io(f, 2, 22);
  return (
    <AbsoluteFill>
      <Fundo src="fundos/cardapio.jpg" dur={INI.menu - INI.casa} giro={4} />
      <Aneis cy={720} raio={330} />
      <Brilhos n={30} />
      <div style={{ position: 'absolute', top: 470, width: '100%', display: 'flex', justifyContent: 'center', opacity: logo, transform: `scale(${0.7 + logo * 0.3})` }}>
        <Img src={staticFile('img/logo-claro.webp')} style={{ width: 430 }} />
      </div>
      <div style={{ position: 'absolute', top: 1140, left: 70, right: 70, textAlign: 'center', fontFamily: SERIF, fontWeight: 600, fontSize: 92, lineHeight: 1.08, color: C.cream }}>
        <Pal em={at(5.36)}>prepara</Pal> <Pal em={at(5.93)} style={{ color: C.copperLight, fontStyle: 'italic' }}>tudo</Pal><br />
        <Pal em={at(6.29)}>pra você</Pal>
      </div>
    </AbsoluteFill>
  );
};

const ITENS: [string, number][] = [['Entradas', 7.86], ['Quiches', 8.54], ['Pratos principais', 9.27], ['Acompanhamentos', 10.67], ['Sobremesas', 11.73]];
const Cardapio: React.FC = () => {
  const f = useCurrentFrame();
  const at = (sec: number) => t(sec) - INI.menu;
  const titulo = io(f, 0, 16);
  return (
    <AbsoluteFill>
      <Fundo src="fundos/cardapio.jpg" dur={INI.data - INI.menu} giro={-4} escuro={0.55} />
      <Brilhos n={30} />
      <div style={{ position: 'absolute', top: 360, width: '100%', textAlign: 'center', opacity: titulo }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 34, letterSpacing: 12, color: C.peach }}>CARDÁPIO DE NATAL</div>
        <div style={{ height: 22 }} /><Linha p={titulo} />
      </div>
      <div style={{ position: 'absolute', top: 540, left: 0, right: 0 }}>
        {ITENS.map(([nome, sec], i) => {
          const em = at(sec);
          const p = io(f, em - 3, em + 12);
          const ativo = i === ITENS.length - 1 || f < at(ITENS[i + 1][1]) - 3;
          return (
            <div key={nome} style={{ height: 150, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 26, opacity: p * (ativo ? 1 : 0.5), transform: `translateX(${(1 - p) * (i % 2 ? 160 : -160)}px)` }}>
              <span style={{ color: C.copper, fontSize: 40, transform: `rotate(${p * 360}deg)`, display: 'inline-block' }}>✦</span>
              <span style={{ fontFamily: SERIF, fontWeight: 600, fontSize: ativo ? 100 : 84, color: ativo ? C.cream : C.peach }}>{nome}</span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const Data: React.FC = () => {
  const f = useCurrentFrame();
  const at = (sec: number) => t(sec) - INI.data;
  const g = io(f, at(15.02) - 4, at(15.02) + 14);
  return (
    <AbsoluteFill>
      <Fundo src="fundos/data.jpg" dur={INI.ret - INI.data} giro={3} escuro={0.5} />
      <Sequence from={at(14.9)}><Raios /></Sequence>
      <Brilhos n={50} vel={1.6} />
      <div style={{ position: 'absolute', top: 470, left: 60, right: 60, textAlign: 'center' }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 42, letterSpacing: 10, color: C.peach }}>
          <Pal em={at(13.07)}>ANOTA AÍ</Pal>
        </div>
        <div style={{ height: 40 }} />
        <div style={{ fontFamily: SERIF, fontStyle: 'italic', fontWeight: 500, fontSize: 86, color: C.cream }}>
          <Pal em={at(14.2)}>Encomendas</Pal> <Pal em={at(14.65)}>até</Pal>
        </div>
        <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 290, lineHeight: 1, color: C.cream, marginTop: 30, opacity: g, transform: `scale(${0.6 + g * 0.4})`, textShadow: `0 0 60px rgba(242,180,138,${0.6 * g})` }}>10/12</div>
        <div style={{ marginTop: 20, fontFamily: SANS, fontWeight: 700, fontSize: 40, letterSpacing: 8, color: C.copperLight }}>
          <Pal em={at(15.53)}>DEZEMBRO</Pal>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// relógio: ponteiro das horas vai de 10h a 15h (3h no mostrador) enquanto o arco cobre preenche
const Relogio: React.FC<{ inicio: number }> = ({ inicio }) => {
  const f = useCurrentFrame();
  const p = io(f, inicio, inicio + 40);
  const R = 150, cx = 200, cy = 200;
  const a0 = (10 / 12) * 360, a1 = a0 + 150 * p; // 10h -> 15h = 150°
  const pt = (ang: number, r: number) => [cx + r * Math.sin((ang * Math.PI) / 180), cy - r * Math.cos((ang * Math.PI) / 180)];
  const [x0, y0] = pt(a0, R - 18), [x1, y1] = pt(a1, R - 18);
  const [hx, hy] = pt(a1, 88), [mx, my] = pt(a1 * 12, 124);
  return (
    <svg width={400} height={400} viewBox="0 0 400 400" style={{ opacity: io(f, inicio - 10, inicio + 6) }}>
      <circle cx={cx} cy={cy} r={R + 18} fill={C.cream} stroke={C.copper} strokeWidth={4} />
      {Array.from({ length: 12 }).map((_, i) => { const [a, b] = pt(i * 30, R + 4), [c, d] = pt(i * 30, R - (i % 3 ? 4 : 14)); return <line key={i} x1={a} y1={b} x2={c} y2={d} stroke={C.brown} strokeWidth={i % 3 ? 2 : 5} strokeLinecap="round" />; })}
      {p > 0.01 && <path d={`M ${x0} ${y0} A ${R - 18} ${R - 18} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${x1} ${y1}`} fill="none" stroke={C.copper} strokeWidth={22} strokeLinecap="round" strokeOpacity={0.85} />}
      <line x1={cx} y1={cy} x2={mx} y2={my} stroke={C.copperInk} strokeWidth={5} strokeLinecap="round" />
      <line x1={cx} y1={cy} x2={hx} y2={hy} stroke={C.brown} strokeWidth={10} strokeLinecap="round" />
      <circle cx={cx} cy={cy} r={12} fill={C.copper} />
    </svg>
  );
};

const Retirada: React.FC = () => {
  const f = useCurrentFrame();
  const at = (sec: number) => t(sec) - INI.ret;
  const nota = io(f, at(19.6), at(19.6) + 16);
  return (
    <AbsoluteFill>
      <Fundo src="fundos/retirada.jpg" dur={INI.cta - INI.ret} giro={-3} escuro={0} />
      <AbsoluteFill style={{ background: 'radial-gradient(55% 40% at 50% 45%, rgba(252,243,236,.85), rgba(252,243,236,0) 75%)' }} />
      <Brilhos n={26} cor={C.copper} />
      <div style={{ position: 'absolute', top: 300, left: 60, right: 60, textAlign: 'center' }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 38, letterSpacing: 10, color: C.copperInk }}>
          <Pal em={at(16.64)}>RETIRADA NO DIA</Pal>
        </div>
        <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 230, lineHeight: 1, color: C.brown, marginTop: 10 }}>
          <Pal em={at(17.36)}>24/12</Pal>
        </div>
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: 20 }}><Relogio inicio={at(18.4)} /></div>
        <div style={{ fontFamily: SERIF, fontStyle: 'italic', fontWeight: 600, fontSize: 86, color: C.copperInk, marginTop: 10 }}>
          <Pal em={at(18.4)}>das</Pal> <Pal em={at(18.62)}>10h</Pal> <Pal em={at(18.91)}>às</Pal> <Pal em={at(19.16)}>15h</Pal>
        </div>
        <div style={{ marginTop: 26, opacity: nota, fontFamily: SANS, fontWeight: 600, fontSize: 32, color: C.ink, lineHeight: 1.45 }}>
          Av. Rachel de Queiroz · Barra da Tijuca<br />Entrega: consulte endereço e taxa no WhatsApp
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Chamada: React.FC = () => {
  const f = useCurrentFrame();
  const at = (sec: number) => t(sec) - INI.cta;
  const logo = io(f, 0, 16), d = io(f, at(22.47) - 4, at(22.47) + 12), fim = io(f, at(23.2), at(23.2) + 16);
  const pulso = 1 + Math.sin(f / 6) * 0.02 * d;
  return (
    <AbsoluteFill>
      <Fundo src="fundos/chamada.jpg" dur={DURACAO - INI.cta} giro={2} escuro={0} />
      <AbsoluteFill style={{ background: 'radial-gradient(55% 42% at 50% 42%, rgba(252,243,236,.92), rgba(252,243,236,0) 78%)' }} />
      <Aneis cy={560} raio={250} cor={C.copper} entrada={0} />
      <Brilhos n={30} cor={C.copper} />
      <div style={{ position: 'absolute', top: 360, width: '100%', display: 'flex', justifyContent: 'center', opacity: logo, transform: `scale(${0.8 + logo * 0.2})` }}>
        <Img src={staticFile('img/logo.webp')} style={{ width: 330 }} />
      </div>
      <div style={{ position: 'absolute', top: 870, left: 60, right: 60, textAlign: 'center' }}>
        <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: 108, lineHeight: 1.02, color: C.brown }}>
          <Pal em={at(20.75)}>Monte seu</Pal><br />
          <Pal em={at(21.49)} style={{ fontStyle: 'italic', fontWeight: 500, color: C.copperInk }}>pré-pedido</Pal>
        </div>
        <div style={{ height: 44 }} />
        <div style={{ opacity: d, transform: `scale(${(0.8 + d * 0.2) * pulso})`, display: 'inline-flex', alignItems: 'center', gap: 16, background: 'linear-gradient(180deg, #B25A28, #8A3F16)', color: '#fff', borderRadius: 999, padding: '28px 62px', fontFamily: SANS, fontWeight: 700, fontSize: 48, boxShadow: '0 24px 50px -20px rgba(138,63,22,.9)' }}>
          Link na bio ↑
        </div>
        <div style={{ opacity: fim, marginTop: 44, fontFamily: SANS, fontWeight: 700, fontSize: 36, color: C.ink, lineHeight: 1.5 }}>
          barra-deck-natal.vercel.app<br /><span style={{ color: C.copperInk }}>WhatsApp (21) 98171-6022</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- transições ---------- */
const Varredura: React.FC = () => {
  const f = useCurrentFrame();
  const x = interpolate(f, [0, 12], [-130, 130], { extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic) });
  return <AbsoluteFill style={{ background: `linear-gradient(105deg, transparent 0%, ${C.copperLight} 40%, ${C.copper} 50%, ${C.brown} 60%, transparent 100%)`, transform: `translateX(${x}%)` }} />;
};
const Flash: React.FC = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{ background: C.cream, opacity: interpolate(f, [0, 3, 10], [0, 0.85, 0], { extrapolateRight: 'clamp' }) }} />;
};

export const Reel: React.FC = () => {
  const cenas: [number, number, React.FC][] = [
    [INI.abre, INI.casa, Abertura], [INI.casa, INI.menu, Casa], [INI.menu, INI.data, Cardapio],
    [INI.data, INI.ret, Data], [INI.ret, INI.cta, Retirada], [INI.cta, DURACAO, Chamada],
  ];
  return (
    <AbsoluteFill style={{ background: C.espresso }}>
      {cenas.map(([a, b, Cena]) => (
        <Sequence key={a} from={a} durationInFrames={b - a}><Cena /></Sequence>
      ))}
      {[INI.casa, INI.data, INI.ret, INI.cta].map((c) => (
        <Sequence key={`v${c}`} from={c - 6} durationInFrames={14}><Varredura /></Sequence>
      ))}
      <Sequence from={INI.menu - 3} durationInFrames={12}><Flash /></Sequence>
      <Sequence from={s(OFFSET)}><Audio src={staticFile('audio/narracao.mp3')} /></Sequence>
    </AbsoluteFill>
  );
};
