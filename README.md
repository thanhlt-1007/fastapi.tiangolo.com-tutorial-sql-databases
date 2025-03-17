# fastapi.tiangolo.com-tutorial-sql-databases

- SQL (Relational) Databases

- Reference: https://fastapi.tiangolo.com/tutorial/sql-databases/

## pyenv

```sh
pyenv install 3.11
pyenv global 3.11
```

## poetry

```sh
pipx install --suffix=@1.8.2 poetry==1.8.2
pipx ensurepath
source ~/.bashrc
poetry@1.8.2 --version
```

## venv

```sh
poetry@1.8.2 env use 3.11
poetry@1.8.2 run python --version
```

## Install

```sh
poetry@1.8.2 install
```

## FastAPI

```sh
poetry@1.8.2 run fastapi dev src/sql_databases/main.py
```
