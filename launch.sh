#!/bin/sh

if [ ! -d .venv ]; then
  virtualenv .venv
  . .venv/bin/activate
  pip install Mastodon.py
else
  . .venv/bin/activate
fi

python Autofollow.py

deactivate
