FROM python:3.12-slim-bookworm
WORKDIR /app
COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app/ /app
EXPOSE 80
CMD ["python", "app.py"]
