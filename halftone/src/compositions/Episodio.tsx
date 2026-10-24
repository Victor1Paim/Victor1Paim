import React from 'react';
import {AbsoluteFill, Audio, Freeze, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {marca} from '../../marca/marca';
import {paleta} from '../../series/ano-zero/paleta';
import {CartaoSessao} from '../components/CartaoSessao';
import {Cena} from '../components/Cena';
import {CTAFinal} from '../components/CTAFinal';
import {DURACAO_APRESENTA, HalftoneApresenta} from '../components/HalftoneApresenta';
import {MomentoDecisao} from '../components/MomentoDecisao';
import {Rebobina} from '../components/Rebobina';
import {Relogio} from '../components/Relogio';
import {Reticula} from '../components/Reticula';
import {SeloFiccao} from '../components/SeloFiccao';
import type {Episodio as EpisodioT} from '../tipos';

export const NOME_SERIE = 'Ano Zero';
export const NOME_TEMPORADA = 'T1 · A Virada';
const DURACAO_CTA = 2.5;
const DURACAO_CARTAO = 1.5;

// Lê o ep.json e monta o episódio inteiro. Os tempos do ep.json são do vídeo, em segundos.
export const Episodio: React.FC<{ep: EpisodioT}> = ({ep}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const s = (seg: number) => Math.round(seg * fps);
  const cor = paleta.sessoes[ep.sessao];

  const md = ep.momentoDecisao;
  const mdIni = md ? s(md.inicio) : -1;
  const mdDur = md ? s(md.duracao ?? 2) : 0;
  const congelado = md !== undefined && frame >= mdIni && frame < mdIni + mdDur;

  const cenaAtual = ep.cenas.find((c) => frame >= s(c.inicio) && frame < s(c.fim));
  const hora = cenaAtual?.hora ?? ep.horaInicio;

  const apresentaEm = s(ep.apresentaEm ?? 3);
  const cartaoEm = apresentaEm + DURACAO_APRESENTA;
  const rebobinaEm = cartaoEm + (ep.cartaoSessao ? s(DURACAO_CARTAO) : 0);

  const cenas = (
    <AbsoluteFill>
      {ep.cenas.map((c) => (
        <Sequence key={c.id} from={s(c.inicio)} durationInFrames={Math.max(1, s(c.fim) - s(c.inicio))} name={`${c.id} · ${c.beat ?? ''}`}>
          <Cena cena={c} sessao={ep.sessao} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );

  return (
    <AbsoluteFill style={{background: marca.cores.preto}}>
      <Freeze frame={mdIni} active={congelado}>
        {cenas}
      </Freeze>

      {md ? (
        <Sequence from={mdIni} durationInFrames={mdDur} name="Momento Decisão">
          <MomentoDecisao pergunta={md.pergunta} opcoes={md.opcoes} corSessao={cor} />
        </Sequence>
      ) : null}

      <Reticula />
      <Relogio hora={hora} corSessao={cor} />

      <Sequence from={apresentaEm} durationInFrames={DURACAO_APRESENTA} name="Halftone apresenta">
        <HalftoneApresenta serie={NOME_SERIE} temporada={NOME_TEMPORADA} />
      </Sequence>
      {ep.cartaoSessao ? (
        <Sequence from={cartaoEm} durationInFrames={s(DURACAO_CARTAO)} name="Cartão de sessão">
          <CartaoSessao sessao={ep.sessao} hora={ep.horaInicio} />
        </Sequence>
      ) : null}
      {ep.rebobina ? (
        <Sequence from={rebobinaEm} durationInFrames={s(1)} name="Rebobina">
          <Rebobina hora={ep.horaInicio} />
        </Sequence>
      ) : null}

      <Sequence from={durationInFrames - s(DURACAO_CTA)} name="CTA">
        <CTAFinal texto={ep.cta} serie={`${NOME_SERIE} · Ep. ${String(ep.episodio).padStart(2, '0')}`} />
      </Sequence>

      {/* Selo de ficção sempre visível, por cima de tudo. */}
      <SeloFiccao />

      {(ep.narracao ?? []).map((n, i) => (
        <Sequence key={i} from={s(n.inicio ?? 0)} layout="none">
          <Audio src={staticFile(n.arquivo)} volume={n.volume ?? 1} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
