#!/usr/bin/env bash
# Opt-in bootstrap for the local LLM backend (src/goalcat/config_local.yaml) — installs Ollama and
# pulls the model that backend is pinned to. Not run automatically on venv setup: this targets
# macOS/Homebrew specifically, downloads ~2 GB, and is only needed by whoever actually exercises
# the local path (see src/goalcat/config_local.yaml). Every step here is a no-op if
# already done, so this is safe to re-run.

set -euo pipefail

MODEL="qwen2.5:3b"

if ! command -v brew >/dev/null 2>&1; then
    echo "Homebrew not found — this script targets the macOS/Homebrew setup this project was" >&2
    echo "verified against. Install Ollama manually (https://ollama.com/download) and run" >&2
    echo "'ollama pull $MODEL', or adapt this script for your platform." >&2
    exit 1
fi

if command -v ollama >/dev/null 2>&1; then
    echo "Ollama already installed ($(ollama --version))."
else
    echo "Installing Ollama via Homebrew..."
    brew install ollama
fi

echo "Starting the Ollama service..."
brew services start ollama

echo "Pulling $MODEL (skips download if already present)..."
ollama pull "$MODEL"

echo "Done. Point PipelineConfig at src/goalcat/config_local.yaml to use the local backend."
