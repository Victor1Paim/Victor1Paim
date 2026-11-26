"""Funções comuns do motor do canal de terror."""
import json, os, re, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # canal-terror/
REPO = os.path.dirname(RAIZ)
GEMINI = os.path.join(REPO, '.claude/skills/gemini-midia/scripts/gemini.mjs')
CHAVE_GEMINI = os.path.expanduser('~/.config/canal-terror/gemini.key')

# Sinais de que a conta ficou sem crédito/cota: param a produção e avisam o usuário.
SEM_CREDITO = re.compile(r'insufficient_quota|billing_hard_limit|PerDay|per_day|PAYMENT_REQUIRED|\b402\b|credit balance', re.I)
# Limite por minuto: esperar e tentar de novo, sem parar a produção.
LIMITE_MINUTO = re.compile(r'\b429\b|rate.?limit|requests_per|RESOURCE_EXHAUSTED|quota', re.I)


class SemCredito(SystemExit):
    pass


def parar_se_sem_credito(servico, texto):
    if SEM_CREDITO.search(texto or ''):
        msg = (f'\n*** {servico}: a API recusou por COTA/CRÉDITO. Produção parada. ***\n'
               f'Resposta: {texto.strip()[:400]}\n'
               f'Avise o usuário para recarregar ou trocar o serviço ({servico}).')
        print(msg, file=sys.stderr)
        raise SemCredito(3)


def esperar_se_limite(texto, tentativa):
    """True se foi limite de ritmo (já esperou); False se é outro erro."""
    import time
    if LIMITE_MINUTO.search(texto or ''):
        espera = 35 + 25 * tentativa
        print(f'  limite de pedidos por minuto; esperando {espera} s', file=sys.stderr)
        time.sleep(espera)
        return True
    return False


def env_gemini():
    e = dict(os.environ)
    if 'GEMINI_API_KEY' not in e and os.path.exists(CHAVE_GEMINI):
        e['GEMINI_API_KEY'] = open(CHAVE_GEMINI).read().strip()
    return e


def ler_historia(caminho):
    """Parágrafos da história: tudo depois da linha '---' do .md."""
    txt = open(caminho, encoding='utf-8').read()
    corpo = txt.split('\n---\n', 1)[1] if '\n---\n' in txt else txt
    return [p.strip() for p in re.split(r'\n\s*\n', corpo) if p.strip()]


def duracao(arquivo):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', arquivo],
                                capture_output=True, text=True, check=True).stdout)


def jload(p, padrao=None):
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else padrao


def jsave(p, d):
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
