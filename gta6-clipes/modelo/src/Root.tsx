import React from 'react';
import {Composition} from 'remotion';
import {Corte} from './Corte';
import dados from './corte.json';

export const Root: React.FC = () => (
  <Composition
    id="Corte"
    component={Corte}
    width={1080}
    height={1920}
    fps={30}
    durationInFrames={Math.round(dados.duracao * 30)}
    defaultProps={{dados}}
  />
);
