from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token,  refresh_jwt_token, verify_jwt_token
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('messages', views.MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', obtain_jwt_token, name="auth-login"),
    path('auth/register/', views.CreateUserView.as_view(), name="auth-register"),
    path('auth/token-refresh/', refresh_jwt_token),
    path('auth/token-verify/', verify_jwt_token),
]
