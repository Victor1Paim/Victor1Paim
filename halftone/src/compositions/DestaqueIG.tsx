import React from 'react';
import {AbsoluteFill} from 'remotion';
import {marca} from '../../marca/marca';
import {fontes} from '../theme/fontes';

// Capa de destaque do Instagram: borda pontilhada; papel para os do canal, cor da série para os da série.
export const DestaqueIG: React.FC<{titulo: string; cor: string}> = ({titulo, cor}) => {
  const n = 48;
  return (
    <AbsoluteFill style={{background: marca.cores.preto, alignItems: 'center', justifyContent: 'center'}}>
      <svg width={760} height={760} viewBox="-1.2 -1.2 2.4 2.4">
        {Array.from({length: n}, (_, i) => {
          const a = (i / n) * Math.PI * 2;
          return <circle key={i} cx={Math.cos(a)} cy={Math.sin(a)} r={0.035} fill={cor} />;
        })}
        <circle cx={0.62} cy={-0.62} r={0.07} fill={marca.cores.vermelho} />
      </svg>
      <div
        style={{
          position: 'absolute',
          fontFamily: fontes.titulo,
          fontSize: 110,
          lineHeight: 1,
          color: cor,
          textAlign: 'center',
          maxWidth: 560,
          textTransform: 'uppercase',
        }}
      >
        {titulo}
      </div>
    </AbsoluteFill>
  );
};
