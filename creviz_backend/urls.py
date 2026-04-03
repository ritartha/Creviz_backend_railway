from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Django admin panel
    path("admin/", admin.site.urls),

    # JWT endpoints (global shortcuts)
    path("api/auth/login/",   TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(),    name="token_refresh"),
    path("api/auth/verify/",  TokenVerifyView.as_view(),     name="token_verify"),

    # App routes
    path("api/accounts/",    include("apps.accounts.urls")),
    path("api/portfolio/",   include("apps.portfolio.urls")),
    path("api/marketplace/", include("apps.marketplace.urls")),
    path("api/commissions/", include("apps.commissions.urls")),
    path("api/contact/",     include("apps.contact.urls")),
]

# Serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )