import React from 'react';
import {useCurrentFrame} from 'remotion';
import {COR, FPS, MAO, entre, mola} from './estilo';
import {Fala, Palavra} from './linha';

const DESTAQUE = /^(imposto|taxa|melhoria|contribuição|tributo|caixa|geral|serviço|obra|não|lei|imóvel|fiscalização|salva)/i;

const agrupar = (ps: Palavra[]) => {
  const grupos: Palavra[][] = [];
  let g: Palavra[] = [];
  ps.forEach((p, i) => {
    g.push(p);
    const fimFrase = /[.,:?!]$/.test(p.t);
    const proxPausa = ps[i + 1] && ps[i + 1].ini - p.fim > 0.35;
    if (g.length >= 4 || fimFrase || proxPausa || i === ps.length - 1) {
      grupos.push(g);
      g = [];
    }
  });
  return grupos;
};

// Legenda queimada, manuscrita, 1 grupo curto por vez; palavra-chave em vermelho.
export const Legenda: React.FC<{fala: Fala; y: number}> = ({fala, y}) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const grupos = agrupar(fala.palavras);
  const atual = grupos.find((g, i) => t >= g[0].ini - 0.05 && (i === grupos.length - 1 || t < grupos[i + 1][0].ini - 0.05));
  if (!atual || t > atual[atual.length - 1].fim + 0.6) return null;
  const ini = Math.round(atual[0].ini * FPS);
  const s = entre(f, ini - 2, 6, 0.85, 1, mola);
  return (
    <div
      style={{
        position: 'absolute',
        left: 60,
        right: 60,
        top: y,
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        gap: '0 22px',
        transform: `scale(${s})`,
        fontFamily: MAO,
        fontSize: 76,
        lineHeight: 1.08,
        textTransform: 'uppercase',
        letterSpacing: 2,
      }}
    >
      {atual.map((p, i) => {
        const falada = t >= p.ini - 0.03;
        const chave = DESTAQUE.test(p.t);
        return (
          <span
            key={i}
            style={{
              color: chave ? COR.vermelho : COR.tinta,
              opacity: falada ? 1 : 0.28,
              WebkitTextStroke: `10px ${COR.papel}`,
              paintOrder: 'stroke fill',
            }}
          >
            {p.t}
          </span>
        );
      })}
    </div>
  );
};
