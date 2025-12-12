from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentViewSet, SubscriptionView, UserCreateAPIView,
                         UserViewSet)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(
            permission_classes=AllowAny,
        ),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(
            permission_classes=AllowAny,
        ),
        name="token_refresh",
    ),
    path("subscribe/", SubscriptionView.as_view(), name="subscribe"),
    path('', include(router.urls)),
]
