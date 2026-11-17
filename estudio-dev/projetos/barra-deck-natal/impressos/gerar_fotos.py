"""Gera fotos realistas (ilustrativas) dos pratos da Ceia de Natal com a API de imagens da OpenAI.

Uso:
  python3 impressos/gerar_fotos.py                 # gera as que faltam
  python3 impressos/gerar_fotos.py chester tender  # só estes ids (refaz)
Saída: assets/img/pratos/<id>.webp (640x640) e assets/img/categorias/<id>.webp (1200x675).
Custos registrados em impressos/custos.jsonl. A chave é injetada pelo proxy (ou OPENAI_API_KEY).
"""
import base64
import io
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
KEY = os.environ.get('OPENAI_API_KEY', 'proxy')
MODELO = 'gpt-image-2'

ESTILO = (
    'Photorealistic professional food photography for a premium Brazilian restaurant Christmas menu. '
    '45-degree angle, the dish centered and filling most of the frame, served on elegant handmade ceramic or '
    'a white porcelain dish, warm soft natural window light, shallow depth of field, rich appetizing detail. '
    'Background: warm cream linen tablecloth with subtle out-of-focus Christmas details (a pine sprig, a small '
    'copper bauble, warm fairy lights bokeh) in brown and copper tones. Realistic home-style portion, not '
    'overly styled. No text, no labels, no logos, no hands, no people.'
)

PRATOS = {
    # entradas
    'bolinho-bacalhau': 'Brazilian salt cod fritters (bolinhos de bacalhau), golden and crispy, piled on a platter with lime wedges and parsley.',
    'empanado-camarao': 'Breaded fried shrimp (camarão empanado), golden crispy, arranged on a platter with lemon wedges and a small bowl of tartar sauce.',
    'croquete-alemao': 'German style meat croquettes (croquete do alemão), elongated golden breaded croquettes on a platter with mustard.',
    'coxinha': 'Brazilian coxinhas, teardrop-shaped fried chicken croquettes, golden, piled on a serving platter.',
    'kibe-queijo': 'Brazilian fried kibbeh stuffed with melted cheese (kibe com queijo), one cut open showing the cheese, on a platter with lemon.',
    # quiches
    'quiche-alho-poro': 'Whole leek quiche (quiche de alho-poró) in a fluted tart pan, one slice cut, golden custard with green leek.',
    'quiche-minas-tomate': 'Quiche with Brazilian minas cheese and sun-dried tomatoes, golden top, one slice removed.',
    'quiche-presunto': 'Ham, cheese and oregano quiche, golden melted cheese top sprinkled with oregano, one slice cut.',
    'quiche-brie': 'Brie and dried apricot quiche, slices of brie and apricots on golden top, one slice cut.',
    'quiche-gorgonzola': 'Gorgonzola, pear and honey quiche, thin pear slices and drizzle of honey on golden top.',
    'quiche-camarao': 'Shrimp quiche, pink shrimp visible on golden custard top, fresh herbs, one slice cut.',
    'quiche-bacalhau': 'Salt cod quiche (quiche de bacalhau) with flakes of cod and olives, golden top, one slice cut.',
    # principais
    'lombo': 'Roasted Brazilian pork loin (lombo suíno assado), sliced, glossy golden crust, on a serving board.',
    'maminha': 'Stuffed roasted beef rump (maminha recheada) sliced showing the stuffing, on a platter.',
    'tender': 'Glazed Christmas ham ball (tender bolinha) scored and caramelized with cloves, on a platter.',
    'escondidinho-carne-seca': 'Brazilian escondidinho de carne-seca: baked cassava puree with dried beef, golden gratinated cheese top, in a ceramic baking dish, one portion scooped.',
    'escondidinho-camarao': 'Brazilian shrimp escondidinho: baked cassava puree with creamy shrimp, golden gratin top, in a ceramic baking dish.',
    'bacalhau-desfiado': 'Shredded salt cod Portuguese style (bacalhau desfiado à portuguesa) with olive oil, onions, olives, boiled eggs and potatoes in a ceramic dish.',
    'postas-bacalhau': 'Thick loins of desalted salt cod (postas de bacalhau) baked with olive oil, potatoes, onions and black olives in a ceramic dish.',
    'chester': 'Whole roasted Christmas chester (large chicken), golden glossy skin, on a big platter with orange slices and rosemary.',
    'pernil': 'Roasted boneless pork leg (pernil sem osso), sliced, caramelized crust, on a carving board.',
    'arroz-polvo': 'Brazilian octopus rice (arroz de polvo), moist rice with tender octopus pieces and herbs in a ceramic dish.',
    'arroz-frutos-mar': 'Seafood rice (arroz de frutos do mar) with shrimp, mussels and squid in a ceramic dish.',
    'arroz-camarao': 'Brazilian shrimp rice (arroz de camarão), creamy rice with pink shrimp and parsley in a ceramic dish.',
    # acompanhamentos
    'arroz-branco': 'Bowl of fluffy white Brazilian rice.',
    'arroz-natalino': 'Brazilian Christmas rice (arroz natalino) with raisins, cashew, walnuts, corn, bacon, olives, egg and ham.',
    'arroz-bacalhau': 'Salt cod rice (arroz de bacalhau) with cod flakes, olives and parsley in a ceramic dish.',
    'farofa-tradicional': 'Brazilian farofa (toasted cassava flour with butter and onions) in a ceramic bowl.',
    'farofa-ameixa': 'Brazilian farofa with prunes (farofa de ameixa) in a ceramic bowl.',
    'farofa-ovos': 'Brazilian egg farofa (farofa de ovos) with scrambled egg pieces and parsley in a bowl.',
    'cuscuz': 'Moroccan couscous with vegetables, raisins and herbs in a ceramic bowl.',
    'salada-aipo': 'Celery salad (salada de aipo) with creamy dressing, apple and walnuts in a glass bowl.',
    'salpicao': 'Brazilian chicken salpicão: shredded chicken salad with carrots, raisins, corn and topped with potato sticks, in a bowl.',
    'empadao-frango': 'Brazilian chicken pot pie (empadão de frango) in a round ceramic dish, golden crust, one slice cut showing filling.',
    'empadao-camarao': 'Brazilian shrimp pot pie (empadão de camarão), golden crust, slice cut showing creamy shrimp filling.',
    # sobremesas
    'rabanada': 'Brazilian rabanada (Christmas French toast) dusted with sugar and cinnamon, stacked on a plate with cinnamon sticks.',
    'rabanada-panetone': 'Panettone French toast slices (rabanada de panetone) with candied fruits, dusted with sugar and cinnamon.',
    'torta-limao': 'Brazilian lime pie (torta de limão) with toasted meringue top and lime zest, one slice cut.',
    'cheesecake-damasco': 'Cheesecake with glossy apricot topping, whole, one slice cut.',
    'pave-chocolate': 'Brazilian chocolate pavê in a rectangular glass dish, layers of biscuits and cream, chocolate shavings on top.',
    'pave-pacoca': 'Brazilian peanut paçoca pavê in a glass dish, layers of cream and biscuits, crumbled paçoca on top.',
}

CATEGORIAS = {
    'entradas': 'An abundant spread of Brazilian Christmas appetizers: salt cod fritters, coxinhas, kibbeh and breaded shrimp on platters.',
    'quiches': 'Several golden quiches on a wooden table, one sliced, leek and cheese visible.',
    'principais': 'A festive Brazilian Christmas dinner table with a roasted chester, glazed ham, roasted pork and baked salt cod.',
    'acompanhamentos': 'Bowls of Brazilian Christmas side dishes: Christmas rice, farofa, couscous and chicken salpicão.',
    'sobremesas': 'Brazilian Christmas desserts table: rabanadas, lime pie, chocolate pavê and cheesecake.',
}


def gerar(nome, descricao, tamanho, destino, saida_px):
    corpo = {'model': MODELO, 'prompt': f'{descricao} {ESTILO}', 'size': tamanho, 'quality': 'medium', 'n': 1}
    for tentativa in range(4):
        try:
            req = urllib.request.Request('https://api.openai.com/v1/images/generations', data=json.dumps(corpo).encode(),
                                         headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.loads(r.read())
            break
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            if tentativa == 3:
                return f'ERRO {nome}: {e}'
            time.sleep(8 * (tentativa + 1))
    img = Image.open(io.BytesIO(base64.b64decode(d['data'][0]['b64_json']))).convert('RGB')
    img = img.resize(saida_px, Image.LANCZOS)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    img.save(destino, 'WEBP', quality=82, method=6)
    with open(os.path.join(AQUI, 'custos.jsonl'), 'a') as f:
        f.write(json.dumps({'quando': time.strftime('%Y-%m-%d %H:%M'), 'modelo': MODELO, 'item': nome,
                            'tamanho': tamanho, 'qualidade': 'medium', 'uso': d.get('usage')}) + '\n')
    return f'ok {nome}'


if __name__ == '__main__':
    pedidos = sys.argv[1:]
    tarefas = []
    for k, desc in PRATOS.items():
        dest = os.path.join(SITE, 'assets', 'img', 'pratos', f'{k}.webp')
        if (pedidos and k in pedidos) or (not pedidos and not os.path.exists(dest)):
            tarefas.append((k, desc, '1024x1024', dest, (640, 640)))
    for k, desc in CATEGORIAS.items():
        dest = os.path.join(SITE, 'assets', 'img', 'categorias', f'{k}.webp')
        if (pedidos and f'cat-{k}' in pedidos) or (not pedidos and not os.path.exists(dest)):
            tarefas.append((f'cat-{k}', desc, '1536x1024', dest, (1200, 675)))
    print(len(tarefas), 'imagens')
    with ThreadPoolExecutor(6) as ex:
        for r in ex.map(lambda t: gerar(*t), tarefas):
            print(r, flush=True)
