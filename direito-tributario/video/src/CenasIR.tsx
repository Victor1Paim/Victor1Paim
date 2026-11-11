import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {COR, Escrito, MAO, Moeda, Traco, W, entre, mola, suave, tinta} from './estilo';
import {Bloco, quando} from './linha';
import {Carteira, Cofre, DefsSeta, G, Marcador, Seta} from './icones';

// Teste 02 — "Por que uns recebem restituição do IR e outros pagam?"
const pop = (f: number, ini: number, dur = 12) => entre(f, ini, dur, 0, 1, mola);

const Voo: React.FC<{f: number; ini: number; de: [number, number]; para: [number, number]; dur?: number; arco?: number}> = ({f, ini, de, para, dur = 18, arco = 140}) => {
  const p = entre(f, ini, dur, 0, 1, suave);
  if (p <= 0 || p >= 1) return null;
  return <Moeda x={de[0] + (para[0] - de[0]) * p} y={de[1] + (para[1] - de[1]) * p - Math.sin(p * Math.PI) * arco} r={28} />;
};

const Etiqueta: React.FC<{cor: string; children: React.ReactNode; tam?: number; giro?: number; s?: number}> = ({cor, children, tam = 84, giro = -2, s = 1}) => (
  <div style={{display: 'inline-block', transform: `scale(${s}) rotate(${giro}deg)`, background: cor, padding: '6px 34px 0',
    border: `5px solid ${COR.tinta}`, borderRadius: 14}}>
    <Escrito tam={tam}>{children}</Escrito>
  </div>
);

/* 1. GANCHO — sobreposto à apresentadora em tela cheia */
export const CenaGancho: React.FC<{b: Bloco}> = ({b}) => {
  const f = useCurrentFrame();
  const sai = 1 - entre(f, b.quadros - 4, 10);
  const tIR = quando(b, 'imposto');
  const tRec = quando(b, 'recebe');
  const tPaga = quando(b, 'paga?');
  return (
    <AbsoluteFill style={{opacity: sai}}>
      <div style={{position: 'absolute', top: 150, left: 0, right: 0, textAlign: 'center'}}>
        <Etiqueta cor={COR.mostarda} s={pop(f, tIR - 3)}>Imposto de Renda</Etiqueta>
      </div>
      {/* + de volta */}
      <div style={{position: 'absolute', left: 40, top: 1130, transform: `translateX(${(1 - pop(f, tRec - 2, 14)) * -500}px)`}}>
        <Etiqueta cor={COR.salvia} giro={-6} tam={70}>+ de volta</Etiqueta>
      </div>
      <svg width={W} height={1920} style={{position: 'absolute', inset: 0}}>
        <Voo f={f} ini={tRec + 2} de={[930, 1000]} para={[200, 1090]} dur={20} arco={220} />
        <Voo f={f} ini={tRec + 8} de={[930, 1000]} para={[240, 1090]} dur={20} arco={220} />
        <Voo f={f} ini={tPaga} de={[300, 1350]} para={[880, 1250]} dur={16} arco={160} />
      </svg>
      {/* − paga */}
      <div style={{position: 'absolute', right: 40, top: 1300, transform: `translateX(${(1 - pop(f, tPaga - 3, 14)) * 500}px)`}}>
        <Etiqueta cor={COR.laranja} giro={5} tam={70}>− paga</Etiqueta>
      </div>
    </AbsoluteFill>
  );
};

/* 2. RESPOSTA — parte de baixo da tela dividida (1080×1152): o holerite */
export const CenaResposta: React.FC<{b: Bloco}> = ({b}) => {
  const f = useCurrentFrame();
  const tDesc = quando(b, 'descontado');
  const tAno = quando(b, 'ano.');
  const linhas = [
    {nome: 'Salário', cor: COR.tinta},
    {nome: 'Desconto IR', cor: COR.vermelho},
    {nome: 'Líquido', cor: COR.tinta},
  ];
  const circ = entre(f, tDesc, 14);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 150, top: 30, width: 780, height: 560, background: '#F7F3EA',
        border: `6px solid ${COR.tinta}`, borderRadius: 10, transform: 'rotate(-2deg)'}}>
        <div style={{height: 26, background: COR.teal, borderBottom: `5px solid ${COR.tinta}`}} />
        <Escrito tam={74} cor={COR.teal} style={{marginTop: 26}}>Holerite</Escrito>
        {linhas.map((l, i) => (
          <div key={i} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', margin: '34px 60px 0', opacity: entre(f, 4 + i * 6, 10)}}>
            <Escrito tam={60} cor={l.cor}>{l.nome}</Escrito>
            <div style={{width: 200, height: 18, borderRadius: 9, background: i === 1 ? COR.vermelho : COR.cinza, opacity: 0.7}} />
          </div>
        ))}
        <svg width={780} height={640} style={{position: 'absolute', left: 0, top: 0}}>
          <Traco d="M 40 330 C 20 250 700 240 740 320 C 760 400 60 420 40 330" p={circ} cor={COR.vermelho} largura={7} />
        </svg>
      </div>
      {/* 12 risquinhos: "durante o ano" */}
      <svg width={W} height={1152} style={{position: 'absolute', inset: 0}}>
        {Array.from({length: 12}).map((_, i) => {
          const p = entre(f, tAno - 14 + i * 1.5, 6);
          return <Traco key={i} d={`M ${200 + i * 62} 625 l 0 50`} p={p} largura={7} cor={i % 2 ? COR.teal : COR.tinta} />;
        })}
      </svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 690, opacity: entre(f, tAno - 4, 8)}}>
        <Escrito tam={56}>12 meses</Escrito>
      </div>
    </AbsoluteFill>
  );
};

/* 3. RETIDO NA FONTE — motion em tela cheia */
const MESES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
export const CenaFonte: React.FC<{b: Bloco}> = ({b}) => {
  const f = useCurrentFrame();
  const tMes = quando(b, 'todo');
  const tFonte = quando(b, 'fonte.');
  const tDecl = quando(b, 'declaração,');
  const tConta = quando(b, 'conta');
  const passo = Math.max(2, (tFonte + 6 - tMes) / 12);
  const encolhe = entre(f, tDecl - 4, 14);
  const doc = pop(f, tDecl, 14);
  const soma = entre(f, tConta - 2, 16);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 130, left: 0, right: 0, textAlign: 'center'}}>
        <Etiqueta cor={COR.tealClaro} s={pop(f, 6)}>Retido na fonte</Etiqueta>
      </div>
      <svg width={W} height={1920} style={{position: 'absolute', inset: 0}}>
        <g opacity={1 - encolhe} transform={`translate(${540 - 540 * (1 - encolhe * 0.2)} ${encolhe * 60}) scale(${1 - encolhe * 0.2})`}>
          {MESES.map((m, i) => {
            const ini = tMes + i * passo;
            const s = pop(f, ini, 10);
            const x = 175 + (i % 4) * 243;
            const y = 470 + Math.floor(i / 4) * 200;
            return (
              <g key={m}>
                {s > 0 && (
                  <G x={x} y={y} s={s} r={(i % 3) - 1}>
                    <rect x={-90} y={-75} width={180} height={150} rx={10} fill="#F7F3EA" {...tinta} />
                    <rect x={-90} y={-75} width={180} height={40} rx={10} fill={COR.laranja} {...tinta} />
                    <text y={45} textAnchor="middle" fontFamily={MAO} fontSize={64} fill={COR.tinta}>{m.toUpperCase()}</text>
                  </G>
                )}
                <Voo f={f} ini={ini + 4} de={[x, y]} para={[540, 1180]} dur={16} arco={90} />
              </g>
            );
          })}
        </g>
        <G x={540} y={1250} s={pop(f, tMes - 6) * (1 - encolhe)}>
          <Cofre />
        </G>
        {doc > 0 && (
          <G x={540} y={1080} s={doc} r={-3}>
            <rect x={-260} y={-300} width={520} height={600} fill="#F7F3EA" {...tinta} strokeWidth={6} />
            <rect x={-260} y={-300} width={520} height={34} fill={COR.teal} {...tinta} />
            <text y={-190} textAnchor="middle" fontFamily={MAO} fontSize={70} fill={COR.teal}>DECLARAÇÃO</text>
            <text y={-130} textAnchor="middle" fontFamily={MAO} fontSize={44} fill={COR.tinta} opacity={0.6}>ANUAL</text>
            {[0, 1, 2, 3].map((i) => (
              <Traco key={i} d={`M -190 ${-50 + i * 60} L 190 ${-50 + i * 60}`} p={entre(f, tDecl + 6 + i * 3, 8)} cor={COR.cinza} largura={7} />
            ))}
            <Traco d="M -190 200 L 190 200" p={soma} largura={7} />
            <text x={0} y={265} textAnchor="middle" fontFamily={MAO} fontSize={58} fill={COR.vermelho} opacity={soma}>CONTA DO ANO</text>
          </G>
        )}
      </svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 1400, opacity: entre(f, tFonte - 6, 8) * (1 - encolhe)}}>
        <Escrito tam={60}>imposto retido</Escrito>
      </div>
    </AbsoluteFill>
  );
};

/* 4. A BALANÇA — motion em tela cheia */
export const CenaBalanca: React.FC<{b: Bloco}> = ({b}) => {
  const f = useCurrentFrame();
  const tMais = quando(b, 'mais');
  const tRest = quando(b, 'restituição.');
  const tMenos = quando(b, 'menos,');
  const tDif = quando(b, 'diferença.');
  // inclinação: + = lado RETIDO (esquerda) mais pesado
  const giro =
    interpolate(f, [tMais - 4, tMais + 10], [0, 12], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: mola}) +
    interpolate(f, [tMenos - 6, tMenos + 10], [0, -24], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: mola});
  const fase2 = f >= tMenos - 6;
  const rad = (giro * Math.PI) / 180;
  const cx = 540;
  const cy = 700;
  const braco = 330;
  const pe = (lado: -1 | 1) => ({x: cx + lado * braco * Math.cos(rad), y: cy - lado * braco * Math.sin(rad)});
  const E = pe(-1);
  const D = pe(1);
  const pilha = fase2 ? 2 : 5;
  const verde = pop(f, tRest - 2);
  const verm = pop(f, tDif - 4);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 130, left: 0, right: 0, textAlign: 'center'}}>
        <Etiqueta cor={COR.mostarda} s={pop(f, 4)}>A conta</Etiqueta>
      </div>
      <svg width={W} height={1920} style={{position: 'absolute', inset: 0}}>
        <DefsSeta />
        {/* coluna */}
        <path d={`M ${cx} ${cy} L ${cx} 1120 M ${cx - 130} 1120 L ${cx + 130} 1120`} {...tinta} strokeWidth={14} />
        <g transform={`rotate(${-giro} ${cx} ${cy})`}>
          <path d={`M ${cx - braco} ${cy} L ${cx + braco} ${cy}`} {...tinta} strokeWidth={12} />
        </g>
        <circle cx={cx} cy={cy} r={20} fill={COR.mostarda} {...tinta} />
        {[E, D].map((p, i) => (
          <g key={i}>
            <path d={`M ${p.x} ${p.y} L ${p.x - 110} ${p.y + 190} M ${p.x} ${p.y} L ${p.x + 110} ${p.y + 190}`} {...tinta} strokeWidth={4} />
            <path d={`M ${p.x - 140} ${p.y + 190} Q ${p.x} ${p.y + 260} ${p.x + 140} ${p.y + 190} Z`} fill={COR.cinza} {...tinta} />
          </g>
        ))}
        {/* prato esquerdo: moedas retidas */}
        {Array.from({length: pilha}).map((_, i) => (
          <Moeda key={i} x={E.x - 40 + (i % 3) * 40} y={E.y + 165 - Math.floor(i / 3) * 40} r={28} />
        ))}
        {/* prato direito: o devido */}
        <G x={D.x} y={D.y + 140}>
          <rect x={-70} y={-60} width={140} height={110} fill="#F7F3EA" {...tinta} />
          <path d="M -45 -25 L 45 -25 M -45 5 L 45 5" stroke={COR.cinza} strokeWidth={6} strokeLinecap="round" />
        </G>
        {/* fase 1: volta pra carteira */}
        {!fase2 && <Voo f={f} ini={tRest} de={[E.x, E.y + 120]} para={[250, 1450]} dur={16} arco={60} />}
        {!fase2 && <Voo f={f} ini={tRest + 6} de={[E.x, E.y + 120]} para={[280, 1450]} dur={16} arco={60} />}
        {/* fase 2: sai da carteira e completa */}
        {fase2 && <Voo f={f} ini={tDif - 2} de={[250, 1440]} para={[D.x, D.y + 100]} dur={18} arco={180} />}
        <G x={250} y={1470} s={pop(f, tRest - 8) * 1.1}>
          <Carteira />
        </G>
      </svg>
      <div style={{position: 'absolute', left: 90, top: 330, width: 340}}>
        <Escrito tam={56}>retido</Escrito>
      </div>
      <div style={{position: 'absolute', right: 90, top: 330, width: 340}}>
        <Escrito tam={56}>devido</Escrito>
      </div>
      <div style={{position: 'absolute', left: 420, top: 1360, width: 620}}>
        {!fase2 && verde > 0 && <Etiqueta cor={COR.salvia} s={verde} tam={68}>Restituição</Etiqueta>}
        {fase2 && verm > 0 && <Etiqueta cor={COR.laranja} s={verm} tam={64} giro={2}>Paga a diferença</Etiqueta>}
      </div>
    </AbsoluteFill>
  );
};

/* 5. CTA — parte de baixo da tela dividida */
export const CenaCta: React.FC<{b: Bloco}> = ({b}) => {
  const f = useCurrentFrame();
  const tDecl = quando(b, 'declaração.');
  const m = pop(f, 2, 14);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 0, right: 0, top: 120, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 30, transform: `scale(${m})`}}>
        <svg width={180} height={250}>
          <G x={90} y={125} s={1.1}><Marcador /></G>
        </svg>
        <Escrito tam={110} cor={COR.vermelho}>Salva</Escrito>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 440, textAlign: 'center'}}>
        <Etiqueta cor={COR.tealClaro} s={pop(f, tDecl - 4)} tam={64}>Época da declaração</Etiqueta>
      </div>
    </AbsoluteFill>
  );
};
