import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {marca} from '../../marca/marca';
import {paleta} from '../../series/ano-zero/paleta';
import {Reticula} from '../components/Reticula';
import {SimboloHalftone} from '../components/SimboloHalftone';
import {Boneco, BonecoProps} from '../estilo2/Boneco';
import {Cenario} from '../motion/Cenario';
import {LegendaKaraoke} from '../motion/LegendaKaraoke';
import {FILEIRAS_FRENTE, FILEIRAS_FUNDO, Multidao} from '../motion/Multidao';
import {fontes} from '../theme/fontes';
import {Barreira, BeiraMar, Calcadao, CloseMao, TelaChamada} from './Cenas';
import tl from './timeline.json';

// Ano Zero · Ep. 1 "A mão" — motion graphics, 15 planos, estilo "mistura":
// painel de status no topo, personagens cartoon, cenários chapados, retícula, legenda palavra por palavra.

const P = Object.fromEntries(tl.planos.map((p) => [p.id, p]));
const L = Object.fromEntries(tl.linhas.map((l) => [l.id, l]));
const EV = tl.eventos;
export const DURACAO_EP01 = Math.ceil(tl.duracao * 30);

const suave = (x: number) => {
  const k = Math.min(1, Math.max(0, x));
  return k * k * (3 - 2 * k);
};
const rampa = (t: number, a: number, b: number) => suave((t - a) / (b - a));
const ultima = (t: number) => {
  let u = -1;
  for (const b of tl.batidas) {
    if (b > t) break;
    u = b;
  }
  return u;
};
const pulso = (t: number) => {
  const b = ultima(t);
  return b < 0 || t - b > 0.6 ? 0 : Math.exp(-(t - b) * 9);
};
const nBatidas = (t: number, desde = 0) => tl.batidas.filter((b) => b >= desde && b <= t).length;

// ---------- elenco ----------
type Pose = Partial<BonecoProps>;
const BIA = (x: number, y: number, s: number, p: Pose = {}) => (
  <Boneco x={x} y={y} escala={s} pele="#8A5A3C" vestido camisa="#EDE6D6" cabelo="rabo" corCabelo="#1A1210" {...p} />
);
const CAIO = (x: number, y: number, s: number, p: Pose = {}) => (
  <Boneco x={x} y={y} escala={s} pele="#7A4E33" camisa="#F4F2EC" calca="#CDBF9F" bermuda cabelo="cacheado" corCabelo="#14100E" fitinha {...p} />
);
const RAFA = (x: number, y: number, s: number, p: Pose = {}) => (
  <Boneco x={x} y={y} escala={s} pele="#E0B48F" camisa="#F4F2EC" calca="#D9D4C7" bermuda regata cabelo="ondulado" corCabelo="#5A3B22" oculosCabeca {...p} />
);
const SEGURANCA = (x: number, y: number, s: number, p: Pose = {}) => (
  <Boneco x={x} y={y} escala={s} pele="#B08A6E" camisa="#D9D4C7" calca="#2A2F38" cabelo="curto" corCabelo="#3B2E26" cracha {...p} />
);

// ---------- peças de tela ----------
const Onomatopeia: React.FC<{texto: string; x: number; y: number; desde: number; t: number; rot?: number; cor?: string; tam?: number}> = ({
  texto, x, y, desde, t, rot = -8, cor = marca.cores.papel, tam = 110,
}) => {
  const u = t - desde;
  if (u < 0 || u > 0.55) return null;
  const k = u < 0.08 ? 0.6 + (u / 0.08) * 0.6 : 1.2 - Math.min(0.2, (u - 0.08) * 0.6);
  return (
    <div
      style={{
        position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) rotate(${rot}deg) scale(${k})`,
        fontFamily: fontes.marca, fontSize: tam, color: cor, WebkitTextStroke: '10px #0A0C10', paintOrder: 'stroke fill',
        opacity: u > 0.4 ? 1 - (u - 0.4) / 0.15 : 1, letterSpacing: 2,
      }}
    >
      {texto}
    </div>
  );
};

const Status: React.FC<{rotulo: string; valor: string; alerta?: number}> = ({rotulo, valor, alerta = 0}) => (
  <div
    style={{
      flex: 1, background: 'rgba(7,9,13,0.84)', borderRadius: 14, padding: '10px 16px 12px',
      border: `2px solid ${alerta > 0 ? paleta.perigo : 'rgba(237,230,214,0.12)'}`, boxShadow: alerta > 0 ? `0 0 ${34 * alerta}px ${paleta.perigo}` : 'none',
    }}
  >
    <div style={{fontFamily: fontes.mono, fontSize: 22, letterSpacing: 6, color: marca.cores.cinza}}>{rotulo}</div>
    <div style={{fontFamily: fontes.marca, fontSize: 44, lineHeight: 1.1, color: alerta > 0.3 ? paleta.perigo : '#E8C27A'}}>{valor}</div>
  </div>
);

const Painel: React.FC<{t: number}> = ({t}) => {
  const hora = t >= P.celular.inicio ? '23:05' : t >= EV.pulo23_02 ? '23:02' : '23:00';
  const faltam = hora === '23:05' ? '55 MIN' : hora === '23:02' ? '58 MIN' : '60 MIN';
  const regraT = P.levanta.inicio + 2.3;
  const regras = t >= regraT ? '1/3' : '0/3';
  const alertaRegra = t >= regraT ? Math.max(0.3, Math.exp(-(t - regraT) * 1.6)) : 0;
  const alertaHora = (t >= EV.pulo23_02 && t < EV.pulo23_02 + 1.2) || (t >= P.celular.inicio && t < P.celular.inicio + 1) ? 0.8 : 0;
  return (
    <div style={{position: 'absolute', top: 150, left: 36, right: 36}}>
      <div style={{display: 'flex', gap: 12}}>
        <Status rotulo="HORA" valor={hora} alerta={alertaHora} />
        <Status rotulo="FALTAM" valor={faltam} />
        <Status rotulo="REGRAS" valor={regras} alerta={alertaRegra} />
      </div>
      <div style={{display: 'flex', gap: 10, marginTop: 12}}>
        <div style={{background: paleta.perigo, color: marca.cores.papel, fontFamily: fontes.marca, fontSize: 26, letterSpacing: 2, padding: '6px 16px', borderRadius: 6}}>
          DIA 1 DA INFECÇÃO
        </div>
        <div style={{background: 'rgba(7,9,13,0.84)', color: marca.cores.papel, fontFamily: fontes.mono, fontSize: 24, letterSpacing: 4, padding: '8px 14px', borderRadius: 6}}>
          EP. 1/12
        </div>
      </div>
    </div>
  );
};

// ---------- câmera ----------
type Cam = [number, number, number]; // x, y, zoom
const lerpCam = (a: Cam, b: Cam, k: number): Cam => [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k];

const Mundo: React.FC<{cam: Cam; blur?: number; children: React.ReactNode; tremor?: [number, number]}> = ({cam, blur = 0, children, tremor = [0, 0]}) => (
  <AbsoluteFill style={{filter: blur ? `blur(${blur}px)` : undefined}}>
    <AbsoluteFill style={{transform: `translate(${540 - cam[0] * cam[2] + tremor[0]}px, ${960 - cam[1] * cam[2] + tremor[1]}px) scale(${cam[2]})`, transformOrigin: '0 0'}}>
      <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{overflow: 'visible'}}>
        {children}
      </svg>
    </AbsoluteFill>
  </AbsoluteFill>
);

const Aneis: React.FC<{t: number; x: number; y: number; desde: number; ate: number}> = ({t, x, y, desde, ate}) => (
  <g>
    {tl.batidas
      .filter((b) => b >= desde && b < ate && b <= t && t - b < 1.1)
      .map((b) => {
        const q = (t - b) / 1.1;
        return <circle key={b} cx={x} cy={y} r={24 + q * 260} fill="none" stroke={paleta.perigo} strokeWidth={Math.max(1, 10 * (1 - q))} opacity={(1 - q) * 0.95} />;
      })}
  </g>
);

const palco = (t: number, hora: string, faltam: string, opts: {multidaoParada?: boolean} = {}) => (
  <>
    <Cenario t={t} hora={hora} faltam={faltam} />
    <Multidao t={t} fileiras={FILEIRAS_FUNDO} agito={opts.multidaoParada ? 0 : 1} />
  </>
);

// ---------- planos ----------
const Plano: React.FC<{id: string; t: number}> = ({id, t}) => {
  const p = P[id];
  const u = t - p.inicio;
  const d = p.fim - p.inicio;
  const k = suave(u / d);
  const pu = pulso(t);
  const danca = (fase: number) => -pu * 14 * (0.7 + fase);

  switch (id) {
    case 'mao':
      return (
        <Mundo cam={lerpCam([540, 1000, 1.0], [560, 1010, 1.14], k)}>
          <CloseMao u={u} />
        </Mundo>
      );
    case 'rebobina': {
      const volta = u < 0.9 ? (0.9 - u) / 0.9 : 0;
      return (
        <>
          <Mundo cam={lerpCam([560, 960, 1.0], [640, 990, 1.1], k)} tremor={[volta * Math.sin(t * 60) * 18, 0]}>
            {palco(t, '23:00', 'FALTAM 60 MIN')}
            {SEGURANCA(330, 1240, 0.46, {y: 1240 + danca(0.2), bracoE: 20 + pu * 30, bracoD: -20 - pu * 30, boca: 'sorriso'})}
            {RAFA(760, 1262 + danca(0.5), 0.47, {bracoE: 30 + pu * 40, bracoD: -30 - pu * 40, boca: 'sorriso'})}
            {BIA(880, 1270 + danca(0.1), 0.48, {boca: 'reta', olhar: 0.6})}
            {CAIO(1000, 1276 + danca(0.8), 0.48, {boca: 'sorriso', olhar: -0.6})}
            <Multidao t={t} fileiras={FILEIRAS_FRENTE} />
          </Mundo>
          {volta > 0 ? (
            <AbsoluteFill style={{background: 'rgba(7,9,13,0.45)', alignItems: 'center', justifyContent: 'center'}}>
              {Array.from({length: 18}, (_, i) => (
                <div key={i} style={{position: 'absolute', left: 0, right: 0, top: ((i * 113 + t * 2400) % 1920), height: 4, background: '#EDE6D6', opacity: 0.12}} />
              ))}
              <div style={{fontFamily: fontes.marca, fontSize: 96, color: marca.cores.papel, WebkitTextStroke: '8px #0A0C10', paintOrder: 'stroke fill'}}>◀◀ 20 S</div>
              <div style={{fontFamily: fontes.mono, fontSize: 34, letterSpacing: 8, color: marca.cores.papel, marginTop: 10}}>REBOBINA</div>
            </AbsoluteFill>
          ) : null}
        </>
      );
    }
    case 'calcadao':
      return (
        <Mundo cam={lerpCam([560, 1120, 1.0], [600, 1110, 1.06], k)}>
          <Calcadao t={t} />
          {RAFA(900, 1380, 0.6, {olhar: -0.8, boca: 'sorriso'})}
          {CAIO(660, 1400, 0.64, {olhar: 0.4, boca: 'sorriso', bracoE: 20, bracoD: -20})}
          {BIA(250, 2050, 1.25, {costas: true})}
        </Mundo>
      );
    case 'closeBia': {
      const foco = rampa(u, d - 2.4, d - 1.6);
      return (
        <>
          <Mundo cam={lerpCam([540, 1000, 1.1], [540, 975, 1.22], k)} blur={foco * 8}>
            <Calcadao t={t} />
            {BIA(540, 1960, 1.25, {sobrancelha: 'brava', boca: 'reta', olhar: u > d * 0.45 ? 0.8 : -0.3, lanterna: 0, bracoD: -6})}
          </Mundo>
          <Mundo cam={lerpCam([540, 1000, 1.1], [540, 975, 1.22], k)} blur={(1 - foco) * 14}>
            {RAFA(1180, 2480, 1.9, {costas: true})}
          </Mundo>
        </>
      );
    }
    case 'caminho': {
      const fim = rampa(u, d - 0.5, d);
      const cam = lerpCam(lerpCam([470, 1180, 1.0], [620, 1170, 1.05], k), [228, 1258, 3.0], fim);
      return (
        <Mundo cam={cam}>
          <Calcadao t={t} />
          {CAIO(300, 1480, 0.66, {olhar: 0.7, boca: 'reta'})}
          {BIA(560, 1500, 0.7, {sobrancelha: 'brava', bracoE: 70, bracoD: -70, boca: t < L.r1.inicio ? 'aberta' : 'reta', olhar: t < L.r1.inicio ? -0.6 : 0.7})}
          {RAFA(830, 1490, 0.66, {olhar: -0.7, boca: t >= L.r1.inicio && t < L.r1.inicio + L.r1.duracao ? 'aberta' : 'reta', bracoD: -35})}
        </Mundo>
      );
    }
    case 'beiramar':
      return (
        <Mundo cam={lerpCam([560, 1150, 1.0], [560, 1180, 1.08], k)}>
          <BeiraMar t={t} />
          {CAIO(600, 1600, 0.86, {olhar: -0.5, boca: t > L.b2.inicio + L.b2.duracao ? 'sorriso' : 'reta'})}
          {BIA(70, 1980, 1.2, {costas: true})}
        </Mundo>
      );
    case 'palcoAlto': {
      const camb = Math.sin(t * 5) * 9 * rampa(u, 0.6, 1.4);
      return (
        <Mundo cam={lerpCam([540, 640, 0.86], [430, 1070, 1.4], k)}>
          {palco(t, '23:00', 'FALTAM 60 MIN')}
          {SEGURANCA(330, 1240, 0.46, {inclina: camb, boca: 'preocupado', olhar: -0.4})}
          {RAFA(760, 1262 + danca(0.5), 0.47, {olhar: -1, boca: 'reta'})}
          {BIA(880, 1270, 0.48, {olhar: 1, boca: 'reta'})}
          {CAIO(1000, 1276 + danca(0.8), 0.48, {olhar: -0.6, boca: 'sorriso'})}
          <Multidao t={t} fileiras={FILEIRAS_FRENTE} />
        </Mundo>
      );
    }
    case 'cracha': {
      const caiu = rampa(t, EV.queda, EV.queda + 0.45);
      const dedo = t < EV.queda ? (nBatidas(t) % 2 ? 26 : 6) : 10;
      const cam: Cam =
        t < p.inicio + 1.6
          ? lerpCam([354, 994, 3.0], [354, 990, 3.2], u / 1.6)
          : t < EV.queda
            ? [282, 1080, 3.4]
            : lerpCam([282, 1080, 3.4], [430, 1190, 1.55], rampa(t, EV.queda, EV.queda + 0.6));
      return (
        <Mundo cam={cam}>
          {palco(t, '23:00', 'FALTAM 60 MIN')}
          {SEGURANCA(330, 1240, 0.46, {inclina: caiu * 90, boca: 'aberta', olhar: 0, bracoE: dedo, piscar: caiu > 0.9})}
          {RAFA(760, 1262, 0.47, {olhar: -1, boca: t > L.r2.inicio ? 'aberta' : 'reta', bracoD: -110})}
          <Multidao t={t} fileiras={FILEIRAS_FRENTE} />
        </Mundo>
      );
    }
    case 'imovel': {
      const dip = rampa(u, d - 0.35, d);
      return (
        <>
          <Mundo cam={[470, 1205, 2.3]}>
            {palco(t, u < 0.6 ? '23:00' : '23:02', u < 0.6 ? 'FALTAM 60 MIN' : 'FALTAM 58 MIN', {multidaoParada: true})}
            {SEGURANCA(330, 1240, 0.46, {inclina: 90, boca: 'reta', piscar: true, bracoE: 10, bracoD: -10})}
          </Mundo>
          <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 55%, transparent 35%, rgba(0,0,0,0.75) 85%)'}} />
          <AbsoluteFill style={{background: '#000', opacity: dip}} />
        </>
      );
    }
    case 'levanta': {
      const subida = Math.min(3, nBatidas(t, P.levanta.inicio + 1.0));
      const corpo = [90, 55, 20, 0][subida];
      const tique = subida >= 3 ? (nBatidas(t) % 2 ? 1 : -1) * 14 * Math.min(1, pu * 2) : 0;
      const cam: Cam = u < 1.1 ? lerpCam([570, 870, 3.0], [560, 880, 3.1], u / 1.1) : lerpCam([560, 880, 3.1], [400, 1090, 1.75], rampa(u, 1.1, 1.6));
      return (
        <Mundo cam={cam} blur={u > 1.1 && u < 1.4 ? 6 : 0}>
          {palco(t, '23:02', 'FALTAM 58 MIN', {multidaoParada: true})}
          <Aneis t={t} x={570} y={870} desde={EV.batidaVolta} ate={EV.batidaPara} />
          {SEGURANCA(330, 1240, 0.46, {eco: true, inclina: corpo, cabeca: 24 + tique, boca: 'aberta', bracoE: 30, bracoD: -50})}
        </Mundo>
      );
    }
    case 'camadas': {
      const tique = (nBatidas(t) % 2 ? 1 : -1) * 14 * Math.min(1, pu * 2);
      const whip = rampa(u, d - 0.25, d);
      return (
        <Mundo cam={lerpCam([520, 1080, 1.3], [600, 1070, 1.36], k).map((v, i) => (i === 0 ? v + whip * 700 : v)) as Cam} blur={whip * 18}>
          {palco(t, '23:02', 'FALTAM 58 MIN', {multidaoParada: true})}
          <Aneis t={t} x={570} y={870} desde={EV.batidaVolta} ate={EV.batidaPara} />
          {SEGURANCA(330, 1240, 0.46, {eco: true, cabeca: 24 + (t < EV.batidaPara ? tique : 0), boca: 'aberta', bracoE: 30, bracoD: -50})}
          {RAFA(760, 1262, 0.47, {olhar: -1, boca: t > L.r3.inicio ? 'aberta' : 'preocupado', sobrancelha: 'triste'})}
          {BIA(880, 1270, 0.48, {olhar: -1, boca: 'preocupado', bracoD: -80})}
          {CAIO(1000, 1276, 0.48, {olhar: -1, boca: 'preocupado'})}
          <g transform={`skewX(${t < EV.batidaPara ? -pu * 6 : 0})`}>
            <Multidao t={t} fileiras={FILEIRAS_FRENTE} agito={0} />
          </g>
        </Mundo>
      );
    }
    case 'barreira': {
      const tremor: [number, number] = [Math.sin(t * 13) * 7 + Math.sin(t * 5.3) * 5, Math.cos(t * 11) * 6];
      return (
        <Mundo cam={lerpCam([400, 1250, 1.05], [640, 1240, 1.15], k)} tremor={tremor}>
          <Barreira t={t} />
          {Array.from({length: 7}, (_, i) => {
            const x = ((i * 260 + u * (i % 2 ? 340 : -300)) % 1800) - 300;
            return <g key={i} opacity={0.9}>{(i % 2 ? RAFA : CAIO)(x, 1700 + (i % 3) * 60, 0.55, {costas: true})}</g>;
          })}
          {BIA(560, 1560, 0.78, {sobrancelha: 'triste', boca: 'preocupado', olhar: Math.sin(u * 1.4) > 0 ? 1 : -1})}
          {Array.from({length: 5}, (_, i) => {
            const x = ((i * 400 - u * 420) % 2000) + 100;
            return <g key={`f${i}`}>{SEGURANCA(x, 2150, 1.0, {costas: true, camisa: '#1C2028', calca: '#111', corCabelo: '#111'})}</g>;
          })}
        </Mundo>
      );
    }
    case 'lanterna': {
      const flashes = [0.3, 0.9, 1.5];
      const aceso = flashes.some((f) => u >= f && u < f + 0.22) ? 1 : 0;
      return (
        <>
          <Mundo cam={lerpCam([620, 1080, 1.6], [640, 1060, 1.7], k)}>
            <BeiraMar t={t} />
            {BIA(520, 1900, 1.15, {costas: true, bracoD: -150, lanterna: aceso})}
          </Mundo>
          {aceso ? <AbsoluteFill style={{background: 'radial-gradient(circle at 62% 38%, rgba(255,246,216,0.55), transparent 45%)'}} /> : null}
        </>
      );
    }
    case 'celular': {
      const toques = [EV.toque1 - p.inicio, EV.toque2 - p.inicio];
      const preto = u > d - 0.25;
      return (
        <>
          <Mundo cam={lerpCam([540, 1000, 1.0], [540, 990, 1.06], k)}>
            <TelaChamada u={u} toques={toques} />
            {toques.filter((tc) => u >= tc && u - tc < 1.1).map((tc) => {
              const q = (u - tc) / 1.1;
              return <rect key={tc} x={190 - q * 200} y={360 - q * 200} width={700 + q * 400} height={1300 + q * 400} rx={70 + q * 60} fill="none" stroke={paleta.perigo} strokeWidth={10 * (1 - q)} opacity={1 - q} />;
            })}
          </Mundo>
          {preto ? <AbsoluteFill style={{background: '#000'}} /> : null}
        </>
      );
    }
    default:
      return null;
  }
};

const Cartao: React.FC<{u: number}> = ({u}) => {
  const k = suave(u / 0.4);
  return (
    <AbsoluteFill style={{background: marca.cores.preto, alignItems: 'center', justifyContent: 'center', padding: '0 80px', paddingBottom: 220, opacity: k}}>
      <SimboloHalftone tamanho={170} />
      <div style={{marginTop: 34, fontFamily: fontes.mono, fontSize: 28, letterSpacing: 8, color: marca.cores.cinza}}>ANO ZERO · EP. 1 DE 12 · A MÃO</div>
      <div style={{marginTop: 22, fontFamily: fontes.marca, fontSize: 64, lineHeight: 1.12, color: marca.cores.papel, textAlign: 'center'}}>
        No próximo: atender o irmão ou proteger a própria posição?
      </div>
      <div style={{marginTop: 30, display: 'flex', gap: 18}}>
        <div style={{background: paleta.sessoes.bia, color: '#0A0C10', fontFamily: fontes.marca, fontSize: 40, padding: '8px 24px', borderRadius: 10}}>A · ATENDER</div>
        <div style={{background: '#EDE6D6', color: '#0A0C10', fontFamily: fontes.marca, fontSize: 40, padding: '8px 24px', borderRadius: 10}}>B · SILENCIAR</div>
      </div>
      <div style={{marginTop: 34, fontFamily: fontes.mono, fontSize: 32, letterSpacing: 5, color: paleta.perigo}}>PRÓXIMO EP.: QUARTA, 20H</div>
      <div style={{marginTop: 18, fontFamily: fontes.mono, fontSize: 24, letterSpacing: 4, color: marca.cores.cinza}}>SÉRIE DE FICÇÃO · HALFTONE · @HALFTONE.TV1</div>
    </AbsoluteFill>
  );
};

export const Ep01: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const plano = tl.planos.find((p) => t >= p.inicio && t < p.fim) ?? tl.planos[tl.planos.length - 1];
  const naCena = plano.id !== 'cartao';
  const tique = tl.batidas.filter((b) => b >= EV.batidaVolta + 1.0 && b < EV.batidaPara && b <= t).slice(-1)[0];
  const tum = tl.batidas.filter((b) => b >= EV.batidaVolta && b < EV.batidaVolta + 1.2 && b <= t).slice(-1)[0];

  return (
    <AbsoluteFill style={{background: marca.cores.preto}}>
      {naCena ? <Plano id={plano.id} t={t} /> : <Cartao u={t - plano.inicio} />}
      {naCena ? <Reticula opacidade={0.1} /> : null}

      {/* onomatopeias para quem assiste sem som */}
      {tum !== undefined && plano.id === 'levanta' ? <Onomatopeia texto="TUM" x={700} y={760} desde={tum} t={t} rot={-10} /> : null}
      {tique !== undefined && (plano.id === 'levanta' || plano.id === 'camadas') ? <Onomatopeia texto="CLACK" x={300} y={820} desde={tique} t={t} rot={8} cor={paleta.perigo} tam={96} /> : null}
      {plano.id === 'lanterna'
        ? [0.3, 0.9, 1.5].map((f) => <Onomatopeia key={f} texto="CLIC" x={760} y={620} desde={P.lanterna.inicio + f} t={t} rot={6} tam={84} />)
        : null}
      {plano.id === 'celular'
        ? [EV.toque1, EV.toque2].map((tc) => <Onomatopeia key={tc} texto="TRRRIM" x={540} y={1440} desde={tc} t={t} rot={-6} cor={paleta.sessoes.caio} tam={100} />)
        : null}

      {naCena && plano.id !== 'celular' ? <LegendaKaraoke t={t} linhas={tl.linhas} libras={tl.libras} /> : null}
      {naCena ? <Painel t={t} /> : null}

      <Audio src={staticFile(tl.trilha)} volume={0.6} />
      {tl.linhas.map((l) => (
        <Sequence key={l.id} from={Math.round(l.inicio * fps)} layout="none" name={`voz ${l.id}`}>
          <Audio src={staticFile(l.arquivo)} volume={1} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
