# Internship Management Odoo Module

## Description

Ce module Odoo (v16/v17 Community) permet la gestion complète des stages académiques pour les établissements universitaires. Il centralise la gestion des étudiants, entreprises partenaires, conventions, tuteurs, candidatures, questions, réponses et rapports de stage, tout en offrant des outils d'analyse et de suivi avancés.

## Fonctionnalités principales

- **Gestion des étudiants** :
  - Création, modification, consultation des fiches étudiants (Nom, Prénom, Email, Filière, Niveau, CV, etc.)
  - Extraction automatique du texte du CV (PDF/Image) via OCR
  - Suivi des stages réalisés par chaque étudiant

- **Gestion des entreprises** :
  - Base de données des entreprises partenaires (Nom, Contact, Email, Téléphone, Secteur, Adresse, etc.)
  - Suivi des stages proposés/réalisés par chaque entreprise

- **Gestion des stages** :
  - Création d'une fiche de stage liée à un étudiant, une entreprise, un tuteur académique et professionnel
  - Statuts du stage (En attente, En cours, Terminé, Annulé)
  - Génération automatique de la convention de stage (PDF depuis template QWeb)
  - Signature électronique (étudiant, tuteur académique, tuteur professionnel)
  - Dashboard analytique (KPIs, graphiques, évolution, répartition par entreprise/filière, etc.)
  - Notifications par email et SMS (Twilio)

- **Gestion des candidatures** :
  - Suivi des candidatures à un stage (étudiant, date, statut, lettre de motivation, CV)
  - Système de questions/réponses personnalisées pour chaque stage
  - Stockage des réponses (texte, choix multiples, etc.)

- **Gestion des rapports de stage** :
  - Téléversement du rapport par l'étudiant
  - Validation/feedback par le tuteur
  - Analyse automatique du rapport (OCR, détection des sections obligatoires)
  - Suivi de l'état du rapport (Brouillon, Soumis, Validé, Rejeté)

- **Gestion des sections obligatoires de rapport** :
  - Définition des sections attendues (introduction, objectifs, conclusion, etc.)
  - Vérification automatique de leur présence via OCR

- **Sécurité et accès** :
  - Contrôle d'accès par rôles (étudiant, tuteur, admin)
  - Historique et suivi des actions (chatter, activités)

- **Interface utilisateur** :
  - Vues Formulaire, Liste, Kanban, Dashboard, Graphique, Pivot
  - Menus clairs et navigation intuitive

## Structure du module

- `models/`
  - `student.py` : Modèle étudiant (internship.student)
  - `company.py` : Modèle entreprise (internship.company)
  - `internship.py` : Modèle stage (internship.internship)
  - `application.py` : Modèle candidature (internship.application)
  - `application_answer.py` : Réponses aux questions de candidature
  - `question.py` : Questions personnalisées pour les candidatures
  - `report.py` : Modèle rapport de stage (internship.report)
  - `report_section.py` : Sections obligatoires de rapport (internship.report.section)
  - `sms_utils.py` : Utilitaires d'envoi SMS (Twilio)

- `views/`
  - `student_views.xml` : Vues étudiant (formulaire, liste, notebook CV, stages)
  - `company_views.xml` : Vues entreprise (formulaire, liste, stages)
  - `internship_views.xml` : Vues stage (formulaire, liste, dashboard, signatures)
  - `application_views.xml` : Vues candidature (formulaire, liste, réponses)
  - `report_views.xml` : Vues rapport de stage (formulaire, liste, feedback, OCR)
  - `menus.xml` : Menus principaux et sous-menus
  - `dashboard_views.xml` : Dashboard analytique

- `report/`
  - `convention_report.xml` : Définition du rapport PDF de convention de stage
  - `internship_convention_template.xml` : Template QWeb du PDF

- `security/`
  - `ir.model.access.csv` : Règles d'accès par modèle

- `data/`
  - `email_templates.xml` : Modèles d'emails (envoi de convention, notifications)

- `demo/`
  - `demo_data.xml` : Données de démonstration (étudiants, entreprises, stages, etc.)

- `static/`
  - `description/` : Images, icônes, logo
  - `src/` : JS/CSS pour dashboard, templates QWeb

- `install.py` : Script d'installation (optionnel)

## Points techniques et originaux

- Extraction OCR automatique du texte des rapports et CV (PDF/Image)
- Vérification automatique des sections obligatoires dans les rapports
- Dashboard analytique interactif (KPIs, graphiques, pivot)
- Notifications SMS (Twilio) et emails automatisés
- Signature électronique intégrée
- Système de questions/réponses personnalisées pour les candidatures
- Respect de l'architecture MVC Odoo, code commenté et structuré

## Contraintes respectées
- Compatible Odoo 16/17 Community
- 100% Python, pas de dépendances commerciales
- Sécurité et droits d'accès gérés
- Documentation et code conformes aux standards Odoo

## Pour aller plus loin
- Possibilité d'ajouter des workflows de validation avancés
- Intégration avec d'autres modules Odoo (RH, CRM, etc.)
- Export/Import de données

## Présentation vidéo

👉 [Lien à insérer ici pour la vidéo de démonstration]

## Auteurs
- Bechir Ben Tekfa

---

> Ce module a été développé dans le cadre d'un TP d'amélioration de la gestion des stages académiques. Il va au-delà des exigences de base en proposant des fonctionnalités avancées et une expérience utilisateur moderne.
