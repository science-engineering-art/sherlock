FROM docker.uclv.cu/python:3.9

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

RUN python -m spacy download en_core_web_sm

COPY ./models /src/models

COPY ./main.py /src/main.py

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]