import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF
import os
import io

# === CONFIGURATION ===
CARTE_LARGEUR, CARTE_HAUTEUR = 600, 350
FONT_PATH = "fonts/arial.ttf"

def creer_carte(nom, prenom, matricule, photo_file):
    carte = Image.new("RGB", (CARTE_LARGEUR, CARTE_HAUTEUR), (255, 255, 255))
    draw = ImageDraw.Draw(carte)

    # Charger la photo si elle existe
    if photo_file:
        try:
            photo = Image.open(photo_file).resize((120, 160))
            carte.paste(photo, (30, 95))
        except:
            pass

    # Texte
    try:
        font = ImageFont.truetype(FONT_PATH, 24)
    except:
        font = ImageFont.load_default()

    draw.text((180, 100), f"Nom : {nom}", fill="black", font=font)
    draw.text((180, 150), f"Prénom : {prenom}", fill="black", font=font)
    draw.text((180, 200), f"Matricule : {matricule}", fill="black", font=font)

    return carte

# === INTERFACE ===
st.title("🎓 Générateur de Cartes Étudiants")
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

        buf = io.BytesIO()
        carte.save(buf, format="JPEG")
        buf.seek(0)
        pdf.add_page()
        pdf.image(buf, x=0, y=0, w=CARTE_LARGEUR, h=CARTE_HAUTEUR)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    st.success("✅ PDF généré avec succès !")
    st.download_button("📥 Télécharger le PDF", data=pdf_bytes, file_name="cartes_etudiants.pdf")
