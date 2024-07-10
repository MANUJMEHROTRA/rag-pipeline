from pymongo import MongoClient,DESCENDING
from datetime import datetime
import json
from openai import OpenAI
client_openAI = OpenAI()

# Connect to MongoDB
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.fmcg_company
faqs_collection = db.faqs


# Define dummy text for search
dummy_text = "What is the process for returning an item?"

# Generate embedding for dummy text
def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client_openAI.embeddings.create(input = [text], model=model).data[0].embedding

dumm_embedding = get_embedding(dummy_text)

# Find similar FAQs using cosine similarity and sort by score (descending)
similar_faqs = faqs_collection.find({
    "$expr": {
        "$gt": [
            { "$dot": ["$question_embedding", dumm_embedding] },  # Cosine similarity
            0.4 # Threshold for similarity (adjust as needed)
        ]
    }
}).sort([("$expr", DESCENDING)])  # Sort by cosine similarity score (descending)

print(similar_faqs)
# Limit results to top 3
top_3_faqs = list(similar_faqs.limit(3))  # Convert cursor to list and limit

# Process and display results
for faq in top_3_faqs:
    print(f"Question: {faq['question']}")
    print(f"Answer: {faq['answer']}")
    print("-" * 20)
