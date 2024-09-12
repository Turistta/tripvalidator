# Microsserviço de Validação de Itinerário

## Introdução

Este documento detalha a arquitetura e o funcionamento de um microsserviço REST destinado à validação de roteiros de viagem gerados para os usuários. Utilizando modelos de NLP comerciais e APIs de terceiros, o serviço avalia a coerência, a viabilidade e a adequação dos itinerários sugeridos, garantindo que estejam em conformidade com as preferências dos usuários e sejam realistas para execução.

O objetivo é fornecer um feedback detalhado sobre possíveis ajustes nos itinerários, assegurando que eles sejam sintaticamente corretos, semanticamente viáveis, e que a validação seja idempotente e consistente.

## Funcionalidades

O microsserviço oferece as seguintes funcionalidades:

1. **Validação Sintática**: Garante que o itinerário fornecido esteja corretamente estruturado.
2. **Validação Semântica**: Utiliza modelos de IA para verificar a viabilidade das rotas e coerência do roteiro.
3. **Sugestões de Otimização**: Oferece sugestões para melhorar os segmentos de viagem, como trocas de pontos de interesse, ajuste de tempo de parada, etc.
4. **Feedback Detalhado**: Fornece feedback sobre possíveis falhas ou melhorias no roteiro.

### Componentes Principais

1. **Servidor FastAPI**: Gerencia requisições e coordena as interações com as APIs de validação de IA.
2. **Serviço de Validação de Itinerário**: Responsável por enviar dados para a API de NLP e processar as respostas para fornecer feedback e sugestões.
3. **Parser de Resultados**: Processa os resultados brutos das APIs de IA e transforma em um formato compreensível para o cliente.

### Fluxo de Dados

1. **Recepção de Dados**: O cliente envia um pedido contendo um itinerário de viagem a ser validado.
2. **Validação de Itinerário**: O Serviço de Validação constrói um pedido para a API de IA, utilizando o itinerário fornecido.
3. **Recebimento e Processamento de Resultados**: A resposta da IA é processada pelo parser de validação, transformando o feedback em sugestões de melhorias no itinerário.
4. **Resposta ao Cliente**: Um objeto JSON contendo o feedback, sugestões e a pontuação de validação é enviado ao cliente.

## Integração com APIs de IA

### API OpenAI

- **Endpoint**: `https://api.openai.com/v1/chat/completions`
- **Função**: Valida o itinerário gerado, fornecendo feedback detalhado sobre coerência e sugestões de melhoria.

## Instalação

### Pré-requisitos

- Python 3.12 ou superior
- [Ambiente Virtual](https://docs.python.org/3/library/venv.html#venv-def) (recomendado)
- Chave de API OpenAI

#### Instalação de Dependências

Instale as dependências usando o `pip`:

```bash
pip install -r requirements.txt
```

#### Configuração das Variáveis de Ambiente

Renomeie o arquivo `.env_sample` para `.env` e configure as variáveis, incluindo a chave da API OpenAI.

### Execução

Para iniciar o servidor FastAPI:

```bash
cd src
uvicorn server:app --reload --port 3000 --host 0.0.0.0
```

### Testes

Para executar todos os testes:

```bash
pytest
```

Você pode também executar testes individuais para cada serviço:

```bash
pytest src/tests/validation
```

Executa apenas os testes de validação de itinerário.