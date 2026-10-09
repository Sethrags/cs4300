# CineBook: Movie Theater Booking

CineBook is a Django and Django REST Framework application for browsing movies, checking available seats, reserving a seat, and reviewing a personal booking history. It includes a Bootstrap user interface, a JSON REST API, Django admin, automated tests, and Behave BDD scenarios.

**Live deployment:** https://cs4300-homework2.onrender.com/

## Features

- Movie catalogue with title, description, release date, and runtime
- Per-movie seats with live availability status
- Authenticated, atomic reservations that prevent duplicate seat bookings
- Personal booking history and booking cancellation through the API
- Browsable REST endpoints for movies, seats, and bookings
- Django admin for adding catalogue data
- Unit tests, API integration tests, and Behave BDD scenarios

## Project structure

```text
homework2/
├── bookings/                         # Django application
│   ├── migrations/                   # Database schema migration
│   ├── static/bookings/css/          # Application CSS
│   ├── templates/bookings/           # Bootstrap HTML templates
│   ├── admin.py                      # Django admin registration
│   ├── api.py                        # REST Framework viewsets
│   ├── models.py                     # Movie, Seat, and Booking models
│   ├── serializers.py                # JSON serializers
│   ├── tests.py                      # Unit and API integration tests
│   └── views.py                      # Browser-facing views
├── features/                         # Behave BDD feature scenarios and steps
├── movie_theater_booking/            # Django project configuration and URLs
├── manage.py                         # Django management entry point
├── requirements.txt                  # Runtime and test dependencies
├── Procfile                          # Process command for deployment platforms
└── render.yaml                       # Render deployment configuration
```

## Local setup and running the site

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
python manage.py runserver 0.0.0.0:3000
```

Open `http://127.0.0.1:3000/` for the site and `http://127.0.0.1:3000/admin/` to add movies and seats. Log in at `/accounts/login/` before reserving seats.

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

## Testing

Run the Django unit and API integration tests:

```bash
python manage.py test
```

Run the Behave BDD scenarios:

```bash
python manage.py behave --simple
```

Generate the coverage report for the application code:

```bash
coverage run manage.py test
coverage report
```

The test suite currently has 15 Django tests, 2 Behave scenarios, and 90% coverage of the `bookings` application. The coverage configuration enforces the assignment's 80% target.

## Deployment on Render

The application is deployed as the free Render web service **cs4300-homework2**:

- Live URL: https://cs4300-homework2.onrender.com/
- Repository branch: `main`
- Root directory: `homework2`
- Build command: `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
- Start command: `gunicorn movie_theater_booking.wsgi:application --bind 0.0.0.0:$PORT`

The current free deployment uses SQLite rather than PostgreSQL. Render's free filesystem is ephemeral, so deployed users and catalogue data can reset after a restart, spin-down, or redeploy. Add movies and seats through the admin site or REST API when demonstrating the application.

## AI-use disclosure

OpenAI Codex was used as an assistant to generate portions of the initial implementation, including Django models, views, serializers, templates, tests, and documentation. I am responsible for reviewing, validating, adapting, understanding, and citing this assistance in accordance with the course policy.
