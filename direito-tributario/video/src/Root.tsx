import React from 'react';
import {Composition} from 'remotion';
import {Video} from './Video';
import {FPS, H, W} from './estilo';
import {montarLinha} from './linha';
import {PROJETOS} from './projetos';

export const Root: React.FC = () => (
  <>
    {Object.entries(PROJETOS).map(([id, p]) => (
      <Composition key={id} id={id} component={Video} durationInFrames={montarLinha(p.falas).total}
        fps={FPS} width={W} height={H} defaultProps={{id}} />
    ))}
  </>
);
