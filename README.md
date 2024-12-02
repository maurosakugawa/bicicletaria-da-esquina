
# Gerenciador de Estoque para uma Bicicletaria

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/) [![Django](https://img.shields.io/badge/Django-4.x-green)](https://www.djangoproject.com/) [![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey)](https://www.sqlite.org/) [![Bootstrap](https://img.shields.io/badge/Bootstrap-5.x-purple)](https://getbootstrap.com/) [![GPLv3](https://img.shields.io/badge/License-GPLv3-blue)](https://www.gnu.org/licenses/gpl-3.0.html)


Este projeto é um sistema básico de gerenciamento para lojas de bicicletas, desenvolvido com Django/Python. Ele permite gerenciar o estoque, registrar ordens de serviço e gerar relatórios em PDF.

---

## **Funcionalidades**

- 📦 **Gerenciamento de Estoque**: Controle de bicicletas e peças.
- 📋 **Ordens de Serviço**: Registro e acompanhamento das ordens.
- 🔐 **Controle de Autenticação e Permissões**: Diferentes níveis de acesso.
- 🖨️ **Relatórios em PDF**: Geração de relatórios detalhados.

---

## **Instalação**

### **1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

----------

## **Funcionalidades**

-   📦 **Gerenciamento de Estoque**: Controle de bicicletas e peças.
-   📋 **Ordens de Serviço**: Registro e acompanhamento das ordens.
-   🔐 **Controle de Autenticação e Permissões**: Diferentes níveis de acesso.
-   🖨️ **Relatórios em PDF**: Geração de relatórios detalhados.



### **2. Crie e ative um ambiente virtual**

Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
### 3. Instale as dependências
```bash
pip install -r requirements.txt
```
**Nota**: Caso não tenha o `pip` instalado, siga as instruções [aqui](https://pip.pypa.io/en/stable/installation/).

### **4. Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto e configure as variáveis necessárias. Use o exemplo fornecido em `.env.example` como base.

### 5. Aplique as migrações
```bash
python manage.py migrate
```



### **6. Popule o banco de dados (opcional)**

Caso deseje iniciar com dados de exemplo (usuários e permissões):
```bash
python manage.py loaddata fixtures/dados_iniciais.json
```
**Nota**: O arquivo `dados_iniciais.json` contém dados básicos para teste, incluindo usuários e permissões. Consulte a seção [Banco de Dados](#banco-de-dados) para mais detalhes.

### 7. Inicie o servidor
```bash
python manage.py runserver
```
Acesse o sistema em: [http://127.0.0.1:8000](http://127.0.0.1:8000)
### Banco de Dados

-   Este sistema utiliza o **SQLite3** como banco de dados padrão.
- O arquivo db.sqlite3 consta entre os arquivos do repositório, caso precise existe ainda a possibilidade de utilizar o comando abaixo para popular o banco de dados.
-   O arquivo `db.sqlite3` pode ser gerado ou carregado a partir dos dados iniciais fornecidos:
	- Execute o comando abaixo para carregar os dados:
	```bash
	python manage.py loaddata fixtures/data_db.json
	```
### **Usuários e Permissões (Dados de Teste)**

-   **Usuário Administrador**:
    -   **Username**: `admin`
    -   **Senha**: `senha1234`
    -   Permissões: Superusuário.
-   **Usuário Colaborador**:
     -   **Username**: `FuncionarioDesconhecido`
    -   **Senha**: `senha1234`
-   **Usuário Funcionario**:
     -   **Username**: `col`
    -   **Senha**: `senha1234`
**Atenção**: Altere a senha padrão ao usar o sistema em produção.

### **Contribuição**

Contribuições são bem-vindas! Sinta-se à vontade para:

-   Abrir **issues** relatando problemas ou sugerindo melhorias.
-   Enviar **pull requests** com melhorias ou correções.
-   Clonar o repositório e criar novas funcionalidades.

### **Licença**

Este projeto está licenciado sob a GPLv3 License.  
Você pode usar, modificar e distribuir o código de acordo com os termos da licença GPLv3.

