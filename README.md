# tripvalidator
Microsserviço REST com uso de NLP para validar itinerários turísticos


## Requisitos para Iniciar o Projeto

- Python 3.12+
- OpenAI API Key

## Como iniciar o serviço?
Abra o terminal e execute os comandos que forem fornecidos
### 1 - Clonar o projeto

Clonar o projeto 
```
git clone https://github.com/Turistta/tripvalidator.git
```

Entrar na raiz do projeto
```
cd tripvalidator
```


### 2 - Preparar o ambiente
Criar um Ambiente Virtual (venv) para isolar as dependências do projeto  

```
python3 -m venv venv
```

Ativar o Ambiente Virtual criado
```
source venv/bin/activate
```

### 3 - Instalar as depedências do projeto

```
pip install -r requirements.txt
```
### 4 - Configura o .env
Use o arquivo `app/.env_sample` no diretório `app` como exemplo para configurar o arquivo `.env` da aplicação.

No arquivo `.env` deve ser configurado a chave de acesso aos serviços da [OPEN AI](https://platform.openai.com/docs/quickstart). Caso ainda não tenha uma chave de acesso aos serviços da OPEN AI é necessário criar a chave antes de prosseguir, caso já tenha insira a chave no lugar adequado no arquivo `.env`.

### 5 - Iniciar o serviço
Use o comando para iniciar o serviço na porta `8000`
```
uvicorn app.main:app --reload
```

## Como parar o serviço?
### 1 - Localizar o processo que está rodando
De acordo com a configuração do projeto ele iniciara na porta 8000

Com o seguinte comando encontre o PID do processo que roda na porta 8000

```
sudo lsof -i :8000
```

Caso tenha configurado outra porta basta trocar `8000` pelo número da porta utilizada

### 2 - Encerrar o processo de forma controlada

Usando o sinal **SIGTERM**
```
kill -15 <PID>
```

Ou simplesmente utilize `CTRL + C` no terminal em que o serviço está sendo consumido.


### 3 - Desativar o ambiente virtual
Use o comando 
```
deactivate
```