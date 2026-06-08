# BIPM Docker Exercise

A small Flask web app running in Docker, built for the Big Data course at
[HWR Berlin](https://www.hwr-berlin.de/). It demonstrates a multi-service
setup: a Flask web container talking to a Redis container via Docker Compose.

## Features

- **Home** page with a Redis-backed hit counter and the HWR logo (served via
  Flask static files).
- **Titanic** page that loads the Titanic dataset with Pandas and shows a bar
  chart of survival rate by gender (rendered with Matplotlib) plus a data table.
- **About** page.
- Navigation menu (Home / Titanic / About) and a footer with author name and a
  link to the HWR Berlin homepage.
- Redis password and host configured through environment variables (`.env`).

## Architecture

- `web`: Flask app (`app/app.py`), port `4000` -> container `80`.
- `redis`: Redis cache for the hit counter, protected with a password.

## Run

```bash
docker compose up --build
```

Then open http://localhost:4000.

Stop and clean up:

```bash
docker compose down -v
```

## Layout

```
.
├── docker-compose.yml
├── Dockerfile
├── .env                 # REDIS_PASSWORD, REDIS_HOST (gitignored)
└── app/
    ├── app.py
    ├── requirements.in
    ├── requirements.txt
    ├── data/titanic.csv
    ├── static/hwr.png
    └── templates/
        ├── base.html
        ├── home.html
        ├── titanic.html
        └── about.html
```

## Author

Nikolas Jack Altran
