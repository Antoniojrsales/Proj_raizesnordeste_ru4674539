from django.shortcuts import render
from rest_framework import generics
from .domain.produto import Produto
from .application.serializers import ProdutoSerializer

class ProdutoListAPIView(generics.ListAPIView):
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        """
        Sobrescrevemos o método para filtrar produtos por filial via URL.
        Exemplo: /api/produtos/?filial=2
        """
        queryset = Produto.objects.filter(disponivel=True)
        filial_id = self.request.query_params.get('filial')
        
        if filial_id is not None:
            # Filtra produtos que possuem a filial específica na lista de filiais
            queryset = queryset.filter(filiais__id_filial=filial_id)
            
        return queryset