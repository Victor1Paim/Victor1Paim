import {Palavra} from '../linha';

export type Modo = 'ela' | 'dividida' | 'motion';
export type Modelo = 'lista' | 'comparacao' | 'numero' | 'passos' | 'definicao' | 'mito';

export type ItemCartao = {tipo: 'item' | 'esquerda' | 'direita' | 'destaque'; texto?: string; icone?: string; cor?: string; ini: number};
export type Trecho = {modo: Modo; modelo: Modelo | null; titulo: string; icone: string | null; ini: number; fim: number; itens: ItemCartao[]};
export type Elemento = {
  tipo: 'icone' | 'etiqueta' | 'numero' | 'carimbo' | 'pergunta' | 'moedas' | 'zoom' | 'seta';
  texto?: string;
  icone?: string;
  cor?: string;
  lugar?: string;
  direcao?: 'cima' | 'baixo';
  ini: number;
  dur: number;
};
export type Dados = {
  nome: string;
  duracao: number;
  video: string;
  palavras: Palavra[];
  trechos: Trecho[];
  elementos: Elemento[];
  legenda: boolean;
  cortes?: number[]; // instantes (s) dos cortes de pausa, já na linha do tempo cortada
  zoomNosCortes?: boolean; // alterna um leve zoom a cada corte (disfarça o salto); padrão true
  enquadramentoDividida?: number; // deslocamento vertical (px) do vídeo na tela dividida; padrão -170
};
