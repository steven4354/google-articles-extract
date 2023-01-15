import os
from sentence_transformers import SentenceTransformer, util
import torch
import hashlib
import pinecone
from scipy.spatial.distance import cosine
import time

print(os.environ.get('PINECONE_API_KEY'))

pinecone.init(api_key=os.environ.get('PINECONE_API_KEY'), environment="us-west1-gcp")

index_name = "search1"

if index_name in pinecone.list_indexes():
    print(f"Index {index_name} already exists.")
else:
    # dimension is from 'all-MiniLM-L6-v2' chatgpt said it was 768
    pinecone.create_index(index_name, dimension=768, metric="cosine", pod_type="p1")
    print(f"Index {index_name} created successfully.")

index = pinecone.Index(index_name) 

model = SentenceTransformer('all-MiniLM-L6-v2')

folder_path = "read"
sentences1 = []
sentences2 = ["What companies does Thrasio own? Or what companies did Thrasio buy or acquire?"]

# Iterate over all files in the directory
for filename in os.listdir(folder_path):
    # Check if the file is a .txt file
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        # Open the file
        with open(file_path, "r") as file:
            # Read the contents of the file into a variable
            file_contents = file.read()
            # Split the contents of the file by newline character
            rows = file_contents.split("\n")
            # Iterate over each string in the list
            for i in range(len(rows)):
                # Strip leading and trailing spaces
                rows[i] = rows[i].strip()
            # Convert the rows list into an array
            array = list(rows)
            
            # Print the array
            # print(array)

            # Add the array to the list of sentences
            sentences1.append(array)

# Compute embedding for setnences
embeddings1 = model.encode(sentences1, convert_to_tensor=True)
embeddings2 = model.encode(sentences2, convert_to_tensor=True)

# take the first item from embeddings2 and print it
print(embeddings2[0])

# pinecone upsert
start_time = time.time()
print("Uploading embeddings to Pinecone...")
index.upsert(
    vectors=zip(range(len(sentences1)), embeddings1.tolist())
)
end_time = time.time()

total_time = end_time - start_time
print("Total execution time:", total_time)

# Find the closest n sentences to the one in sentences2
closest_n = 10
top_n = []
for i, embedding in enumerate(embeddings1):
    similarity = 1 - cosine(embeddings2[0], embedding)
    top_n.append((sentences1[i], similarity))

top_n = sorted(top_n, key=lambda x: x[1], reverse=True)[:closest_n]

# Print the top n matching sentences
for i in range(closest_n):
    print(top_n[i][0])

# Compute cosine-similarits
# cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2[0])

# indexes = sorted(map(lambda x: x[0], enumerate(cosine_scores)), key=lambda x: cosine_scores[x][0], reverse=True)

# print(indexes)