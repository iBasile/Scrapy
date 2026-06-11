import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

# ==========================================
# CONFIGURATION
# ==========================================

URL_DEPART = "https://example.com"

DOSSIER_SORTIE = "backup"

USER_AGENT = {
    "User-Agent": "Scrappy/1.0"
}

URL_DEPART = input("URL de départ : ")
DOSSIER_SORTIE = input("Dossier de sortie : ")

# ==========================================
# OUTILS
# ==========================================

def nettoyer_nom_fichier(nom):
    nom = re.sub(r'[<>:"/\\|?*]', "_", nom)
    return nom[:200]

def url_vers_nom_dossier(url):
    parsed = urlparse(url)

    chemin = parsed.path.strip("/")

    if not chemin:
        chemin = "accueil"

    return nettoyer_nom_fichier(chemin)

def extraire_texte(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    lignes = []

    for element in soup.find_all([
        "h1", "h2", "h3", "h4", "h5", "h6",
        "p", "li", "blockquote"
    ]):
        texte = element.get_text(" ", strip=True)

        if texte:
            lignes.append(texte)
            lignes.append("")

    return "\n".join(lignes)

def telecharger_image(url_image, dossier):
    try:
        r = requests.get(
            url_image,
            headers=USER_AGENT,
            timeout=20
        )

        if r.status_code != 200:
            return

        nom = os.path.basename(
            urlparse(url_image).path
        )

        if not nom:
            nom = "image.jpg"

        nom = nettoyer_nom_fichier(nom)

        chemin = os.path.join(dossier, nom)

        with open(chemin, "wb") as f:
            f.write(r.content)

        print(f"    Image : {nom}")

    except Exception as e:
        print(f"    Erreur image : {e}")

# ==========================================
# EXPLORATION
# ==========================================

def sauvegarder_page(url, domaine):
    print(f"\nAnalyse : {url}")

    try:
        r = requests.get(
            url,
            headers=USER_AGENT,
            timeout=20
        )

        r.raise_for_status()

    except Exception as e:
        print(f"Erreur : {e}")
        return [], False

    soup = BeautifulSoup(r.text, "html.parser")

    nom_dossier = url_vers_nom_dossier(url)

    dossier_page = os.path.join(
        DOSSIER_SORTIE,
        nom_dossier
    )

    os.makedirs(dossier_page, exist_ok=True)

    # ==========================
    # Sauvegarde texte
    # ==========================

    texte = extraire_texte(r.text)

    with open(
        os.path.join(dossier_page, "contenu.txt"),
        "w",
        encoding="utf-8"
    ) as f:
        f.write(texte)

    # ==========================
    # Images
    # ==========================

    for img in soup.find_all("img"):
        src = img.get("src")

        if not src:
            continue

        url_img = urljoin(url, src)

        telecharger_image(
            url_img,
            dossier_page
        )

    # ==========================
    # Liens internes
    # ==========================

    liens = []

    for a in soup.find_all("a", href=True):

        href = a["href"]

        lien = urljoin(url, href)

        parsed = urlparse(lien)

        if parsed.scheme not in ("http", "https"):
            continue

        if parsed.netloc != domaine:
            continue

        lien = (
            parsed.scheme
            + "://"
            + parsed.netloc
            + parsed.path
        )

        liens.append(lien)

    return liens, True

# ==========================================
# PROGRAMME PRINCIPAL
# ==========================================

def main():

    os.makedirs(
        DOSSIER_SORTIE,
        exist_ok=True
    )

    domaine = urlparse(URL_DEPART).netloc

    a_visiter = deque([URL_DEPART])

    visites = set()

    while a_visiter:

        url = a_visiter.popleft()

        if url in visites:
            continue

        visites.add(url)

        nouveaux_liens, ok = sauvegarder_page(
            url,
            domaine
        )

        if not ok:
            continue

        for lien in nouveaux_liens:

            if lien not in visites:
                a_visiter.append(lien)

    print("\nTerminé.")
    print(f"Pages visitées : {len(visites)}")

if __name__ == "__main__":
    main()
