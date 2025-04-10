from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .serializers import CustomTokenObtainPairView



urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    # Más rutas específicas de usuarios
]
