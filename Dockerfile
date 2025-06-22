FROM python:3.11
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
COPY README.md ./
COPY PyTado ./PyTado
RUN poetry install
COPY . .
CMD ["poetry", "run", "python", "hello_world.py"]
