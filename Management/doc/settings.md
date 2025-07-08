# Management Environment Settings

The FastAPI backend reads configuration from environment variables. Copy `.env.example` to `.env` and adjust the values for your environment.

- `MANAGEMENT_DATABASE_URL` – PostgreSQL connection string used by the application.
- `MANAGEMENT_SECRET_KEY` – secret value used for signing JWT tokens.
- `MANAGEMENT_DEBUG` – enable debug mode when set to `True`.
- `MANAGEMENT_CORS_ORIGINS` – comma separated list of allowed CORS origins.
- `MANAGEMENT_JWT_ACCESS_TOKEN_EXPIRE_MINUTES` – access token expiration window in minutes.
- `MANAGEMENT_JWT_REFRESH_TOKEN_EXPIRE_DAYS` – refresh token expiration window in days.
- `MANAGEMENT_JWT_ISSUER` – issuer claim embedded in generated JWTs.
- `MANAGEMENT_JWT_AUDIENCE` – audience claim that must match when validating JWTs.
- `MANAGEMENT_REDIS_HOST` – hostname of the Redis instance used for background tasks.
- `MANAGEMENT_REDIS_PORT` – port of the Redis server.
- `MANAGEMENT_REDIS_PASSWORD` – password for the Redis server, if required.
- `MANAGEMENT_ARQ_REDIS_DB` – Redis database index used for ARQ jobs.
- `TEST_DATABASE_URL` – database used when running the test suite.

JWT access and refresh tokens now include the following claims:

- `iss` – set from `MANAGEMENT_JWT_ISSUER`.
- `aud` – set from `MANAGEMENT_JWT_AUDIENCE`.
- `jti` – a unique identifier generated for each token.
