import React from 'react';
import {marca} from '../../marca/marca';
import {fontes} from '../theme/fontes';
import {SEGURA} from '../theme/layout';

// Selo do topo, sempre visível no vídeo. Padrão "FICÇÃO · HALFTONE" (na capa, só "FICÇÃO");
// `texto` troca por um rótulo da série, ex.: "DIA 1 · DA INFECÇÃO".
export const SeloFiccao: React.FC<{capa?: boolean; texto?: string}> = ({capa, texto}) => (
  <div
    style={{
      position: 'absolute',
      top: SEGURA.topo - 70,
      left: SEGURA.esquerda,
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      fontFamily: fontes.mono,
      fontWeight: 500,
      fontSize: capa ? 30 : 24,
      letterSpacing: 4,
      color: marca.cores.papel,
      opacity: 0.85,
      padding: '8px 14px',
      border: `1.5px solid ${marca.cores.papel}55`,
      borderRadius: 4,
      background: `${marca.cores.preto}88`,
    }}
  >
    <span style={{width: 10, height: 10, borderRadius: '50%', background: marca.cores.vermelho}} />
    {texto ?? (capa ? 'FICÇÃO' : 'FICÇÃO · HALFTONE')}
  </div>
);
