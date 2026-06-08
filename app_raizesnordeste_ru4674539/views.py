from rest_framework import generics
from .domain.produto import Produto
from .domain.pedido import Pedido, ItensPedido
from .domain.cliente import Cliente
from .domain.filial import Filial
from .application.serializers import ProdutoSerializer, PedidoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
import json

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
        # Filtra para trazer apenas o produto com o nome exato
        produtos = Produto.objects.filter(disponivel=True)
        
        context = {
            'produtos': produtos
        }
        return render(request, 'app_raizesnordeste_ru4674539/pages/totem.html', context)
    
class CriarPedidoView(View):
    def post(self, request, *file, **kwargs):
        try:
            # Converte a string JSON recebida no corpo da requisição em um dicionário Python
            dados = json.loads(request.body)
            itens_carrinho = dados.get('itens', [])

            if not itens_carrinho:
                return JsonResponse({'sucesso': False, 
                                     'erro': 'O carrinho está vazio.'}, status=400)
            
            # Busca instâncias padrão para as chaves estrangeiras obrigatórias
            # (Ajuste os filtros abaixo de acordo com os dados reais do seu banco)
            cliente_totem = Cliente.objects.first() # Puxa o primeiro cliente como Consumidor
            filial_barra = Filial.objects.first()   # Puxa a filial padrão (Barra do Ceará)

            if not cliente_totem or not filial_barra:
                return JsonResponse({'sucesso': False, 
                                    'erro': 'Configuração de Cliente ou Filial padrão não encontrada no banco.'}, status=400)

            total_geral = 0.00
            # Abre uma transação atômica no banco de dados MySQL
            with transaction.atomic():
               # Cria o cabeçalho do Pedido (repare no campo id_ial conforme o seu print)
                pedido = Pedido.objects.create(id_cliente=cliente_totem,
                                                id_filial=filial_barra,
                                                canal_venda='TOTEM',
                                                status_pagamento='PENDENTE',
                                                valor_total=0.00)
                
                # 2. Varre o array de itens para popular a tabela de sub-itens do pedido
                for item in itens_carrinho:
                    id_prod = item.get('id')
                    qtd = int(item.get('quantidade'))
                    preco_venda = float(item.get('preco'))
                    
                    # Busca o produto no banco de dados para garantir a integridade dos preços
                    produto = Produto.objects.get(id_produto=id_prod)
                    subtotal = preco_venda * qtd
                    total_geral += subtotal

                    # Cria o registro na sua tabela pivot de itens de pedido
                    ItensPedido.objects.create(id_pedido=pedido, 
                                               id_produto=produto, 
                                               quantidade=qtd, 
                                               preco_unitario=preco_venda)
                
                # 3. Atualiza o total real acumulado no registro do pedido pai
                pedido.valor_total = total_geral
                pedido.save()

            # Retorna a resposta positiva para o JavaScript prosseguir com o SweetAlert2
            return JsonResponse({'sucesso': True, 'pedido_id': pedido.id_pedido}, status=201)

        except Produto.DoesNotExist:
            return JsonResponse({'sucesso': False, 'erro': 'Um dos produtos selecionados não existe no banco.'}, status=400)
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': f'Erro no servidor: {str(e)}'}, status=500)

class PagamentoView(View):
    def get(self, request, pedido_id, *args, **kwargs):
        # Busca o pedido no MySQL pelo ID real ou retorna um erro 404 se não existir
        pedido = get_object_or_404(Pedido, id_pedido=pedido_id)
        
        context = {
            'pedido': pedido
        }
        return render(request, 'app_raizesnordeste_ru4674539/pages/pagamento.html', context)

class ConfirmarPagamentoView(View):
    def post(self, request, *args, **kwargs):
        try:
            # 1. Converte o JSON enviado pelo botão de sucesso do checkout
            dados = json.loads(request.body)
            pedido_id = dados.get('pedido_id')

            if not pedido_id:
                return JsonResponse({'sucesso': False, 'erro': 'ID do pedido não fornecido.'}, status=400)

            # 2. Busca o pedido específico de forma segura no MySQL
            pedido = Pedido.objects.get(id_pedido=pedido_id)

            # 3. Transição de Estado: Altera o status para PAGO (Conforme mapeamos no seu model)
            pedido.status_pagamento = 'PAGO'
            pedido.save()

            # Retorna a resposta positiva para o front-end disparar o SweetAlert2
            return JsonResponse({'sucesso': True, 'mensagem': 'Pagamento processado e baixado no MySQL com sucesso!'})

        except Pedido.DoesNotExist:
            return JsonResponse({'sucesso': False, 'erro': 'Pedido não encontrado no banco de dados.'}, status=404)
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': f'Erro interno no servidor: {str(e)}'}, status=500)