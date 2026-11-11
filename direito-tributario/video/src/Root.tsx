import React from 'react';
import {Composition} from 'remotion';
import {Video} from './Video';
import {FPS, H, W} from './estilo';
import {Fala, montarLinha} from './linha';
import teste01 from './dados-teste-01.json';

const falas01 = teste01.falas as Fala[];

export const Root: React.FC = () => (
  <>
    <Composition
      id="teste-01"
      component={Video}
      durationInFrames={montarLinha(falas01).total}
      fps={FPS}
      width={W}
      height={H}
      defaultProps={{falas: falas01}}
    />
  </>
);
