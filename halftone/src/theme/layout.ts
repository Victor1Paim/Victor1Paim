// Áreas seguras 9:16 (plano-mestre, seções 7 e 10.4): nada importante nos ~20% de baixo
// nem na faixa direita dos botões. A capa precisa do essencial no centro 1080×1440.
export const QUADRO = {largura: 1080, altura: 1920, fps: 30};

export const SEGURA = {
  topo: 140,
  esquerda: 64,
  direita: 1080 - 150, // faixa dos botões do TikTok/Reels
  base: 1920 - 384, // ~20% inferiores livres
};

export const CAPA_CENTRO = {topo: 240, altura: 1440};
