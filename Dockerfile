FROM python:3.10
RUN mkdir -p /sl_aiohttp
WORKDIR /sl_aiohttp

COPY ./ ./
RUN pip install -r requirements.txt

EXPOSE 9000


ENV PYTHONPATH "${PYTHONPATH}:/sl_aiohttp"
ENV PYTHONUNBUFFERED 1

CMD python src/main.py