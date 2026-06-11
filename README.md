# Scrappy

## Présentation du projet

Scrappy est un utilitaire Python permettant de créer une archive locale d'un site web.

À partir d'une URL de départ, le programme explore automatiquement les pages internes du site, récupère leur contenu textuel et télécharge les images associées afin de constituer une sauvegarde du site.

Chaque page visitée est enregistrée dans son propre dossier contenant :

- Le contenu textuel de la page.
- Les images présentes sur la page.

---

## Fonctionnalités

- Exploration automatique des liens internes.
- Parcours récursif du site.
- Évitement des pages déjà visitées. (<- Je sais pas si cette phrase est française mais bon 😝)
- Sauvegarde du contenu textuel des pages.
- Téléchargement des images.
- Organisation automatique des données dans des dossiers.
- Fonctionnement sans base de données.

---

## Cas d'utilisation

Ce logiciel peut être utilisé pour :

- Archiver son propre site web.
- Conserver une copie locale avant une refonte.
- Réaliser des sauvegardes de contenu.
- Préparer une migration de site.
- Effectuer un audit de contenu.
- Conserver un historique des pages publiées.
- Voir si des liens sont corrompus sur le site

---

## Prérequis

- Python 3.9 ou supérieur
- Connexion Internet
- Permissions d'écriture sur le disque

---

## Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/iBasile/Scrapy.git
cd Scrappy
```

### 2. Créer un environnement virtuel Python
```python
python3 -m venv ScrapyVenv
```

### 3. Activer l'environnement virtuel
Sous Windows :
```powershell
tutorial-env\Scripts\activate
```
Sur Unix et MacOS, lancez :
```bash
source ScrapyVenv/bin/activate
```
### 4. Installer les dépendances :
```python
pip install requests beautifulsoup4
```
### 5. Lancer le script :
```python
python3 main.py
```

## Contact
Basile BARGIBANT
contact.basilebargibant@proton.me
