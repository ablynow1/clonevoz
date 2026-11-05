# clonevoz

Clona a voz de qualquer pessoa a partir de um áudio curto, ou cria uma voz nova a partir de uma descrição em texto.
Tudo roda **no seu Mac**: sem internet (depois da 1ª vez), sem conta e sem pagar.

Por baixo: [Qwen3-TTS](https://huggingface.co/mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit) pelo `mlx-audio` e Whisper pra transcrever a referência.

## O que precisa

- Mac com chip Apple (M1, M2, M3, M4...). **Não roda em Mac Intel nem em Windows.**
- Uns **6 GB livres** no disco (programas + modelos).
- [Homebrew](https://brew.sh) instalado (o instalador usa ele pra pôr o `ffmpeg`).

## Instalar (uma vez só)

Abra o Terminal e rode:

```bash
git clone https://github.com/ablynow1/clonevoz.git
cd clonevoz
./instalar.sh
```

## Clonar uma voz

1. Grave ou pegue um áudio de **10 a 30 segundos** só com a pessoa falando, sem música e sem barulho.
   Áudio de WhatsApp serve.
2. Jogue o arquivo na pasta `minha-voz/`.
3. Rode:

```bash
./clonar.sh minha-voz/meu-audio.ogg "Texto que a voz clonada vai falar."
```

Ele gera **3 tomadas** na pasta `saida/`. Ouça e fique com a melhor.

Outras opções:

```bash
./clonar.sh minha-voz/meu-audio.ogg --arquivo roteiro.txt     # texto longo vindo de um .txt
./clonar.sh minha-voz/meu-audio.ogg "Texto" --tomadas 5       # mais tomadas pra escolher
```

## Criar uma voz que não existe

```bash
./desenhar.sh "Texto que a voz vai falar."                                        # 8 vozes prontas pra comparar
./desenhar.sh "Texto" --voz "Mulher de 40 anos, voz rouca, calma, tom de rádio"   # a voz que você descrever
```

Sai em `saida/vozes-desenhadas/`.

## Dicas

- A **1ª vez** demora: baixa o modelo de voz (~2 GB) e o Whisper (~1,6 GB). Depois fica rápido.
- Quanto mais limpo o áudio de referência, melhor o clone.
- Pontuação muda a fala: reticências viram pausa, ponto de exclamação dá energia.
- Sigla e palavra em inglês saem melhor escritas como se fala ("cê a cê", "Meta Édis").

## Use com responsabilidade

Só clone a voz de quem deixou. Usar a voz de alguém sem permissão pra enganar, fingir ser a pessoa ou aplicar golpe é crime.
