import json, sys, base64, urllib.request, time
sys.path.insert(0,'/home/user/Victor1Paim/eagle-english/scripts')
import vozes
from vozes import chave, pedir, tirar_estalo, _gravar, registrar
D='/home/user/Victor1Paim/barra-deck'
TXT="Ceia de Natal do Barra Déqui! O fogão é nosso. A noite é sua! Tem entradas, quiches, chester, tender, bacalhau… e muitas outras opções!"
def estilo(g): return ("Leia em português do Brasil, com sotaque carioca natural, como "+("um locutor" if g=="m" else "uma locutora")+
  " de comercial de Natal: voz calorosa, animada e sorridente, com energia e variação de entonação, convidando o ouvinte com entusiasmo, ritmo ágil de Reels. Texto: ")
for voz,g in [("Puck","m"),("Fenrir","m"),("Laomedeia","f"),("Sulafat","f")]:
    for tent in range(3):
        body={"contents":[{"parts":[{"text":estilo(g)+TXT}]}],"generationConfig":{"responseModalities":["AUDIO"],
              "speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":voz}}}}}
        req=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-preview-tts:generateContent",
            data=json.dumps(body).encode(),headers={"x-goog-api-key":chave(),"Content-Type":"application/json"})
        for k in range(4):
            try: d=pedir(req); break
            except Exception as e: print(' erro',e,flush=True); time.sleep(15)
        u=d.get("usageMetadata",{}); registrar(D,"gemini-2.5-pro-preview-tts","voz",entrada_texto=u.get("promptTokenCount",0),saida_audio=u.get("candidatesTokenCount",0))
        s=f'{D}/amostras/{voz}.wav'; _gravar(tirar_estalo(base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])),s)
        p=vozes.conferir(s,TXT.replace('Déqui','Deck'),'pt'); print(voz,tent+1,p,flush=True)
        if p>=85: break
