from django.urls import path
from application.Utils.urlutils import create_path, SlashBehavior
from application.views.ui.login import LoginPage, Logout
from DarkScryC2Managment.application.views.ui.index.clients.clients import ShowClients
from DarkScryC2Managment.application.views.ui.index.index import IndexView

urlpatterns = []

# handle auth
urlpatterns += [
    path('auth/', LoginPage.as_view(), name='loginPage'),
    path('auth/logout/', Logout.as_view(), name='logout')
]

urlpatterns += [
    path('index/', IndexView.as_view(), name='index'),
]

# clients view
urlpatterns+=[
    path('index/clients/', ShowClients.as_view(), name='show_clients'),
]
