from uuid import UUID

from django.contrib.auth.models import User
from django.contrib.auth import aauthenticate, alogin
from django.http import JsonResponse
from django.conf import settings


from asgiref.sync import sync_to_async

from application.Utils.jwtutils import create_jwt_token, jwt_get, create_refresh_token
from application.services.view_base import BaseAsyncView, ApiRouteV2
from application.views.api.Schemas.general import Unauthorize
from .Schemas.auth_schemas import (
    LoginSchema,
    UserRegistration,
    LoginSchemaV2,
    V2LoginResponseSchema,
    V2RefreshRequestSchema,
    V2RefreshResponseSchema
)



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
            return JsonResponse({"id":user.user_id, "username":username}, status=201)
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




        
class AuthV2(ApiRouteV2):
    def __init__(self, tags = ["Auth"], prefix="/auth"):
        super().__init__(tags, prefix)
        self.register_routes()
    
    async def login(self, request, payload:LoginSchemaV2, *args, **kargs):
        user = await aauthenticate(username=payload.username, password=payload.password)
        if user:
            await alogin(request, user)

            access_token = create_jwt_token(user.user_id)
            refresh_token = create_refresh_token(user.user_id)

            exp = jwt_get(token=access_token, payload_key="exp", jwt_secrete=settings.JWT_SECRET)
            iat = jwt_get(token=access_token, payload_key="iat", jwt_secrete=settings.JWT_SECRET)
            expires_in = exp - iat

            return V2LoginResponseSchema(
                token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in
            )
        return 401, Unauthorize(detail="Incorrect username or password")
    
    async def refresh_token(self, request, payload: V2RefreshRequestSchema, *args, **kwargs):
        try:
            user_id = jwt_get(token=payload.refresh_token, payload_key="sub", jwt_secrete=settings.JWT_REFRESH_SECRET)
            if not user_id:
                return 401, Unauthorize(detail="Invalid refresh token payload: missing 'sub'")
        except Exception as e:
            print(e)
            return 401, Unauthorize(detail="Invalid refresh token")

        new_access_token = create_jwt_token(UUID(user_id))
        exp = jwt_get(token=new_access_token, payload_key="exp", jwt_secrete=settings.JWT_SECRET)
        iat = jwt_get(token=new_access_token, payload_key="iat", jwt_secrete=settings.JWT_SECRET)
        expires_in = exp - iat

        return V2RefreshResponseSchema(
            token=new_access_token,
            expires_in=expires_in
        )
        
    def register_routes(self):
        self.register_route(
            path="/",
            methods=["POST"],
            view_func=self.login,
            response={200:V2LoginResponseSchema, 401:Unauthorize},
            _login_req=False
        )
        self.register_route(
            path="/refresh",
            methods=["POST"],
            view_func=self.refresh_token,
            response={200: V2RefreshResponseSchema, 401: Unauthorize},
            _login_req=False
        )


