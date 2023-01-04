from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("", include("home.urls")),
    path("core/", include("core.urls")),
    path("users/", include("users.urls")),
    path("interactions/", include("interactions.urls")),
    path("graphs/", include("graphs.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
