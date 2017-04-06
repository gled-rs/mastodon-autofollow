#!/bin/sh

if [ ! -d .venv ]; then
  virtualenv .venv
  source .venv/bin/activate
  pip install Mastodon.py
else
  source .venv/bin/activate
fi

python Autofollow.py

deactivate
