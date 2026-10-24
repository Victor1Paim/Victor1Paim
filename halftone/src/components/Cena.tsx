import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig} from 'remotion';
import {marca} from '../../marca/marca';
import {paleta, type Sessao} from '../../series/ano-zero/paleta';
import {fontes} from '../theme/fontes';
import {SEGURA} from '../theme/layout';
import type {Cena as CenaT} from '../tipos';
import {AneisSom} from './AneisSom';
import {Legenda} from './Legenda';
import {LuzCena} from './LuzCena';
import {Nevoa} from './Nevoa';
import {Particulas} from './Particulas';
import {Placa} from './Placa';
import {TelaCelular} from './TelaCelular';
import {TiqueEco} from './TiqueEco';

// Monta as camadas de uma cena: placas → luz → névoa/partículas → anéis → celular → legendas.
export const Cena: React.FC<{cena: CenaT; sessao: Sessao}> = ({cena, sessao}) => {
  const {fps} = useVideoConfig();
  const duracao = cena.fim - cena.inicio;
  // Sessões do Caio: imagem um pouco mais fria (ele não ouve; o público vê os anéis).
  const filtro = sessao === 'caio' ? 'saturate(0.78) brightness(0.94) hue-rotate(-8deg)' : undefined;
  return (
    <AbsoluteFill style={{background: marca.cores.preto, overflow: 'hidden'}}>
      <AbsoluteFill style={{filter: filtro}}>
        {cena.placas.map((placa, i) => {
          const camada = <Placa key={placa + i} placa={placa} profundidade={i} camera={cena.camera} />;
          return cena.tiqueEco?.camada === i ? (
            <TiqueEco key={placa + i} bpm={cena.tiqueEco.bpm}>
              {camada}
            </TiqueEco>
          ) : (
            camada
          );
        })}
        {cena.luz ? <LuzCena tipo={cena.luz.tipo} tremulacao={cena.luz.tremulacao} /> : null}
        {cena.nevoa ? <Nevoa /> : null}
        {cena.particulas ? <Particulas /> : null}
        {sessao === 'caio' ? <AbsoluteFill style={{background: '#4A7FA8', mixBlendMode: 'soft-light', opacity: 0.25}} /> : null}
      </AbsoluteFill>

      {cena.som?.filter((s) => s.aneis).map((s, i) => <AneisSom key={i} x={s.x} y={s.y} bpm={s.bpm} />)}
      {cena.som?.filter((s) => s.arquivo).map((s, i) => (
        // Caio não ouve: nas sessões dele a mixagem é abafada (volume baixo; filtro grave vem na mixagem).
        <Audio key={i} src={staticFile(s.arquivo!)} volume={(s.volume ?? 1) * (sessao === 'caio' ? 0.35 : 1)} loop={s.tipo === 'continuo'} />
      ))}

      {cena.celular ? (
        <Sequence
          from={Math.round((cena.celular.inicio ?? 0) * fps)}
          durationInFrames={Math.max(1, Math.round(((cena.celular.fim ?? duracao) - (cena.celular.inicio ?? 0)) * fps))}
          layout="none"
        >
          <TelaCelular celular={cena.celular} />
        </Sequence>
      ) : null}

      {cena.marcador ? (
        <div
          style={{
            position: 'absolute',
            top: SEGURA.topo + 40,
            left: SEGURA.esquerda,
            fontFamily: fontes.mono,
            fontSize: 26,
            letterSpacing: 6,
            color: paleta.sessoes[sessao],
          }}
        >
          {cena.marcador}
        </div>
      ) : null}

      {/* Legendas acima dos ~20% inferiores e fora da faixa direita dos botões. */}
      {(cena.legendas ?? []).map((l, i) => {
        const ini = l.inicio ?? 0;
        const fim = l.fim ?? duracao;
        return (
          <Sequence key={i} from={Math.round(ini * fps)} durationInFrames={Math.max(1, Math.round((fim - ini) * fps))} layout="none">
            <div
              style={{
                position: 'absolute',
                left: SEGURA.esquerda,
                width: SEGURA.direita - SEGURA.esquerda,
                bottom: 1920 - SEGURA.base,
                display: 'flex',
                justifyContent: 'center',
                textAlign: 'center',
              }}
            >
              <Legenda legenda={l} sessao={sessao} />
            </div>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
