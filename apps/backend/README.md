# EduPredict Backend

FastAPI backend providing:
- JWT auth + RBAC (Admin/Teacher/Student)
- Academic data CRUD
- Prediction + explainability endpoints

This folder is managed as a Python project via `pyproject.toml`.

## Key endpoints (current)

- Auth
	- `POST /auth/register` (creates a Student)
	- `POST /auth/login` (OAuth2 password flow; returns access+refresh tokens)
	- `POST /auth/refresh` (rotates refresh token)
	- `POST /auth/logout` (revokes refresh token)
	- `GET /auth/me`
- Admin
	- `POST /bootstrap/admin` (create the *first* admin; disabled by default)
	- `GET /admin/users`
	- `POST /admin/users`
	- `PATCH /admin/users/{user_id}`
- Academics
	- `GET /academics/me` (student-only)
	- `GET /academics` (teacher/admin; student only for self)
	- `POST /academics` (teacher/admin)
	- `PATCH /academics/{record_id}` (teacher/admin)
	- `DELETE /academics/{record_id}` (admin-only)

## RBAC rules (server-enforced)

- **Student**: view own profile; view own academic records.
- **Teacher**: create/update academic records; list records.
- **Admin**: manage users/roles; delete academic records; everything a teacher can do.

## Local development notes

### Database

Use the repo-level `docker-compose.yml` for Postgres.

### Migrations

Alembic is configured for async SQLAlchemy. Migration files live in `alembic/versions/`.

### Bootstrap the first admin (safe, opt-in)

By default, the bootstrap endpoint is disabled.

Set in `.env`:

- `ALLOW_ADMIN_BOOTSTRAP=true`
- `ADMIN_BOOTSTRAP_TOKEN=<long random secret>`

Then call `POST /bootstrap/admin` with that token. The endpoint only succeeds if **no admin exists yet**.

## OpenAPI

Once the API is running, OpenAPI docs are available at:
- `/docs` (Swagger UI)
- `/redoc`
