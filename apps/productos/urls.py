from django.urls import path
from .views import (
    CategoriaListView, CategoriaCreateView, ProductoListView, ProductoCreateView, ProductoDetailView,
    ProductoUpdateView, ProductoDeleteView, CategoriaDetailView, CategoriaUpdateView, CategoriaDeleteView,
    ProductoPorCategoriaView, ReporteBajoStockView
)


urlpatterns = [
    # Endpoints de categorías existentes
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/crear/', CategoriaCreateView.as_view(), name='categoria-create'),
    
    # Nuevos endpoints de categorías
    path('categorias/<int:pk>/', CategoriaDetailView.as_view(), name='categoria-detail'),
    path('categorias/<int:pk>/actualizar/', CategoriaUpdateView.as_view(), name='categoria-update'),
    path('categorias/<int:pk>/eliminar/', CategoriaDeleteView.as_view(), name='categoria-delete'),
    path('categorias/<int:categoria_id>/productos/', ProductoPorCategoriaView.as_view(), name='categoria-productos'),
    
    # Endpoints de productos (ya implementados)
    path('productos/', ProductoListView.as_view(), name='producto-list'),
    path('productos/crear/', ProductoCreateView.as_view(), name='producto-create'),
    path('productos/<int:pk>/', ProductoDetailView.as_view(), name='producto-detail'),
    path('productos/<int:pk>/actualizar/', ProductoUpdateView.as_view(), name='producto-update'),
    path('productos/<int:pk>/eliminar/', ProductoDeleteView.as_view(), name='producto-delete'),
    path('reportes/bajo-stock/', ReporteBajoStockView.as_view(), name='reporte-bajo-stock')
]
