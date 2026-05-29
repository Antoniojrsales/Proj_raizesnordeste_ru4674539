from rest_framework import generics
from .domain.produto import Produto
from .domain.pedido import Pedido
from .application.serializers import ProdutoSerializer, PedidoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.views import View

class HomeView(View):
    def get(self, request):
        return render(request, 'app_raizesnordeste_ru4674539/pages/home.html')

class ProdutoListAPIView(generics.ListAPIView):
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        """
        Filtro dinâmico por filial via URL para o RF05 (Regionalização).
        """
        queryset = Produto.objects.filter(disponivel=True)
        filial_id = self.request.query_params.get('filial')
        
        if filial_id is not None:
            queryset = queryset.filter(filiais__id_filial=filial_id)
            
        return queryset


class PedidoListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint para o Totem/App registrarem um novo pedido (POST).
    Processa os itens, calcula o valor total e dispara os pontos de fidelidade (RF03).
    """
    queryset = Pedido.objects.all().order_by('-data_pedido')
    serializer_class = PedidoSerializer

class PedidoPagamentoMockAPIView(APIView):
    """
    Endpoint de simulação para o RF02 (Pagamento Desacoplado).
    Recebe uma simulação de operadora de cartão/PIX e atualiza o pedido.
    """
    def post(self, request, pk):
        try:
            pedido = Pedido.objects.get(pk=pk)
        except Pedido.DoesNotExist:
            return Response(
                {"error": "Pedido não encontrado."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Evita reprocessamento (Garante a Idempotência exigida pelo RF02)
        if pedido.status_pagamento == 'APROVADO':
            return Response(
                {"message": "Este pedido já foi pago e processado anteriormente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Captura a simulação enviada pelo corpo da requisição (ou assume APROVADO por padrão)
        simulacao = request.data.get('simulacao', 'APROVADO').upper()

        if simulacao in ['APROVADO', 'SUCCESS']:
            pedido.status_pagamento = 'APROVADO'
            pedido.save()
            return Response({
                "id_pedido": pedido.id_pedido,
                "status_pagamento": pedido.status_pagamento,
                "message": "Pagamento processado com sucesso pelo gateway externo (Mock)."
            }, status=status.HTTP_200_OK)
        else:
            pedido.status_pagamento = 'RECUSADO'
            pedido.save()
            return Response({
                "id_pedido": pedido.id_pedido,
                "status_pagamento": pedido.status_pagamento,
                "message": "Pagamento recusado pela operadora simulada."
            }, status=status.HTTP_200_OK)
        
class TotemView(View):
    def get(self, request):
        produtos = Produto.objects.all()

        context = {
            'produtos': produtos
        }
        return render(request, 'app_raizesnordeste_ru4674539/pages/totem.html', context)