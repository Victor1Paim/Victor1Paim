import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {marca} from '../../marca/marca';
import {paleta} from '../../series/ano-zero/paleta';
import {fontes} from '../theme/fontes';
import type {Celular} from '../tipos';

// Chamadas, mensagens e alertas — sempre fictícios e estilizados,
// sem imitar emissora, jornal, operadora ou órgão real.
export const TelaCelular: React.FC<{celular: Celular}> = ({celular}) => {
  const frame = useCurrentFrame();
  const entra = interpolate(frame, [0, 8], [60, 0], {extrapolateRight: 'clamp'});
  const toca = celular.tipo === 'chamada' || celular.tipo === 'videochamada';
  const vibra = toca ? Math.sin(frame * 2.4) * (frame % 30 < 15 ? 4 : 0) : 0;
  const titulo: Record<Celular['tipo'], string> = {
    chamada: 'chamada de voz',
    videochamada: 'videochamada',
    mensagem: 'mensagem',
    alerta: 'alerta',
    'chamada-recusada': 'CHAMADA RECUSADA',
  };
  return (
    <div
      style={{
        position: 'absolute',
        left: 540 - 230 + vibra,
        top: 470 + entra,
        width: 460,
        height: 820,
        borderRadius: 56,
        background: '#0C0F14',
        border: `3px solid ${marca.cores.cinza}66`,
        boxShadow: '0 30px 80px rgba(0,0,0,0.7), 0 0 120px rgba(150,190,255,0.18)',
        padding: 36,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        color: marca.cores.papel,
        fontFamily: fontes.texto,
      }}
    >
      <div style={{alignSelf: 'stretch', display: 'flex', justifyContent: 'space-between', fontFamily: fontes.mono, fontSize: 20, color: marca.cores.cinza}}>
        <span>Réveillon</span>
        <span style={{color: (celular.bateria ?? 100) <= 10 ? paleta.perigo : marca.cores.cinza}}>{celular.bateria ?? 61}%</span>
      </div>
      <div style={{marginTop: 120, fontFamily: fontes.mono, fontSize: 22, letterSpacing: 4, color: celular.tipo === 'chamada-recusada' ? paleta.perigo : marca.cores.cinza}}>
        {titulo[celular.tipo]}
      </div>
      {celular.de ? <div style={{marginTop: 18, fontSize: 64, fontWeight: 700}}>{celular.de}</div> : null}
      {celular.texto ? (
        <div
          style={{
            marginTop: 40,
            alignSelf: 'stretch',
            background: celular.tipo === 'alerta' ? `${paleta.perigo}22` : '#1A2029',
            border: celular.tipo === 'alerta' ? `1.5px solid ${paleta.perigo}88` : 'none',
            borderRadius: 18,
            padding: 22,
            fontSize: 30,
            lineHeight: 1.3,
          }}
        >
          {celular.texto}
        </div>
      ) : null}
      {toca ? (
        <div style={{marginTop: 'auto', marginBottom: 40, display: 'flex', gap: 120}}>
          <div style={{width: 96, height: 96, borderRadius: '50%', background: paleta.perigo}} />
          <div style={{width: 96, height: 96, borderRadius: '50%', background: paleta.sessoes.davi}} />
        </div>
      ) : null}
    </div>
  );
};
