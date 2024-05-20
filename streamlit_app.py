import streamlit as st
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

st.write(open("markdowns/intro.md").read())
st.image("images/materials_diagram.png")

image = st.file_uploader("Upload an image", type=["jpg", "png"])

if image is not None:
    st.image(image, caption='Uploaded Image.', use_column_width=True)

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

result
