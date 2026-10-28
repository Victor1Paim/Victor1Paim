#!/usr/bin/env node
// Gemini voz (TTS) e imagem via REST. Sem dependências (Node 20+). A chave vem só do ambiente: GEMINI_API_KEY.
//   node gemini.mjs models                                   lista modelos de voz/imagem da conta
//   node gemini.mjs tts   --text-file roteiro.txt --out voz.wav [--voice Kore] [--style "..."] [--model M] [--go]
//   node gemini.mjs image --prompt-file p.txt --out img.png [--aspect 9:16] [--model M] [--go]
//   node gemini.mjs usage                                    soma o registro de chamadas (custo.jsonl)
// Sem --go o comando só mostra o que faria (tamanho, cache, modelo) e não chama a API nem pede a chave.
import { readFileSync, writeFileSync, mkdirSync, existsSync, copyFileSync, appendFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join } from 'node:path';

const BASE = 'https://generativelanguage.googleapis.com/v1beta';
const CACHE = process.env.GEMINI_CACHE_DIR || 'producoes/.cache-gemini';
const LOG = join(CACHE, 'custo.jsonl');
const DEFAULTS = {
  tts: process.env.GEMINI_TTS_MODEL || 'gemini-2.5-flash-preview-tts',
  image: process.env.GEMINI_IMAGE_MODEL || 'gemini-2.5-flash-image',
};

const die = (m) => { console.error(`✗ ${m}`); process.exit(1); };

function parseArgs(argv) {
  const a = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    if (!argv[i].startsWith('--')) { a._.push(argv[i]); continue; }
    const k = argv[i].slice(2);
    if (k === 'go') a.go = true;
    else a[k] = argv[++i];
  }
  return a;
}

function apiKey() {
  const k = process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY;
  if (!k) die('GEMINI_API_KEY não está definida no ambiente. Peça ao usuário para colocá-la nas configurações do ambiente (nunca no chat nem em arquivo do repositório).');
  return k;
}

async function api(path, { body, method = body ? 'POST' : 'GET' } = {}) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: { 'x-goog-api-key': apiKey(), ...(body ? { 'Content-Type': 'application/json' } : {}) },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let json; try { json = JSON.parse(text); } catch { /* resposta não-JSON */ }
  if (!res.ok) die(`Gemini API ${res.status}: ${(json?.error?.message || text).slice(0, 400)}`);
  return json;
}

const sha = (...p) => createHash('sha256').update(p.join('\u0000')).digest('hex').slice(0, 24);
const readText = (a, inline, file) => (a[inline] ?? (a[file] ? readFileSync(a[file], 'utf8') : '')).trim();
const save = (out, buf) => { mkdirSync(dirname(out), { recursive: true }); writeFileSync(out, buf); };
function log(entry) { mkdirSync(CACHE, { recursive: true }); appendFileSync(LOG, JSON.stringify({ ts: new Date().toISOString(), ...entry }) + '\n'); }

// PCM 16 bits mono (como o Gemini devolve) -> WAV
export function pcmToWav(pcm, rate = 24000, channels = 1) {
  const h = Buffer.alloc(44);
  h.write('RIFF', 0); h.writeUInt32LE(36 + pcm.length, 4); h.write('WAVEfmt ', 8);
  h.writeUInt32LE(16, 16); h.writeUInt16LE(1, 20); h.writeUInt16LE(channels, 22);
  h.writeUInt32LE(rate, 24); h.writeUInt32LE(rate * channels * 2, 28); h.writeUInt16LE(channels * 2, 32);
  h.writeUInt16LE(16, 34); h.write('data', 36); h.writeUInt32LE(pcm.length, 40);
  return Buffer.concat([h, pcm]);
}

async function models() {
  let token = '', rows = [];
  do {
    const r = await api(`/models?pageSize=200${token ? `&pageToken=${token}` : ''}`);
    rows.push(...(r.models || [])); token = r.nextPageToken || '';
  } while (token);
  for (const m of rows.filter((m) => /tts|image|imagen/i.test(m.name)))
    console.log(`${m.name.replace('models/', '')}\t${(m.supportedGenerationMethods || []).join(',')}\t${m.displayName || ''}`);
}

async function tts(a) {
  const text = readText(a, 'text', 'text-file');
  if (!text) die('informe --text ou --text-file');
  if (!a.out) die('informe --out arquivo.wav');
  const model = a.model || DEFAULTS.tts, voice = a.voice || 'Kore', style = a.style || '';
  const max = Number(a['max-chars'] || 4000);
  if (text.length > max) die(`texto com ${text.length} caracteres (limite ${max}). Divida por cena: uma chamada por trecho, para regenerar só o que mudar.`);
  const key = sha('tts', model, voice, style, text), cached = join(CACHE, `${key}.wav`);
  console.log(`tts · modelo ${model} · voz ${voice} · ${text.length} caracteres (≈ ${Math.round(text.length / 15)} s de fala) · cache ${existsSync(cached) ? 'ENCONTRADO (sem custo)' : 'vazio'}`);
  if (existsSync(cached)) { mkdirSync(dirname(a.out), { recursive: true }); copyFileSync(cached, a.out); console.log(`✓ ${a.out} (do cache)`); return; }
  if (!a.go) return console.log('Simulação. Rode de novo com --go para chamar a API (gera custo na sua conta).');
  const r = await api(`/models/${model}:generateContent`, { body: {
    contents: [{ parts: [{ text: style ? `${style}: ${text}` : text }] }],
    generationConfig: { responseModalities: ['AUDIO'], speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: voice } } } },
  } });
  const part = r.candidates?.[0]?.content?.parts?.find((p) => p.inlineData);
  if (!part) die(`resposta sem áudio: ${JSON.stringify(r).slice(0, 300)}`);
  const rate = Number(/rate=(\d+)/.exec(part.inlineData.mimeType || '')?.[1] || 24000);
  const wav = pcmToWav(Buffer.from(part.inlineData.data, 'base64'), rate);
  save(cached, wav); save(a.out, wav);
  log({ kind: 'tts', model, voice, chars: text.length, usage: r.usageMetadata });
  console.log(`✓ ${a.out} · ${(wav.length - 44) / (rate * 2)} s · ${rate} Hz`);
}

async function image(a) {
  const prompt = readText(a, 'prompt', 'prompt-file');
  if (!prompt) die('informe --prompt ou --prompt-file');
  if (!a.out) die('informe --out arquivo.png');
  const model = a.model || DEFAULTS.image, aspect = a.aspect || '9:16';
  const key = sha('image', model, aspect, prompt);
  const cached = ['png', 'jpg', 'webp'].map((e) => join(CACHE, `${key}.${e}`)).find(existsSync);
  console.log(`imagem · modelo ${model} · proporção ${aspect} · prompt ${prompt.length} caracteres · cache ${cached ? 'ENCONTRADO (sem custo)' : 'vazio'}`);
  if (cached) { mkdirSync(dirname(a.out), { recursive: true }); copyFileSync(cached, a.out); console.log(`✓ ${a.out} (do cache)`); return; }
  if (!a.go) return console.log('Simulação. Rode de novo com --go para chamar a API (gera custo na sua conta).');
  const r = await api(`/models/${model}:generateContent`, { body: {
    contents: [{ parts: [{ text: prompt }] }],
    generationConfig: { responseModalities: ['TEXT', 'IMAGE'], imageConfig: { aspectRatio: aspect } },
  } });
  const part = r.candidates?.[0]?.content?.parts?.find((p) => p.inlineData);
  if (!part) die(`resposta sem imagem: ${JSON.stringify(r).slice(0, 300)}`);
  const ext = { 'image/png': 'png', 'image/jpeg': 'jpg', 'image/webp': 'webp' }[part.inlineData.mimeType] || 'png';
  const buf = Buffer.from(part.inlineData.data, 'base64');
  save(join(CACHE, `${key}.${ext}`), buf); save(a.out, buf);
  log({ kind: 'image', model, aspect, usage: r.usageMetadata });
  console.log(`✓ ${a.out} (${ext}, ${buf.length} bytes)`);
}

function usage() {
  if (!existsSync(LOG)) return console.log('nenhuma chamada registrada');
  const by = {};
  for (const l of readFileSync(LOG, 'utf8').trim().split('\n')) {
    const e = JSON.parse(l), k = `${e.kind} · ${e.model}`;
    by[k] ??= { chamadas: 0, caracteres: 0, tokens_entrada: 0, tokens_saida: 0 };
    by[k].chamadas++; by[k].caracteres += e.chars || 0;
    by[k].tokens_entrada += e.usage?.promptTokenCount || 0; by[k].tokens_saida += e.usage?.candidatesTokenCount || 0;
  }
  console.table(by);
}

if (process.argv[1] && import.meta.url.endsWith(process.argv[1].split('/').pop())) {
  const a = parseArgs(process.argv.slice(2));
  const cmd = { models, tts, image, usage }[a._[0]];
  if (!cmd) die('uso: gemini.mjs models | tts | image | usage');
  await cmd(a);
}
