import React from 'react';
import {Composition} from 'remotion';
import {Video} from './Video';
import {FPS, H, W} from './estilo';
import {montarLinha} from './linha';
import {PROJETOS} from './projetos';
import {Kit, calcularKit} from './kit/Kit';
import {DURACAO_DEMO, GravacaoDemo} from './GravacaoDemo';

export const Root: React.FC = () => (
  <>
    {/* Kit: gravação + elementos flutuantes. Props {nome}; vazio = último vídeo preparado. */}
    <Composition id="kit" component={Kit} durationInFrames={300} fps={FPS} width={W} height={H}
      defaultProps={{nome: ''}} calculateMetadata={calcularKit} />
    <Composition id="gravacao-demo" component={GravacaoDemo} durationInFrames={DURACAO_DEMO} fps={FPS} width={W} height={H} />
    {Object.entries(PROJETOS).map(([id, p]) => (
      <Composition key={id} id={id} component={Video} durationInFrames={montarLinha(p.falas).total}
        fps={FPS} width={W} height={H} defaultProps={{id}} />
    ))}
  </>
);
