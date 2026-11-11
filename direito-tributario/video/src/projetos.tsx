import React from 'react';
import {Bloco, Fala} from './linha';
import {Desenho} from './estilo';
import {Apresentador as BonecoSvg} from './Apresentador';
import {ApresentadorImagem} from './ApresentadorImagem';
import * as C1 from './Cenas';
import * as C2 from './CenasIR';
import teste01 from './dados-teste-01.json';
import teste02 from './dados-teste-02.json';

type PropsApresentador = {boca: number; gesto: number; alt: number};
export type Projeto = {
  falas: Fala[];
  cenas: Record<string, React.FC<{b: Bloco}>>;
  Apresentador: React.FC<PropsApresentador>;
  gestos: Record<string, string[]>;
};

export const PROJETOS: Record<string, Projeto> = {
  'teste-01': {
    falas: teste01.falas as Fala[],
    cenas: {
      '01_gancho': C1.CenaGancho, '02_tres': C1.CenaTres, '03_imposto': C1.CenaImposto,
      '04_taxa': C1.CenaTaxa, '05_melhoria': C1.CenaMelhoria, '06_fecho': C1.CenaFecho,
    },
    Apresentador: (p) => <Desenho><BonecoSvg {...p} /></Desenho>,
    gestos: {'01_gancho': ['imposto?', 'não.'], '06_fecho': ['então:', 'salva']},
  },
  'teste-02': {
    falas: teste02.falas as Fala[],
    cenas: {
      '01_gancho': C2.CenaGancho, '02_resposta': C2.CenaResposta, '03_fonte': C2.CenaFonte,
      '04_balanca': C2.CenaBalanca, '05_cta': C2.CenaCta,
    },
    Apresentador: ({boca, alt}) => <ApresentadorImagem pasta="teste-02" boca={boca} alt={alt} />,
    gestos: {},
  },
};
