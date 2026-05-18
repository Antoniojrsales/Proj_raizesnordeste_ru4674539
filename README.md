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
git clone https://github.com/Antoniojrsales/Proj_raizesnordeste_ru4674539
cd Proj_raizesnordeste_ru4674539
```

### 2. Configurar o Ambiente Virtual (venv):
python -m venv venv
# No Windows para ativar:
.\venv\Scripts\activate
# No Linux/Mac para ativar:
source venv/bin/activate

### 3. Instalar as Dependências:
pip install -r requirements.txt

### 4. Executar as Migrações do Banco de Dados (SQLite):
python manage.py migrate

### 5. Iniciar o Servidor de Desenvolvimento:
python manage.py runserver

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