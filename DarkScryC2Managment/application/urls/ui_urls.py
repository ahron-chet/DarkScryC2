from django.urls import path
from application.Utils.urlutils import create_path, SlashBehavior
from application.views.ui.login import LoginPage, Logout
from application.views.ui.clients import ShowClients
from application.views.ui.index import IndexView

urlpatterns = []

# handle auth
urlpatterns += [
    path('auth/', LoginPage.as_view(), name='loginPage'),
    path('auth/logout/', Logout.as_view(), name='logout')
]

urlpatterns += [
    path('index/', IndexView.as_view(), name='index'),
]

urlpatterns+=[
    path('index/clients/', ShowClients.as_view(), name='show_clients'),
]
