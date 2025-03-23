import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF
import os
import tempfile

# === CONFIGURATION ===
CARTE_LARGEUR, CARTE_HAUTEUR = 1200, 700
FONT_PATH = "fonts/arial.ttf"

def creer_carte(nom, prenom, matricule, photo_file):
    carte = Image.new("RGB", (CARTE_LARGEUR, CARTE_HAUTEUR), (255, 255, 255))
    draw = ImageDraw.Draw(carte)

    # Charger la photo si elle existe
    if photo_file:
        try:
            photo = Image.open(photo_file).resize((240, 320))  # 2x résolution
            carte.paste(photo, (60, 190))
        except:
            pass

    # Texte
    try:
        font = ImageFont.truetype(FONT_PATH, 48)  # taille double
    except:
        font = ImageFont.load_default()

    draw.text((360, 200), f"Nom : {nom}", fill="black", font=font)
    draw.text((360, 300), f"Prénom : {prenom}", fill="black", font=font)
    draw.text((360, 400), f"Matricule : {matricule}", fill="black", font=font)

    return carte

# === INTERFACE ===
st.title("🎓 Générateur de Cartes Étudiants (Haute Qualité)")
excel_file = st.file_uploader("📄 Importer le fichier Excel", type=["xlsx"])
photos = st.file_uploader("🖼️ Importer les photos", accept_multiple_files=True)

if excel_file and photos:
    df = pd.read_excel(excel_file)
    photo_dict = {p.name: p for p in photos}
    pdf = FPDF(unit="pt", format=[CARTE_LARGEUR, CARTE_HAUTEUR])

    for _, row in df.iterrows():
        nom = row["Nom"]
        prenom = row["Prénom"]
        matricule = str(row["Matricule"])
        photo_file = photo_dict.get(row["Photo"])

        carte = creer_carte(nom, prenom, matricule, photo_file)

        # Sauvegarder l'image temporairement avec haute qualité
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmpfile:
            carte.save(tmpfile.name, format="JPEG", quality=95, subsampling=0)
            pdf.add_page()
            pdf.image(tmpfile.name, x=0, y=0, w=CARTE_LARGEUR, h=CARTE_HAUTEUR)

    # Générer le PDF en mémoire
    output_path = "cartes_etudiants_haute_qualite.pdf"
    pdf.output(output_path)
    with open(output_path, "rb") as f:
        st.success("✅ PDF haute qualité généré avec succès !")
        st.download_button("📥 Télécharger le PDF", data=f, file_name=output_path)
