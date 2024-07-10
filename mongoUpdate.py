from pymongo import MongoClient
from datetime import datetime
import json
from openai import OpenAI
client_openAI = OpenAI()



# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.fmcg_company
faqs_collection = db.faqs


faq_json = './data/faq.json'

with open(faq_json, 'r') as file:
    faqs = json.load(file)

print(faqs)

# Function to generate embeddings
# def generate_embeddings(text):
def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client_openAI.embeddings.create(input = [text], model=model).data[0].embedding

faqs_embed = []

for faq in faqs:
    question_embedding = get_embedding(faq['question'])
    answer_embedding = get_embedding(faq['answer'])
    faq["question_embedding"] =  question_embedding
    faq["answer_embedding"]= answer_embedding
    faqs_embed
    print("Embeddings added successfully")

faqs_collection.insert_many(faqs)
print("FAQs inserted successfully")