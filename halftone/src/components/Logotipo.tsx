import React from 'react';
import {marca} from '../../marca/marca';
import {fontes} from '../theme/fontes';

// HALFT●NE em Archivo Black, com o "O" trocado por um ponto vermelho.
export const Logotipo: React.FC<{altura: number; cor?: string; escalaPonto?: number}> = ({
  altura,
  cor = marca.cores.papel,
  escalaPonto = 1,
}) => {
  const ponto = altura * 0.74 * escalaPonto;
  const estilo: React.CSSProperties = {fontFamily: fontes.marca, fontSize: altura, lineHeight: 1, color: cor};
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: altura * 0.03, letterSpacing: altura * 0.01}}>
      <span style={estilo}>HALFT</span>
      <span
        style={{
          width: ponto,
          height: ponto,
          borderRadius: '50%',
          background: marca.cores.vermelho,
          display: 'inline-block',
          margin: `0 ${altura * 0.04}px`,
        }}
      />
      <span style={estilo}>NE</span>
    </div>
  );
};
