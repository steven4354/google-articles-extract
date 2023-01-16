```
source .env \
&& docker build -t google-articles . \
--build-arg PINECONE_API_KEY=$PINECONE_API_KEY \
&& docker run -v $(pwd):/app google-articles
```

logs should show up if you use python print

---

the rest of the cosine similarity code was completed here: https://github.com/steven4354/pinecone_cosine_test
