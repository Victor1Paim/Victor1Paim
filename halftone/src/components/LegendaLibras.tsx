import React from 'react';
import {marca} from '../../marca/marca';
import {paleta} from '../../series/ano-zero/paleta';
import {fontes} from '../theme/fontes';

// Caixa com etiqueta LIBRAS, texto em azul, sem voz. Português natural e correto.
export const LegendaLibras: React.FC<{texto: string; personagem?: string; opacidade?: number}> = ({texto, personagem, opacidade = 1}) => (
  <div
    style={{
      opacity: opacidade,
      background: `${marca.cores.preto}e6`,
      border: `2px solid ${paleta.libras}88`,
      borderRadius: 10,
      padding: '18px 24px 22px',
      maxWidth: 820,
    }}
  >
    <div style={{display: 'flex', gap: 14, alignItems: 'center', marginBottom: 8}}>
      <span
        style={{
          fontFamily: fontes.mono,
          fontWeight: 500,
          fontSize: 20,
          letterSpacing: 4,
          color: marca.cores.preto,
          background: paleta.libras,
          padding: '3px 10px',
          borderRadius: 3,
        }}
      >
        LIBRAS
      </span>
      {personagem ? (
        <span style={{fontFamily: fontes.mono, fontSize: 22, letterSpacing: 3, color: paleta.libras}}>{personagem}</span>
      ) : null}
    </div>
    <div style={{fontFamily: fontes.texto, fontWeight: 600, fontSize: 44, lineHeight: 1.25, color: paleta.libras}}>{texto}</div>
  </div>
);
