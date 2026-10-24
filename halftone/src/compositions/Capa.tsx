import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import placasExistentes from '../gerado/placas.json';
import {marca} from '../../marca/marca';
import {paleta} from '../../series/ano-zero/paleta';
import {Reticula} from '../components/Reticula';
import {SeloFiccao} from '../components/SeloFiccao';
import {fontes} from '../theme/fontes';
import {CAPA_CENTRO} from '../theme/layout';
import type {Episodio} from '../tipos';
import {NOME_SERIE, NOME_TEMPORADA} from './Episodio';

// A IA gera só a arte (capa-arte.png, sem texto); o código aplica o resto (plano-mestre, seção 8).
// Tudo que importa fica no centro 1080×1440 (grid 3:4 do Instagram).
export const Capa: React.FC<{ep: Episodio; arte?: string}> = ({ep, arte}) => {
  const cor = paleta.sessoes[ep.sessao];
  const temArte = arte && (placasExistentes as string[]).includes(arte);
  return (
    <AbsoluteFill style={{background: marca.cores.preto}}>
      {temArte ? <Img src={staticFile(arte!)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /> : null}
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${marca.cores.preto}cc 0%, transparent 30%, transparent 55%, ${marca.cores.preto}f0 85%)`}} />
      <Reticula opacidade={0.12} />
      <AbsoluteFill style={{top: CAPA_CENTRO.topo, height: CAPA_CENTRO.altura, padding: '70px 72px', display: 'flex', flexDirection: 'column'}}>
        <div style={{fontFamily: fontes.mono, fontSize: 28, letterSpacing: 8, color: marca.cores.papel, opacity: 0.85}}>HALFTONE APRESENTA</div>
        <div style={{marginTop: 10, fontFamily: fontes.titulo, fontSize: 64, color: marca.cores.papel}}>
          {NOME_SERIE.toUpperCase()} <span style={{color: marca.cores.cinza, fontSize: 40}}>· {NOME_TEMPORADA.toUpperCase()}</span>
        </div>
        <div style={{marginTop: 'auto', fontFamily: fontes.mono, fontSize: 40, letterSpacing: 6, color: cor}}>
          EP. {String(ep.episodio).padStart(2, '0')}
        </div>
        <div style={{fontFamily: fontes.titulo, fontSize: 210, lineHeight: 0.95, color: marca.cores.papel, textTransform: 'uppercase'}}>{ep.titulo}</div>
        <div style={{marginTop: 26, display: 'flex', alignItems: 'center', gap: 18, fontFamily: fontes.mono, fontSize: 36, color: marca.cores.papel}}>
          <span style={{width: 18, height: 18, borderRadius: '50%', background: marca.cores.vermelho}} />
          {ep.horaInicio}
        </div>
      </AbsoluteFill>
      <SeloFiccao capa />
    </AbsoluteFill>
  );
};
