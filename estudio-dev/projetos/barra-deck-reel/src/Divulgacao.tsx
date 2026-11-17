import React from 'react';
import {
  AbsoluteFill, Easing, Img, OffthreadVideo, Sequence, interpolate, random, staticFile, useCurrentFrame,
} from 'remotion';
import { loadFont } from '@remotion/fonts';
import FONTES from './fontes.json';

FONTES.forEach((f) => {
  loadFont({ family: f.family, url: staticFile(f.file), style: f.style, weight: f.weight, unicodeRange: f.unicodeRange });
});
const SERIF = 'Cormorant Garamond';
const SANS = 'Karla';

// Paleta do site Barra Deck
const C = {
  cream: '#FCF3EC', paper: '#FFFAF6', copper: '#C0652F', copperInk: '#A04E1F', copperLight: '#F2B48A',
  peach: '#F7C9A5', brown: '#4C220E', espresso: '#2A1409', ink: '#3B1D0D', muted: '#76523F',
};

const FPS = 30;
const s = (sec: number) => Math.round(sec * FPS);
export const DURACAO_DIVULGACAO = s(30);

const ease = Easing.bezier(0.16, 1, 0.3, 1);
const io = (f: number, a: number, b: number) =>
  interpolate(f, [a, b], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease });
const sai = (f: number, a: number, b: number) =>
  interpolate(f, [a, b], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.in(Easing.cubic) });

const FELTRO = `url(${staticFile('img/feltro.webp')})`;

/* ---------- fundo: criativos desfocados + escurecidos ---------- */
const FundoVideo: React.FC<{ src: string; rate?: number; dur: number }> = ({ src, rate = 1, dur }) => {
  const f = useCurrentFrame();
  const z = interpolate(f, [0, dur], [1.12, 1.2]);
  return (
    <AbsoluteFill style={{ overflow: 'hidden', background: C.espresso }}>
      <OffthreadVideo src={staticFile(src)} muted playbackRate={rate}
        style={{ width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${z})`, filter: 'blur(11px) saturate(1.15) brightness(.92)' }} />
    </AbsoluteFill>
  );
};

const Veu: React.FC = () => (
  <>
    <AbsoluteFill style={{ background: 'linear-gradient(180deg, rgba(42,20,9,.66) 0%, rgba(42,20,9,.36) 35%, rgba(42,20,9,.44) 65%, rgba(42,20,9,.8) 100%)' }} />
    <AbsoluteFill style={{ backgroundImage: FELTRO, backgroundSize: '360px 360px', opacity: 0.6 }} />
    <AbsoluteFill style={{ background: 'radial-gradient(70% 45% at 50% 42%, rgba(192,101,47,.18), transparent 70%)' }} />
  </>
);

const Brilhos: React.FC<{ n?: number }> = ({ n = 46 }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      {Array.from({ length: n }).map((_, i) => {
        const x = random(`x${i}`) * 1080;
        const v = 0.5 + random(`v${i}`) * 1.3;
        const y = ((random(`y${i}`) * 2100 + f * v * 2) % 2100) - 100;
        const r = 2 + random(`r${i}`) * 5;
        const tw = 0.5 + 0.5 * Math.sin(f / (6 + random(`t${i}`) * 8) + i);
        return <div key={i} style={{ position: 'absolute', left: x + Math.sin((f + i * 20) / 30) * 14, top: y, width: r, height: r, borderRadius: '50%', background: C.copperLight, opacity: (0.25 + random(`o${i}`) * 0.55) * tw, boxShadow: `0 0 ${r * 4}px ${C.copperLight}` }} />;
      })}
    </AbsoluteFill>
  );
};

const Linha: React.FC<{ p: number; cor?: string; w?: number }> = ({ p, cor = C.copperLight, w = 360 }) => (
  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 18 }}>
    <div style={{ height: 2, width: (w / 2) * p, background: `linear-gradient(90deg, transparent, ${cor})` }} />
    <div style={{ color: cor, fontSize: 28, transform: `rotate(${(1 - p) * 180}deg) scale(${p})` }}>✦</div>
    <div style={{ height: 2, width: (w / 2) * p, background: `linear-gradient(270deg, transparent, ${cor})` }} />
  </div>
);

/* ---------- cenas ---------- */
const Abertura: React.FC = () => {
  const f = useCurrentFrame();
  const a = io(f, 0, 22), b = io(f, 14, 34), c = io(f, 24, 44);
  const fim = sai(f, s(3.3), s(3.8));
  return (
    <AbsoluteFill style={{ opacity: fim }}>
      <div style={{ position: 'absolute', top: 520, width: '100%', display: 'flex', justifyContent: 'center', opacity: a, transform: `scale(${0.85 + a * 0.15})` }}>
        <Img src={staticFile('img/logo-claro.webp')} style={{ width: 520 }} />
      </div>
      <div style={{ position: 'absolute', top: 1040, width: '100%', textAlign: 'center' }}>
        <div style={{ opacity: b }}><Linha p={b} /></div>
        <div style={{ opacity: c, transform: `translateY(${(1 - c) * 24}px)`, marginTop: 28, fontFamily: SANS, fontWeight: 700, fontSize: 44, letterSpacing: 14, color: C.peach }}>CEIA DE NATAL 2026</div>
      </div>
    </AbsoluteFill>
  );
};

const Manchete: React.FC = () => {
  const f = useCurrentFrame();
  const a = io(f, 0, 16), b = io(f, 12, 30), c = io(f, 26, 44);
  const fim = sai(f, s(3.3), s(3.8));
  return (
    <AbsoluteFill style={{ opacity: fim }}>
      <div style={{ position: 'absolute', top: 640, left: 70, right: 70, textAlign: 'center' }}>
        <div style={{ opacity: a, transform: `translateY(${(1 - a) * 40}px)`, fontFamily: SERIF, fontWeight: 600, fontSize: 132, lineHeight: 1, color: C.cream }}>O fogão é nosso.</div>
        <div style={{ opacity: b, transform: `translateY(${(1 - b) * 40}px)`, fontFamily: SERIF, fontStyle: 'italic', fontWeight: 500, fontSize: 132, lineHeight: 1.1, color: C.copperLight, marginTop: 10 }}>A noite é sua.</div>
        <div style={{ opacity: c, marginTop: 60, fontFamily: SANS, fontWeight: 500, fontSize: 40, lineHeight: 1.45, color: '#F1E1D4' }}>Encomende a ceia inteira e passe<br />o Natal na mesa, não na cozinha.</div>
      </div>
    </AbsoluteFill>
  );
};

type Prato = { img: string; nome: string; det: string; preco: string };
const CARDAPIO: { titulo: string; nota?: string; pratos: Prato[] }[] = [
  { titulo: 'Entradas', pratos: [
    { img: 'bolinho-bacalhau', nome: 'Bolinho de bacalhau', det: '50 unid.', preco: 'R$ 150' },
    { img: 'empanado-camarao', nome: 'Empanado de camarão', det: '50 unid.', preco: 'R$ 150' },
    { img: 'coxinha', nome: 'Coxinha', det: '100 unid.', preco: 'R$ 100' },
  ] },
  { titulo: 'Quiches', nota: 'Aro 24', pratos: [
    { img: 'quiche-alho-poro', nome: 'Alho-poró', det: 'quiche', preco: 'R$ 130' },
    { img: 'quiche-brie', nome: 'Brie com damasco', det: 'quiche', preco: 'R$ 180' },
    { img: 'quiche-camarao', nome: 'Camarão', det: 'quiche', preco: 'R$ 200' },
  ] },
  { titulo: 'Principais', nota: 'Sem acompanhamento', pratos: [
    { img: 'chester', nome: 'Chester', det: 'unidade', preco: 'R$ 275' },
    { img: 'tender', nome: 'Tender bolinha', det: 'unidade', preco: 'R$ 190' },
    { img: 'postas-bacalhau', nome: 'Postas de bacalhau', det: '1,3 kg', preco: 'R$ 300' },
  ] },
  { titulo: 'Acompanhamentos', pratos: [
    { img: 'arroz-natalino', nome: 'Arroz natalino', det: '1,3 kg', preco: 'R$ 150' },
    { img: 'farofa-ameixa', nome: 'Farofa de ameixa', det: '1 kg', preco: 'R$ 75' },
    { img: 'salpicao', nome: 'Salpicão de frango', det: '1 kg', preco: 'R$ 120' },
  ] },
  { titulo: 'Sobremesas', pratos: [
    { img: 'pudim', nome: 'Pudim grande', det: 'unidade', preco: 'R$ 150' },
    { img: 'cheesecake', nome: 'Cheesecake', det: 'frutas vermelhas', preco: 'R$ 175' },
    { img: 'rabanada', nome: 'Rabanada', det: 'unidade', preco: 'R$ 8' },
  ] },
];
const DUR_CAT = s(2.4);

const Cartao: React.FC<{ p: Prato; entra: number; saida: number; i: number }> = ({ p, entra, saida, i }) => {
  const f = useCurrentFrame();
  const a = io(f, entra, entra + 14);
  const b = sai(f, saida, saida + 8);
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: 32, padding: 22, borderRadius: 30,
      background: `${FELTRO} 0 0 / 360px 360px, ${C.paper}`, boxShadow: '0 30px 60px -28px rgba(0,0,0,.75)',
      border: `2px solid rgba(192,101,47,.35)`, opacity: a * b,
      transform: `translateX(${(1 - a) * (i % 2 ? -260 : 260) + (1 - b) * -120}px)`,
    }}>
      <Img src={staticFile(`pratos/${p.img}.webp`)} style={{ width: 230, height: 230, borderRadius: 22, objectFit: 'cover', flex: 'none' }} />
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: 62, lineHeight: 1.02, color: C.brown }}>{p.nome}</div>
        <div style={{ fontFamily: SANS, fontWeight: 500, fontSize: 30, color: C.muted, marginTop: 8 }}>{p.det}</div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 46, color: C.copperInk, marginTop: 14 }}>{p.preco}</div>
      </div>
    </div>
  );
};

const Cardapio: React.FC = () => {
  const f = useCurrentFrame();
  const idx = Math.min(CARDAPIO.length - 1, Math.floor(f / DUR_CAT));
  const cat = CARDAPIO[idx];
  const ini = idx * DUR_CAT, fimCat = ini + DUR_CAT;
  const t = io(f, ini, ini + 12), tOut = idx === CARDAPIO.length - 1 ? 1 : sai(f, fimCat - 8, fimCat);
  const topo = io(f, 0, 14);
  return (
    <AbsoluteFill>
      <div style={{ position: 'absolute', top: 250, width: '100%', textAlign: 'center', opacity: topo }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 32, letterSpacing: 12, color: C.peach }}>CARDÁPIO DE NATAL</div>
      </div>
      <div style={{ position: 'absolute', top: 330, width: '100%', textAlign: 'center', opacity: t * tOut, transform: `translateY(${(1 - t) * 30}px)` }}>
        <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: 118, lineHeight: 1, color: C.cream }}>{cat.titulo}</div>
        <div style={{ height: 52, marginTop: 8, fontFamily: SERIF, fontStyle: 'italic', fontWeight: 500, fontSize: 44, color: C.copperLight }}>{cat.nota ?? ''}</div>
      </div>
      <div style={{ position: 'absolute', top: 560, left: 64, right: 64, display: 'grid', gap: 30 }}>
        {cat.pratos.map((p, i) => (
          <Cartao key={`${idx}-${p.img}`} p={p} i={i} entra={ini + 4 + i * 5} saida={idx === CARDAPIO.length - 1 ? 99999 : fimCat - 10} />
        ))}
      </div>
      {/* barra de progresso das categorias */}
      <div style={{ position: 'absolute', top: 1520, width: '100%', display: 'flex', justifyContent: 'center', gap: 14, opacity: topo }}>
        {CARDAPIO.map((c, i) => (
          <div key={c.titulo} style={{ width: i === idx ? 54 : 14, height: 14, borderRadius: 99, background: i <= idx ? C.copperLight : 'rgba(247,201,165,.3)' }} />
        ))}
      </div>
    </AbsoluteFill>
  );
};

const Infos: React.FC = () => {
  const f = useCurrentFrame();
  const linhas: [string, string][] = [
    ['ENCOMENDAS ATÉ', '10 de dezembro'],
    ['RETIRADA', '24/12 · 10h às 15h'],
    ['ONDE', 'Clube da Aeronáutica\nda Barra da Tijuca'],
    ['ENTREGA', 'sob consulta no WhatsApp'],
  ];
  const fim = sai(f, s(4.5), s(5));
  return (
    <AbsoluteFill style={{ opacity: fim }}>
      <div style={{ position: 'absolute', top: 360, left: 80, right: 80 }}>
        <div style={{ textAlign: 'center', opacity: io(f, 0, 14) }}>
          <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: 104, color: C.cream, lineHeight: 1 }}>Anote na agenda</div>
          <div style={{ marginTop: 26 }}><Linha p={io(f, 4, 20)} /></div>
        </div>
        <div style={{ marginTop: 60, display: 'grid', gap: 26 }}>
          {linhas.map(([r, v], i) => {
            const p = io(f, 10 + i * 8, 26 + i * 8);
            return (
              <div key={r} style={{ opacity: p, transform: `translateY(${(1 - p) * 30}px)`, padding: '24px 34px', borderRadius: 26, background: `${FELTRO} 0 0 / 360px 360px, ${C.paper}`, boxShadow: '0 24px 50px -26px rgba(0,0,0,.7)', borderLeft: 'none', border: '2px solid rgba(192,101,47,.35)' }}>
                <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 26, letterSpacing: 8, color: C.copperInk }}>{r}</div>
                <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: 60, lineHeight: 1.08, color: C.brown, whiteSpace: 'pre-line', marginTop: 6 }}>{v}</div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Chamada: React.FC = () => {
  const f = useCurrentFrame();
  const a = io(f, 0, 16), b = io(f, 10, 28), c = io(f, 22, 40), d = io(f, 34, 52);
  const pulso = 1 + Math.sin(f / 7) * 0.02 * c;
  return (
    <AbsoluteFill>
      <div style={{ position: 'absolute', top: 240, width: '100%', display: 'flex', justifyContent: 'center', opacity: a }}>
        <Img src={staticFile('img/logo-claro.webp')} style={{ width: 300 }} />
      </div>
      <div style={{ position: 'absolute', top: 560, left: 60, right: 60, textAlign: 'center' }}>
        <div style={{ opacity: b, transform: `translateY(${(1 - b) * 30}px)`, fontFamily: SERIF, fontWeight: 600, fontSize: 120, lineHeight: 1, color: C.cream }}>
          Monte sua <span style={{ fontStyle: 'italic', fontWeight: 500, color: C.copperLight }}>ceia</span>
        </div>
        <div style={{ opacity: c, transform: `scale(${(0.85 + c * 0.15) * pulso})`, margin: '54px auto 0', width: 380, padding: 26, borderRadius: 32, background: '#fff', boxShadow: '0 30px 60px -24px rgba(0,0,0,.8)' }}>
          <Img src={staticFile('img/qrcode.png')} style={{ width: '100%', display: 'block' }} />
        </div>
        <div style={{ opacity: c, marginTop: 30, display: 'inline-block', padding: '20px 46px', borderRadius: 999, background: 'linear-gradient(180deg, #B25A28, #8A3F16)', fontFamily: SANS, fontWeight: 700, fontSize: 44, color: '#fff' }}>barradeck.vercel.app</div>
        <div style={{ opacity: d, marginTop: 34, fontFamily: SANS, fontWeight: 600, fontSize: 34, lineHeight: 1.5, color: '#F1E1D4' }}>
          Cardápio completo em PDF no site<br /><span style={{ color: C.peach }}>WhatsApp (21) 98171-6022</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Varredura: React.FC = () => {
  const f = useCurrentFrame();
  const x = interpolate(f, [0, 12], [-130, 130], { extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic) });
  return <AbsoluteFill style={{ background: `linear-gradient(105deg, transparent 0%, ${C.copperLight} 40%, ${C.copper} 50%, ${C.brown} 60%, transparent 100%)`, transform: `translateX(${x}%)`, opacity: 0.9 }} />;
};

// linha do tempo (segundos)
const T = { abre: 0, manchete: 3.8, cardapio: 7.6, infos: 7.6 + 12, chamada: 7.6 + 12 + 5 };

export const Divulgacao: React.FC = () => (
  <AbsoluteFill style={{ background: C.espresso }}>
    {/* fundo: criativo 1 até o fim do cardápio, criativo 2 nas informações e na chamada */}
    <Sequence durationInFrames={s(T.infos)}><FundoVideo src="criativos/fundo1.mp4" dur={s(T.infos)} rate={1.2} /></Sequence>
    <Sequence from={s(T.infos)}><FundoVideo src="criativos/fundo2.mp4" dur={DURACAO_DIVULGACAO - s(T.infos)} rate={1.2} /></Sequence>
    <Veu />
    <Brilhos />
    <Sequence durationInFrames={s(T.manchete)}><Abertura /></Sequence>
    <Sequence from={s(T.manchete)} durationInFrames={s(T.cardapio - T.manchete)}><Manchete /></Sequence>
    <Sequence from={s(T.cardapio)} durationInFrames={s(T.infos - T.cardapio)}><Cardapio /></Sequence>
    <Sequence from={s(T.infos)} durationInFrames={s(T.chamada - T.infos)}><Infos /></Sequence>
    <Sequence from={s(T.chamada)}><Chamada /></Sequence>
    {[T.cardapio, T.infos, T.chamada].map((c) => (
      <Sequence key={c} from={s(c) - 6} durationInFrames={14}><Varredura /></Sequence>
    ))}
  </AbsoluteFill>
);
