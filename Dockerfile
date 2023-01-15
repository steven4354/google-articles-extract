FROM python:3.8

# Set the environment variables using the values from the .env file
ARG PINECONE_API_KEY
ENV PINECONE_API_KEY=$PINECONE_API_KEY

COPY . /app/
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod +x run.sh
ENTRYPOINT ["sh", "/app/run.sh"]
VOLUME /app
