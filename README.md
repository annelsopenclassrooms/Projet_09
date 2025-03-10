# Application de critiques de livres et d'articles

## Description
Cette application permet aux utilisateurs de demander, lire et publier des critiques de livres et d'articles littéraires. Elle inclut un système de billets permettant aux utilisateurs de solliciter des avis et de répondre aux demandes de critique.

## Fonctionnalités principales
- **Billets** : Création et gestion de demandes de critiques.
- **Critiques** : Réponse aux billets et publication de critiques autonomes.
- **Flux** : Affichage des billets et critiques des utilisateurs suivis.
- **Suivi d'utilisateurs** : Suivre d'autres utilisateurs pour voir leurs publications.
- **Authentification** : Inscription et connexion sécurisées.

## Installation et exécution
### Prérequis
- Python 3.x
- Django
- SQLite

### Installation
1. Cloner le repository :
   ```sh
   git clone https://github.com/votre-repo.git
   cd votre-repo
   ```
2. Créer un environnement virtuel et l’activer :
   ```sh
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```
3. Installer les dépendances :
   ```sh
   pip install -r requirements.txt
   ```
4. Appliquer les migrations de la base de données :
   ```sh
   python manage.py migrate
   ```
5. Lancer le serveur de développement :
   ```sh
   python manage.py runserver
   ```

## Utilisation
- Accédez à `http://127.0.0.1:8000/` dans votre navigateur.
- Inscrivez-vous et connectez-vous pour commencer à interagir avec l’application.

## Modèles de données
L'application utilise les modèles suivants :
- **User** : Gestion des utilisateurs.
- **Ticket** : Représente une demande de critique.
- **Review** : Représente une critique en réponse à un billet ou autonome.

## Spécifications techniques
- Développé avec **Django**.
- Base de données **SQLite** incluse.
- Respect des conventions **PEP8**.

 
