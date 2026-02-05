import os
from PIL import Image, ImageDraw, ImageFont
from rembg import remove

def creer_carte_pro(chemin_photo_joueur, chemin_fond):
    # --- 1. Extraction du nom (comme avant) ---
    nom_fichier = os.path.basename(chemin_photo_joueur)
    nom_sans_ext = os.path.splitext(nom_fichier)[0]
    parts = nom_sans_ext.split('_')
    
    # Logique pour récupérer le nom (ex: MHB_PRENOM_NOM)
    try:
        # On essaie de prendre les parties 2 et 3
        nom_complet = " ".join(parts[2:4]).replace('-', ' ').upper()
        if not nom_complet: raise IndexError
    except IndexError:
        nom_complet = nom_sans_ext.replace('_', ' ').upper()

    # --- 2. Préparation du fond ---
    fond = Image.open(chemin_fond).convert("RGBA")
    W, H = fond.size # Dimensions du fond (Largeur, Hauteur)

    # --- 3. Traitement du Joueur ---
    print(f"Traitement de : {nom_complet}...")
    img_joueur = Image.open(chemin_photo_joueur)
    
    # Détourage
    joueur_detoure = remove(img_joueur).convert("RGBA")

    # --- 4. Redimensionnement INTELLIGENT ---
    # On veut que le joueur remplisse environ 90% à 100% de la largeur de la carte
    # pour donner cet effet "imposant" comme sur l'exemple Tyra Axner.
    ratio_zoom = 1.0 # 1.0 = 100% de la largeur du fond
    
    largeur_souhaitee = int(W * ratio_zoom)
    # Calcul de la hauteur proportionnelle
    ratio_orig = largeur_souhaitee / float(joueur_detoure.size[0])
    hauteur_souhaitee = int(float(joueur_detoure.size[1]) * float(ratio_orig))
    
    joueur_final = joueur_detoure.resize((largeur_souhaitee, hauteur_souhaitee), Image.Resampling.LANCZOS)

    # --- 5. Positionnement (L'ANCRAGE EN BAS) ---
    # Centrer horizontalement
    pos_x = (W - largeur_souhaitee) // 2
    
    # Pour la verticale : on veut que le BAS du joueur touche le BAS de la carte
    # On ajoute un petit décalage (offset) si on veut qu'il soit un peu plus bas ou haut
    # Si la photo est coupée au cou, il faut la coller tout en bas.
    offset_bas = 0 
    pos_y = H - hauteur_souhaitee - offset_bas

    # Si le visage se retrouve trop bas (car la photo originale est très longue), 
    # on peut forcer une position minimale pour la tête.
    # (Optionnel, à activer si besoin)
    # if pos_y < 100: pos_y = 100 

    # --- 6. Assemblage ---
    composition = Image.new("RGBA", fond.size)
    composition.paste(fond, (0, 0))
    # Collage du joueur (le 3ème argument sert de masque de transparence)
    composition.paste(joueur_final, (pos_x, pos_y), joueur_final)

    # --- 7. Ajout du Texte (Le Nom) ---
    draw = ImageDraw.Draw(composition)
    
    # Chargement d'une police (Essaye Arial, sinon defaut)
    try:
        # Sur Windows, arialbd.ttf est souvent "Arial Bold"
        font_size = 60 # Taille à ajuster selon la taille de votre image de fond
        font = ImageFont.truetype("arialbd.ttf", font_size)
        # Si vous voulez une police plus "sport", téléchargez un fichier .ttf (ex: "Impact") 
        # et mettez le chemin ici : "C:/Fonts/Impact.ttf"
    except IOError:
        font = ImageFont.load_default()
        print("Police non trouvée, utilisation police par défaut.")

    # Calculer la taille du texte pour le centrer
    bbox = draw.textbbox((0, 0), nom_complet, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Position du texte : Centré horizontalement, et en bas (sur le chevron bleu)
    text_x = (W - text_width) / 2
    text_y = H - 100 # Remonte de 100px depuis le bas (Ajustez selon votre chevron)
    
    # Dessiner le texte (en blanc)
    # On peut ajouter une petite ombre noire pour la lisibilité
    draw.text((text_x + 2, text_y + 2), nom_complet, font=font, fill="black")
    draw.text((text_x, text_y), nom_complet, font=font, fill="white")

    # --- 8. Sauvegarde ---
    nom_sortie = f"carte_fini_{nom_complet.replace(' ', '_')}.png"
    composition.save(nom_sortie)
    print(f"Carte terminée : {nom_sortie}")

# --- EXEMPLE D'UTILISATION ---
input_img = r"C:/Chemin/Vers/Votre/Photo.png" 
bg_img = r"C:/Chemin/Vers/Votre/Fond.png"

# creer_carte_pro(input_img, bg_img)