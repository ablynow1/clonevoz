#!/bin/bash
D="$(cd "$(dirname "$0")" && pwd)"
exec "$D/.venv/bin/python" "$D/clonar.py" "$@"
