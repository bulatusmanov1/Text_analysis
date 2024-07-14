FROM python:3.12-bookworm

WORKDIR /app
COPY . .

RUN pip install poetry
RUN poetry lock
RUN poetry install

CMD ["poetry", "run", "python3"]
