# EduPredict Backend — Free Deployment (Hugging Face Spaces)

This backend is **FastAPI + ML (scikit-learn / LightGBM / SHAP)** and runs as a **Docker Space** on Hugging Face (free tier).

## 1) Create the Space

1. On Hugging Face, create a new **Space**.
2. Space SDK: **Docker**.
3. Visibility: Public (required for free tier).

## 2) Connect the repo

Connect the Space to your GitHub repo/branch, or push directly to the Space git remote.

## 3) Required environment variables

Set these in the Space settings (Secrets/Variables):

- `DATABASE_URL` — use a **managed Postgres** connection string (Supabase or Neon)
  - Example (shape): `postgresql+asyncpg://USER:PASSWORD@HOST:5432/DBNAME`
- `JWT_SECRET` — a long random string
- `JWT_ISSUER` — e.g. `edupredict`
- `JWT_AUDIENCE` — e.g. `edupredict-web`
- `CORS_ALLOW_ORIGINS` — comma-separated list of allowed frontend origins
  - Include your Cloudflare Pages URL(s), for example:
    - `https://edupredict.pages.dev`

Optional:
- `MODEL_REGISTRY_PATH` — where model artifacts are stored.
  - Note: Free Spaces do **not** provide persistent disk by default; artifacts written to disk may reset on rebuild.
  - If you need persistence, use a managed store (DB/object storage) or re-train after deploy.

## 4) Database migrations

This project uses Alembic. After you create the Postgres database and set `DATABASE_URL`, run migrations.

You can run migrations locally pointing to the production DB URL, or add a one-time release step in your deployment workflow.

## 5) Health check

Once deployed:
- `GET /health` should return OK.
- `GET /docs` should show the OpenAPI docs.

## Notes

- This deployment keeps the existing Python ML pipeline intact.
- If you need an always-on backend, you may outgrow free tiers; expect sleeping on inactivity.
