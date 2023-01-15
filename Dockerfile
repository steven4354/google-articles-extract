FROM python:3.8
COPY . /app/
RUN pip install requests bs4 nltk serpapi
WORKDIR /app
RUN chmod +x run.sh
ENTRYPOINT ["sh", "/app/run.sh"]
VOLUME /app
