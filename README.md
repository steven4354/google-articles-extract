```
source .env \
&& docker build -t google-articles . \
--build-arg PINECONE_API_KEY=$PINECONE_API_KEY \
&& docker run -v $(pwd):/app google-articles
```

logs should show up if you use python print