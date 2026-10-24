import React from 'react';
import {AbsoluteFill} from 'remotion';
import {marca} from '../../marca/marca';
import {SimboloHalftone} from '../components/SimboloHalftone';

// Avatar 1080×1080. `simplificado` = menos pontos, para tamanhos pequenos.
export const Avatar: React.FC<{simplificado: boolean}> = ({simplificado}) => (
  <AbsoluteFill style={{background: marca.cores.preto, alignItems: 'center', justifyContent: 'center'}}>
    <SimboloHalftone tamanho={860} simplificado={simplificado} />
  </AbsoluteFill>
);
