"""Narração corrida numa voz → cortada por palavra (Whisper) → cada trecho no início da sua cena (vídeo original intacto)."""
import json, sys, base64, urllib.request, time, subprocess, re, unicodedata
sys.path.insert(0,'/home/user/Victor1Paim/eagle-english/scripts')
from vozes import chave, pedir, tirar_estalo, _gravar, registrar, limpar_estalo_wav
D='/home/user/Victor1Paim/barra-deck'; voz=sys.argv[1]; g=sys.argv[2]
SEG=["Ceia de Natal do Barra Déqui!","O fogão é nosso. A noite é sua!","Tem entradas deliciosas…","quiches…",
     "pratos principais que deixam sua mesa completa…","acompanhamentos…","e sobremesas… e muitas outras opções!",
     "Encomendas até dez de dezembro. Retirada dia vinte e quatro, das dez às quinze horas.","Monte sua ceia pelo link que tá na bio!"]
ANC=[("ceia",0),("fogao",1),("tem",0),("quiches",0),("pratos",0),("acompanhamentos",0),("sobremesas",1),("encomendas",0),("monte",0)]
CENA=[0,3.37,7.57,9.73,12.13,14.53,16.93,19.57,24.57,30.0]
EST=("Leia em português do Brasil, com sotaque carioca natural, como "+("um locutor" if g=="m" else "uma locutora")+
 " de comercial de Natal: voz calorosa, animada e sorridente, com energia e variação de entonação, convidando o ouvinte com entusiasmo, ritmo ágil de Reels, fazendo pequenas pausas nas reticências. Texto: ")
bruto=f'{D}/voz_{voz}.wav'
body={"contents":[{"parts":[{"text":EST+" ".join(SEG)}]}],"generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":voz}}}}}
req=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-preview-tts:generateContent",data=json.dumps(body).encode(),headers={"x-goog-api-key":chave(),"Content-Type":"application/json"})
for k in range(4):
    try: d=pedir(req); break
    except Exception as e: print(' erro',e,flush=True); time.sleep(15)
u=d.get("usageMetadata",{}); registrar(D,"gemini-2.5-pro-preview-tts","voz",entrada_texto=u.get("promptTokenCount",0),saida_audio=u.get("candidatesTokenCount",0))
_gravar(tirar_estalo(base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])),bruto)
import whisper
m=whisper.load_model("turbo"); r=m.transcribe(bruto,language='pt',word_timestamps=True)
W=[(w['start'],w['end'],w['word']) for s in r['segments'] for w in s['words']]
print('whisper:',r['text'].strip(),flush=True)
norm=lambda s: unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode().strip(' .,!?…')
cortes=[];j=0
for a,back in ANC:
    while j<len(W) and a not in norm(W[j][2]): j+=1
    if j>=len(W): sys.exit(f'âncora não achada: {a}')
    i=j-back; ini=W[i][0]; fimprev=W[i-1][1] if i>0 else 0.0
    cortes.append(max(0.0,(fimprev+ini)/2) if i>0 else 0.0); j+=1
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',bruto],capture_output=True,text=True).stdout)
cortes.append(dur)
def sh(*a): subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-y',*a],check=True)
ent=[];fil=[];rel=[]
for k in range(9):
    a,b=cortes[k],cortes[k+1]; L=b-a
    ini=CENA[k]+(0.25 if k==0 else 0.08); disp=CENA[k+1]-ini-0.05
    vel=min(1.2,max(1.0,L/disp)); p=f'{D}/_p{k}.wav'
    sh('-i',bruto,'-af',f'atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,atempo={vel:.3f},afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse','-ar','48000','-ac','1',p)
    ent+=['-i',p]; ms=int(ini*1000); fil.append(f'[{k}:a]adelay={ms}|{ms}[a{k}]'); rel.append((k,round(ini,2),round(L/vel,2),round(disp,2),round(vel,2)))
print('trechos (cena, início, duração, espaço, velocidade):',rel,flush=True)
fil.append(''.join(f'[a{k}]' for k in range(9))+'amix=inputs=9:normalize=0,apad=whole_dur=30,atrim=0:30,afade=t=out:st=29.6:d=0.4,aformat=channel_layouts=stereo[a]')
sh(*ent,'-filter_complex',';'.join(fil),'-map','[a]','-ar','48000',f'{D}/_mix.wav')
rr=subprocess.run(['ffmpeg','-nostdin','-i',f'{D}/_mix.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
mm=json.loads(rr[rr.rindex('{'):rr.rindex('}')+1])
sh('-i',f'{D}/_mix.wav','-af',f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={mm['input_i']}:measured_TP={mm['input_tp']}:measured_LRA={mm['input_lra']}:measured_thresh={mm['input_thresh']}:offset={mm['target_offset']}:linear=true",'-ar','48000',f'{D}/narracao_{voz}.wav')
sh('-i',f'{D}/video-com-texto.mp4','-i',f'{D}/narracao_{voz}.wav','-filter_complex','[0:v]tpad=stop_mode=clone:stop_duration=1,trim=0:30[v]','-map','[v]','-map','1:a','-c:v','libx264','-crf','17','-c:a','aac','-b:a','192k','-t','30','-movflags','+faststart',f'{D}/video-ceia-{voz.lower()}.mp4')
import glob,os
for x in glob.glob(f'{D}/_*'): os.remove(x)
print('ok',f'video-ceia-{voz.lower()}.mp4',flush=True)
