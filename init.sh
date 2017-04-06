#!/bin/sh

if [ ! -d .venv]; then
  virtualenv .venv
  pip install Mastodon.py
fi

source .venv/bin/activate
