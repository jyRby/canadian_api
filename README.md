# API Canadien

API REST pour voter pour le joueur étoile du match et consulter les matchs/joueurs.

---

## Prérequis

- Python 3.11+
- pip
- Docker (pour le déploiement)
---

## Installation locale

1. Cloner le projet :

```bash
git clone <ton-repo-url>
cd canadien_api
```

2. Créer un environnement virtuel et installer les dépendances :

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

3. Initialiser la base de données (SQLite ou autre) :

```bash
flask db init
flask db migrate
flask db upgrade
```

4. Lancer le serveur Flask :

```bash
flask run
```

L’API sera disponible sur `http://127.0.0.1:5000`.

---

## Endpoints principaux

| Endpoint            | Méthode | Headers                     | Body / Params                   |
|--------------------|---------|-----------------------------|--------------------------------|
| `/users/register`   | POST    | None                        | JSON `{ "username": "", "password": "" }` |
| `/users/login`      | POST    | None                        | JSON `{ "username": "", "password": "" }` |
| `/players/`         | GET     | None                        | None                           |
| `/games/`           | GET     | None                        | None                           |
| `/votes/`           | POST    | `Authorization: Bearer <token>` | JSON `{ "game_id": 2025010015, "player_id": 12 }` |
| `/votes/top`        | GET     | None                        | None                           |
| `/votes/`           | GET     | `Authorization: Bearer <token>` | None                        |

---

## Dockerisation

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

CMD ["flask", "run"]
```

### Construire et lancer l'image Docker

```bash
docker build -t canadien_api .
docker run -d -p 5000:5000 canadien_api
```

L’API sera accessible sur `http://localhost:5000`.

---

## Déploiement sur RapidAPI

RapidAPI ne peut pas accéder à `localhost`. Utilise un tunnel public avec **ngrok** :

```bash
ngrok http 5000
```

Tu obtiendras une URL publique (ex. `https://abcd1234.ngrok.io`).

1. Connecte-toi à [RapidAPI](https://rapidapi.com/).
2. Crée un **nouveau projet/API**.
3. Mets l’URL de base de ton API (ngrok URL).
4. Ajoute chaque endpoint avec la méthode, les headers et le corps.
5. Teste les endpoints depuis RapidAPI.
6. Publie l’API si nécessaire.

---

## Notes importantes

- Les champs `game_id` et `player_id` doivent être **entiers** pour POST `/votes/`.
- Le token JWT est obligatoire pour `/votes/` POST et GET.
- Pour tester rapidement la partie vote, utilise le client Python fourni dans le projet.
- Les erreurs SQL détaillées sont loggées dans la console pour debug.

---

##  Exemple de requêtes cURL

### Enregistrement utilisateur

```bash
curl -X POST http://127.0.0.1:5000/users/register \
-H "Content-Type: application/json" \
-d '{"username": "alainFlouflou", "password": "motdepasse"}'
```

### Connexion et récupération du token

```bash
curl -X POST http://127.0.0.1:5000/users/login \
-H "Content-Type: application/json" \
-d '{"username": "alainFlouflou", "password": "motdepasse"}'
```

### Voter pour un joueur (token requis)

```bash
curl -X POST http://127.0.0.1:5000/votes/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <token>" \
-d '{"game_id": 2025010015, "player_id": 12}'
```

### Récupérer les votes de l’utilisateur

```bash
curl -X GET http://127.0.0.1:5000/votes/ \
-H "Authorization: Bearer <token>"
```

### Récupérer le top joueurs

```bash
curl -X GET http://127.0.0.1:5000/votes/top
```

---

## License

MIT License

