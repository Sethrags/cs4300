# CineBook: Movie Theater Booking

CineBook is a Django and Django REST Framework application for browsing movies, checking available seats, reserving a seat, and reviewing a personal booking history. It includes a Bootstrap user interface and a JSON REST API.

## Features

- Movie catalogue with title, description, release date, and runtime
- Per-movie seats with live availability status
- Authenticated, atomic reservations that prevent duplicate seat bookings
- Personal booking history
- Browsable REST endpoints for movies, seats, and bookings
- Django admin for adding catalogue data
- Unit and API integration tests

## Local setup

Use Python 3.11 or newer.

```bash
python -m venv .venv
# PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/` to add movies and seats. Log in at `/accounts/login/` before reserving seats.

## REST API

| Endpoint | Purpose |
| --- | --- |
| `GET /api/movies/` | List movies |
| `POST /api/movies/` | Create a movie (authenticated) |
| `GET /api/seats/?movie=<id>` | List seats for a movie |
| `GET /api/seats/available/?movie=<id>` | List available seats |
| `GET, POST /api/bookings/` | View personal booking history or make a booking |
| `GET, DELETE /api/bookings/<id>/` | Read or cancel one of your bookings |

To create a booking, authenticate with a session or HTTP Basic Auth and POST JSON such as:

```json
{"movie": 1, "seat": 4}
```

Run the tests with:

```bash
python manage.py test
```

## Deployment on Render

1. Push this folder to a GitHub repository.
2. In Render, create a Blueprint from that repository; `render.yaml` supplies the build and start commands.
3. Add a Render PostgreSQL database and set `DATABASE_URL` on the web service.
4. Update `ALLOWED_HOSTS` with the deployed hostname if it differs from the supplied `.onrender.com` setting.
5. Run `python manage.py createsuperuser` from the Render shell to administer the catalogue.

The deployment URL should be recorded here after a user-owned Render deployment is created: `https://<your-service>.onrender.com`.

## AI-use disclosure

OpenAI Codex was used as an assistant to generate portions of the initial implementation, including Django models, views, serializers, templates, tests, and documentation. I am responsible for reviewing, validating, adapting, understanding, and citing this assistance in accordance with the course policy.
