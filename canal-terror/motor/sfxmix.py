"""Mistura de efeitos da biblioteca (sfx/) nas produções: trilha (drone, sting, vinheta), ambientes e efeitos por frase.

sfx.json de uma história (na pasta da história) — ganhos em dB RELATIVOS à voz (0 = mesmo volume que a narração):
  {"ambientes": [{"id": "amb-deserto-noite", "de": 1, "ate": 7, "db": -22}],          # de/ate = parágrafos (inclusive)
   "efeitos":   [{"id": "buzina-carro", "frase": "I hit the horn", "n": 1, "db": -10, "desloc": 0.0, "fim": false}]}
"frase" é procurada nas palavras do Whisper (voz/palavras.json); o som cai no início da frase (ou no fim, com "fim": true).
"""
import json, os, re, subprocess
import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIB = os.path.join(RAIZ, 'sfx')
SR = 48000
# Reforço global (o usuário não ouviu os efeitos na 1ª versão, 26/11): somado ao "db" de cada item.
REFORCO_EFEITOS, REFORCO_AMBIENTES = 8.0, 6.0
_cat = None


def _catalogo():
    global _cat
    if _cat is None:
        _cat = {e['id']: e for e in json.load(open(os.path.join(BIB, 'catalogo.json'), encoding='utf-8'))['efeitos']}
    return _cat


def carregar(id_):
    """Som da biblioteca em estéreo 48 kHz, normalizado para RMS 1,0 (0 dB) na parte audível: o ganho de colocar() vira o nível final em dBFS."""
    e = _catalogo()[id_]
    arq = os.path.join(BIB, e['categoria'], id_ + '.mp3')
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', arq, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(float)
    # volume percebido: RMS da janela de 400 ms mais alta (como o "momentary loudness").
    # (1ª versão usava o RMS do trecho > 5% do pico: nos sons curtos isso deixava o efeito 10–20 dB baixo demais.)
    p2 = (x ** 2).mean(1); w = int(0.4 * SR)
    if len(p2) <= w:
        r = np.sqrt(p2.mean())
    else:
        c = np.concatenate([[0], np.cumsum(p2)]); r = np.sqrt(((c[w:] - c[:-w]) / w).max())
    return x / (r + 1e-12)


def em_loop(x, n, xf=0.4):
    """Repete um som em loop até n amostras, com cruzamento curto (por segurança, mesmo nos loops perfeitos)."""
    if len(x) >= n:
        return x[:n].copy()
    k = int(xf * SR); out = x.copy()
    rampa = np.linspace(0, 1, k)[:, None]
    while len(out) < n:
        out[-k:] = out[-k:] * (1 - rampa) + x[:k] * rampa
        out = np.concatenate([out, x[k:]])
    return out[:n]


def _norm(w):
    return re.sub(r"[^a-z0-9']", '', w.lower())


def tempo_frase(palavras, frase, n=1, fim=False):
    alvo = [_norm(w) for w in frase.split() if _norm(w)]
    ws = [_norm(w['word']) for w in palavras]
    achados = [i for i in range(len(ws) - len(alvo) + 1) if ws[i:i + len(alvo)] == alvo]
    if len(achados) < n:
        return None
    i = achados[n - 1]
    return palavras[i + len(alvo) - 1]['end'] if fim else palavras[i]['start']


def momentaneo(x):
    """Maior RMS em 400 ms (dBFS) de um trecho mono ou estéreo."""
    p2 = (x ** 2).mean(1) if x.ndim == 2 else x ** 2
    w = int(0.4 * SR)
    if len(p2) == 0: return -120.0
    if len(p2) <= w: return 10 * np.log10(p2.mean() + 1e-12)
    c = np.concatenate([[0], np.cumsum(p2)])
    return 10 * np.log10(((c[w:] - c[:-w]) / w).max() + 1e-12)


def colocar(trilha, x, t0, db_abs):
    i = int(t0 * SR)
    if i >= len(trilha) or i + len(x) <= 0:
        return
    if i < 0: x, i = x[-i:], 0
    x = x[:len(trilha) - i] * 10 ** (db_abs / 20)
    trilha[i:i + len(x)] += x


def aplicar_historia(trilha, pasta, T0, tempos, voz_db, avisos):
    """Ambientes e efeitos de uma história (sfx.json + voz/palavras.json), com a narração começando em T0."""
    cfg_p = os.path.join(pasta, 'sfx.json')
    if not os.path.exists(cfg_p):
        return 0
    cfg = json.load(open(cfg_p, encoding='utf-8'))
    pal = json.load(open(os.path.join(pasta, 'voz', 'palavras.json')))
    n = 0
    for amb in cfg.get('ambientes', []):
        ini = T0 + tempos[amb['de']]['inicio'] - 0.6
        fim = T0 + (tempos[amb['ate'] + 1]['inicio'] if amb['ate'] + 1 < len(tempos) else tempos[-1]['fim'] + 2.5)
        x = em_loop(carregar(amb['id']), int((fim - ini) * SR))
        f = min(int(1.5 * SR), len(x) // 3); x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
        colocar(trilha, x, ini, voz_db + amb.get('db', -22) + REFORCO_AMBIENTES); n += 1
    for ef in cfg.get('efeitos', []):
        t = tempo_frase(pal, ef['frase'], ef.get('n', 1), ef.get('fim', False))
        if t is None:
            avisos.append(f"{os.path.basename(pasta)}: frase não achada para {ef['id']}: \"{ef['frase']}\""); continue
        t_abs = T0 + t + ef.get('desloc', 0.0)
        # nível pela voz NAQUELE momento (pico de 400 ms entre −0,5 s e +1,5 s), não pela média: assim o efeito aparece
        local = momentaneo(trilha[max(0, int((t_abs - 0.5) * SR)):int((t_abs + 1.5) * SR)])
        ref = local if local > -60 else voz_db
        colocar(trilha, carregar(ef['id']), t_abs, ref + ef.get('db', -10) + REFORCO_EFEITOS); n += 1
    return n
