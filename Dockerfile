FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "-m", "flask", "--app", "app.py", "run", "-h", "0.0.0.0", "-p", "8081"]
