import streamlit as st
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from huggingface_hub import login
import dotenv

st.write(open("markdowns/intro.md").read())
st.image("images/materials_diagram.png")

dotenv.load_dotenv()

token = os.getenv('PALIGEMMATOKEN')

login(token=token, add_to_git_credential=True)

from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
import requests
import torch
from PIL import Image

# Select which model to use
model_id = 'google/paligemma-3b-mix-224'


# Setting up the initial model
model = PaliGemmaForConditionalGeneration.from_pretrained(model_id)
processor = AutoProcessor.from_pretrained(model_id)

image = st.file_uploader("Upload an image", type=["jpg", "png"])

prompt = 'Are there containers in the image?'

# Code if image is uploaded
if image is not None:
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    
    # Convert image to PIL format
    image = Image.open(image)
    
    # Generate the inputs
    inputs = processor(prompt, image, return_tensors="pt")

    # Generate the outputs
    outputs = model.generate(**inputs, max_new_tokens=250)
    # Print the outputs
    st.write(prompt + " : " + processor.decode(outputs[0], skip_special_tokens=True)[len(prompt):])

material = st.text_input("Enter the description of the material")

path = "data_git/"

# Check if files exist at the specified paths
if not os.path.exists(os.path.join(path, 'materials.csv')):
    st.error("Materials data file not found.")
    st.stop()

if not os.path.exists(os.path.join(path, 'material_desc.csv')):
    st.error("Material descriptions data file not found.")
    st.stop()

# Load the data
materials = pd.read_csv(path + 'materials.csv')
material_desc_df = pd.read_csv(path + 'material_desc.csv')

# Initialize the TfidfVectorizer 
tfidf = TfidfVectorizer()

# Corpus
corpus = material_desc_df['text'].to_list()

# Add new material to corpus
corpus.append(material)
# Construct the TF-IDF matrix
tfidf_matrix = tfidf.fit_transform(corpus)
# Generate the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix,tfidf_matrix)

# Get scores of the last material
sim_scores = list(enumerate(cosine_sim[-1]))

# Sort the materials based on the similarity scores
sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

# Get the scores for 10 most similar materials
sim_scores = sim_scores[1:11]

# Get the material indices
material_indices = [i[0] for i in sim_scores]

# Return the top 10 most similar materials
top_n_scores = material_desc_df['product_id'].iloc[material_indices]

# Create DataFrame with top 10 most similar materials and their scores
top_n_scores_df = pd.DataFrame({'product_id': top_n_scores, 'similarity_score': [i[1] for i in sim_scores]})

# Merge with materials DataFrame to get material details
result = pd.merge(top_n_scores_df, materials, on='product_id')

# This single line of text with the df prints the table
result

material = st.text_input("Enter the formula used for this material")
