FROM python:3.10.5

RUN useradd --create-home userapi
WORKDIR /SL_aiohttp

RUN pip install -U pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system
COPY ./ .


EXPOSE 5432
