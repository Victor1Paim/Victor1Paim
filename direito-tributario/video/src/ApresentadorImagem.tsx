import React from 'react';
import {Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {W} from './estilo';

// Apresentador a partir de uma ilustração (gpt-image-2) + remendos de boca aberta e olhos fechados.
// alt = altura do painel (1920 tela cheia, 768 tela dividida). Rosto em (512, 540) na imagem 1024×1536.
const BOCA = {x: 430, y: 515, w: 165, h: 105};
const OLHOS = {x: 380, y: 415, w: 270, h: 100};

export const ApresentadorImagem: React.FC<{pasta: string; boca: number; alt: number; zoom?: number}> = ({pasta, boca, alt, zoom = 1}) => {
  const f = useCurrentFrame();
  const t = interpolate(alt, [768, 1920], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const s = interpolate(t, [0, 1], [1.2, 1.38]) * zoom * (1 + boca * 0.006);
  const rostoY = interpolate(t, [0, 1], [395, 700]);
  const tx = W / 2 - 512 * s;
  const ty = rostoY - 540 * s + Math.sin(f / 23) * 4;
  const pisca = f % 110 >= 104;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1024, height: 1536, transformOrigin: '0 0',
      transform: `translate(${tx}px, ${ty}px) scale(${s}) rotate(${Math.sin(f / 37) * 0.4}deg)`}}>
      <Img src={staticFile(`${pasta}/apresentador.jpg`)} style={{position: 'absolute', inset: 0}} />
      <Img src={staticFile(`${pasta}/boca.png`)}
        style={{position: 'absolute', left: BOCA.x, top: BOCA.y, width: BOCA.w, height: BOCA.h, opacity: Math.min(1, boca * 1.7)}} />
      {pisca && <Img src={staticFile(`${pasta}/olhos.png`)} style={{position: 'absolute', left: OLHOS.x, top: OLHOS.y, width: OLHOS.w, height: OLHOS.h}} />}
    </div>
  );
};
