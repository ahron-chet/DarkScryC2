# Management CLI

`Management/scripts/manager.py` exposes a small command line interface for user
administration. Because the script uses package-relative imports it must be
executed as a module from the project root so that the `Management` package is
on the Python path.

```bash
# from the repository root
poetry -P Management run python -m Management.scripts.manager <command> [options]
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

### `create_user`

Create a new user in the database.

```
poetry -P Management run python -m Management.scripts.manager create_user \
  --username alice --password Strong1! \
  --email alice@example.com --role reader
```

### `list_users`

List all users and their roles. No additional arguments are required:

```
poetry -P Management run python -m Management.scripts.manager list_users
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
