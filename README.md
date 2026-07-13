# Tickets API

Tickets API est une petite API REST de gestion de tickets, développée avec FastAPI.

L'idée est volontairement simple : pouvoir créer un ticket, consulter les tickets
existants, les modifier et les fermer. Ce projet a aussi été l'occasion de mettre
en place une structure claire avec des routes, un repository SQLAlchemy, des
schémas Pydantic et une suite de tests.

## Ce que permet l'API

- vérifier que l'application fonctionne avec un health check ;
- créer un ticket ;
- récupérer la liste des tickets avec pagination ;
- consulter un ticket précis ;
- modifier un ticket ;
- fermer un ticket.

Chaque ticket possède un titre, une description, un statut et une date de
création. Les statuts disponibles sont `open`, `stalled` et `closed`.

## Technologies utilisées

- Python 3.13
- FastAPI
- SQLAlchemy 2
- SQLite
- Pydantic
- pytest
- Ruff
- uv
- Docker

## Lancer le projet en local

Il faut avoir Python 3.13 et [uv](https://docs.astral.sh/uv/) installés sur la
machine.

Commence par récupérer les dépendances :

```bash
uv sync
```

Tu peux ensuite lancer l'API avec :

```bash
make run
```

Si tu préfères lancer directement la commande :

```bash
uv run uvicorn app.main:app --reload
```

L'API est alors disponible sur http://127.0.0.1:8000.

FastAPI génère automatiquement deux interfaces très pratiques pour découvrir et
tester les routes :

- Swagger UI : http://127.0.0.1:8000/docs
- ReDoc : http://127.0.0.1:8000/redoc

## Routes disponibles

| Méthode | Route | Description |
| --- | --- | --- |
| `GET` | `/health` | Vérifie que l'API répond |
| `GET` | `/v1/tickets/` | Liste les tickets |
| `POST` | `/v1/tickets/` | Crée un ticket |
| `GET` | `/v1/tickets/{ticket_id}` | Récupère un ticket |
| `PUT` | `/v1/tickets/{ticket_id}` | Modifie un ticket |
| `PATCH` | `/v1/tickets/{ticket_id}/close` | Ferme un ticket |

La liste est paginée avec deux paramètres optionnels :

- `limit`, compris entre 1 et 100, vaut 10 par défaut ;
- `offset`, supérieur ou égal à 0, vaut 0 par défaut.

Le nombre total de tickets est renvoyé dans l'en-tête HTTP `X-Total-Count`.

## Quelques exemples

Créer un ticket :

```bash
curl -X POST http://127.0.0.1:8000/v1/tickets/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Impossible de se connecter",
    "description": "La page de connexion retourne une erreur 500"
  }'
```

Afficher les tickets :

```bash
curl "http://127.0.0.1:8000/v1/tickets/?limit=10&offset=0"
```

Modifier le ticket numéro 1 :

```bash
curl -X PUT http://127.0.0.1:8000/v1/tickets/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Connexion impossible",
    "description": "Le problème est toujours présent"
  }'
```

Fermer ce ticket :

```bash
curl -X PATCH http://127.0.0.1:8000/v1/tickets/1/close
```

## Lancer les tests

La suite de tests couvre les schémas, le repository, les dépendances et les routes
HTTP. Chaque test utilise sa propre base SQLite en mémoire afin de rester isolé
des autres tests.

Pour lancer tous les tests :

```bash
make test
```

Pour afficher également la couverture du code :

```bash
make cov
```

Tu peux aussi vérifier la qualité et le formatage du code :

```bash
make lint
make format
```

## Utiliser Docker

Pour construire l'image :

```bash
make docker-build
```

Puis lancer le conteneur :

```bash
make docker-run
```

Le conteneur s'appelle `ticket-managements` et expose l'API sur
http://localhost:8010. Pour l'arrêter :

```bash
docker stop ticket-managements
```

## Organisation du projet

```text
app/
├── core/           # Configuration de la base et des logs
├── models/         # Modèles SQLAlchemy
├── repositories/   # Accès aux données
├── routers/        # Routes FastAPI
├── schemas/        # Schémas Pydantic
├── dependencies.py # Dépendances injectées dans les routes
└── main.py         # Point d'entrée de l'application

tests/              # Tests unitaires et tests de l'API
```

## À savoir

Pour le moment, l'application utilise une base SQLite en mémoire. C'est pratique
pour garder le projet léger et facile à tester, mais cela signifie que les
tickets disparaissent lorsque l'application redémarre. Pour un environnement de
production, il faudrait utiliser une base persistante, par exemple PostgreSQL,
et gérer les évolutions du schéma avec des migrations.
