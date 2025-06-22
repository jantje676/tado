FROM python:3.11
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev
COPY . .
CMD ["poetry", "run", "python", "hello_world.py"]
