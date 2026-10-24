import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {marca} from '../../marca/marca';
import {paleta, type Sessao} from '../../series/ano-zero/paleta';
import {fontes} from '../theme/fontes';
import type {Legenda as LegendaT} from '../tipos';
import {LegendaLibras} from './LegendaLibras';

const corPersonagem = (personagem: string | undefined, sessao: Sessao) =>
  personagem && personagem in paleta.sessoes ? paleta.sessoes[personagem as Sessao] : paleta.sessoes[sessao];

// Camadas de legenda (bíblia, seção 6.1): narrador, diálogo, pensamento, Libras e sons.
export const Legenda: React.FC<{legenda: LegendaT; sessao: Sessao}> = ({legenda, sessao}) => {
  const frame = useCurrentFrame();
  const op = interpolate(frame, [0, 4], [0, 1], {extrapolateRight: 'clamp'});
  const base: React.CSSProperties = {
    fontFamily: fontes.texto,
    fontSize: 46,
    lineHeight: 1.25,
    textShadow: '0 2px 14px rgba(0,0,0,0.95), 0 0 2px rgba(0,0,0,1)',
    opacity: op,
  };
  const nome = legenda.personagem?.toUpperCase();
  switch (legenda.tipo) {
    case 'libras':
      return <LegendaLibras texto={legenda.texto} personagem={nome} opacidade={op} />;
    case 'narrador':
      return <div style={{...base, fontFamily: fontes.textoItalico, fontStyle: 'italic', color: marca.cores.papel}}>{legenda.texto}</div>;
    case 'pensamento': {
      // Pensamento do Caio: azul, sem voz. Bia e Davi: cor da sessão.
      const cor = legenda.personagem === 'caio' ? paleta.libras : corPersonagem(legenda.personagem, sessao);
      return <div style={{...base, fontFamily: fontes.textoItalico, fontStyle: 'italic', color: cor}}>({legenda.texto})</div>;
    }
    case 'som':
      return (
        <div style={{...base, fontFamily: fontes.mono, fontSize: 32, color: marca.cores.cinza}}>[{legenda.texto}]</div>
      );
    case 'dialogo':
    default:
      return (
        <div style={{...base, color: marca.cores.papel}}>
          {nome ? (
            <span style={{fontWeight: 700, fontSize: 30, letterSpacing: 3, color: corPersonagem(legenda.personagem, sessao), marginRight: 14}}>
              {nome}
            </span>
          ) : null}
          {legenda.texto}
        </div>
      );
  }
};
