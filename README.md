# FIFA PREDICTIOR

## Set up pyenv

Add those commands below to your shell

```
export PYENV_ROOT="$HOME/.pyenv
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

## Set up python with pyenv

Python version will be specified with ".python_env" file in current directory

```
pyenv install
```

## Install Make

For Mac

```sh
brew install make
```

For Debian

```sh
apt update && apt install make
```

## Instructions

Set up venv for Python in the current directory

```sh
python3 -m venv .venv
source .venv/bin/activate
```

### Install wheel

```sh
pip install wheel
```

### Install Requirements

```sh
pip install -r dev_requirements.txt
pip install -r requirements.txt
```

### Setup project

```sh
make local-install
```


