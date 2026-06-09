# ☕ Projeto: Rede Raízes do Nordeste - Back-end Centralizado

Este projeto é uma plataforma robusta de back-end desenvolvida em **Django** e **Django Rest Framework** para centralizar a gestão de pedidos de uma franquia regional. Ele integra dados de múltiplos canais (Totem, App e Balcão), demonstrando habilidades em **Clean Architecture**, APIs RESTful e persistência de dados.

# 👨‍💻 Responsavel:
**Aluno:** Antonio Gomes Sales Junior  
**RU:** 4674539  
**Curso:** Análise e Desenvolvimento de Sistemas (ADS) - UNINTER  
**Local:** Fortaleza - CE

## 🏛️ Arquitetura e Organização
Para garantir a escalabilidade e manutenibilidade, o sistema foi estruturado seguindo os princípios da **Clean Architecture** (Arquitetura Limpa), dividindo as responsabilidades em camadas independentes:

* **Domain:** Núcleo da aplicação com as regras de negócio e modelos (Clientes, Produtos, Filiais).
* **Application:** Camada de tradução de dados através de Serializers especializados.
* **API/Infrastructure:** Endpoints para comunicação com dispositivos externos e configurações de banco de dados.

## ✅ Etapas de Inicialização
Siga os passos abaixo para clonar o repositório e rodar o back-end na sua máquina local utilizando o ambiente virtual.

### 1. Clonar o Repositório:
```bash
git clone https://github.com/Antoniojrsales/Proj_raizesnordeste_ru4674539.git

cd Proj_raizesnordeste_ru4674539
```

### 2. Configurar o Ambiente Virtual (venv):
python -m venv venv
### No Windows para ativar:
.\venv\Scripts\activate
### No Linux/Mac para ativar:
source venv/bin/activate

### 3. Configurar as Variáveis de Ambiente (`.env`)
O repositório disponibiliza o arquivo `.env.example` como gabarito de portabilidade. Para inicializar o contexto criptográfico do Django:
1. Duplique o arquivo `.env.example` na raiz do projeto.
2. Renomeie a cópia criada para apenas `.env`.
3. O arquivo já vem pré-configurado com chaves seguras padrões para o ambiente de testes locais em SQLite.

### 4. Instalar as Dependências:
pip install -r requirements.txt

### 5. Executar as Migrações do Banco de Dados (SQLite):
python manage.py migrate

### 6. Carregar a Massa de Dados Inicial
python manage.py loaddata dados_iniciais.json

### 7. Iniciar o Servidor de Desenvolvimento:
python manage.py runserver

### 🛠️ Resolução de Problemas de Infraestrutura
Se durante o processo de deploy na máquina secundária você enfrentar alguma das barreiras de ambiente listadas abaixo, aplique a correção indicada:

🚨 **1. Erro de Inicialização:** CommandError: You must set settings.ALLOWED_HOSTS if DEBUG is False.
Causa: O Django interceptou que a flag de depuração foi alterada ou o arquivo .env não pôde ser mapeado no diretório atual, bloqueando o tráfego por segurança.

**Solução:** O arquivo settings.py já foi blindado para aceitar requisições de teste em qualquer barramento local configurando a diretiva global ALLOWED_HOSTS = ['*']. Garanta apenas que o arquivo .env esteja de fato na pasta raiz do projeto.

🚨 **2. Erro de Carregamento de Sementes:** UnicodeDecodeError: 'utf-8' codec can't decode...
Causa: O terminal do Windows em português utiliza a codificação legada Windows-1252 e falha ao interpretar strings com acentuação regional do cardápio (ex: café, pão).

Solução: Antes de executar o comando loaddata, force o terminal do sistema operacional a operar no padrão internacional UTF-8 injetando a variável de ambiente:

No PowerShell: $env:PYTHONUTF8=1

No Prompt de Comando (CMD): set PYTHONUTF8=1

Alternativa: O arquivo dados_iniciais.json contido neste repositório já foi convertido nativamente para UTF-8 Puro para mitigar esse comportamento.

Caso o terminal continue brigando, significa que o arquivo foi salvo com a codificação antiga do Windows quando você fez o export. 

Vamos limpá-lo:
1.Abra o arquivo dados_iniciais.json no VS Code do novo PC.
2.Na barra inferior direita do VS Code, clique onde diz a codificação atual (pode estar aparecendo UTF-8 ou Windows-1252).
3.Selecione a opção "Save with Encoding" (Salvar com Codificação) e escolha UTF-8.
4.Salve o arquivo (Ctrl + S) e tente rodar o python manage.py loaddata dados_iniciais.json de novo no terminal.

🚨 **3. Intercepção ao Fechar Pedido:** HTTP 403 Forbidden (CSRF cookie not set.)
Causa: O navegador do novo computador não possui histórico de navegação local, fazendo com que as requisições assíncronas em segundo plano do JavaScript (Fetch API) sejam barradas por ausência do cookie criptográfico.

Solução: O template injeta nativamente o bloco seguro {% csrf_token %} na árvore do DOM. Caso ocorra a intercepção em navegadores limpos, basta atualizar a página inicial do Totem utilizando o comando Ctrl + F5 para forçar o servidor a descarregar e fixar a assinatura de segurança nos cookies locais.

## 🛠️ Tecnologias Utilizadas
Este projeto foi construído utilizando as seguintes ferramentas e bibliotecas para garantir robustez e escalabilidade:

* **Python 3.x:** Linguagem base para o desenvolvimento do back-end.
* **Django 5.2.x:** Framework web de alto nível para desenvolvimento rápido e seguro.
* **Django Rest Framework (DRF):** Toolkit para construção de APIs RESTful flexíveis.
* **SQLite:** Banco de dados relacional para persistência local e portabilidade acadêmica.
* **Docker & Docker-Compose:** Para conteinerização e isolamento do ambiente de execução.
* **Decouple (.env):** Para gestão segura de variáveis de ambiente e configurações sensíveis.

## 📂 Estrutura de Pastas do Projeto:
A organização dos arquivos reflete a divisão estrita de responsabilidades proposta pela **Clean Architecture**, isolando o domínio e as regras de negócio de componentes externos:

```text
├── app_raizesnordeste_ru4674539/ 
│   └── aplication/ 
│       └── serializers.py                      
│   └── domain/  
│       ├── canal_venda.py
│       ├── cliente.py
│       ├── filial.py
│       ├── pedido.py
│       └── produto.py   
│   └── infrastructure/
│   └── migrations/
│       └── 0001_initial.py 
│   └── static/
│       └── app_raizesnordeste_ru4674539/
│           └── css/
│           └── JS/
├── templates/ 
│   └── app_raizesnordeste_ru4674539/ 
│       └── pages/
│       └── partial/                              
│       ├── admin.py                
│       ├── apps.py
│       ├── models.py
│       ├── testes.py
│       ├── urls.py
│       └── views.py                     
├── base_templates/ 
│   ├── global/   
│       └── base.html            
├── core/ 
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── venv
├── .env
├── .gitignore
├── db.sqlite3
├── docker-compose.yml          
├── manage.py                    
├── README.md
└── requirements.txt
```

## 🚀 Endpoints da API e Regras de Negócio Implementadas

A API foi projetada seguindo as especificações do estudo de caso, garantindo contratos de dados rígidos (JSON), validações de segurança e tratamento de erros integrados.

### 1. Registro de Pedidos e Fidelização Automática (RF03)
* **Rota:** `POST /api/pedidos/`
* **Descrição:** Recebe a requisição dos canais de venda (ex: Totem). O preço não é enviado pelo cliente para evitar fraudes; o back-end busca o valor real no banco de dados, calcula o montante total da venda de forma atômica e atualiza instantaneamente o saldo de fidelidade do cliente cadastrado (R$ 1,00 gasto = 1 ponto acumulado).

**Exemplo de Payload Enviado (Front-end):**
```json
{
    "id_cliente": 1,
    "id_filial": 2,
    "canal_venda": "Totem",
    "itens": [
        {
            "id_produto": 1,
            "quantidade": 2
        }
    ]
}
```

### 2. Painel da Cozinha e Leitura Profunda / Nested Reads (RF01)
* **Rota:** GET /api/pedidos/
* **Descrição:** Permite que as cozinhas e gerentes listem os pedidos em tempo real. Utiliza serialização profunda com SerializerMethodField para aninhar os detalhes de consumo, exibindo o nome comercial do produto e preço unitário consolidado.

**Exemplo de Payload Enviado (Front-end):**
```json
[
    {
        "id_pedido": 1,
        "id_cliente": 1,
        "id_filial": 2,
        "canal_venda": "Totem",
        "itens": [
            {
                "id_produto": 1,
                "nome_produto": "Cuzcuz com ovo",
                "quantidade": 2,
                "preco_pago": "12.00"
            }
        ],
        "valor_total": "24.00",
        "data_pedido": "2026-05-18T19:33:01.997506-03:00"
    }
]
```

### 🛡️ **Tratamento de Erros e Integridade (RNF04)**
A API responde sob um contrato previsível. Caso haja envio de chaves estrangeiras inválidas ou dados nulos em campos obrigatórios, o sistema intercepta a operação retornando HTTP 400 Bad Request com o mapeamento exato da falha:

```json
{
    "id_cliente": [
        "Pk inválido \"99\" - objeto não existe."
    ]
}
```