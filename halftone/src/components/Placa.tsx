import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import placasExistentes from '../gerado/placas.json';
import {marca} from '../../marca/marca';
import {personagens} from '../../series/ano-zero/paleta';
import {fontes} from '../theme/fontes';
import type {MovimentoCamera} from '../tipos';

const existentes = new Set<string>(placasExistentes as string[]);

// "rafa/pose-ombro" → series/ano-zero/personagens/rafa/pose-ombro.png
// "calcadao-noite/fundo" → series/ano-zero/cenarios/calcadao-noite/fundo.png
export const caminhoPlaca = (placa: string, serie = 'ano-zero') => {
  const pasta = (personagens as readonly string[]).includes(placa.split('/')[0]) ? 'personagens' : 'cenarios';
  return `series/${serie}/${pasta}/${placa}.png`;
};

const Rascunho: React.FC<{placa: string; profundidade: number}> = ({placa, profundidade}) => {
  const personagem = (personagens as readonly string[]).includes(placa.split('/')[0]);
  if (!personagem && profundidade === 0) {
    return (
      <AbsoluteFill style={{background: `linear-gradient(180deg, #0B1220 0%, ${marca.cores.preto} 55%, #1A1408 100%)`}}>
        <div style={{position: 'absolute', top: 260, left: 64, fontFamily: fontes.mono, fontSize: 22, color: marca.cores.cinza, opacity: 0.6}}>
          [placa pendente] {placa}
        </div>
      </AbsoluteFill>
    );
  }
  // Silhueta simples para personagens e camadas do meio enquanto a arte não existe.
  const x = 540 + (profundidade % 2 ? -160 : 160) * (profundidade > 1 ? 1 : 0);
  return (
    <AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          left: x - 170,
          top: 760,
          width: 340,
          height: 900,
          borderRadius: '170px 170px 40px 40px',
          background: personagem ? '#1C232B' : '#121820',
          boxShadow: `0 0 0 2px ${marca.cores.cinza}33`,
        }}
      />
      <div style={{position: 'absolute', left: x - 170, top: 1680, width: 340, textAlign: 'center', fontFamily: fontes.mono, fontSize: 20, color: marca.cores.cinza}}>
        [{placa}]
      </div>
    </AbsoluteFill>
  );
};

// Uma camada de imagem com parallax e câmera. Profundidade 0 = fundo (mexe menos).
export const Placa: React.FC<{
  placa: string;
  profundidade: number;
  camera?: {movimento: MovimentoCamera; de?: number; para?: number};
  estilo?: React.CSSProperties;
}> = ({placa, profundidade, camera, estilo}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const t = interpolate(frame, [0, Math.max(1, durationInFrames - 1)], [0, 1], {extrapolateRight: 'clamp'});
  const fator = 1 + profundidade * 0.35;
  const mov = camera?.movimento ?? 'parado';
  const de = camera?.de ?? 1;
  const para = camera?.para ?? (mov === 'aproximacao' ? 1.08 : mov === 'afastamento' ? 0.94 : 1);
  const escalaBase = de + (para - de) * t;
  const escala = 1 + (escalaBase - 1) * fator + 0.04; // margem para o parallax não mostrar bordas
  const panX = mov === 'panoramica' ? interpolate(t, [0, 1], [30, -30]) * fator : 0;
  const tremor = mov === 'tremor' ? Math.sin(frame * 1.7) * 6 * fator : 0;
  const caminho = caminhoPlaca(placa);
  return (
    <AbsoluteFill style={{transform: `translate(${panX + tremor}px, ${tremor * 0.6}px) scale(${escala})`, ...estilo}}>
      {existentes.has(caminho) ? (
        <Img src={staticFile(caminho)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      ) : (
        <Rascunho placa={placa} profundidade={profundidade} />
      )}
    </AbsoluteFill>
  );
};
