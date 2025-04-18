from django.urls import path
from . import views
from .views import (
    CategoriaListView,
    CategoriaCreateView,
    ProductoListView,
    ProductoCreateView
)



urlpatterns = [
    # Endpoints de categorías
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/crear/', CategoriaCreateView.as_view(), name='categoria-create'),
    
    # Endpoints de productos
    path('productos/', ProductoListView.as_view(), name='producto-list'),
    path('productos/crear/', ProductoCreateView.as_view(), name='producto-create'),
]
