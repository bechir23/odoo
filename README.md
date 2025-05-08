# Module Odoo - Gestion des Stages Académiques

## Présentation Générale

Ce module Odoo 16 permet de gérer l'ensemble du processus de suivi des stages académiques : étudiants, entreprises, candidatures, stages, rapports, conventions, analyse automatique (OCR), et tableaux de bord analytiques. Il offre une interface moderne, centralisée et adaptée aux besoins des établissements universitaires.

## Installation (Windows, Python 3.12, Odoo 16)

### 1. Prérequis
- Python 3.12
- Git
- PostgreSQL
- Tesseract OCR (https://github.com/tesseract-ocr/tesseract)

### 2. Création de l'environnement virtuel
```bash
cd C:\Bureau\odoo_project
python -m venv venv
cd venv\Scripts
activate.bat
cd ..
```

### 3. Clonage d'Odoo 16
```bash
git clone https://github.com/odoo/odoo.git --depth 1 --branch 16.0 odoo-16
```

### 4. Installation des dépendances Python
- Installez d'abord les dépendances Odoo :
```bash
cd odoo-16
pip install -r requirements.txt
cd ..
```
- Ajoutez à `requirements.txt` (à la racine du projet ou dans custom-addons) :
```
pytesseract>=0.3.8
pdf2image>=1.16.0
Pillow>=8.3.1
PyPDF2>=2.0.0
```
Installez :
```bash
pip install -r requirements.txt
```

### 5. Installation de Tesseract
- Installez Tesseract OCR et ajoutez le chemin de `tesseract.exe` à la variable d'environnement PATH.

### 6. Placement du module
- Placez le dossier `internship_management` dans `custom-addons/`.

### 7. Lancement d'Odoo
```bash
cd odoo-16
python odoo-bin -c odoo.conf --addons-path=../custom-addons,addons
```

## Fonctionnalités détaillées

### 1. Gestion des étudiants
- Création/modification d'une fiche étudiant (nom, numéro, email, téléphone, filière, niveau).
- Ajout d'un CV (PDF ou image) avec extraction automatique du texte via OCR (PyPDF2, pytesseract).
- Visualisation de tous les stages réalisés par l'étudiant.
- Accès rapide aux candidatures et rapports associés.

### 2. Gestion des entreprises
- Création/modification d'une fiche entreprise (nom, secteur, adresse, site web, contact, email, téléphone).
- Visualisation de tous les stages réalisés dans l'entreprise.

### 3. Gestion des stages
- Création d'un stage lié à un étudiant, une entreprise, un tuteur académique et professionnel.
- Saisie du sujet, description, dates, signatures électroniques.
- Suivi du statut : En attente, En cours, Terminé, Annulé.
- Génération automatique de la convention de stage (PDF) depuis un template QWeb, avec toutes les informations et signatures.
- Envoi de la convention par email et notification SMS (Twilio).

### 4. Gestion des candidatures
- Un étudiant peut postuler à un stage, joindre un CV et une lettre de motivation.
- Questions personnalisées par stage (texte, choix multiples, cases à cocher, date, etc.).
- Stockage des réponses pour chaque candidature.
- Suivi du statut de la candidature : Nouveau, En cours, Entretien, Accepté, Rejeté.

### 5. Gestion des rapports de stage
- Téléversement du rapport (PDF ou image) par l'étudiant.
- Extraction automatique du texte du rapport (OCR pour images, extraction texte pour PDF).
- Détection automatique des sections obligatoires (introduction, objectifs, résultats, conclusion, etc.).
- Feedback et validation/rejet par le tuteur.
- Suivi du statut du rapport : Brouillon, Soumis, Validé, Rejeté.

### 6. Sections obligatoires de rapport
- Définition des sections attendues (nom, description, séquence, obligatoire).
- Vérification automatique de leur présence dans le rapport via OCR.

### 7. Tableaux de bord et analyses
- Dashboard interactif :
  - KPIs (nombre total de stages, en cours, terminés, en attente, annulés)
  - Graphiques : répartition par statut, entreprise, filière, évolution mensuelle
  - Tableau croisé dynamique : analyse par tuteur académique et statut
  - Liste des stages récents
- Filtres dynamiques : statut, entreprise, filière, période

### 8. Sécurité et accès
- Gestion des droits par rôle (étudiant, tuteur, administrateur)
- Historique des actions (chatter, activités)

### 9. Données de démonstration
- Le dossier `demo/` contient des étudiants, entreprises, stages, candidatures, questions, réponses et rapports pré-remplis pour tester toutes les fonctionnalités.

## Utilisation pas à pas

### Ajouter un étudiant
1. Aller dans le menu "Étudiants".
2. Cliquer sur "Créer" et remplir les champs (nom, email, filière, etc.).
3. Ajouter un CV (PDF ou image) : le texte sera extrait automatiquement.

### Ajouter une entreprise
1. Aller dans le menu "Entreprises".
2. Cliquer sur "Créer" et renseigner les informations (nom, secteur, contact, etc.).

### Créer un stage
1. Aller dans le menu "Stages".
2. Cliquer sur "Créer".
3. Sélectionner l'étudiant, l'entreprise, les tuteurs, saisir le sujet, les dates, etc.
4. Générer la convention PDF et la faire signer.

### Gérer les candidatures
1. Aller dans le menu "Candidatures".
2. Cliquer sur "Créer" pour enregistrer une nouvelle candidature à un stage.
3. Répondre aux questions personnalisées si besoin.
4. Suivre le statut de la candidature.

### Gérer les rapports de stage
1. Aller dans le menu "Rapports".
2. Cliquer sur "Créer" pour déposer un rapport.
3. Lancer l'analyse OCR pour extraire le texte et vérifier les sections obligatoires.
4. Le tuteur peut valider ou rejeter le rapport et laisser un feedback.

### Utiliser le dashboard
1. Aller dans le menu "Dashboard".
2. Visualiser les indicateurs, graphiques, évolutions et analyses croisées.
3. Utiliser les filtres pour affiner l'analyse (statut, entreprise, filière, période).

## Structure des fichiers

- `models/` : tous les modèles Python (étudiant, entreprise, stage, candidature, rapport, section, question, réponse, utilitaires SMS)
- `views/` : vues Odoo (formulaires, listes, kanban, dashboard, menus)
- `report/` : templates QWeb pour PDF (convention)
- `security/` : droits d'accès
- `data/` : templates d'emails
- `demo/` : données de démonstration
- `static/` : images, JS, CSS pour dashboard
- `install.py` : script d'installation rapide

## Points techniques avancés
- Extraction OCR automatique (PyPDF2, pytesseract, pdf2image, Pillow)
- Génération de PDF dynamique (QWeb)
- Dashboard analytique interactif (KPIs, graphiques, pivot)
- Notifications SMS (Twilio) et emails
- Signature électronique
- Architecture MVC Odoo, code commenté et structuré

## Script d'installation rapide
```python
# custom-addons/internship_management/install.py
import os

def install():
    print("Installing Internship Management Module...")
    os.system('odoo-bin -u internship_management')
    print("Installation complete.")
```



## Vidéo de démonstration
👉 [Lien à insérer ici pour la vidéo de démonstration]

## Auteur
- Bechir Ben Tekfa
- Yassine Yahyaoui
- Med Yassine Ezzaouia
---
> Ce module propose une expérience complète, automatisée et analytique pour tous les acteurs du suivi académique.
