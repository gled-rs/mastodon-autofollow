#!/bin/sh

if [ ! -d .venv ]; then
  virtualenv .venv
  . .venv/bin/activate
  pip install Mastodon.py
else
  . .venv/bin/activate
fi

if [ -d .git ]; then
  git pull 2>&1 > /dev/null
fi

python Autofollow.py

deactivate
