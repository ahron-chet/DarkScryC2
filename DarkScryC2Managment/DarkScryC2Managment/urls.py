from django.contrib import admin
from django.urls import path, include
from application.Utils.urlutils import create_include_path, SlashBehavior
from application.views.api import api_ninja
urlpatterns = [
    path("admin/", admin.site.urls),
    # e.g. /api/v1/ => application.urls.api_urls
    # *create_include_path("api/v1", "application.urls.api_urls", SlashBehavior.BOTH),
    path("api/v1/", include("application.urls.api_urls")),
    

    # e.g. / => application.urls.ui_urls
    path("", include("application.urls.ui_urls")),
]

urlpatterns += [
    path("api/v2/", api_ninja.urls)
]