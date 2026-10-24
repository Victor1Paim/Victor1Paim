import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {marca} from '../../marca/marca';
import {fontes} from '../theme/fontes';
import {SimboloHalftone} from './SimboloHalftone';

// Cartão de abertura do canal: no máximo 1 s, sempre depois do gancho.
export const DURACAO_APRESENTA = 30;

export const HalftoneApresenta: React.FC<{serie: string; temporada?: string}> = ({serie, temporada}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const fim = Math.min(durationInFrames, DURACAO_APRESENTA);
  const revelar = interpolate(frame, [0, fim * 0.45], [0, 1], {extrapolateRight: 'clamp'});
  const saida = interpolate(frame, [fim - 5, fim], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const texto = interpolate(frame, [4, 12], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: marca.cores.preto, alignItems: 'center', justifyContent: 'center', opacity: saida}}>
      <SimboloHalftone tamanho={300} revelar={revelar} />
      <div
        style={{
          marginTop: 48,
          fontFamily: fontes.mono,
          fontSize: 30,
          letterSpacing: 10,
          color: marca.cores.cinza,
          opacity: texto,
        }}
      >
        HALFTONE APRESENTA
      </div>
      <div
        style={{
          marginTop: 18,
          fontFamily: fontes.titulo,
          fontSize: 120,
          color: marca.cores.papel,
          opacity: texto,
          transform: `translateY(${(1 - texto) * 20}px)`,
        }}
      >
        {serie.toUpperCase()}
      </div>
      {temporada ? (
        <div style={{fontFamily: fontes.mono, fontSize: 26, letterSpacing: 6, color: marca.cores.papel, opacity: texto * 0.8}}>
          {temporada.toUpperCase()}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
