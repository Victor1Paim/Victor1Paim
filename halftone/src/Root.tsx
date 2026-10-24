import React from 'react';
import {Composition, Still} from 'remotion';
import ep01 from '../series/ano-zero/t1/ep01/ep.json';
import testeTecnico from '../series/ano-zero/t1/teste-tecnico/ep.json';
import {marca} from '../marca/marca';
import {paleta} from '../series/ano-zero/paleta';
import {Avatar} from './compositions/Avatar';
import {Capa} from './compositions/Capa';
import {DestaqueIG} from './compositions/DestaqueIG';
import {Episodio} from './compositions/Episodio';
import {Trailer} from './compositions/Trailer';
import {DURACAO_TESTE_MOTION, TesteMotion} from './motion/TesteMotion';
import {DURACAO_TESTE_LAYOUT, TesteLayout} from './estilo2/TesteLayout';
import {DURACAO_EP01, Ep01} from './ep01/Ep01';
import {QUADRO} from './theme/layout';
import type {Episodio as EpisodioT} from './tipos';

// Cada episódio novo entra nesta lista.
const episodios: {id: string; ep: EpisodioT}[] = [
  {id: 'AnoZero-T1-TesteTecnico', ep: testeTecnico as EpisodioT},
  {id: 'AnoZero-T1-Ep01', ep: ep01 as EpisodioT},
];

const destaques = [
  {id: 'ComeceAqui', titulo: 'Comece aqui', cor: marca.cores.papel},
  {id: 'AnoZero', titulo: 'Ano Zero', cor: paleta.perigo},
  {id: 'Personagens', titulo: 'Perso­nagens', cor: paleta.perigo},
  {id: 'Bastidores', titulo: 'Bastidores', cor: marca.cores.papel},
  {id: 'Teorias', titulo: 'Teorias', cor: marca.cores.papel},
];

export const Root: React.FC = () => (
  <>
    {episodios.map(({id, ep}) => (
      <React.Fragment key={id}>
        <Composition
          id={id}
          component={Episodio}
          width={QUADRO.largura}
          height={QUADRO.altura}
          fps={QUADRO.fps}
          durationInFrames={Math.round(ep.duracaoAlvoSeg * QUADRO.fps)}
          defaultProps={{ep}}
        />
        <Still id={`${id}-Capa`} component={Capa} width={1080} height={1920} defaultProps={{ep, arte: `series/ano-zero/t1/ep${String(ep.episodio).padStart(2, '0')}/capa-arte.png`}} />
      </React.Fragment>
    ))}
    <Composition id="AnoZero-TesteMotion" component={TesteMotion} width={1080} height={1920} fps={30} durationInFrames={DURACAO_TESTE_MOTION} />
    <Composition id="AnoZero-TesteLayout" component={TesteLayout} width={1080} height={1920} fps={30} durationInFrames={DURACAO_TESTE_LAYOUT} />
    <Composition id="AnoZero-T1-Ep01-Motion" component={Ep01} width={1080} height={1920} fps={30} durationInFrames={DURACAO_EP01} />
    <Composition id="AnoZero-Trailer" component={Trailer} width={1080} height={1920} fps={30} durationInFrames={25 * 30} />
    <Still id="Avatar" component={Avatar} width={1080} height={1080} defaultProps={{simplificado: false}} />
    <Still id="Avatar-Simplificado" component={Avatar} width={1080} height={1080} defaultProps={{simplificado: true}} />
    {destaques.map((d) => (
      <Still key={d.id} id={`Destaque-${d.id}`} component={DestaqueIG} width={1080} height={1920} defaultProps={{titulo: d.titulo, cor: d.cor}} />
    ))}
  </>
);
