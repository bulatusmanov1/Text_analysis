FROM python:3.12-bookworm

WORKDIR /app

RUN pip install poetry

COPY . .
RUN poetry install

CMD ["poetry", "run", "python3"]
