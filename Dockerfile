FROM python:3.11

RUN mkdir /INFO_ABOUT_BOOK_API

WORKDIR /INFO_ABOUT_BOOK_API

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . .

CMD ["python", "main.py", "--bind=0.0.0.0:8000"]