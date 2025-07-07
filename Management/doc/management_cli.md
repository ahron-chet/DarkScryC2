# Management CLI

The management CLI is exposed via the `manager` entrypoint defined in
`pyproject.toml` under `[tool.poetry.scripts]`. The entrypoint maps to
`scripts.manager:main`, so Poetry installs this script automatically and it
can be executed with `poetry run` from the repository root.

The `scripts/` directory now lives at the top level of the Management package so
CLI utilities can be maintained separately from the FastAPI application code.

```bash
poetry run manager <command> [options]
```

Database migrations are handled with **Alembic**. Common commands:

```bash
poetry run alembic revision --autogenerate -m "message"
poetry run alembic upgrade head
```

Before running any command be sure the management backend environment variables
are configured. At minimum set `MANAGEMENT_DATABASE_URL` and
`MANAGEMENT_SECRET_KEY` (they can also be placed in your shell profile or a
`.env` file that you load manually):

```bash
export MANAGEMENT_DATABASE_URL="postgresql+asyncpg://user:pass@localhost/db"
export MANAGEMENT_SECRET_KEY="change-me"
```

## Available commands

### `init_db`

Create all database tables. Run this once before other commands.

```
poetry run manager init_db
```

### `create_user`

Create a new user in the database.

```
poetry run manager create_user \
  --username alice --password Strong1! \
  --email alice@example.com --role reader
```

### `list_users`

List all users and their roles. No additional arguments are required:

```
poetry run manager list_users
```

## Extending the CLI

Each command is implemented as an async function and registered via
`subparsers` in `build_parser()`:

```python
async def list_users_command(args: argparse.Namespace) -> None:
    ...

sub = subparsers.add_parser("list_users")
sub.set_defaults(func=list_users_command)
```

New actions can import application services and operate asynchronously just like
`create_user_command`.
