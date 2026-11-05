"""Cria uma voz NOVA a partir de uma descrição em texto (Qwen3-TTS VoiceDesign, roda local no Mac).

Uso:
  ./desenhar.sh "texto que a voz vai falar"                       -> gera as 8 vozes prontas abaixo
  ./desenhar.sh "texto" --voz "Mulher de 40 anos, voz rouca..."    -> gera só a voz que você descreveu
  ./desenhar.sh "texto" --so grave trailer                         -> gera só as prontas com esses nomes

O resultado vai pra pasta saida/vozes-desenhadas/ em mp3.
"""
import argparse, os, subprocess, time

AQUI = os.path.dirname(os.path.abspath(__file__))
MODELO = "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit"
TEXTO_PADRAO = "Oi! Essa voz não existe: ela foi desenhada a partir de uma descrição, direto no meu computador."

VOZES = {
    "01-grave-documentario": "Voz masculina grave e profunda, brasileira, de narrador de documentário. Calma, séria, pausada, com autoridade e mistério.",
    "02-sussurro-intimo": "Voz masculina brasileira baixa e próxima do microfone, quase um sussurro, intimista e hipnótica, ritmo lento.",
    "03-mentor-confiante": "Homem brasileiro de 35 anos, voz firme e confiante de mentor de negócios, direto, sem exagero, tom de conversa séria.",
    "04-trailer-cinema": "Voz masculina brasileira muito grave de trailer de cinema, dramática e imponente, cada frase com peso.",
    "05-jovem-direto": "Homem brasileiro jovem, voz clara e natural, fala rápida e direta como criador de conteúdo, mas sem euforia.",
    "06-rouco-maduro": "Homem brasileiro de 50 anos, voz levemente rouca e madura, experiente, calma, transmite confiança.",
    "07-feminina-seria": "Voz feminina brasileira grave e elegante, séria e calma, narradora de documentário, sem sorrir.",
    "08-feminina-intima": "Mulher brasileira de 30 anos, voz suave e baixa, próxima, misteriosa e segura.",
}

p = argparse.ArgumentParser(description="Cria vozes novas a partir de uma descrição.")
p.add_argument("texto", nargs="?", default=TEXTO_PADRAO, help="o que a voz vai falar")
p.add_argument("--voz", help="descrição da voz que você quer (em vez das 8 prontas)")
p.add_argument("--so", nargs="*", default=[], help="gera só as prontas cujo nome tenha essas palavras")
a = p.parse_args()

import numpy as np, soundfile as sf
from mlx_audio.tts.utils import load_model

vozes = {"minha-descricao": a.voz} if a.voz else VOZES
pasta = os.path.join(AQUI, "saida", "vozes-desenhadas")
os.makedirs(pasta, exist_ok=True)

print("Carregando o modelo de voz (na 1ª vez baixa ~2 GB)...", flush=True)
m = load_model(MODELO)
for nome, desc in vozes.items():
    if a.so and not any(s in nome for s in a.so):
        continue
    t = time.time()
    res = list(m.generate_voice_design(text=a.texto, language="Portuguese", instruct=desc))
    audio = np.concatenate([np.array(r.audio) for r in res])
    out = os.path.join(pasta, nome)
    sf.write(out + ".wav", audio, m.sample_rate)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", out + ".wav", "-b:a", "160k", out + ".mp3"], check=True)
    os.remove(out + ".wav")
    print(f"{nome}: {len(audio)/m.sample_rate:.1f}s em {time.time()-t:.0f}s -> {out}.mp3", flush=True)

print("Pronto! Abra a pasta saida/vozes-desenhadas/.")
