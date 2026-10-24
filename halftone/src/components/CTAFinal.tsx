import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {marca} from '../../marca/marca';
import {fontes} from '../theme/fontes';
import {SimboloHalftone} from './SimboloHalftone';

// Cartão final: próximo episódio e convite para seguir.
export const CTAFinal: React.FC<{texto: string; serie: string; nota?: string}> = ({texto, serie, nota}) => {
  const frame = useCurrentFrame();
  const op = interpolate(frame, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: `${marca.cores.preto}ee`, alignItems: 'center', justifyContent: 'center', opacity: op, paddingBottom: 200}}>
      <SimboloHalftone tamanho={160} />
      <div style={{marginTop: 40, fontFamily: fontes.mono, fontSize: 26, letterSpacing: 8, color: marca.cores.cinza}}>{serie.toUpperCase()}</div>
      <div style={{marginTop: 16, fontFamily: fontes.titulo, fontSize: 96, color: marca.cores.papel, textAlign: 'center', maxWidth: 860}}>
        {texto}
      </div>
      <div style={{marginTop: 30, fontFamily: fontes.mono, fontSize: 30, letterSpacing: 4, color: marca.cores.vermelho}}>
        ● SIGA {marca.handle.toUpperCase()}
      </div>
      {nota ? (
        <div style={{marginTop: 26, fontFamily: fontes.mono, fontSize: 24, letterSpacing: 4, color: marca.cores.cinza}}>{nota}</div>
      ) : null}
    </AbsoluteFill>
  );
};
