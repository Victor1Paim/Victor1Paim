import React from 'react';
import {marca} from '../../marca/marca';
import {paleta} from '../../series/ano-zero/paleta';
import {LegendaLibras} from '../components/LegendaLibras';
import {fontes} from '../theme/fontes';
import {SEGURA} from '../theme/layout';
import {TL} from './tempo';

// Legenda palavra por palavra: a palavra acende quando é dita.
// Narrador em itálico papel; diálogo com o nome na cor do personagem; Libras em caixa azul.

const COR: Record<string, string> = {
  bia: paleta.sessoes.bia,
  bia_pensa: paleta.sessoes.bia,
  rafa: '#C9B8F0',
  ambulante: '#9FC7A8',
  multidao: '#9FC7A8',
};

const NOME: Record<string, string> = {multidao: 'VOZ NA MULTIDÃO'};

type Palavra = {w: string; t0: number; t1: number};
type LinhaLeg = {quem: string; inicio: number; duracao: number; palavras: Palavra[]};
type LibrasLeg = {quem: string; texto: string; inicio: number; duracao: number};

export const LegendaKaraoke: React.FC<{t: number; linhas?: LinhaLeg[]; libras?: LibrasLeg[]}> = ({t, linhas: ls = TL.linhas, libras: lb = TL.libras}) => {
  const linha = ls.find((l) => t >= l.inicio && t < l.inicio + l.duracao + 0.35);
  const libras = lb.find((l) => t >= l.inicio && t < l.inicio + l.duracao);
  const caixa: React.CSSProperties = {
    position: 'absolute',
    left: SEGURA.esquerda,
    width: SEGURA.direita - SEGURA.esquerda,
    bottom: 1920 - SEGURA.base + 30,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    textAlign: 'center',
  };
  if (libras && !linha) {
    return (
      <div style={caixa}>
        <LegendaLibras texto={libras.texto} personagem={libras.quem.toUpperCase()} />
      </div>
    );
  }
  if (!linha) return null;
  const local = t - linha.inicio;
  const pensa = linha.quem.endsWith('_pensa');
  const narrador = linha.quem === 'narrador' || pensa;
  return (
    <div style={caixa}>
      {pensa ? (
        <div style={{fontFamily: fontes.mono, fontWeight: 500, fontSize: 26, letterSpacing: 4, color: COR[linha.quem] ?? marca.cores.papel, marginBottom: 8, textShadow: '0 2px 10px #000'}}>
          {linha.quem.replace('_pensa', '').toUpperCase()} · PENSAMENTO
        </div>
      ) : null}
      {!narrador ? (
        <div style={{fontFamily: fontes.mono, fontWeight: 500, fontSize: 30, letterSpacing: 4, color: COR[linha.quem] ?? marca.cores.papel, marginBottom: 8, textShadow: '0 2px 10px #000'}}>
          {NOME[linha.quem] ?? linha.quem.toUpperCase()}
        </div>
      ) : null}
      <div
        style={{
          fontFamily: fontes.texto,
          fontStyle: narrador ? 'italic' : 'normal',
          fontWeight: narrador ? 600 : 700,
          fontSize: narrador ? 50 : 58,
          lineHeight: 1.25,
          maxWidth: 860,
          textShadow: '0 3px 16px rgba(0,0,0,0.95), 0 0 3px #000',
          background: 'rgba(7,9,13,0.62)',
          borderRadius: 14,
          padding: '10px 18px 12px',
        }}
      >
        {linha.palavras.map((p, i) => {
          const dita = local >= p.t0;
          const agora = local >= p.t0 && local < p.t1 + 0.05;
          return (
            <span
              key={i}
              style={{
                color: pensa ? COR[linha.quem] : agora && !narrador ? (COR[linha.quem] ?? marca.cores.papel) : marca.cores.papel,
                opacity: dita ? 1 : 0.32,
                marginRight: '0.28em',
                display: 'inline-block',
              }}
            >
              {p.w}
            </span>
          );
        })}
      </div>
    </div>
  );
};
