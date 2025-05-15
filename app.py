import streamlit as st
import requests
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# Función para obtener la letra
def get_lyrics(artist, title):
    url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("lyrics", "")
    else:
        return None

# Función para limpiar texto
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-záéíóúüñ\s]', '', text)
    words = text.split()
    all_stopwords = set(stopwords.words('spanish')) | set(stopwords.words('english'))
    return [word for word in words if word not in all_stopwords]

# Interfaz Streamlit
st.title("Análisis de Letras de Canciones 🎵")

artist = st.text_input("Introduce el nombre del artista:", "Bad Bunny")
title = st.text_input("Introduce el título de la canción:", "DtMF")

if st.button("Analizar letra"):
    lyrics = get_lyrics(artist, title)
    if lyrics:
        st.subheader("Letra de la canción:")
        st.text(lyrics[:1000] + "..." if len(lyrics) > 1000 else lyrics)

        words = clean_text(lyrics)
        freq = Counter(words)

        # Mostrar WordCloud
        st.subheader("Nube de palabras:")
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words))
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)

        # Mostrar Top 10
        st.subheader("Top 10 palabras más frecuentes:")
        for word, count in freq.most_common(10):
            st.write(f"{word}: {count}")
    else:
        st.error("Letra no encontrada.")
