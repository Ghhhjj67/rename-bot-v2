FROM python:3.9.7-slim-buster
WORKDIR /app
RUN apt -qq update && apt -qq install -y git wget python3-dev
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
RUN chmod +x /app/start.sh
ENTRYPOINT ["./start.sh"]
