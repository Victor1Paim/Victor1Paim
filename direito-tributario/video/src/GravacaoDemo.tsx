import React from 'react';
import {AbsoluteFill, Audio, staticFile, useCurrentFrame} from 'remotion';
import {COR, H} from './estilo';
import {ApresentadorImagem} from './ApresentadorImagem';
import {Fala, volumeEm} from './linha';
import teste03 from './dados-teste-03.json';

// "Gravação" de mentira para testar o kit sem câmera: apresentadora ilustrada (teste-02) + voz do teste-03.
const fala = teste03.falas[0] as Fala;
export const DURACAO_DEMO = Math.ceil(fala.duracao * 30) + 15;

export const GravacaoDemo: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: COR.papelEscuro}}>
      <ApresentadorImagem pasta="teste-02" boca={volumeEm(fala, f)} alt={H} />
      <Audio src={staticFile(fala.audio)} />
    </AbsoluteFill>
  );
};
