import streamlit as st
from sentence_transformers import SentenceTransformer
from hybrid_chunking import hybrid_chunk_transcript
from extract import get_transcript_youtube
import faiss
import numpy as np
import requests
import os

# --- Page config ---
st.set_page_config(page_title="YouTube Q&A", layout="centered")
st.title("🎥 YouTube Semantic Q&A")
st.markdown("Paste a YouTube video link, ask questions, and get AI-generated answers based on the transcript.")

# --- Cached model load ---
@st.cache_resource
def load_model():
    import torch  # Local import to avoid Streamlit scanning
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()

# --- Input YouTube URL ---
youtube_url = st.text_input("Enter a YouTube video URL:")

# --- API Key load (env or secrets) ---
api_key = os.getenv("TOGETHER_API_KEY") or st.secrets.get("TOGETHER_API_KEY")

if youtube_url:
    with st.spinner(" Fetching transcript from YouTube..."):
        transcript = get_transcript_youtube(youtube_url)

    if transcript.startswith("[ERROR]"):
        st.error(" Failed to fetch transcript. Please check the URL.")
        st.stop()

    with st.spinner(" Chunking transcript..."):
        chunks = hybrid_chunk_transcript(transcript)

    with st.spinner(" Embedding chunks..."):
        embeddings = model.encode(chunks)
        embeddings_np = np.array(embeddings).astype('float32')

    # --- FAISS index creation ---
    index = faiss.IndexFlatL2(embeddings_np.shape[1])
    index.add(embeddings_np)

    st.success(" Transcript is ready! Ask a question below.")

    # --- Input question ---
    question = st.text_input(" Ask a question about the video:")

    if question:
        with st.spinner("🔎 Retrieving relevant content..."):
            query_embedding = model.encode([question]).astype('float32')
            k = 5
            distances, indices = index.search(query_embedding, k)
            retrieved_chunks = [chunks[i] for i in indices[0]]
            context = "\n".join(retrieved_chunks)

        # --- Prompt formatting ---
        prompt = f"""
Answer the question based on the context below.

Context:
{context}

Question: {question}
Answer:
"""

        if not api_key:
            st.warning("🔑 Please set your Together API key via environment variable or Streamlit secrets.")
        else:
            with st.spinner("🤖 Generating answer with Mistral-7B..."):
                response = requests.post(
                    "https://api.together.xyz/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": "mistralai/Mistral-7B-Instruct-v0.1",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 500,
                        "temperature": 0.7
                    }
                )

            if response.status_code == 200:
                try:
                    answer = response.json()['choices'][0]['message']['content']
                    st.subheader(" Answer:")
                    st.write(answer.strip())
                except Exception as e:
                    st.error("⚠️ Failed to parse response from Together API.")
                    st.text(response.text)
            else:
                st.error(f"❌ API Error: {response.status_code}")
                st.text(response.text)
