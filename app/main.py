import streamlit as st
from PIL import Image
import os
import sys

# Ajoute le chemin du projet au PATHs
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scoring import calculate_style_score
from color_utils import get_dominant_color, are_complementary

# Configuration de la page
st.set_page_config(page_title="OutfitAI", page_icon="👗")
st.title("🎨 OutfitAI ")
st.write("Upload tes vêtements pour obtenir un score de style !")

# Sidebar pour les paramètres
with st.sidebar:
    st.header("Paramètres")
    weather = st.selectbox("Météo", ["sun", "rain", "cold", "normal"])
    debug_mode = st.checkbox("Mode Debug")

# Zone d'upload
col1, col2 = st.columns(2)
with col1:
    top = st.file_uploader("Haut (t-shirt, chemise...)", type=["jpg", "png", "jpeg"])
with col2:
    bottom = st.file_uploader("Bas (jean, jupe...)", type=["jpg", "png", "jpeg"])

# Calcul du score
if st.button("Évaluer la tenue") and top and bottom:
    # Sauvegarde temporaire
    top_path = f"temp_top.{top.name.split('.')[-1]}"
    bottom_path = f"temp_bottom.{bottom.name.split('.')[-1]}"
    
    with open(top_path, "wb") as f:
        f.write(top.getbuffer())
    with open(bottom_path, "wb") as f:
        f.write(bottom.getbuffer())

    try:
        # Calcul et affichage
        score = calculate_style_score(top_path, bottom_path, weather)
        
        st.success("✅ Analyse terminée !")
        st.metric("Score de style", f"{score}/100")
        st.progress(score / 100)
        
        # Affichage des images
        st.image([Image.open(top_path), Image.open(bottom_path)], 
                caption=["Haut", "Bas"], width=200)
        
        # Debug (optionnel)
        if debug_mode:
            top_color = get_dominant_color(top_path)
            bottom_color = get_dominant_color(bottom_path)
            st.write(f"🔍 Debug - Couleurs : {top_color} (haut) / {bottom_color} (bas)")
            st.write(f"🔍 Debug - Complémentaires : {are_complementary(top_color, bottom_color)}")
    
    except Exception as e:
        st.error(f"🚨 Erreur : {str(e)}")
    finally:
        # Nettoyage
        if os.path.exists(top_path):
            os.remove(top_path)
        if os.path.exists(bottom_path):
            os.remove(bottom_path)
