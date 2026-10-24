import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {marca} from '../../marca/marca';
import {fontes} from '../theme/fontes';
import {SEGURA} from '../theme/layout';

// A imagem congela 1,5–2 s com escurecimento (forte o bastante para ler A/B sobre qualquer placa), aparecem A e B,
// e o narrador pergunta: "Nessa situação, o que você faria?" (bíblia, seção 7.2).
// O congelamento em si é feito no Episodio, com <Freeze>.
export const MomentoDecisao: React.FC<{pergunta: string; opcoes: {A: string; B: string}; corSessao: string}> = ({
  pergunta,
  opcoes,
  corSessao,
}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const escuro = interpolate(frame, [0, 4], [0, 0.78], {extrapolateRight: 'clamp'});
  const entra = (atraso: number) => interpolate(frame, [atraso, atraso + 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const barra = interpolate(frame, [0, durationInFrames], [1, 0], {extrapolateRight: 'clamp'});
  const opcao = (letra: 'A' | 'B', texto: string, atraso: number) => (
    <div
      style={{
        opacity: entra(atraso),
        transform: `translateY(${(1 - entra(atraso)) * 24}px)`,
        display: 'flex',
        alignItems: 'center',
        gap: 26,
        background: `${marca.cores.preto}d9`,
        border: `2px solid ${marca.cores.papel}40`,
        borderRadius: 14,
        padding: '26px 30px',
        width: 760,
      }}
    >
      <span style={{fontFamily: fontes.titulo, fontSize: 80, lineHeight: 1, color: corSessao}}>{letra}</span>
      <span style={{fontFamily: fontes.texto, fontWeight: 600, fontSize: 44, color: marca.cores.papel}}>{texto}</span>
    </div>
  );
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{background: marca.cores.preto, opacity: escuro}} />
      <AbsoluteFill style={{alignItems: 'center', paddingTop: 520, paddingRight: 1080 - SEGURA.direita - 40, gap: 34}}>
        <div style={{fontFamily: fontes.mono, fontSize: 26, letterSpacing: 8, color: corSessao, opacity: entra(0)}}>MOMENTO DECISÃO</div>
        <div style={{fontFamily: fontes.titulo, fontSize: 74, lineHeight: 1.1, textAlign: 'center', color: marca.cores.papel, maxWidth: 820, opacity: entra(2)}}>
          {pergunta}
        </div>
        {opcao('A', opcoes.A, 6)}
        {opcao('B', opcoes.B, 9)}
        <div style={{width: 760, height: 6, background: `${marca.cores.papel}22`, marginTop: 12}}>
          <div style={{width: `${barra * 100}%`, height: '100%', background: marca.cores.vermelho}} />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
