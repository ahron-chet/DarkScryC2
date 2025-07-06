"""Documentation for the management CLI."""

# This file explains how to extend `Management/scripts/manager.py` with
# additional actions. Each CLI action should be implemented as a function and
# registered via `subparsers` in `build_parser()`.
#
# Example:
#
#     def list_users_command(args: argparse.Namespace) -> None:
#         ...
#
#     sub = subparsers.add_parser("list_users")
#     sub.set_defaults(func=list_users_command)
#
# New actions can import application services and operate asynchronously just
# like `create_user_command`.
