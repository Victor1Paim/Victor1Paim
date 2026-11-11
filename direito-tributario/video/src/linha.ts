import {FPS} from './estilo';

export type Palavra = {t: string; ini: number; fim: number};
export type Fala = {
  id: string;
  modo: 'dividida' | 'motion';
  texto: string;
  audio: string;
  duracao: number;
  palavras: Palavra[];
  volume: number[];
};
export type Bloco = Fala & {de: number; quadros: number};

const RESPIRO = 8; // quadros de pausa entre falas
const INICIO = 6;
const FIM = 45;

export const montarLinha = (falas: Fala[]) => {
  let t = INICIO;
  const blocos: Bloco[] = falas.map((f, i) => {
    const quadros = Math.ceil(f.duracao * FPS) + (i === falas.length - 1 ? FIM : RESPIRO);
    const b = {...f, de: t, quadros};
    t += quadros;
    return b;
  });
  return {blocos, total: t};
};

const norm = (s: string) => s.toLowerCase().replace(/[^\p{L}\p{N}]/gu, '');

// Quadro (relativo ao início da fala) em que a palavra começa. n = ocorrência (1ª, 2ª...).
export const quando = (b: Fala, palavra: string, n = 1) => {
  let c = 0;
  for (const p of b.palavras) {
    if (norm(p.t) === norm(palavra) && ++c === n) return Math.round(p.ini * FPS);
  }
  throw new Error(`palavra "${palavra}" não está na fala ${b.id}`);
};

// Volume (0..1) da voz no quadro relativo f.
export const volumeEm = (b: Fala, f: number) => b.volume[Math.max(0, Math.min(b.volume.length - 1, f))] ?? 0;
