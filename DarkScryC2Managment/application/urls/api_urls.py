from django.urls import path
from application.Utils.urlutils import create_path, SlashBehavior
from application.views.api.auth import LoginView, RegisterView
from ..views.api.modules import shellWebSocket


urlpatterns = [
    *create_path('auth', LoginView.as_view(), name='api_auth', slash_behavior=SlashBehavior.BOTH),
    *create_path('auth/register', RegisterView.as_view(), name='register_user', slash_behavior=SlashBehavior.BOTH),
]




urlpatterns_webSocket = [
    path("ws/shell/<str:agent_id>/", shellWebSocket.ShellConsumer.as_asgi())
]
