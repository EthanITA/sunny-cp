#!/bin/bash

# packages
sudo apt update
sudo apt install -y python3 flex bison minizinc

# python libraries
pip install -r requirements.txt

# mzn2feat install
git clone --depth=1 https://github.com/CP-Unibo/mzn2feat.git && bash ./mzn2feat/install --no-xcsp && rm -rf ./mzn2feat/.git