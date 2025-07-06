import argparse
import asyncio

from Management.app.core.database import AsyncSessionLocal
from Management.app.schemas.user import UserCreate, UserRole
from Management.app.services.user_service import UserService


async def create_user_command(args: argparse.Namespace) -> None:
    """Create a new user from CLI arguments."""
    async with AsyncSessionLocal() as session:
        service = UserService()
        user_in = UserCreate(
            username=args.username,
            password=args.password,
            email=args.email,
            role=UserRole(args.role),
        )
        user = await service.create(session, user_in)
        print(f"Created user {user.username} with id {user.user_id}")


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the management CLI."""
    parser = argparse.ArgumentParser(description="Management CLI")
    subparsers = parser.add_subparsers(dest="action", required=True)

    create_user_parser = subparsers.add_parser(
        "create_user", help="Create a new user"
    )
    create_user_parser.add_argument("--username", required=True)
    create_user_parser.add_argument("--password", required=True)
    create_user_parser.add_argument("--email", required=True)
    create_user_parser.add_argument(
        "--role",
        default=UserRole.READER.value,
        choices=[role.value for role in UserRole],
    )
    create_user_parser.set_defaults(func=create_user_command)

    return parser


def main(argv: list[str] | None = None) -> None:
    """Entry point for the management CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    asyncio.run(args.func(args))


if __name__ == "__main__":
    main()
