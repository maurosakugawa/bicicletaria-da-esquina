# Gerenciador de estoque para uma bicicletaria
  Este projeto é um sistema básico de gerenciamento para lojas de bicicletas, desenvolvido com Django/Python. Ele permite gerenciar o estoque, as ordens de serviço, realizar checkout e gerar relatório em PDF.
## Instalação
  1. Clone o repositório ou faça download.
  2. Crie um ambiente virtual com:
     python -m venv venv
     source venv/bin/activate (Linux ou MacOs)
     venv\scripts\activate (windows)
  3. Instale as dependência:
     pip install -r requirements.txt
     * caso não tenha o pip instalado terá que instalá-lo antes.
  4. Configure o arquivo .env com as variáveis de ambiente.
  5. Realiza as migrações com:
     python manage.py migrate
  6. Inicie o servidor com:
     python manage.py runserver

## Funcionalidade
  Gerenciamento de estoque de bicicletas e peças.
  Registro de ordens de serviço.
  Controle de autenticação e níveis de permissão.
  Exportação de relatórios de serviço em PDF.
## Contribuição
  Sinta-se à vontade para abrir issues e enviar pull requests para melhorias, ou clonar e criar melhorias em seu próprio repositório.
