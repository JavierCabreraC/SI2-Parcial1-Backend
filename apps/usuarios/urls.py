from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views



urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('register/', views.register, name='register'),
    # path('profile/', views.profile, name='profile'),
    # Endpoints de administración
    path('admin/usuarios/', views.UsuarioListView.as_view(), name='usuario-list'),
    path('admin/usuarios/crear/', views.UsuarioCreateView.as_view(), name='usuario-create'),
    # Más rutas específicas de usuarios
]
