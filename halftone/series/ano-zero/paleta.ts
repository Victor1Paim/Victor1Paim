// Paleta da série (bíblia, seção 9.2).
export const paleta = {
  noite: '#07090D',
  mar: '#0E1A24',
  nevoa: '#2A3640',
  brancoReveillon: '#D9D4C7',
  perigo: '#E0413A', // som, anéis, ecos
  sessoes: {
    bia: '#F2B544',
    caio: '#7FB8D6',
    davi: '#3DDC97',
  },
  // Libras e pensamentos do Caio aparecem em azul (bíblia, seção 6.1).
  libras: '#7FB8D6',
} as const;

export type Sessao = keyof typeof paleta.sessoes;

export const nomeSessao: Record<Sessao, {numero: number; nome: string}> = {
  bia: {numero: 1, nome: 'BIA'},
  caio: {numero: 2, nome: 'CAIO'},
  davi: {numero: 3, nome: 'DAVI'},
};

// Personagens com folha de referência; usado para achar a pasta de cada placa.
export const personagens = [
  'bia', 'caio', 'davi', 'edson', 'lurdes', 'rafa', 'tuca', 'arnaldo', 'ecos',
] as const;
