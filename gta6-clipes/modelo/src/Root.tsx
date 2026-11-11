import React from 'react';
import {Composition} from 'remotion';
import {Corte, Dados} from './Corte';
import padrao from './corte.json';

// Cada corte é um JSON de props: npx remotion render src/index.ts Corte saida.mp4 --props=cortes/x.json
export const Root: React.FC = () => (
  <Composition
    id="Corte"
    component={Corte}
    width={1080}
    height={1920}
    fps={30}
    durationInFrames={Math.round(padrao.duracao * 30)}
    defaultProps={{dados: padrao as Dados}}
    calculateMetadata={({props}) => ({durationInFrames: Math.round(props.dados.duracao * 30)})}
  />
);
