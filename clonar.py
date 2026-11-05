"""Clona uma voz a partir de um áudio de referência (Qwen3-TTS Base, roda local no Mac).

Uso:
  ./clonar.sh minha-voz/audio.ogg "texto que a voz vai falar"
  ./clonar.sh minha-voz/audio.ogg --arquivo roteiro.txt
  ./clonar.sh minha-voz/audio.ogg "texto" --tomadas 5

A transcrição da referência sai sozinha pelo Whisper (também local).
O resultado vai pra pasta saida/ em mp3.
"""
import argparse, os, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
MODELO = "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit"
WHISPER = "mlx-community/whisper-large-v3-turbo"
TEXTO_PADRAO = "Oi! Essa é a minha voz clonada, rodando direto no meu computador, sem internet e sem pagar nada."

p = argparse.ArgumentParser(description="Clona uma voz a partir de um áudio de referência.")
p.add_argument("referencia", help="áudio com a voz (ogg, m4a, mp3, wav...). 10 a 30 s, só a pessoa falando")
p.add_argument("texto", nargs="?", default=None, help="o que a voz clonada vai falar")
p.add_argument("--arquivo", help="lê o texto de um .txt em vez de passar na linha")
p.add_argument("--tomadas", type=int, default=3, help="quantas versões gerar (padrão 3, escolha a melhor)")
p.add_argument("--idioma", default="pt", help="código do idioma (padrão pt)")
a = p.parse_args()

if a.arquivo:
    with open(a.arquivo, encoding="utf-8") as f:
        texto = f.read().strip()
else:
    texto = a.texto or TEXTO_PADRAO

if not os.path.isfile(a.referencia):
    sys.exit(f"Não achei o áudio: {a.referencia}")

import numpy as np, soundfile as sf
import mlx_whisper
from mlx_audio.tts.utils import load_model

base = os.path.splitext(os.path.basename(a.referencia))[0]
os.makedirs(os.path.join(AQUI, "saida"), exist_ok=True)
wav = os.path.join(AQUI, "saida", f".{base}-ref.wav")

# referência em mono 24 kHz, no máximo 30 s
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", a.referencia,
                "-ac", "1", "-ar", "24000", "-t", "30", wav], check=True)

print("Transcrevendo a referência...", flush=True)
ref_text = mlx_whisper.transcribe(wav, path_or_hf_repo=WHISPER, language=a.idioma)["text"].strip()
print("referência:", ref_text, flush=True)

print("Carregando o modelo de voz (na 1ª vez baixa ~2 GB)...", flush=True)
m = load_model(MODELO)
for i in range(1, a.tomadas + 1):
    t = time.time()
    res = list(m.generate(text=texto, ref_audio=wav, ref_text=ref_text, lang_code=a.idioma))
    audio = np.concatenate([np.array(r.audio) for r in res])
    out = os.path.join(AQUI, "saida", f"{base}-tomada{i}")
    sf.write(out + ".wav", audio, m.sample_rate)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", out + ".wav", "-b:a", "160k", out + ".mp3"], check=True)
    os.remove(out + ".wav")
    print(f"tomada {i}: {len(audio)/m.sample_rate:.1f}s em {time.time()-t:.0f}s -> {out}.mp3", flush=True)

os.remove(wav)
print("Pronto! Abra a pasta saida/ e escolha a melhor tomada.")
