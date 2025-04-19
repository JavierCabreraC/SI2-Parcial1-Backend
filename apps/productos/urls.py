from django.urls import path
from .views import (
    CategoriaListView, CategoriaCreateView, ProductoListView, ProductoCreateView, ProductoDetailView,
    ProductoUpdateView, ProductoDeleteView
)



urlpatterns = [
    # Endpoints de categorías existentes
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/crear/', CategoriaCreateView.as_view(), name='categoria-create'),
    
    # Endpoints de productos existentes
    path('productos/', ProductoListView.as_view(), name='producto-list'),
    path('productos/crear/', ProductoCreateView.as_view(), name='producto-create'),
    
    # Nuevos endpoints de productos para actualizar y eliminar
    path('productos/<int:pk>/', ProductoDetailView.as_view(), name='producto-detail'),
    path('productos/<int:pk>/actualizar/', ProductoUpdateView.as_view(), name='producto-update'),
    path('productos/<int:pk>/eliminar/', ProductoDeleteView.as_view(), name='producto-delete'),
]
