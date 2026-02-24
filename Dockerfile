FROM ubuntu:latest
LABEL authors="sarah"

ENTRYPOINT ["top", "-b"]
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]