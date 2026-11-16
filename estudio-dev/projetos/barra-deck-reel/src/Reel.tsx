import React from 'react';
import {
  AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, random, staticFile,
  useCurrentFrame, useVideoConfig,
} from 'remotion';
import { loadFont } from '@remotion/fonts';
import FONTES from './fontes.json';

// fontes locais (public/fontes) — baixadas por scripts/baixar_fontes.py
FONTES.forEach((f) => {
  loadFont({ family: f.family, url: staticFile(f.file), style: f.style, weight: f.weight, unicodeRange: f.unicodeRange });
});
const SERIF = 'Cormorant Garamond';
const SERIF_I = 'Cormorant Garamond';
const SANS = 'Karla';

// Paleta da marca (logo Barra Deck)
const C = {
  cream: '#FCF3EC', paper: '#FFFAF6', copper: '#C0652F', copperInk: '#A04E1F', copperLight: '#F2B48A',
  brown: '#4C220E', espresso: '#2A1409', ink: '#3B1D0D',
};

const FPS = 30;
const s = (sec: number) => Math.round(sec * FPS);
const OFFSET = 0.5;              // narração começa em 0,5 s
const t = (sec: number) => s(sec + OFFSET); // tempo da narração -> frame do vídeo
export const DURACAO = s(24);

const ease = Easing.bezier(0.2, 0.7, 0.2, 1);
const io = (f: number, a: number, b: number, from = 0, to = 1) =>
  interpolate(f, [a, b], [from, to], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease });

/* ---------- elementos ---------- */

const Brilhos: React.FC<{ cor?: string; n?: number }> = ({ cor = C.copperLight, n = 46 }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      {Array.from({ length: n }).map((_, i) => {
        const x = random(`x${i}`) * 1080;
        const vel = 0.6 + random(`v${i}`) * 1.4;
        const y = ((random(`y${i}`) * 2100 + f * vel * 2.2) % 2100) - 100;
        const r = 2 + random(`r${i}`) * 5;
        const sway = Math.sin((f + i * 20) / 30) * 14;
        const op = 0.25 + random(`o${i}`) * 0.55;
        return <div key={i} style={{ position: 'absolute', left: x + sway, top: y, width: r, height: r, borderRadius: '50%', background: cor, opacity: op, boxShadow: `0 0 ${r * 3}px ${cor}` }} />;
      })}
    </AbsoluteFill>
  );
};

const Ornamento: React.FC<{ cor?: string; largura?: number; p?: number }> = ({ cor = C.copper, largura = 340, p = 1 }) => (
  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 18, opacity: p }}>
    <div style={{ height: 2, width: (largura / 2) * p, background: `linear-gradient(90deg, transparent, ${cor})` }} />
    <div style={{ color: cor, fontSize: 30, transform: `rotate(${(1 - p) * 90}deg)` }}>✦</div>
    <div style={{ height: 2, width: (largura / 2) * p, background: `linear-gradient(270deg, transparent, ${cor})` }} />
  </div>
);

const Foto: React.FC<{ src: string; inicio: number; fim: number; zoom?: [number, number]; pos?: string; style?: React.CSSProperties }> = ({ src, inicio, fim, zoom = [1.04, 1.16], pos = 'center', style }) => {
  const f = useCurrentFrame();
  const z = interpolate(f, [inicio, fim], zoom, { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <div style={{ overflow: 'hidden', ...style }}>
      <Img src={staticFile(src)} style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: pos, transform: `scale(${z})` }} />
    </div>
  );
};

const Grao: React.FC = () => (
  <AbsoluteFill style={{ opacity: 0.18, mixBlendMode: 'multiply', backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .3 0 0 0 0 .15 0 0 0 0 .05 0 0 0 .5 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")` }} />
);

/* ---------- cena 1: abertura ---------- */
const Abertura: React.FC = () => {
  const f = useCurrentFrame();
  const fim = t(4.5);
  const logo = io(f, 0, 18);
  const titulo = io(f, 8, 28);
  const arco = io(f, 14, 36);
  return (
    <AbsoluteFill style={{ background: `radial-gradient(80% 50% at 50% 40%, #F8E3D2, ${C.cream} 70%)` }}>
      <Grao />
      <div style={{ position: 'absolute', top: 210, width: '100%', display: 'flex', justifyContent: 'center', opacity: logo, transform: `translateY(${(1 - logo) * -30}px)` }}>
        <Img src={staticFile('img/logo.webp')} style={{ width: 360 }} />
      </div>
      <div style={{ position: 'absolute', top: 560, width: '100%', textAlign: 'center', opacity: titulo, transform: `translateY(${(1 - titulo) * 30}px)` }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, letterSpacing: 10, fontSize: 30, color: C.copperInk }}>CEIA DE NATAL 2026</div>
        <div style={{ height: 22 }} />
        <Ornamento p={titulo} />
      </div>
      <div style={{ position: 'absolute', left: 140, right: 140, top: 720, height: 900, opacity: arco, transform: `translateY(${(1 - arco) * 60}px)` }}>
        <div style={{ position: 'absolute', inset: -16, borderRadius: '440px 440px 34px 34px', border: `2px solid ${C.copper}`, opacity: 0.55 }} />
        <Foto src="img/cheesecake.webp" inicio={0} fim={fim} zoom={[1.02, 1.1]} pos="50% 70%" style={{ position: 'absolute', inset: 0, borderRadius: '420px 420px 30px 30px', boxShadow: '0 50px 90px -40px rgba(42,20,9,.7)' }} />
      </div>
      <Brilhos n={30} cor={C.copper} />
    </AbsoluteFill>
  );
};

/* ---------- cena 2: categorias ---------- */
const CATS: { nome: string; img: string; em: number; pos?: string }[] = [
  { nome: 'Entradas', img: 'img/entradas.webp', em: 4.6 },
  { nome: 'Quiches', img: 'img/quiches.webp', em: 5.4 },
  { nome: 'Pratos principais', img: 'img/bacalhau.webp', em: 6.0 },
  { nome: 'Acompanhamentos', img: 'img/acompanhamentos.webp', em: 7.3 },
  { nome: 'Sobremesas', img: 'img/pave-morango.webp', em: 8.1, pos: '50% 50%' },
];
const Categorias: React.FC = () => {
  const f = useCurrentFrame();
  const base = t(4.5);
  return (
    <AbsoluteFill style={{ background: C.espresso }}>
      {CATS.map((c, i) => {
        const a = t(c.em) - base, b = (i < CATS.length - 1 ? t(CATS[i + 1].em) : t(9.2)) - base;
        if (f < a - 2 || f > b + 8) return null;
        const p = io(f, a - 2, a + 10);
        const sai = io(f, b - 2, b + 8);
        return (
          <AbsoluteFill key={c.nome}>
            <AbsoluteFill style={{ opacity: p }}>
              <Foto src={c.img} inicio={a} fim={b + 8} zoom={[1.3, 1.4]} pos={c.pos} style={{ position: 'absolute', inset: 0, filter: 'blur(28px) brightness(.45) saturate(1.2)' }} />
            </AbsoluteFill>
            <div style={{ position: 'absolute', left: 110, right: 110, top: 380, height: 760, transform: `translateY(${(1 - p) * 80}px) scale(${0.94 + p * 0.06})`, opacity: p }}>
              <div style={{ position: 'absolute', inset: -14, borderRadius: 40, border: `2px solid ${C.copperLight}`, opacity: 0.5 }} />
              <Foto src={c.img} inicio={a} fim={b + 8} zoom={[1.02, 1.1]} pos={c.pos} style={{ position: 'absolute', inset: 0, borderRadius: 30, boxShadow: '0 40px 80px -30px rgba(0,0,0,.8)' }} />
            </div>
            <div style={{ position: 'absolute', top: 1220, width: '100%', textAlign: 'center', opacity: io(f, a + 3, a + 14), transform: `translateY(${(1 - io(f, a + 3, a + 14)) * 26}px)` }}>
              <div style={{ fontFamily: SANS, fontWeight: 700, letterSpacing: 8, fontSize: 28, color: C.copperLight }}>{String(i + 1).padStart(2, '0')} · CARDÁPIO</div>
              <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: c.nome.length > 12 ? 104 : 128, lineHeight: 1, color: C.cream, marginTop: 16 }}>{c.nome}</div>
            </div>
          </AbsoluteFill>
        );
      })}
      <Sequence from={t(9.15) - base}>
        <FeitoNaCasa />
      </Sequence>
    </AbsoluteFill>
  );
};

const FeitoNaCasa: React.FC = () => {
  const f = useCurrentFrame();
  const p = io(f, 0, 14);
  const selo = io(f, 6, 22);
  return (
    <AbsoluteFill style={{ background: C.cream }}>
      <Foto src="img/pave-oreo.webp" inicio={0} fim={s(2)} zoom={[1.06, 1.14]} style={{ position: 'absolute', inset: 0, clipPath: `circle(${p * 120}% at 50% 50%)` }} />
      <AbsoluteFill style={{ background: 'linear-gradient(180deg, rgba(42,20,9,0) 45%, rgba(42,20,9,.75) 85%)' }} />
      <div style={{ position: 'absolute', left: '50%', top: 300, width: 300, height: 300, marginLeft: -150, borderRadius: '50%', background: C.brown, display: 'grid', placeContent: 'center', textAlign: 'center', transform: `scale(${selo}) rotate(${-8 - (1 - selo) * 30}deg)`, boxShadow: '0 30px 60px -20px rgba(0,0,0,.6)' }}>
        <div style={{ position: 'absolute', inset: 14, borderRadius: '50%', border: '2px dashed rgba(252,243,236,.45)' }} />
        <div style={{ fontFamily: SERIF_I, fontStyle: 'italic', fontWeight: 600, fontSize: 64, lineHeight: 1, color: C.cream }}>Feito<br />na casa</div>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- cena 3 e 4: informações ---------- */
const Info: React.FC<{ rotulo: string; grande: string; detalhe?: string; nota?: string; foto: string }> = ({ rotulo, grande, detalhe, nota, foto }) => {
  const f = useCurrentFrame();
  const a = io(f, 0, 14), b = io(f, 5, 20), c = io(f, 12, 28);
  return (
    <AbsoluteFill style={{ background: C.espresso }}>
      <Foto src={foto} inicio={0} fim={s(4)} zoom={[1.1, 1.2]} style={{ position: 'absolute', inset: 0, opacity: 0.22, filter: 'blur(6px)' }} />
      <AbsoluteFill style={{ background: `radial-gradient(70% 45% at 50% 45%, rgba(192,101,47,.28), transparent 70%)` }} />
      <Brilhos n={40} />
      <div style={{ position: 'absolute', top: 520, left: 90, right: 90, textAlign: 'center' }}>
        <div style={{ opacity: a, fontFamily: SANS, fontWeight: 700, letterSpacing: 10, fontSize: 30, color: C.copperLight }}>{rotulo}</div>
        <div style={{ height: 30 }} />
        <Ornamento cor={C.copperLight} p={a} />
        <div style={{ opacity: b, transform: `scale(${0.92 + b * 0.08})`, fontFamily: SERIF, fontWeight: 600, fontSize: 190, lineHeight: 1, color: C.cream, marginTop: 40 }}>{grande}</div>
        {detalhe && <div style={{ opacity: c, transform: `translateY(${(1 - c) * 20}px)`, fontFamily: SERIF_I, fontStyle: 'italic', fontWeight: 500, fontSize: 70, color: '#F7C9A5', marginTop: 26 }}>{detalhe}</div>}
        {nota && <div style={{ opacity: c, fontFamily: SANS, fontWeight: 500, fontSize: 38, lineHeight: 1.45, color: '#F1E1D4', marginTop: 50, whiteSpace: 'pre-line' }}>{nota}</div>}
      </div>
    </AbsoluteFill>
  );
};

/* ---------- cena 5: chamada final ---------- */
const Chamada: React.FC = () => {
  const f = useCurrentFrame();
  const a = io(f, 0, 16), b = io(f, 8, 24), c = io(f, 18, 34), d = io(f, 30, 46);
  const pulso = 1 + Math.sin(f / 7) * 0.015 * d;
  return (
    <AbsoluteFill style={{ background: `radial-gradient(80% 50% at 50% 35%, #F8E3D2, ${C.cream} 70%)` }}>
      <Grao />
      <Brilhos n={34} cor={C.copper} />
      <div style={{ position: 'absolute', top: 230, width: '100%', display: 'flex', justifyContent: 'center', opacity: a }}>
        <Img src={staticFile('img/logo.webp')} style={{ width: 300 }} />
      </div>
      <div style={{ position: 'absolute', top: 620, left: 80, right: 80, textAlign: 'center' }}>
        <div style={{ opacity: b, transform: `translateY(${(1 - b) * 30}px)`, fontFamily: SERIF, fontWeight: 600, fontSize: 118, lineHeight: 1.02, color: C.brown }}>
          Monte seu<br /><span style={{ fontFamily: SERIF_I, fontStyle: 'italic', fontWeight: 500, color: C.copperInk }}>pré-pedido</span>
        </div>
        <div style={{ height: 50 }} />
        <div style={{ opacity: c, transform: `scale(${pulso})`, display: 'inline-flex', alignItems: 'center', gap: 18, background: `linear-gradient(180deg, #B25A28, #8A3F16)`, color: '#fff', borderRadius: 999, padding: '30px 60px', fontFamily: SANS, fontWeight: 700, fontSize: 46, boxShadow: '0 24px 50px -20px rgba(138,63,22,.9)' }}>
          Link na bio ↑
        </div>
        <div style={{ opacity: d, marginTop: 60, fontFamily: SANS, fontWeight: 600, fontSize: 36, color: C.ink, lineHeight: 1.55 }}>
          barra-deck-natal.vercel.app<br />
          <span style={{ color: C.copperInk }}>WhatsApp (21) 98171-6022</span>
        </div>
        <div style={{ opacity: d, marginTop: 34, fontFamily: SANS, fontWeight: 500, fontSize: 28, color: '#76523F' }}>Encomendas até 10/12 · Retirada 24/12, 10h–15h</div>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- transição: varredura cobre ---------- */
const Varredura: React.FC = () => {
  const f = useCurrentFrame();
  const x = interpolate(f, [0, 12], [-120, 120], { extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic) });
  return <AbsoluteFill style={{ background: `linear-gradient(100deg, transparent 0%, ${C.copper} 45%, ${C.brown} 55%, transparent 100%)`, transform: `translateX(${x}%)` }} />;
};

export const Reel: React.FC = () => {
  const cortes = [t(4.5), t(9.15) /* dentro de categorias */, t(10.6), t(13.0), t(16.9)];
  return (
    <AbsoluteFill style={{ background: C.cream }}>
      <Sequence durationInFrames={t(4.5)}><Abertura /></Sequence>
      <Sequence from={t(4.5)} durationInFrames={t(10.6) - t(4.5)}><Categorias /></Sequence>
      <Sequence from={t(10.6)} durationInFrames={t(13.0) - t(10.6)}>
        <Info rotulo="ENCOMENDAS ATÉ" grande="10/12" foto="img/pave-oreo.webp" nota="Faça seu pré-pedido com antecedência" />
      </Sequence>
      <Sequence from={t(13.0)} durationInFrames={t(16.9) - t(13.0)}>
        <Info rotulo="RETIRADA NO RESTAURANTE" grande="24/12" detalhe="das 10h às 15h" foto="img/pudim.webp" nota={'Av. Rachel de Queiroz · Barra da Tijuca\nEntrega: consulte endereço e taxa no WhatsApp'} />
      </Sequence>
      <Sequence from={t(16.9)}><Chamada /></Sequence>
      {[cortes[0], cortes[2], cortes[3], cortes[4]].map((c) => (
        <Sequence key={c} from={c - 6} durationInFrames={14}><Varredura /></Sequence>
      ))}
      <Sequence from={s(OFFSET)}><Audio src={staticFile('audio/narracao.mp3')} /></Sequence>
    </AbsoluteFill>
  );
};
