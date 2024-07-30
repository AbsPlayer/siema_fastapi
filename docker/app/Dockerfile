FROM python:3.10

WORKDIR /app

COPY ../../app/requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ../../app /app

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "app.main:app", "--reload"]
