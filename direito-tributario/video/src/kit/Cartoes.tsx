import React from 'react';
import {useCurrentFrame} from 'remotion';
import {COR, Escrito, FPS, W, entre, mola} from '../estilo';
import {ICONES} from '../icones2';
import {ItemCartao, Trecho} from './tipos';

// Cartões em motion (tela cheia ou metade de baixo da tela dividida), montados pelo roteiro.
type Area = {top: number; h: number};
const CORES_ITEM = [COR.mostarda, COR.tealClaro, COR.salvia, COR.laranja, COR.jeans];

const Icone: React.FC<{nome: string; tam: number}> = ({nome, tam}) => {
  const i = ICONES[nome] ?? ICONES.alerta;
  return (
    <svg width={tam} height={tam} viewBox="-150 -150 300 300" style={{overflow: 'visible', flexShrink: 0}}>
      <g transform={`scale(${i.s})`}>{i.el}</g>
    </svg>
  );
};

const useEntrada = (ini: number, dur = 12) => {
  const f = useCurrentFrame();
  return entre(f, Math.round(ini * FPS), dur, 0, 1, mola);
};

const Titulo: React.FC<{tr: Trecho; k: number}> = ({tr, k}) => {
  const p = useEntrada(tr.ini + 0.1, 14);
  if (!tr.titulo) return null;
  return (
    <div style={{display: 'flex', justifyContent: 'center', marginBottom: 26 * k}}>
      <div style={{transform: `scale(${p}) rotate(-2deg)`, display: 'flex', alignItems: 'center', gap: 16, background: COR.mostarda,
        border: `5px solid ${COR.tinta}`, borderRadius: 14, padding: `${6 * k}px ${36 * k}px 0`, maxWidth: 940}}>
        {tr.icone && <Icone nome={tr.icone} tam={110 * k} />}
        <Escrito tam={74 * k}>{tr.titulo}</Escrito>
      </div>
    </div>
  );
};

const Linha: React.FC<{it: ItemCartao; k: number; n: number; marca?: React.ReactNode}> = ({it, k, n, marca}) => {
  const p = useEntrada(it.ini);
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 22 * k, opacity: Math.min(1, p * 2),
      transform: `translateX(${(1 - p) * 300}px) rotate(${(n % 2 ? 1 : -1) * 0.8}deg)`, background: '#F7F3EA',
      border: `5px solid ${COR.tinta}`, borderRadius: 18, padding: `${12 * k}px ${26 * k}px ${6 * k}px`, margin: `${12 * k}px 0`}}>
      {marca ?? (it.icone ? <Icone nome={it.icone} tam={90 * k} /> : <Icone nome="check" tam={70 * k} />)}
      <Escrito tam={58 * k} style={{textAlign: 'left'}}>{it.texto}</Escrito>
    </div>
  );
};

const Destaque: React.FC<{it?: ItemCartao; k: number; cor?: string}> = ({it, k, cor = COR.mostarda}) => {
  const p = useEntrada(it?.ini ?? 0, 14);
  if (!it) return null;
  return (
    <div style={{display: 'flex', justifyContent: 'center', margin: `${20 * k}px 0`}}>
      <div style={{position: 'relative', transform: `scale(${p})`}}>
        <div style={{position: 'absolute', left: -20, right: -20, bottom: 26 * k, height: 50 * k, background: cor, opacity: 0.8, borderRadius: 12}} />
        <Escrito tam={130 * k * Math.min(1, 9 / Math.max(1, (it.texto ?? '').length))} style={{position: 'relative'}}>{it.texto}</Escrito>
      </div>
    </div>
  );
};

const Lista: React.FC<{tr: Trecho; k: number}> = ({tr, k}) => (
  <div>
    <Titulo tr={tr} k={k} />
    {tr.itens.filter((i) => i.tipo === 'item').map((it, n) => <Linha key={n} it={it} k={k} n={n} />)}
    <Destaque it={tr.itens.find((i) => i.tipo === 'destaque')} k={k * 0.7} />
  </div>
);

const Passos: React.FC<{tr: Trecho; k: number}> = ({tr, k}) => (
  <div>
    <Titulo tr={tr} k={k} />
    {tr.itens.filter((i) => i.tipo === 'item').map((it, n) => (
      <Linha key={n} it={it} k={k} n={n} marca={
        <div style={{width: 76 * k, height: 76 * k, borderRadius: '50%', background: CORES_ITEM[n % 5], border: `5px solid ${COR.tinta}`,
          display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
          <Escrito tam={52 * k}>{n + 1}</Escrito>
        </div>} />
    ))}
  </div>
);

const Comparacao: React.FC<{tr: Trecho; k: number}> = ({tr, k: kIn}) => {
  const k = Math.min(kIn, 1.05); // duas colunas: não pode crescer como os outros
  const [a, b] = tr.titulo.split(/\s+(?:x|vs\.?|versus)\s+/i);
  const col = (lado: 'esquerda' | 'direita', nome: string | undefined, c: string, n: number) => (
    <div style={{flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column', alignItems: 'stretch'}}>
      <div style={{background: c, border: `5px solid ${COR.tinta}`, borderRadius: 16, padding: `${6 * k}px 0 0`, marginBottom: 10 * k,
        transform: `rotate(${n ? 1.5 : -1.5}deg)`}}>
        <Escrito tam={70 * k}>{nome ?? lado}</Escrito>
      </div>
      {tr.itens.filter((i) => i.tipo === lado).map((it, j) => <Linha key={j} it={it} k={k * 0.85} n={j + n} marca={it.icone ? undefined : <span />} />)}
    </div>
  );
  return (
    <div>
      {!b && <Titulo tr={tr} k={k} />}
      <div style={{display: 'flex', gap: 26 * k, alignItems: 'flex-start'}}>
        {col('esquerda', b ? a : undefined, COR.tealClaro, 0)}
        <Escrito tam={70 * k} cor={COR.vermelho} style={{alignSelf: 'center'}}>x</Escrito>
        {col('direita', b, COR.laranja, 1)}
      </div>
    </div>
  );
};

const Numero: React.FC<{tr: Trecho; k: number}> = ({tr, k}) => (
  <div>
    <Titulo tr={tr} k={k} />
    <Destaque it={tr.itens.find((i) => i.tipo === 'destaque')} k={k * 1.15} />
    {tr.itens.filter((i) => i.tipo === 'item').map((it, n) => <Linha key={n} it={it} k={k * 0.85} n={n} />)}
  </div>
);

const Definicao: React.FC<{tr: Trecho; k: number}> = ({tr, k}) => {
  const p = useEntrada(tr.ini + 0.15, 16);
  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      {tr.icone && <div style={{transform: `scale(${p})`, filter: 'url(#adesivo)'}}><Icone nome={tr.icone} tam={250 * k} /></div>}
      <Escrito tam={110 * k} cor={COR.teal} style={{transform: `scale(${p})`}}>{tr.titulo}</Escrito>
      <svg width={600 * k} height={30}><path d={`M 10 15 Q ${300 * k} 0 ${590 * k} 18`} stroke={COR.vermelho} strokeWidth={8} fill="none" strokeLinecap="round"
        pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} /></svg>
      <Destaque it={tr.itens.find((i) => i.tipo === 'destaque')} k={k * 0.55} />
      <div style={{width: '100%'}}>{tr.itens.filter((i) => i.tipo === 'item').map((it, n) => <Linha key={n} it={it} k={k * 0.85} n={n} />)}</div>
    </div>
  );
};

const Mito: React.FC<{tr: Trecho; k: number}> = ({tr, k}) => {
  const d = tr.itens.find((i) => i.tipo === 'destaque');
  const p = useEntrada(d?.ini ?? 0, 10);
  const f = useCurrentFrame();
  const mito = d && /mito|falso|n[aã]o/i.test(d.texto ?? '');
  const c = mito ? COR.vermelho : COR.teal;
  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      <div style={{background: '#F7F3EA', border: `5px solid ${COR.tinta}`, borderRadius: 18, padding: `${16 * k}px ${30 * k}px ${8 * k}px`, maxWidth: 900}}>
        <Escrito tam={66 * k}>“{tr.titulo}”</Escrito>
      </div>
      {d && f >= Math.round(d.ini * FPS) && (
        <div style={{marginTop: 30 * k, border: `${10 * k}px solid ${c}`, borderRadius: 20, padding: `${10 * k}px ${40 * k}px 0`,
          transform: `rotate(-8deg) scale(${2 - p})`, opacity: Math.min(1, p * 1.5), background: 'rgba(251,248,241,0.85)'}}>
          <Escrito tam={130 * k * Math.min(1, 7 / Math.max(1, (d.texto ?? '').length))} cor={c} style={{whiteSpace: 'nowrap'}}>{d.texto}</Escrito>
        </div>
      )}
      <div style={{width: '100%', marginTop: 16 * k}}>{tr.itens.filter((i) => i.tipo === 'item').map((it, n) => <Linha key={n} it={it} k={k * 0.85} n={n} />)}</div>
    </div>
  );
};

const MODELOS = {lista: Lista, passos: Passos, comparacao: Comparacao, numero: Numero, definicao: Definicao, mito: Mito};

// Na tela cheia: ilustração grande do último item com ícone (ou do ícone do trecho), trocando com mola.
const Ilustracao: React.FC<{tr: Trecho}> = ({tr}) => {
  const f = useCurrentFrame();
  const vistos = tr.itens.filter((i) => i.icone && f >= Math.round(i.ini * FPS));
  const atual = vistos[vistos.length - 1];
  const nome = atual?.icone ?? (tr.modelo !== 'definicao' ? tr.icone : null);
  const ini = atual ? atual.ini : tr.ini + 0.2;
  const p = entre(f, Math.round(ini * FPS), 14, 0, 1, mola);
  if (!nome) return null;
  return (
    <div style={{display: 'flex', justifyContent: 'center', marginTop: 30, transform: `scale(${p}) rotate(${Math.sin(f / 20) * 3}deg) translateY(${Math.sin(f / 15) * 8}px)`,
      filter: 'url(#adesivo)'}}>
      <Icone nome={nome} tam={380} />
    </div>
  );
};

export const Cartao: React.FC<{tr: Trecho; area: Area}> = ({tr, area}) => {
  const M = MODELOS[tr.modelo ?? 'lista'] ?? Lista;
  const cheia = area.h > 1000;
  const k = cheia ? 1.45 : 0.92;
  return (
    <div style={{position: 'absolute', left: 60, width: W - 120, top: area.top, height: area.h, display: 'flex', flexDirection: 'column',
      justifyContent: 'center', filter: 'url(#boil)'}}>
      <M tr={tr} k={k} />
      {cheia && <Ilustracao tr={tr} />}
    </div>
  );
};
