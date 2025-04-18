from django.urls import path
from . import views
from .views import (
    CategoriaListView,
    CategoriaCreateView
)



urlpatterns = [
    # Endpoints de categorías
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/crear/', CategoriaCreateView.as_view(), name='categoria-create'),
]
