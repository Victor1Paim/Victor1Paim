import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {marca} from '../../marca/marca';
import {Cena} from '../components/Cena';
import {Relogio} from '../components/Relogio';
import {Reticula} from '../components/Reticula';
import {SeloFiccao} from '../components/SeloFiccao';
import {fontes} from '../theme/fontes';
import {paleta} from '../../series/ano-zero/paleta';
import type {Cena as CenaT} from '../tipos';

// Trailer de 01/12 (bíblia, seção 13): 25 s.
const cenas: CenaT[] = [
  {
    id: 't1', inicio: 0, fim: 3, placas: ['areia-palco/fundo', 'multidao-branco/meio'],
    camera: {movimento: 'aproximacao'}, luz: {tipo: 'palco'}, particulas: true,
    som: [{tipo: 'padrao', fonte: 'batida-festa', aneis: true, x: 0.5, y: 0.3, bpm: 120}],
  },
  {
    id: 't2', inicio: 3, fim: 8, placas: ['multidao-branco/fundo', 'ecos/cabecas-virando'],
    camera: {movimento: 'tremor'}, luz: {tipo: 'tela-celular'},
    som: [{tipo: 'padrao', fonte: 'toque-celular', aneis: true, x: 0.5, y: 0.55, bpm: 90}],
    celular: {tipo: 'videochamada', de: 'CAIO', inicio: 0.3},
    legendas: [{tipo: 'som', texto: 'celular tocando'}],
  },
  {
    id: 't3', inicio: 8, fim: 14, placas: ['calcadao-noite/fundo', 'ecos/eco-calcadao', 'bia/lanterna'],
    camera: {movimento: 'aproximacao'}, luz: {tipo: 'poste-sodio', tremulacao: true}, nevoa: true,
    tiqueEco: {camada: 1, bpm: 90},
    som: [{tipo: 'padrao', fonte: 'estalo-mandibula', aneis: true, x: 0.35, y: 0.4, bpm: 90}],
    legendas: [{tipo: 'narrador', texto: 'Todo mundo esperava os fogos.'}],
  },
  {
    id: 't4', inicio: 14, fim: 19, placas: ['beira-mar/fundo', 'beira-mar/sombras'],
    camera: {movimento: 'afastamento'}, luz: {tipo: 'flash-vermelho'}, nevoa: true,
    legendas: [{tipo: 'narrador', texto: 'Ninguém sabia o que eles iam acordar.'}],
  },
];

export const Trailer: React.FC = () => (
  <AbsoluteFill style={{background: marca.cores.preto}}>
    {cenas.map((c) => (
      <Sequence key={c.id} from={c.inicio * 30} durationInFrames={(c.fim - c.inicio) * 30}>
        <Cena cena={c} sessao="bia" />
      </Sequence>
    ))}
    <Sequence from={0} durationInFrames={19 * 30}>
      <Relogio hora="23:00" corSessao={paleta.sessoes.bia} />
    </Sequence>
    <Sequence from={19 * 30}>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', gap: 22, paddingBottom: 200}}>
        <div style={{fontFamily: fontes.mono, fontSize: 28, letterSpacing: 8, color: marca.cores.cinza}}>HALFTONE APRESENTA</div>
        <div style={{fontFamily: fontes.titulo, fontSize: 190, lineHeight: 1, color: marca.cores.papel}}>ANO ZERO</div>
        <div style={{fontFamily: fontes.mono, fontSize: 34, letterSpacing: 6, color: marca.cores.papel}}>A VIRADA</div>
        <div style={{marginTop: 30, fontFamily: fontes.mono, fontSize: 40, letterSpacing: 6, color: marca.cores.vermelho}}>04/12 · 20H</div>
      </AbsoluteFill>
    </Sequence>
    <Reticula />
    <SeloFiccao />
  </AbsoluteFill>
);
