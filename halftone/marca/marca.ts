// Identidade do canal (plano-mestre, seção 4). Vale para todas as séries.
export const marca = {
  nome: 'Halftone',
  nomePerfil: 'Halftone • Séries',
  handle: '@halftone.tv1',
  tagline: 'Séries em capítulos. Seg, qua e sex às 20h.',
  cores: {
    preto: '#07090D',
    papel: '#EDE6D6',
    cinza: '#8A949C',
    // O "gravando" da Halftone. No logo, é o "O".
    vermelho: '#E0413A',
  },
  fontes: {
    titulo: 'Anton', // títulos da série
    marca: 'Archivo Black', // logotipo
    mono: 'IBM Plex Mono', // relógio e interface
    texto: 'Inter', // legendas
  },
} as const;

export type CoresMarca = typeof marca.cores;
