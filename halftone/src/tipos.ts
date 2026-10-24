// Formato do ep.json (plano-mestre, seção 10.3). Tempos em segundos.
import type {Sessao} from '../series/ano-zero/paleta';

export type Beat = 'gancho' | 'desenvolvimento' | 'virada' | 'decisao' | 'final';

export type MovimentoCamera = 'parado' | 'aproximacao' | 'afastamento' | 'panoramica' | 'tremor';

export type TipoLuz = 'poste-sodio' | 'tela-celular' | 'flash-vermelho' | 'palco' | 'fluorescente' | 'nenhuma';

export type TipoLegenda = 'narrador' | 'dialogo' | 'pensamento' | 'libras' | 'som';

export type Legenda = {
  tipo: TipoLegenda;
  texto: string;
  personagem?: string;
  /** Relativo ao início da cena. Padrão: a cena toda. */
  inicio?: number;
  fim?: number;
};

export type Som = {
  tipo: 'padrao' | 'continuo';
  fonte: string;
  /** Desenha anéis vermelhos saindo da fonte. */
  aneis?: boolean;
  /** Posição dos anéis no quadro, de 0 a 1. */
  x?: number;
  y?: number;
  /** Batidas por minuto do padrão (anéis e tique dos ecos seguem esse ritmo). */
  bpm?: number;
  /** Arquivo em public/, opcional enquanto o áudio não existe. */
  arquivo?: string;
  volume?: number;
};

export type Celular = {
  tipo: 'chamada' | 'videochamada' | 'mensagem' | 'alerta' | 'chamada-recusada';
  de?: string;
  texto?: string;
  bateria?: number;
  inicio?: number;
  fim?: number;
};

export type Cena = {
  id: string;
  inicio: number;
  fim: number;
  beat?: Beat;
  /** Ex.: "calcadao-noite/fundo" ou "rafa/pose-ombro". Da primeira (fundo) à última (primeiro plano). */
  placas: string[];
  camera?: {movimento: MovimentoCamera; de?: number; para?: number};
  luz?: {tipo: TipoLuz; tremulacao?: boolean};
  nevoa?: boolean;
  particulas?: boolean;
  som?: Som[];
  legendas?: Legenda[];
  celular?: Celular;
  /** Aplica o tique seco do eco à camada de personagem com este índice. */
  tiqueEco?: {camada: number; bpm?: number};
  /** Hora da história nesta cena (relógio). Padrão: horaInicio do episódio. */
  hora?: string;
  /** Etiqueta curta no canto, ex.: "20 S ANTES". */
  marcador?: string;
};

export type Episodio = {
  serie: string;
  temporada: number;
  episodio: number;
  titulo: string;
  sessao: Sessao;
  horaInicio: string;
  duracaoAlvoSeg: number;
  /** Cartão de sessão no começo (episódio que abre a sessão). */
  cartaoSessao?: boolean;
  rebobina?: boolean;
  /** Quando entra o "Halftone apresenta" (sempre depois do gancho de 0–3 s). */
  apresentaEm?: number;
  cenas: Cena[];
  momentoDecisao?: {
    inicio: number;
    pergunta: string;
    opcoes: {A: string; B: string};
    /** Congelamento, 1,5–2 s. */
    duracao?: number;
  };
  narracao?: {arquivo: string; inicio?: number; volume?: number}[];
  cta: string;
};
