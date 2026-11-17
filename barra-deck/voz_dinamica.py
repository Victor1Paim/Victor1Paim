import json, sys, base64, urllib.request
sys.path.insert(0,'/home/user/Victor1Paim/eagle-english/scripts')
import vozes
from vozes import chave, pedir, tirar_estalo, _gravar, registrar
D='/home/user/Victor1Paim/barra-deck'
ESTILO=("Leia em português do Brasil, com sotaque carioca natural, como um locutor de comercial de Natal: voz masculina calorosa, "
        "animada e sorridente, com energia e variação de entonação, convidando o ouvinte com entusiasmo, ritmo ágil de Reels. Texto: ")
FALAS=[("s1","Ceia de Natal do Barra Déqui!"),("s2","O fogão é nosso. A noite é sua!"),
       ("lista","Tem entradas… quiches… chester, tender, bacalhau e muitas outras opções… os acompanhamentos… e as sobremesas! Tudo feito pela nossa cozinha."),
       ("s8","Encomendas até dez de dezembro! Retirada no dia vinte e quatro, das dez às quinze horas."),
       ("s9","Monte sua ceia pelo link que tá na bio, ou aponte a câmera pro QR code!")]
modelo=sys.argv[1] if len(sys.argv)>1 else "gemini-2.5-pro-preview-tts"; voz=sys.argv[2] if len(sys.argv)>2 else "Achird"
so=sys.argv[3].split(',') if len(sys.argv)>3 else None
for i,t in FALAS:
    if so and i not in so: continue
    for tent in range(3):
        body={"contents":[{"parts":[{"text":ESTILO+t}]}],"generationConfig":{"responseModalities":["AUDIO"],
              "speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":voz}}}}}
        req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
            data=json.dumps(body).encode(),headers={"x-goog-api-key":chave(),"Content-Type":"application/json"})
        import time
        for k in range(4):
            try: d=pedir(req); break
            except Exception as e:
                print('  erro, tentando de novo:',e,flush=True); time.sleep(15)
        u=d.get("usageMetadata",{})
        registrar(D,modelo,"voz",entrada_texto=u.get("promptTokenCount",0),saida_audio=u.get("candidatesTokenCount",0))
        saida=f'{D}/audio2/{i}.wav'
        _gravar(tirar_estalo(base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])),saida)
        p=vozes.conferir(saida,t.replace('Déqui','Deck'),'pt'); print(i,tent+1,p,flush=True)
        if p>=80: break
