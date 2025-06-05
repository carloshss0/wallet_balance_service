FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
&& poetry install --no-root


COPY ./src /app/src

# ENV DATABASE_URL=sqlite:///./wallet_balance.db

EXPOSE 3003

CMD ["uvicorn", "wallet_balance_service.main:app", "--host", "0.0.0.0", "--port", "3003", "--reload", "--app-dir", "src"]
