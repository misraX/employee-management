FROM python:3.12

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv

RUN pipenv requirements > requirements.txt

RUN pip install -r requirements.txt

COPY . /app/

CMD ["python", "main.py"]
