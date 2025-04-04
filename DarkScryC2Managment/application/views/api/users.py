from uuid import UUID
from django.shortcuts import aget_object_or_404
from django.contrib.auth import get_user_model

from ...services.view_base import ApiRouteV2  # The same base class as TaskApi
from .Schemas.users import (
    UserCreateSchema,
    UserUpdateSchema,
    UserOutSchema
)
from .Schemas.general import DeletedSuccessfully
from typing import List

from asgiref.sync import sync_to_async


User = get_user_model()


class UserApi(ApiRouteV2):
    def __init__(self):
        super().__init__(tags=["User"], prefix="/users")
        self.register_routes()


    async def create_user(self, request, payload: UserCreateSchema) -> UserOutSchema:
        """
        Create a new User using the given payload.
        Note: We do NOT include `otpuri` on creation (keep it null by default).
        """
        user = await User.objects.acreate(
            username=payload.username,
            password=payload.password,
            email=payload.email,
            role=payload.role,
            first_name=payload.first_name,
            last_name=payload.last_name,
            company_name=payload.company_name,
            industry=payload.industry,
            country=payload.country
        )
        return self._to_user_out(user)

    async def list_users(self, request) -> List[UserOutSchema]:
        """
        List all Users.
        """
        qs = await sync_to_async(list, thread_sensitive=True)(
            User.objects.all().order_by("-time_generated")
        )
        return [self._to_user_out(u) for u in qs]

    async def get_user(self, request, user_id: UUID) -> UserOutSchema:
        """
        Get details of a specific User by UUID.
        """
        user = await aget_object_or_404(User, user_id=user_id)
        return self._to_user_out(user)

    async def update_user(self, request, user_id: UUID, payload: UserUpdateSchema) -> UserOutSchema:
        """
        Update an existing User. 
        Only include fields that you want to change.
        """
        user = await aget_object_or_404(User, user_id=user_id)
        # Update allowed fields if provided
        if payload.username is not None:
            user.username = payload.username
        if payload.password is not None:
            # Use set_password to ensure password hashing
            user.set_password(payload.password)
        if payload.email is not None:
            user.email = payload.email
        if payload.role is not None:
            user.role = payload.role
        if payload.first_name is not None:
            user.first_name = payload.first_name
        if payload.last_name is not None:
            user.last_name = payload.last_name
        if payload.company_name is not None:
            user.company_name = payload.company_name
        if payload.industry is not None:
            user.industry = payload.industry
        if payload.country is not None:
            user.country = payload.country
        if payload.otpuri is not None:
            user.otpuri = payload.otpuri

        await user.asave()
        return self._to_user_out(user)

    async def delete_user(self, request, user_id: UUID) -> DeletedSuccessfully:
        """
        Delete a user by UUID.
        """
        user = await aget_object_or_404(User, user_id=user_id)
        await user.adelete()
        return DeletedSuccessfully(detail=f"User {user_id} deleted successfully.")


    def _to_user_out(self, user) -> UserOutSchema:
        return UserOutSchema(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            role=user.role,
            first_name=user.first_name,
            last_name=user.last_name,
            company_name=user.company_name,
            industry=user.industry,
            country=user.country,
            time_generated=user.time_generated,
            last_login=user.last_login,
        )


    def register_routes(self):
        # POST /users  -> Create a new User
        self.register_route(
            path="/",
            methods=["POST"],
            view_func=self.create_user,
            response={201: UserOutSchema},
            summary="Create a new User",
            permissions_req=["application.add_user"]
        )

        # GET /users   -> List all Users
        self.register_route(
            path="/",
            methods=["GET"],
            view_func=self.list_users,
            response={200: List[UserOutSchema]},
            summary="List all Users"
        )

        # GET /users/{user_id} -> Get a specific User
        self.register_route(
            path="/{user_id}",
            methods=["GET"],
            view_func=self.get_user,
            response={200: UserOutSchema},
            summary="Get a User by UUID"
        )

        # PUT or PATCH /users/{user_id} -> Update a User
        # (Here we use PUT, but you could also do PATCH, or define both)
        self.register_route(
            path="/{user_id}",
            methods=["PUT"],
            view_func=self.update_user,
            response={201: UserOutSchema},
            summary="Update an existing User",
            permissions_req=["application.change_user"]

        )

        # DELETE /users/{user_id} -> Delete a User
        self.register_route(
            path="/{user_id}",
            methods=["DELETE"],
            view_func=self.delete_user,
            response={201: DeletedSuccessfully},
            summary="Delete a User by UUID",
            permissions_req=["application.delete_user"]
        )
