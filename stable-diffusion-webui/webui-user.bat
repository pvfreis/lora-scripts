@echo off

set PYTHON=
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS= --xformers --medvram --precision full --no-half --no-half-vae --opt-split-attention --disable-safe-unpickle
set OPTIMIZED_TURBO=true

call webui.bat
