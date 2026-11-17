import React from 'react';
import { Composition } from 'remotion';
import { Reel, DURACAO } from './Reel';
import { Divulgacao, DURACAO_DIVULGACAO } from './Divulgacao';

export const Root: React.FC = () => (
  <>
    <Composition id="Reel" component={Reel} durationInFrames={DURACAO} fps={30} width={1080} height={1920} />
    <Composition id="Divulgacao" component={Divulgacao} durationInFrames={DURACAO_DIVULGACAO} fps={30} width={1080} height={1920} />
  </>
);
