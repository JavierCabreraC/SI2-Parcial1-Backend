from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Categoria
from .serializers import CategoriaSerializer
from apps.usuarios.permissions import IsAlmacenista



# Create your views here.
class CategoriaListView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [ IsAlmacenista ]


class CategoriaCreateView(generics.CreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [ IsAlmacenista ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Establecer la fecha de creación antes de guardar
        categoria = serializer.save(fecha_creacion=timezone.now())
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

