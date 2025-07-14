import argparse
import asyncio

from app.core.database import get_db_config, init_db
from app.schemas.user import UserCreate, UserRole
from app.services.user_service import UserService


async def list_users_command(args: argparse.Namespace) -> None:
    """List all users."""
    async with get_db_config().sessionmaker() as session:
        service = UserService()
        users = await service.list(session)
        for user in users:
            print(f"{user.user_id} {user.username} {user.email} {user.role}")


async def create_user_command(args: argparse.Namespace) -> None:
    """Create a new user from CLI arguments."""
    print(get_db_config().settings.database_url)
    async with get_db_config().sessionmaker() as session:
        service = UserService()
        user_in = UserCreate(
            username=args.username,
            password=args.password,
            email=args.email,
            role=UserRole(args.role),
        )
        user = await service.create(session, user_in)
        print(f"Created user {user.username} with id {user.user_id}")


async def init_db_command(args: argparse.Namespace) -> None:
    """Initialize the database schema."""
    await init_db()
    print("Database initialized")


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the management CLI."""
    parser = argparse.ArgumentParser(description="Management CLI")
    subparsers = parser.add_subparsers(dest="action", required=True)

    create_user_parser = subparsers.add_parser("create_user", help="Create a new user")
    create_user_parser.add_argument("--username", required=True)
    create_user_parser.add_argument("--password", required=True)
    create_user_parser.add_argument("--email", required=True)
    create_user_parser.add_argument(
        "--role",
        default=UserRole.READER.value,
        choices=[role.value for role in UserRole],
    )
    create_user_parser.set_defaults(func=create_user_command)

    list_users_parser = subparsers.add_parser("list_users", help="List all users")
    list_users_parser.set_defaults(func=list_users_command)

    init_db_parser = subparsers.add_parser("init_db", help="Initialize database")
    init_db_parser.set_defaults(func=init_db_command)

    return parser


def main(argv: list[str] | None = None) -> None:
    """Entry point for the management CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    asyncio.run(args.func(args))


if __name__ == "__main__":
    main()
