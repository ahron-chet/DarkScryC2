# Management CLI

`Management/scripts/manager.py` exposes a small command line interface for user
administration. Run it with Poetry:

```bash
poetry run python Management/scripts/manager.py <command> [options]
```

## Available commands

### `create_user`

Create a new user in the database.

```
poetry run python Management/scripts/manager.py create_user \
  --username alice --password Strong1! \
  --email alice@example.com --role reader
```

### `list_users`

List all users and their roles. No additional arguments are required:

```
poetry run python Management/scripts/manager.py list_users
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
