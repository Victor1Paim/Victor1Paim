#!/usr/bin/env python3
"""Biblioteca de fundos em vídeo (Maldivas) para os Reels: recorta trechos 9:16 do vídeo 'maldivas.mp4' (Drive do usuário,
1 h, 1920x1080). Saída: assets/fundos/maldivas/mNN.mp4 (1080x1920, 30 fps, sem áudio, 10 s) + assets/fundos/maldivas.json.

Uso: python3 scripts/fundos_maldivas.py CAMINHO/maldivas.mp4
Baixar o original: curl -L -o maldivas.mp4 "https://drive.usercontent.google.com/download?id=16Bgp45iGx1SISJJZJ-cyScSmCDLM66GF&export=download&confirm=t"
(os .mp4 cortados ficam fora do git; o json com os tempos fica no git).
"""
import json, subprocess, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
# segundos do original escolhidos no mapa de cenas (sem pessoas): pôr do sol, píer, bangalôs, tartarugas, barcos, coqueiros...
CENAS = {60: "por do sol", 90: "píer", 120: "bangalôs de cima", 210: "tartaruga", 240: "tartaruga 2", 300: "bangalôs na água",
         360: "barco na praia", 480: "recife de cima", 540: "banco de areia com barco", 600: "barco no mar turquesa",
         660: "barco na areia de cima", 720: "praia branca", 780: "passarela dos bangalôs", 900: "coqueiro e bangalô",
         960: "pôr do sol no mar", 1020: "banco de areia com barcos", 1140: "ondas de cima", 1260: "pôr do sol com barco",
         1380: "coqueiros", 1530: "veleiro de cima", 1710: "banco de areia"}


def main(orig):
    out = PROJ / "assets" / "fundos" / "maldivas"; out.mkdir(parents=True, exist_ok=True)
    lista = []
    for i, (t, nome) in enumerate(CENAS.items(), 1):
        arq = out / f"m{i:02d}.mp4"
        if not arq.exists():
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", str(t), "-t", "10", "-i", str(orig), "-an",
                            "-vf", "crop=608:1080,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "21", str(arq)], check=True)
        lista.append({"arquivo": f"assets/fundos/maldivas/{arq.name}", "origem_s": t, "cena": nome})
        print(arq.name, nome, flush=True)
    (PROJ / "assets" / "fundos" / "maldivas.json").write_text(json.dumps(lista, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
