# Management Environment Settings

The FastAPI backend reads configuration from environment variables. Copy `.env.example` to `.env` and adjust the values for your environment.

- `MANAGEMENT_DATABASE_URL` – PostgreSQL connection string used by the application.
- `MANAGEMENT_SECRET_KEY` – secret value used for signing JWT tokens.
- `MANAGEMENT_DEBUG` – enable debug mode when set to `True`.
- `MANAGEMENT_CORS_ORIGINS` – comma separated list of allowed CORS origins.
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` – access token expiration window in minutes.
- `JWT_REFRESH_TOKEN_EXPIRE_DAYS` – refresh token expiration window in days.
- `TEST_DATABASE_URL` – database used when running the test suite.
