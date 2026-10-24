import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {marca} from '../../marca/marca';
import {nomeSessao, paleta, type Sessao} from '../../series/ano-zero/paleta';
import {fontes} from '../theme/fontes';

// "SESSÃO 2 · CAIO · 23:05"
export const CartaoSessao: React.FC<{sessao: Sessao; hora: string}> = ({sessao, hora}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const op = interpolate(frame, [0, 5, durationInFrames - 6, durationInFrames], [0, 1, 1, 0], {extrapolateRight: 'clamp'});
  const cor = paleta.sessoes[sessao];
  const {numero, nome} = nomeSessao[sessao];
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', background: `${marca.cores.preto}d0`, opacity: op}}>
      <div style={{width: 120, height: 6, background: cor, marginBottom: 36}} />
      <div style={{fontFamily: fontes.mono, fontSize: 30, letterSpacing: 10, color: marca.cores.cinza}}>SESSÃO {numero}</div>
      <div style={{fontFamily: fontes.titulo, fontSize: 170, lineHeight: 1.1, color: cor}}>{nome}</div>
      <div style={{fontFamily: fontes.mono, fontSize: 40, letterSpacing: 6, color: marca.cores.papel}}>{hora}</div>
    </AbsoluteFill>
  );
};
