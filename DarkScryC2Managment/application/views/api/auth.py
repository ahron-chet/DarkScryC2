# application/routes/api/auth/views.py
from django.contrib.auth.models import User
from django.contrib.auth import aauthenticate, alogin
from asgiref.sync import sync_to_async
from django.http import JsonResponse
from .Schemas.auth_schemas import LoginSchema, UserRegistration
from application.services.view_base import BaseAsyncView


class LoginView(BaseAsyncView):
    schema_class = LoginSchema
    login_required = False

    async def post(self, request, *args, **kwargs):
        data:LoginSchema = request.validated_data
        username = data.username
        password = data.password
        user = await aauthenticate(username=username, password=password)
        if user:
            await alogin(request, user)
            return JsonResponse({"message": "Login successful"}, status=201)
        return JsonResponse({"message": "Invalid username or password"}, status=401)

    async def get(self, request, *args, **kwargs):
        return JsonResponse({"detail": "Method not allowed"}, status=405)




class RegisterView(BaseAsyncView):
    schema_class = UserRegistration

    async def post(self, request, *args, **kwargs):
        data = request.validated_data  # validated from Pydantic
        username = data.username
        password = data.password

        new_user = await create_user_if_not_exists(
            username, 
            password, 
            first_name=data.first_name, 
            last_name=data.last_name, 
            company_name=data.company_name, 
            industry=data.industry, 
            country=data.country
        )
        if new_user is None:
            return JsonResponse({"error": "Username already exists"}, status=400)

        return JsonResponse({"message": "User created successfully"}, status=201)

    async def get(self, request, *args, **kwargs):
        return JsonResponse({"detail": "Method not allowed"}, status=405)




@sync_to_async
def create_user_if_not_exists(username, password, first_name, last_name, company_name, industry, country):
    if User.objects.filter(username=username).exists():
        return None
    return User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        company_name=company_name,
        industry=industry,
        country=country
    )

