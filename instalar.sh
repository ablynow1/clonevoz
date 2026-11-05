#!/bin/bash
# Instala tudo que o clonevoz precisa. Rode uma vez: ./instalar.sh
set -e
cd "$(dirname "$0")"

if [ "$(uname -s)" != "Darwin" ] || [ "$(uname -m)" != "arm64" ]; then
  echo "Isso só roda em Mac com chip Apple (M1, M2, M3, M4...)."; exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  if ! command -v brew >/dev/null 2>&1; then
    echo "Falta o Homebrew. Instale com o comando do site https://brew.sh e rode ./instalar.sh de novo."; exit 1
  fi
  echo "Instalando o ffmpeg..."; brew install ffmpeg
fi

if ! command -v uv >/dev/null 2>&1 && [ ! -x "$HOME/.local/bin/uv" ]; then
  echo "Instalando o uv (gerenciador de Python)..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
UV="$(command -v uv || echo "$HOME/.local/bin/uv")"

echo "Criando o ambiente Python..."
"$UV" venv --python 3.12 .venv
"$UV" pip install --python .venv/bin/python -r requirements.txt

chmod +x clonar.sh desenhar.sh
echo
echo "Pronto! Agora é só usar:"
echo '  ./clonar.sh minha-voz/seu-audio.ogg "texto que a voz vai falar"'
