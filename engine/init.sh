#!/bin/bash

### installs Python 3.10.0
sudo apt install -y git python3-pip make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl
git clone https://github.com/yyuu/pyenv.git ~/.pyenv

export PATH="~/.pyenv/bin:$PATH"
source ~/.bashrc
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
# setup py3.10.0 as global
pyenv install 3.10.0
pyenv global 3.10.0


### setup venv
python3.10 -m pip install --user virtualenv
python3.10 -m virtualenv venv && source ./venv/bin/activate && pip install -r ./requirements.txt
