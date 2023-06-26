from django.contrib import admin
from django.urls import path, include
from pages.urls import pages_patterns
from messenger.urls import messenger_patterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", include("core.urls")),
    path("pages/", include(pages_patterns)),
    path("admin/", admin.site.urls),
    # paths de Auth
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("registration.urls")),
    # paths de profiles
    path("profiles/", include("profiles.urls")),
    # paths de messenger
    path("messenger/", include(messenger_patterns)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
