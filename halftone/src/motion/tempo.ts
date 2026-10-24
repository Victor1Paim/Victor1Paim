import timeline from './timeline.json';

// Linha do tempo do teste motion (gerada por scripts/montar-teste-motion.py).
export const TL = timeline;
export const EV = timeline.eventos;

export type Linha = (typeof timeline.linhas)[number];

// Tempo desde a última batida (s) e a força do pulso (1 na batida, cai rápido).
export const ultimaBatida = (t: number) => {
  let ult = -1;
  for (const b of TL.batidas) {
    if (b > t) break;
    ult = b;
  }
  return ult;
};

export const pulso = (t: number, decaimento = 9) => {
  const b = ultimaBatida(t);
  if (b < 0) return 0;
  const d = t - b;
  // sem batida nova há mais de um compasso: música parada
  if (d > 0.75) return 0;
  return Math.exp(-d * decaimento);
};

export const indiceBatida = (t: number) => TL.batidas.filter((b) => b <= t).length;

// Interpolação suave entre dois tempos.
export const rampa = (t: number, a: number, b: number) => {
  const x = Math.min(1, Math.max(0, (t - a) / (b - a)));
  return x * x * (3 - 2 * x);
};

// Ruído determinístico (mesmo valor em cada render).
export const ruido = (n: number) => {
  const a = Math.sin(n * 12.9898) * 43758.5453;
  return a - Math.floor(a) - 0.5;
};
