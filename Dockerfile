FROM python:3.9

RUN mkdir /langchain
WORKDIR /langchain
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD gunicorn --workers 1 --worker-class uvicorn.workers.UvicornWorker app.main:app --bind=0.0.0.0:8000
