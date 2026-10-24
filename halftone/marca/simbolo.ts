// Geometria do símbolo: círculo de pontos de retícula que diminuem na diagonal,
// com o ponto vermelho no alto (plano-mestre, seção 4.3). Coordenadas em -1..1.
// Sem imports: usado pelo componente e pelo script que gera os SVGs.

export type Ponto = {x: number; y: number; r: number; ordem: number};

export const PONTO_VERMELHO = {x: 0.5, y: -0.55};

export const pontosSimbolo = (simplificado = false): Ponto[] => {
  const passo = simplificado ? 0.16 : 0.085;
  const pontos: Ponto[] = [];
  for (let gy = -1; gy <= 1.0001; gy += passo * 0.866) {
    const linha = Math.round((gy + 1) / (passo * 0.866));
    for (let gx = -1; gx <= 1.0001; gx += passo) {
      const x = gx + (linha % 2 ? passo / 2 : 0);
      const y = gy;
      if (x * x + y * y > 0.98) continue;
      // t = 0 embaixo à esquerda (pontos cheios), 1 em cima à direita (pontos finos)
      const t = Math.min(1, Math.max(0, (x - y) / (2 * Math.SQRT2) + 0.5));
      const r = (passo / 2) * 0.92 * Math.pow(1 - t, 1.15);
      if (r < passo * 0.04) continue;
      // abre espaço para o ponto vermelho
      if (Math.hypot(x - PONTO_VERMELHO.x, y - PONTO_VERMELHO.y) < 0.2) continue;
      pontos.push({x, y, r, ordem: (y + 1) / 2});
    }
  }
  return pontos;
};

export const raioVermelho = (simplificado = false) => (simplificado ? 0.13 : 0.075);
