"""Narração corrida numa voz → cortada por palavra (Whisper) → cada trecho no início da sua cena (vídeo original intacto)."""
import json, sys, base64, urllib.request, time, subprocess, re, unicodedata
sys.path.insert(0,'/home/user/Victor1Paim/eagle-english/scripts')
from vozes import chave, pedir, tirar_estalo, _gravar, registrar, limpar_estalo_wav
D='/home/user/Victor1Paim/barra-deck'; voz=sys.argv[1]; g=sys.argv[2]
SEG=["Ceia de Natal do Barra Déqui!","O fogão é nosso. A noite é sua!","Tem entradas deliciosas…","quiches…",
     "pratos principais que deixam sua mesa completa…","acompanhamentos…","e sobremesas… e muitas outras opções!",
     "Encomendas até dez de dezembro. Retirada dia vinte e quatro, das dez às quinze horas.","Monte sua ceia pelo link que tá na bio!"]
ANC=[("ceia",0),(("fogao","foga","nosso"),None),("tem",0),("quiches",0),("pratos",0),("acompanhamentos",0),("sobremesas",1),("encomendas",0),("monte",0)]
CENA=[0,3.37,7.57,9.73,12.13,14.53,16.93,19.57,24.57,30.0]
EST=("Leia em português do Brasil, com sotaque carioca natural, como "+("um locutor" if g=="m" else "uma locutora")+
 " de comercial de Natal para Reels: MUITO dinâmico e empolgado, ritmo rápido e cheio de energia, sorriso na voz, entonação variada, "
 "valorizando as palavras importantes, pausas bem curtas nas reticências, como quem convida um amigo para a melhor ceia do ano. Texto: ")
bruto=f'{D}/voz_{voz}.wav'
import whisper
m=whisper.load_model("turbo")
for tent in range(5):
    body={"contents":[{"parts":[{"text":EST+" ".join(SEG)}]}],"generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":voz}}}}}
    req=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-preview-tts:generateContent",data=json.dumps(body).encode(),headers={"x-goog-api-key":chave(),"Content-Type":"application/json"})
    for k in range(4):
        try: d=pedir(req); break
        except Exception as e: print(' erro',e,flush=True); time.sleep(15)
    u=d.get("usageMetadata",{}); registrar(D,"gemini-2.5-pro-preview-tts","voz",entrada_texto=u.get("promptTokenCount",0),saida_audio=u.get("candidatesTokenCount",0))
    _gravar(tirar_estalo(base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])),bruto)
    r=m.transcribe(bruto,language='pt',word_timestamps=True)
    W=[(w['start'],w['end'],w['word']) for s in r['segments'] for w in s['words']]
    print('whisper:',r['text'].strip(),flush=True)
    txt=r['text'].lower()
    ok=('15' in txt or 'quinze' in txt) and '13' not in txt and 'treze' not in txt and ('10 de dezembro' in txt or 'dez de dezembro' in txt) and ('24' in txt or 'vinte e quatro' in txt) and not any(x in txt for x in ('dinâmico','ritmo','entonação','reticências','bill')) and txt.strip().startswith('ceia')
    print('tentativa',tent+1,'conteúdo ok' if ok else 'ERRO de conteúdo',flush=True)
    if ok: break
norm=lambda s: unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode().strip(' .,!?…')
cortes=[];j=0
for a,back in ANC:
    alts=a if isinstance(a,tuple) else (a,)
    while j<len(W) and not any(x in norm(W[j][2]) for x in alts): j+=1
    if j>=len(W): sys.exit(f'âncora não achada: {a}')
    if back is None: back=0 if norm(W[j][2]).startswith('o') and len(norm(W[j][2]))<3 else (2 if 'nosso' in norm(W[j][2]) else 1)
    i=j-back; ini=W[i][0]; fimprev=W[i-1][1] if i>0 else 0.0
    cortes.append(max(0.0,(fimprev+ini)/2) if i>0 else 0.0); j+=1
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',bruto],capture_output=True,text=True).stdout)
cortes.append(dur)
def sh(*a): subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-y',*a],check=True)
CENA_ORIG=[(0,3.37),(3.37,7.57),(7.57,9.73),(9.73,12.13),(12.13,14.53),(14.53,16.93),(16.93,19.57),(19.57,24.57),(24.57,30.0)]
SRC=f'{D}/video-com-texto.mp4'; partes=[]; ent=[];fil=[];rel=[]; t=0.0
for k in range(9):
    a,b=cortes[k],cortes[k+1]; p=f'{D}/_p{k}.wav'
    sh('-i',bruto,'-af',f'atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse','-ar','48000','-ac','1',p)
    L=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
    so,eo=CENA_ORIG[k]; Lo=eo-so
    N=max(L+0.25+(0.12 if k==0 else 0.05), 1.4 if k not in (0,8) else 2.5)
    if k==8: N=max(N,4.3)   # QR: o botão "link da bio" entra 1,43 s depois
    c=f'{D}/_c{k}.mp4'
    if N<=Lo: sh('-ss',f'{so:.3f}','-t',f'{N:.3f}','-i',SRC,'-an','-vf','fps=30','-c:v','libx264','-crf','17',c); f=1.0
    else:
        f=N/Lo; sh('-ss',f'{so:.3f}','-t',f'{Lo:.3f}','-i',SRC,'-an','-vf',f'setpts={f:.4f}*PTS,fps=30','-c:v','libx264','-crf','17',c)
    partes.append(c); st=t+(0.12 if k==0 else 0.05); ent+=['-i',p]; ms=int(st*1000); fil.append(f'[{k}:a]adelay={ms}|{ms}[a{k}]')
    rel.append((k,round(t,2),round(N,2),round(f,2))); t+=N
print('cenas (n, início, duração, câmera lenta):',rel,'total',round(t,2),flush=True)
open(f'{D}/_l.txt','w').write(''.join(f"file '{x}'\n" for x in partes))
sh('-f','concat','-safe','0','-i',f'{D}/_l.txt','-c','copy',f'{D}/_v.mp4')
fil.append(''.join(f'[a{k}]' for k in range(9))+f'amix=inputs=9:normalize=0,apad=whole_dur={t:.3f},atrim=0:{t:.3f},afade=t=out:st={t-0.4:.3f}:d=0.4,aformat=channel_layouts=stereo[a]')
sh(*ent,'-filter_complex',';'.join(fil),'-map','[a]','-ar','48000',f'{D}/_mix.wav')
rr=subprocess.run(['ffmpeg','-nostdin','-i',f'{D}/_mix.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
mm=json.loads(rr[rr.rindex('{'):rr.rindex('}')+1])
sh('-i',f'{D}/_mix.wav','-af',f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={mm['input_i']}:measured_TP={mm['input_tp']}:measured_LRA={mm['input_lra']}:measured_thresh={mm['input_thresh']}:offset={mm['target_offset']}:linear=true",'-ar','48000',f'{D}/narracao_{voz}.wav')
sh('-i',f'{D}/_v.mp4','-i',f'{D}/narracao_{voz}.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',f'{D}/video-ceia-{voz.lower()}.mp4')
import glob,os
for x in glob.glob(f'{D}/_*'): os.remove(x)
print('ok',f'video-ceia-{voz.lower()}.mp4',flush=True)
