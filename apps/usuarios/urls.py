# from django.urls import path
# from rest_framework_simplejwt.views import TokenRefreshView
# from . import views



# urlpatterns = [
#     path('login/', views.login_view, name='login'),
#     path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     # path('register/', views.register, name='register'),
#     # path('profile/', views.profile, name='profile'),
#     # Endpoints de administración
#     path('admin/usuarios/', views.UsuarioListView.as_view(), name='usuario-list'),
#     path('admin/usuarios/crear/', views.UsuarioCreateView.as_view(), name='usuario-create'),
#     # Más rutas específicas de usuarios
# ]

from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UsuarioListView, 
    UsuarioCreateView,
    PersonalCreateView,
    ClienteCreateView
)



urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/usuarios/', UsuarioListView.as_view(), name='usuario-list'),
    path('admin/usuarios/crear/', UsuarioCreateView.as_view(), name='usuario-create'),
    # Nuevos endpoints
    path('admin/personal/crear/', PersonalCreateView.as_view(), name='personal-create'),
    path('admin/cliente/crear/', ClienteCreateView.as_view(), name='cliente-create'),
    # Más rutas específicas de usuarios
]
