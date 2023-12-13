#!/bin/bash

if [ ! -d venv ]; then
    python3 -m venv venv
fi
source ./venv/bin/activate
pip install -r ./backend/requirements.txt
git config --local commit.template .gitmessage.txt
