import React from 'react';
import {AbsoluteFill, interpolate, Sequence, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {marca} from '../../marca/marca';
import {paleta} from '../../series/ano-zero/paleta';
import {fontes} from '../theme/fontes';
import {Boneco} from './Boneco';

// Teste de layout "cartoon de série": painel de status no topo, cartões de texto grandes,
// cenários chapados com luz quente, personagens de cabeça grande, transições por zoom.

const FPS = 30;
const T = {fachada: 0, edson: 4.2, portaria: 8.6, praia: 13.6, fim: 19};
export const DURACAO_TESTE_LAYOUT = Math.round(T.fim * FPS);

const ease = Easing.bezier(0.16, 1, 0.3, 1);
const entra = (f: number, ini: number, dur = 8) => interpolate(f, [ini, ini + dur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});

// ---------- peças de interface ----------

const CartaoStatus: React.FC<{rotulo: string; valor: string; destaque?: number}> = ({rotulo, valor, destaque = 0}) => (
  <div
    style={{
      flex: 1,
      background: `rgba(7,9,13,0.82)`,
      border: `2px solid ${destaque > 0 ? paleta.perigo : 'rgba(237,230,214,0.12)'}`,
      borderRadius: 14,
      padding: '12px 18px 14px',
      boxShadow: destaque > 0 ? `0 0 ${30 * destaque}px ${paleta.perigo}` : 'none',
    }}
  >
    <div style={{fontFamily: fontes.mono, fontSize: 22, letterSpacing: 6, color: marca.cores.cinza}}>{rotulo}</div>
    <div style={{fontFamily: fontes.marca, fontSize: 46, lineHeight: 1.1, color: destaque > 0.3 ? paleta.perigo : '#E8C27A'}}>{valor}</div>
  </div>
);

const Painel: React.FC<{hora: string; faltam: string; regras: string; destaque: number}> = ({hora, faltam, regras, destaque}) => (
  <div style={{position: 'absolute', top: 150, left: 40, right: 40}}>
    <div style={{display: 'flex', gap: 14}}>
      <CartaoStatus rotulo="HORA" valor={hora} />
      <CartaoStatus rotulo="FALTAM" valor={faltam} />
      <CartaoStatus rotulo="REGRAS" valor={regras} destaque={destaque} />
    </div>
    <div
      style={{
        display: 'inline-block',
        marginTop: 14,
        background: paleta.perigo,
        color: marca.cores.papel,
        fontFamily: fontes.marca,
        fontSize: 26,
        letterSpacing: 2,
        padding: '6px 16px',
        borderRadius: 6,
      }}
    >
      DIA 1 · DA INFECÇÃO
    </div>
  </div>
);

const Etiqueta: React.FC<{texto: string; f: number; ini: number; y: number; cor?: string; tamanho?: number}> = ({texto, f, ini, y, cor = 'rgba(7,9,13,0.88)', tamanho = 58}) => {
  const k = entra(f, ini, 7);
  return (
    <div style={{position: 'absolute', top: y, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: k, transform: `scale(${0.85 + 0.15 * k})`}}>
      <div style={{background: cor, borderRadius: 16, padding: '14px 34px', fontFamily: fontes.marca, fontSize: tamanho, color: marca.cores.papel, boxShadow: '0 10px 30px rgba(0,0,0,.5)'}}>
        {texto}
      </div>
    </div>
  );
};

// ---------- cenas ----------

const Fachada: React.FC = () => {
  const f = useCurrentFrame();
  const dur = (T.edson - T.fachada) * FPS;
  const zoom = interpolate(f, [0, dur - 16, dur], [1, 1.1, 4.2], {extrapolateRight: 'clamp', easing: Easing.in(Easing.cubic)});
  const janelas = [];
  for (let r = 0; r < 10; r++) {
    for (let c = 0; c < 4; c++) {
      const n = r * 4 + c;
      const acende = 4 + ((n * 37) % 23);
      const luz = (n * 13) % 5 < 2 && f > acende;
      janelas.push(
        <rect key={n} x={170 + c * 190} y={300 + r * 112} width={120} height={70} rx={4} fill={luz ? '#E8C27A' : '#141821'} opacity={luz ? 0.92 : 1} />,
      );
    }
  }
  return (
    <AbsoluteFill style={{background: 'linear-gradient(#05070B, #0E1626)'}}>
      <AbsoluteFill style={{transform: `scale(${zoom})`, transformOrigin: '540px 1560px'}}>
        <svg width={1080} height={1920}>
          <defs>
            <radialGradient id="porta-luz" cx="0.5" cy="0.6" r="0.6">
              <stop offset="0" stopColor="#E0413A" stopOpacity="0.45" />
              <stop offset="1" stopColor="#E0413A" stopOpacity="0" />
            </radialGradient>
          </defs>
          <rect x={120} y={240} width={840} height={1500} fill="#1B202B" />
          {janelas}
          <ellipse cx={540} cy={1480} rx={380} ry={240} fill="url(#porta-luz)" />
          <rect x={330} y={1430} width={420} height={76} rx={8} fill={paleta.perigo} />
          <text x={540} y={1484} textAnchor="middle" fontFamily={fontes.marca} fontSize={44} fill={marca.cores.papel}>
            EDIFÍCIO SOLAR DA ORLA
          </text>
          <rect x={410} y={1520} width={260} height={220} fill="#2E2A22" />
          <rect x={410} y={1520} width={260} height={220} fill="#0A0C10" opacity={interpolate(f, [dur - 16, dur], [0, 1], {extrapolateLeft: 'clamp'})} />
          <rect x={0} y={1740} width={1080} height={180} fill="#0A0C10" />
        </svg>
      </AbsoluteFill>
      <Etiqueta texto="31 DE DEZEMBRO" f={f} ini={14} y={560} />
      <Etiqueta texto="COPACABANA" f={f} ini={26} y={680} />
      <Etiqueta texto="23:00" f={f} ini={38} y={800} cor={paleta.perigo} tamanho={72} />
    </AbsoluteFill>
  );
};

const Edson: React.FC = () => {
  const f = useCurrentFrame();
  const dur = (T.portaria - T.edson) * FPS;
  const zoom = interpolate(f, [0, dur], [1.08, 1.0], {easing: ease});
  const cartao2 = f > 62;
  return (
    <AbsoluteFill style={{background: '#14110D'}}>
      <AbsoluteFill style={{transform: `scale(${zoom})`}}>
        <svg width={1080} height={1920}>
          {Array.from({length: 7}, (_, i) => (
            <rect key={i} x={i * 160} y={0} width={150} height={1500} fill="#1E1912" />
          ))}
          {/* porta de vidro com a noite lá fora */}
          <rect x={60} y={560} width={300} height={900} fill="#0B1424" stroke="#3A3326" strokeWidth={14} />
          <path d="M80,600 L200,600 L80,800 Z" fill="#fff" opacity={0.06} />
          {/* elevador */}
          <rect x={560} y={500} width={400} height={960} fill="#6E6450" stroke="#3A3326" strokeWidth={14} />
          <rect x={560 + 196} y={500} width={8} height={960} fill="#3A3326" />
          <rect x={700} y={430} width={120} height={56} rx={6} fill="#1A0D0B" />
          <text x={760} y={472} textAnchor="middle" fontFamily={fontes.mono} fontSize={40} fill={paleta.perigo}>
            T
          </text>
          <rect x={0} y={1460} width={1080} height={460} fill="#0D0B08" />
          <Boneco x={540} y={1580} escala={0.95} pele="#B07A55" camisa="#24365E" cabelo="grisalho" bigode oculos cracha boca={cartao2 ? 'reta' : 'sorriso'} bracoE={cartao2 ? 40 : 10} bracoD={cartao2 ? -40 : -10} olhar={cartao2 ? 0 : -0.5} />
        </svg>
      </AbsoluteFill>
      {!cartao2 ? (
        <div style={{position: 'absolute', top: 400, left: 120, right: 120, opacity: entra(f, 6), transform: `translateY(${(1 - entra(f, 6)) * 30}px)`}}>
          <div style={{background: '#2F5A9E', borderRadius: 18, padding: '18px 0 22px', textAlign: 'center', boxShadow: '0 12px 40px rgba(0,0,0,.6)'}}>
            <div style={{fontFamily: fontes.mono, fontSize: 30, letterSpacing: 6, color: '#D7E2F2'}}>20 ANOS NA PORTARIA</div>
            <div style={{fontFamily: fontes.marca, fontSize: 104, lineHeight: 1.05, color: marca.cores.papel}}>SEU EDSON</div>
          </div>
        </div>
      ) : (
        <div style={{position: 'absolute', top: 400, left: 90, right: 90, opacity: entra(f, 62), transform: `scale(${0.9 + 0.1 * entra(f, 62)})`}}>
          <div style={{background: 'rgba(7,9,13,0.92)', border: `3px solid ${paleta.perigo}`, borderRadius: 18, padding: '20px 26px 24px', textAlign: 'center'}}>
            <div style={{fontFamily: fontes.mono, fontSize: 28, letterSpacing: 6, color: paleta.perigo}}>REGRA DA CASA</div>
            <div style={{fontFamily: fontes.marca, fontSize: 62, lineHeight: 1.12, color: marca.cores.papel}}>DEPOIS DAS 22H, NINGUÉM ENTRA.</div>
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};

const CAMS = ['SAGUÃO', 'PORTÃO', 'GARAGEM', 'ELEVADOR', 'CALÇADA', 'PRAIA'];

const Monitor: React.FC<{i: number; f: number}> = ({i, f}) => {
  const x = 40 + (i % 2) * 510;
  const y = 330 + Math.floor(i / 2) * 250;
  return (
    <g>
      <rect x={x} y={y} width={490} height={230} rx={8} fill="#141B26" stroke="#2A3443" strokeWidth={8} />
      {i === 5
        ? Array.from({length: 14}, (_, k) => (
            <circle key={k} cx={x + 30 + k * 32} cy={y + 170 - Math.abs(Math.sin(f / 4 + k)) * 10} r={13} fill="#5D6E86" />
          ))
        : null}
      {i === 0 ? <rect x={x + 160} y={y + 60} width={140} height={150} fill="#202A38" /> : null}
      {i === 1 ? <rect x={x + 60} y={y + 70} width={360} height={60} fill="#202A38" /> : null}
      {i === 3 ? <rect x={x + 190} y={y + 50} width={110} height={170} fill="#2A2A2A" /> : null}
      {Array.from({length: 6}, (_, k) => (
        <rect key={k} x={x} y={y + 30 + k * 34 + ((f * 2) % 34)} width={490} height={2} fill="#fff" opacity={0.04} />
      ))}
      <text x={x + 18} y={y + 34} fontFamily={fontes.mono} fontSize={22} letterSpacing={2} fill="#9AA6B6">
        CAM 0{i + 1} · {CAMS[i]}
      </text>
    </g>
  );
};

const Portaria: React.FC = () => {
  const f = useCurrentFrame();
  const dur = (T.praia - T.portaria) * FPS;
  const pisca = f > 60 && Math.floor(f / 6) % 2 === 0;
  // empurra para o interfone, depois atravessa o monitor da praia
  const fase1 = interpolate(f, [60, 100], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
  const fase2 = interpolate(f, [dur - 22, dur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.in(Easing.cubic)});
  const z = 1 + fase1 * 0.25 + fase2 * 4.2;
  const ox = 540 + fase1 * 300 * (1 - fase2) + fase2 * (795 - 540);
  const oy = 960 + fase1 * 120 * (1 - fase2) + fase2 * (930 - 960);
  return (
    <AbsoluteFill style={{background: '#0B0E14'}}>
      <AbsoluteFill style={{transform: `scale(${z})`, transformOrigin: `${ox}px ${oy}px`}}>
        <svg width={1080} height={1920}>
          <defs>
            <radialGradient id="abajur" cx="0.5" cy="0.5" r="0.5">
              <stop offset="0" stopColor="#E8A64A" stopOpacity="0.5" />
              <stop offset="1" stopColor="#E8A64A" stopOpacity="0" />
            </radialGradient>
          </defs>
          <rect x={0} y={280} width={1080} height={800} fill="#0F141D" />
          {CAMS.map((_, i) => (
            <Monitor key={i} i={i} f={f} />
          ))}
          <circle cx={220} cy={1250} r={420} fill="url(#abajur)" />
          {/* interfone */}
          <rect x={800} y={1120} width={210} height={300} rx={12} fill="#1A1F28" stroke="#2A3443" strokeWidth={6} />
          {Array.from({length: 12}, (_, k) => {
            const ap = `${Math.floor(k / 3) * 3 + 3 + (k % 3)}01`;
            const alvo = k === 11;
            return (
              <g key={k}>
                <circle cx={845 + (k % 3) * 60} cy={1160 + Math.floor(k / 3) * 62} r={14} fill={alvo && pisca ? paleta.perigo : '#3A1C1C'} />
                <text x={845 + (k % 3) * 60} y={1192 + Math.floor(k / 3) * 62} textAnchor="middle" fontFamily={fontes.mono} fontSize={15} fill="#7E8794">
                  {alvo ? '1201' : ap}
                </text>
              </g>
            );
          })}
          {pisca ? <circle cx={965} cy={1346} r={30 + ((f % 12) / 12) * 60} fill="none" stroke={paleta.perigo} strokeWidth={5} opacity={1 - (f % 12) / 12} /> : null}
          <rect x={0} y={1430} width={1080} height={490} fill="#0A0C10" />
          <Boneco x={430} y={1560} escala={0.78} pele="#B07A55" camisa="#24365E" cabelo="grisalho" bigode oculos cracha sentado olhar={f > 66 ? 1 : 0} boca={f > 66 ? 'preocupado' : 'reta'} bracoD={-60} bracoE={20} />
          {/* balcão da portaria na frente do Edson */}
          <rect x={-20} y={1360} width={1120} height={40} fill="#4A3826" />
          <rect x={-20} y={1400} width={1120} height={520} fill="#2A2018" />
          <rect x={-20} y={1400} width={1120} height={10} fill="#000" opacity={0.4} />
        </svg>
      </AbsoluteFill>
      <div style={{position: 'absolute', top: 640, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: entra(f, 8) * (1 - fase1)}}>
        <div style={{background: 'rgba(7,9,13,0.9)', borderRadius: 18, padding: '12px 40px', fontFamily: fontes.marca, fontSize: 90, color: marca.cores.papel}}>23:00 → 00:00</div>
      </div>
      {f > 66 && fase2 < 0.2 ? (
        <div style={{position: 'absolute', top: 1500, left: 0, right: 0, textAlign: 'center', fontFamily: fontes.marca, fontSize: 50, color: paleta.perigo, opacity: entra(f, 66)}}>
          O 1201 TÁ CHAMANDO.
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

const Praia: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const queda = 1.2;
  const volta = 2.6;
  const regra = 3.4;
  const batidas = [2.6, 3.1, 3.6, 4.1, 4.6, 5.1];
  const ult = batidas.filter((b) => b <= t).pop();
  const pulso = ult !== undefined ? Math.exp(-(t - ult) * 7) : 0;
  const n = batidas.filter((b) => b <= t).length;
  const corpo = t < queda ? 0 : t < volta ? 90 * Math.min(1, (t - queda) / 0.35) : [90, 55, 20, 0][Math.min(3, n)];
  const tique = n > 0 ? (n % 2 ? 1 : -1) * 10 * pulso : 0;
  const zoom = interpolate(f, [0, 20], [1.25, 1], {extrapolateRight: 'clamp', easing: ease});
  return (
    <AbsoluteFill style={{background: '#0B1220'}}>
      <AbsoluteFill style={{transform: `scale(${zoom})`}}>
        <svg width={1080} height={1920}>
          <rect x={0} y={0} width={1080} height={900} fill="#0D1628" />
          <rect x={0} y={900} width={1080} height={1020} fill="#1A1A1C" />
          {/* multidão vista pela câmera de segurança */}
          {Array.from({length: 4}, (_, r) =>
            Array.from({length: 9}, (_, c) => {
              const s = 0.32 + r * 0.1;
              const x = 40 + c * 125 + (r % 2) * 60;
              const y = 950 + r * 150 - (t < queda ? Math.abs(Math.sin(t * 6 + c + r)) * 14 : pulso * 10);
              if (r === 2 && c === 4) return null;
              return (
                <g key={`${r}-${c}`} transform={`translate(${x} ${y}) scale(${s})`}>
                  <path d="M-110,0 Q-110,-150 0,-160 Q110,-150 110,0 Z" fill="#53627A" />
                  <circle cx={0} cy={-215} r={62} fill="#53627A" />
                </g>
              );
            }),
          )}
          {/* caixa de som com anéis */}
          <rect x={900} y={760} width={110} height={200} rx={8} fill="#0A0D12" stroke="#2A3443" strokeWidth={5} />
          {batidas.filter((b) => b <= t && t - b < 1).map((b) => (
            <circle key={b} cx={955} cy={830} r={30 + (t - b) * 260} fill="none" stroke={paleta.perigo} strokeWidth={7 * (1 - (t - b))} opacity={1 - (t - b)} />
          ))}
          <g transform={`translate(560 1330) rotate(${corpo})`}>
            <Boneco x={0} y={0} escala={0.5} pele={t > volta ? '#8C918E' : '#B08A6E'} camisa="#E4DED0" calca="#D9D4C7" cracha boca={t > volta ? 'aberta' : 'preocupado'} inclina={t > volta + 0.4 ? 22 + tique : 0} />
          </g>
        </svg>
      </AbsoluteFill>
      {/* moldura de câmera de segurança */}
      <AbsoluteFill style={{background: 'rgba(60,110,170,0.12)', mixBlendMode: 'screen'}} />
      {Array.from({length: 40}, (_, k) => (
        <div key={k} style={{position: 'absolute', left: 0, right: 0, top: k * 48 + ((f * 3) % 48), height: 2, background: '#fff', opacity: 0.035}} />
      ))}
      <div style={{position: 'absolute', top: 360, left: 50, fontFamily: fontes.mono, fontSize: 30, letterSpacing: 3, color: '#C8D3E0'}}>
        <span style={{color: paleta.perigo}}>● REC</span> CAM 06 · PRAIA · 23:00:{String(41 + Math.floor(t)).padStart(2, '0')}
      </div>
      {t > regra ? (
        <div style={{position: 'absolute', top: 1420, left: 70, right: 70, opacity: entra(f, regra * FPS), transform: `scale(${0.88 + 0.12 * entra(f, regra * FPS)})`}}>
          <div style={{background: paleta.perigo, borderRadius: 18, padding: '18px 24px 22px', textAlign: 'center', boxShadow: `0 0 60px ${paleta.perigo}`}}>
            <div style={{fontFamily: fontes.mono, fontSize: 30, letterSpacing: 6, color: '#2A0806'}}>REGRA 1</div>
            <div style={{fontFamily: fontes.marca, fontSize: 70, lineHeight: 1.1, color: marca.cores.papel}}>O SOM ACORDA ELES.</div>
          </div>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

export const TesteLayout: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const regraT = T.praia + 3.4;
  const destaque = t >= regraT ? Math.max(0.35, Math.exp(-(t - regraT) * 2)) : 0;
  const s = (a: number, b: number) => ({from: Math.round(a * fps), durationInFrames: Math.round((b - a) * fps)});
  return (
    <AbsoluteFill style={{background: marca.cores.preto}}>
      <Sequence {...s(T.fachada, T.edson)} name="Fachada"><Fachada /></Sequence>
      <Sequence {...s(T.edson, T.portaria)} name="Edson"><Edson /></Sequence>
      <Sequence {...s(T.portaria, T.praia)} name="Portaria"><Portaria /></Sequence>
      <Sequence {...s(T.praia, T.fim)} name="Praia"><Praia /></Sequence>
      <Painel hora={t < T.praia ? '23:00' : '23:01'} faltam={t < T.praia ? '60 MIN' : '59 MIN'} regras={t >= regraT ? '1/3' : '0/3'} destaque={destaque} />
    </AbsoluteFill>
  );
};
