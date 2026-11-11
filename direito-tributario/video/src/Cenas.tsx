import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {COR, MAO, Escrito, Moeda, Traco, W, entre, mola, suave, tinta} from './estilo';
import {Bloco, quando} from './linha';
import {Caminhao, Casa, Carteira, Cofre, Cone, DefsSeta, G, Lixeira, Loja, Lupa, Marcador, Sacola, Seta} from './icones';

const pop = (f: number, ini: number, dur = 12) => entre(f, ini, dur, 0, 1, mola);

// Voo de moeda com arco: de (x0,y0) para (x1,y1).
const Voo: React.FC<{f: number; ini: number; de: [number, number]; para: [number, number]; dur?: number}> = ({f, ini, de, para, dur = 18}) => {
  const p = entre(f, ini, dur, 0, 1, suave);
  if (p <= 0 || p >= 1) return null;
  const x = de[0] + (para[0] - de[0]) * p;
  const y = de[1] + (para[1] - de[1]) * p - Math.sin(p * Math.PI) * 160;
  return <Moeda x={x} y={y} r={30} s={1 - p * 0.3} />;
};

const Titulo: React.FC<{texto: string; cor: string; f: number; tam?: number}> = ({texto, cor, f, tam = 120}) => {
  const s = pop(f, 6, 14);
  return (
    <div style={{position: 'absolute', top: 120, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
      <div style={{transform: `scale(${s}) rotate(-2deg)`, background: cor, padding: '6px 44px 0', border: `5px solid ${COR.tinta}`, borderRadius: 14}}>
        <Escrito tam={tam}>{texto}</Escrito>
      </div>
    </div>
  );
};

const Nota: React.FC<{f: number; ini: number; children: React.ReactNode; top: number; cor?: string}> = ({f, ini, children, top, cor = COR.mostarda}) => {
  const p = entre(f, ini, 12);
  return (
    <div style={{position: 'absolute', top, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: p > 0 ? 1 : 0}}>
      <div style={{position: 'relative', padding: '0 24px'}}>
        <div style={{position: 'absolute', left: 0, top: '18%', height: '70%', width: `${p * 100}%`, background: cor, opacity: 0.55, borderRadius: 8}} />
        <Escrito tam={58} style={{position: 'relative'}}>{children}</Escrito>
      </div>
    </div>
  );
};

/* ---------- 1. GANCHO (parte de baixo da tela dividida, 1080×1152) ---------- */
export const CenaGancho: React.FC<{b: Bloco}> = ({b}) => {
  const f = useCurrentFrame();
  const tImp = quando(b, 'imposto?');
  const tNao = quando(b, 'não.');
  const linhas = [0, 1, 2, 3].map((i) => entre(f, 4 + i * 5, 10));
  const sq = pop(f, tImp - 2);
  const st = entre(f, tNao - 2, 8, 2.2, 1, suave);
  return (
    <AbsoluteFill>
      <svg width={W} height={1152}>
        <G x={470} y={380} r={-4}>
          <rect x={-250} y={-320} width={500} height={620} fill="#F7F3EA" {...tinta} />
          <path d="M -250 -320 L -250 300" stroke={COR.teal} strokeWidth={14} />
                    {linhas.map((p, i) => (
            <Traco key={i} d={`M -190 ${-120 + i * 80} L ${150 - (i % 2) * 90} ${-120 + i * 80}`} p={p} largura={6} cor={COR.cinza} />
          ))}
          <Moeda x={-150} y={220} r={36} />
          <Moeda x={-70} y={220} r={36} />
          <Moeda x={10} y={220} r={36} />
        </G>
        {f >= tImp - 2 && (
          <G x={860} y={300} s={sq} r={8}>
            <text textAnchor="middle" y={120} fontSize={360} fill={COR.laranja} stroke={COR.tinta} strokeWidth={6} fontFamily={MAO}>?</text>
          </G>
        )}
      </svg>
      <div style={{position: 'absolute', left: 220, top: 92, width: 500, transform: 'rotate(-4deg)'}}>
        <Escrito tam={70} cor={COR.teal}>Governo</Escrito>
        <Escrito tam={44} cor={COR.tinta} style={{opacity: 0.65}}>cobrança</Escrito>
      </div>
      {f >= tNao - 2 && (
        <div style={{position: 'absolute', left: 120, top: 330, transform: `rotate(-12deg) scale(${st})`, opacity: entre(f, tNao - 2, 4)}}>
          <div style={{border: `9px solid ${COR.vermelho}`, borderRadius: 18, padding: '10px 34px 0', background: 'rgba(236,232,220,0.75)'}}>
            <Escrito tam={104} cor={COR.vermelho}>Nem tudo é imposto</Escrito>
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};

/* ---------- 2. TRÊS TIPOS (tela cheia) ---------- */
const CARTOES = [
  {nome: 'Imposto', cor: COR.mostarda, icone: <Cofre />, s: 0.42},
  {nome: 'Taxa', cor: COR.tealClaro, icone: <Lixeira />, s: 1},
  {nome: 'Contribuição\nde melhoria', cor: COR.salvia, icone: <Cone />, s: 0.75},
];
export const CenaTres: React.FC<{b: Bloco}> = ({b}) => {
  const f = useCurrentFrame();
  const t3 = quando(b, 'três');
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', top: 150, left: 0, right: 0}}>
        <Escrito tam={60} style={{opacity: entre(f, 4, 10)}}>Código Tributário Nacional</Escrito>
        <Escrito tam={44} cor={COR.vermelho} style={{opacity: entre(f, 12, 10), marginTop: 8}}>art. 5º</Escrito>
      </div>
      {CARTOES.map((c, i) => {
        const ini = t3 - 4 + i * 6;
        const p = entre(f, ini, 16, 0, 1, mola);
        const y = 420 + i * 370;
        return (
          <div key={i} style={{position: 'absolute', left: 110, top: y, width: 860, height: 310,
            transform: `translateX(${(1 - p) * 1100}px) rotate(${(i - 1) * 2.5 + (1 - p) * 10}deg)`,
            background: c.cor, border: `6px solid ${COR.tinta}`, borderRadius: 26, display: 'flex', alignItems: 'center'}}>
            <svg width={300} height={300} style={{flexShrink: 0}}>
              <G x={150} y={160} s={c.s}>{c.icone}</G>
            </svg>
            <Escrito tam={i === 2 ? 74 : 104} style={{textAlign: 'left', whiteSpace: 'pre-line'}}>{c.nome}</Escrito>
            <div style={{position: 'absolute', right: 26, top: 14}}>
              <Escrito tam={56} cor={COR.tinta} style={{opacity: 0.5}}>{i + 1}</Escrito>
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

/* ---------- 3. IMPOSTO ---------- */
export const CenaImposto: React.FC<{b: Bloco}> = ({b}) => {
  const f = useCurrentFrame();
  const tServ = quando(b, 'serviço');
  const itens = [
    {t: quando(b, 'renda,'), x: 200, nome: 'renda', el: <Carteira />},
    {t: quando(b, 'compra'), x: 540, nome: 'compra', el: <Sacola />},
    {t: quando(b, 'patrimônio,'), x: 880, nome: 'patrimônio', el: <Casa cor={COR.jeans} />},
  ];
  const tDin = quando(b, 'dinheiro');
  const tGeral = quando(b, 'caixa');
  const cofre = pop(f, tDin - 4, 14);
  const risco = entre(f, tServ + 10, 10);
  return (
    <AbsoluteFill>
      <Titulo texto="Imposto" cor={COR.mostarda} f={f} />
      <Nota f={f} ini={tServ - 6} top={370}>
        <span style={{position: 'relative'}}>
          serviço em troca
          <svg width={460} height={80} style={{position: 'absolute', left: -20, top: 0}}>
            <Traco d="M 10 50 Q 200 20 440 30" p={risco} cor={COR.vermelho} largura={10} />
          </svg>
        </span>
      </Nota>
      <svg width={W} height={1920} style={{position: 'absolute', inset: 0}}>
        {itens.map((it, i) => {
          const s = pop(f, it.t - 3);
          return (
            <g key={i}>
              {s > 0 && <G x={it.x} y={720} s={s * 1.25}>{it.el}</G>}
            </g>
          );
        })}
        {cofre > 0 && <G x={540} y={1250} s={cofre * 1.15}>
          <Cofre />
        </G>}
        {itens.map((it, i) => (
          <Voo key={i} f={f} ini={tDin + i * 5} de={[it.x, 720]} para={[540, 1230]} />
        ))}
        {[0, 1, 2].map((i) => {
          const p = entre(f, tDin + 16 + i * 5, 6);
          return p > 0 ? <Moeda key={i} x={480 + i * 60} y={1110 - i * 12} r={26} s={p} /> : null;
        })}
      </svg>
      {itens.map((it, i) => (
        <div key={i} style={{position: 'absolute', left: it.x - 170, width: 340, top: 860, opacity: entre(f, it.t, 8)}}>
          <Escrito tam={54}>{it.nome}</Escrito>
        </div>
      ))}
      <div style={{position: 'absolute', left: 0, right: 0, top: 1440, opacity: entre(f, tGeral - 4, 8), transform: `scale(${pop(f, tGeral - 4)})`}}>
        <Escrito tam={84} cor={COR.vermelho}>Caixa geral</Escrito>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- 4. TAXA ---------- */
export const CenaTaxa: React.FC<{b: Bloco}> = ({b}) => {
  const f = useCurrentFrame();
  const tServ = quando(b, 'serviço');
  const tCol = quando(b, 'coleta');
  const tFisc = quando(b, 'fiscalização');
  const xCam = interpolate(f, [tCol - 14, tCol + 16], [1300, 690], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: suave});
  const roda = f * 14 * (f < tCol + 16 ? 1 : 0);
  const seta = entre(f, tCol + 22, 14);
  const lupaP = entre(f, tFisc - 6, 30);
  const lupaX = 380 + Math.sin(lupaP * Math.PI * 1.5) * 150;
  const ok = pop(f, tFisc + 26);
  return (
    <AbsoluteFill>
      <Titulo texto="Taxa" cor={COR.tealClaro} f={f} />
      <Nota f={f} ini={tServ - 4} top={370} cor={COR.tealClaro}>serviço específico</Nota>
      <svg width={W} height={1920} style={{position: 'absolute', inset: 0}}>
        <DefsSeta />
        <path d="M 40 870 L 1040 870" {...tinta} strokeWidth={4} opacity={0.5} />
        <G x={230} y={740} s={pop(f, 8)}>
          <Casa />
        </G>
        <G x={420} y={812} s={pop(f, 14) * 0.9}>
          <Lixeira />
        </G>
        <G x={xCam} y={790}>
          <Caminhao roda={roda} />
        </G>
        <Seta d="M 250 600 Q 470 470 660 600" p={seta} />
        <Voo f={f} ini={tCol + 22} de={[250, 620]} para={[660, 640]} dur={16} />
        {/* fiscalização */}
        {f >= tFisc - 8 && (
          <g opacity={entre(f, tFisc - 8, 8)}>
            <path d="M 40 1440 L 1040 1440" {...tinta} strokeWidth={4} opacity={0.5} />
            <G x={380} y={1310}>
              <Loja />
            </G>
            <G x={lupaX} y={1240} r={-10}>
              <Lupa />
            </G>
            {ok > 0 && (
              <G x={790} y={1260} s={ok} r={-8}>
                <rect x={-160} y={-80} width={320} height={160} rx={16} fill="none" stroke={COR.vermelho} strokeWidth={10} />
                <text textAnchor="middle" y={28} fontSize={78} fill={COR.vermelho} fontFamily={MAO}>VISTORIA</text>
              </G>
            )}
          </g>
        )}
      </svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 920, opacity: entre(f, tCol + 4, 8)}}>
        <Escrito tam={60}>coleta de lixo</Escrito>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 1475, opacity: entre(f, tFisc, 8)}}>
        <Escrito tam={60}>ou fiscalização</Escrito>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- 5. CONTRIBUIÇÃO DE MELHORIA ---------- */
export const CenaMelhoria: React.FC<{b: Bloco}> = ({b}) => {
  const f = useCurrentFrame();
  const tObra = quando(b, 'obra');
  const tVal = quando(b, 'valoriza');
  const asfalto = entre(f, tObra - 2, 22);
  const cone = pop(f, tObra - 6);
  const tag = pop(f, tVal - 2);
  const sobe = entre(f, tVal + 4, 18);
  return (
    <AbsoluteFill>
      <Titulo texto={'Contribuição de melhoria'} cor={COR.salvia} f={f} tam={78} />
      <svg width={W} height={1920} style={{position: 'absolute', inset: 0}}>
        <DefsSeta />
        {/* rua de terra → asfalto */}
        <path d="M 0 1180 Q 540 1150 1080 1185 L 1080 1330 Q 540 1300 0 1335 Z" fill="#C9AE85" {...tinta} strokeWidth={4} />
        {[120, 330, 560, 790, 980].map((x) => (
          <circle key={x} cx={x} cy={1255 + (x % 3) * 12} r={7} fill={COR.tinta} opacity={0.35} />
        ))}
        <clipPath id="asf">
          <rect x={0} y={1100} width={W * asfalto} height={300} />
        </clipPath>
        <g clipPath="url(#asf)">
          <path d="M 0 1180 Q 540 1150 1080 1185 L 1080 1330 Q 540 1300 0 1335 Z" fill="#6B6762" {...tinta} strokeWidth={4} />
          {[60, 300, 540, 780, 1020].map((x) => (
            <rect key={x} x={x - 60} y={1248} width={120} height={14} rx={6} fill={COR.mostarda} />
          ))}
        </g>
        <G x={540} y={830} s={1.35}>
          <Casa cor={COR.laranja} />
        </G>
        {cone > 0 && (
          <>
            <G x={150} y={1090} s={cone * 0.8}><Cone /></G>
            <G x={930} y={1090} s={cone * 0.8}><Cone /></G>
          </>
        )}
        {tag > 0 && (
          <G x={830} y={600} s={tag} r={10}>
            <path d="M -110 -60 L 80 -60 L 130 0 L 80 60 L -110 60 Z" fill={COR.mostarda} {...tinta} />
            <circle cx={88} cy={0} r={10} fill={COR.papel} {...tinta} strokeWidth={3} />
            <text x={-15} y={22} textAnchor="middle" fontSize={64} fill={COR.tinta} fontFamily={MAO}>$$$</text>
          </G>
        )}
        {sobe > 0 && <Seta d="M 830 470 L 830 300" p={sobe} cor={COR.vermelho} />}
        <Voo f={f} ini={tVal + 18} de={[560, 760]} para={[930, 1050]} dur={16} />
      </svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 1360, opacity: entre(f, tObra, 8)}}>
        <Escrito tam={62}>obra pública</Escrito>
      </div>
      <div style={{position: 'absolute', left: 560, top: 220, width: 500, opacity: entre(f, tVal + 6, 8)}}>
        <Escrito tam={62} cor={COR.vermelho}>imóvel valoriza</Escrito>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- 6. FECHO (parte de baixo da tela dividida) ---------- */
export const CenaFecho: React.FC<{b: Bloco}> = ({b}) => {
  const f = useCurrentFrame();
  const cols = [
    {t: quando(b, 'imposto'), nome: 'Imposto', sub: 'geral', cor: COR.mostarda, el: <Cofre />, s: 0.5},
    {t: quando(b, 'taxa'), nome: 'Taxa', sub: 'serviço', cor: COR.tealClaro, el: <Caminhao />, s: 0.55},
    {t: quando(b, 'melhoria'), nome: 'Melhoria', sub: 'obra', cor: COR.salvia, el: <Cone />, s: 0.95},
  ];
  const tSalva = quando(b, 'salva');
  const enc = entre(f, tSalva - 4, 12);
  const marc = pop(f, tSalva);
  return (
    <AbsoluteFill>
      {cols.map((c, i) => {
        const p = pop(f, c.t - 3, 14);
        return (
          <div key={i} style={{position: 'absolute', left: 40 + i * 340, top: 60 - enc * 20, width: 320, height: 520,
            transform: `scale(${p * (1 - enc * 0.12)}) rotate(${(i - 1) * 2}deg)`, background: c.cor,
            border: `6px solid ${COR.tinta}`, borderRadius: 22, display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: 22}}>
            <Escrito tam={64}>{c.nome}</Escrito>
            <svg width={300} height={250}>
              <G x={150} y={130} s={c.s}>{c.el}</G>
            </svg>
            <Escrito tam={30} style={{opacity: 0.6}}>paga</Escrito>
            <Escrito tam={60} cor={COR.vermelho}>{c.sub}</Escrito>
          </div>
        );
      })}
      {marc > 0 && (
        <div style={{position: 'absolute', left: 0, right: 0, top: 560, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 20, transform: `scale(${marc})`}}>
          <svg width={160} height={230}>
            <G x={80} y={115}><Marcador /></G>
          </svg>
          <Escrito tam={80} cor={COR.vermelho}>salva este</Escrito>
        </div>
      )}
    </AbsoluteFill>
  );
};
