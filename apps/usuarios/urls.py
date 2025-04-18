from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UsuarioListView, 
    UsuarioCreateView,
    PersonalCreateView,
    ClienteCreateView,
    PersonalListView,
    PersonalDetailView,
    ClienteListView,
    ClienteDetailView
)



urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/usuarios/', UsuarioListView.as_view(), name='usuario-list'),
    path('admin/usuarios/crear/', UsuarioCreateView.as_view(), name='usuario-create'),
    
    # Endpoints para Personal
    path('admin/personal/', PersonalListView.as_view(), name='personal-list'),
    path('admin/personal/<int:pk>/', PersonalDetailView.as_view(), name='personal-detail'),
    path('admin/personal/crear/', PersonalCreateView.as_view(), name='personal-create'),
    
    # Endpoints para Cliente
    path('admin/cliente/', ClienteListView.as_view(), name='cliente-list'),
    path('admin/cliente/<int:pk>/', ClienteDetailView.as_view(), name='cliente-detail'),
    path('admin/cliente/crear/', ClienteCreateView.as_view(), name='cliente-create'),
    
    # Más rutas específicas de usuarios
]
