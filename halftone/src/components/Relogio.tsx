import React from 'react';
import {marca} from '../../marca/marca';
import {fontes} from '../theme/fontes';
import {SEGURA} from '../theme/layout';

export const faltamMin = (hora: string) => {
  const [h, m] = hora.split(':').map(Number);
  const total = h * 60 + m;
  return total === 0 ? 0 : 24 * 60 - total;
};

// HUD do relógio, sempre visível no canto: "23:10 · FALTAM 50 MIN".
export const Relogio: React.FC<{hora: string; corSessao: string}> = ({hora, corSessao}) => {
  const faltam = faltamMin(hora);
  return (
    <div
      style={{
        position: 'absolute',
        top: SEGURA.topo - 70,
        right: 1080 - SEGURA.direita,
        textAlign: 'right',
        fontFamily: fontes.mono,
        color: marca.cores.papel,
        textShadow: '0 2px 12px rgba(0,0,0,0.8)',
      }}
    >
      <div style={{fontSize: 46, fontWeight: 500, letterSpacing: 2}}>{hora}</div>
      <div style={{fontSize: 20, letterSpacing: 4, color: corSessao}}>
        {faltam === 0 ? 'VIRADA' : `FALTAM ${faltam} MIN`}
      </div>
    </div>
  );
};
