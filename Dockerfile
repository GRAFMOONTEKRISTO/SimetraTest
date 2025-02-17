FROM python:3.10

WORKDIR /test_task

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .


EXPOSE 80
CMD ["uvicorn", "--reload", "src.main.server:app", "--host", "0.0.0.0", "--port", "80"]

