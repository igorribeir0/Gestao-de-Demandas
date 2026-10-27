# Gestão de Demandas Internas

Solução desenvolvida para o **Desafio Técnico – Analista de Desenvolvimento Júnior**.

## Tecnologias

- **Python + Flask:** aplicação web, rotas e validação das informações.
- **SQLite:** banco de dados local, criado automaticamente no primeiro uso.
- **HTML/CSS:** formulário de cadastro, consulta de demandas e resumo visual.

## Como executar

É necessário ter Python 3.10 ou superior instalado.

1. Abra um terminal na pasta deste projeto.
2. Instale a dependência:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Inicie a aplicação:

   ```bash
   python app.py
   ```

4. Acesse **http://127.0.0.1:5000** no navegador.

No Windows, caso `python` não seja reconhecido, experimente `py`.

## Estrutura

```text
app.py                Lógica, validação, rotas e persistência SQLite
requirements.txt      Dependência Python
README.md             Documentação
static/style.css      Estilos da interface
templates/index.html  Formulário, lista de demandas e painel de resumo
tests/test_app.py     Testes da regra e do cadastro
```

O arquivo `demandas.db` é criado após a primeira execução, armazenando os registros localmente.

## Regras de negócio

1. Título, descrição, data de solicitação, setor e status são obrigatórios. O cadastro é recusado quando algum desses campos está vazio ou contém apenas espaços.
2. A prioridade **não é digitada pelo usuário**: se a descrição contiver `urgente` ou `erro` (sem diferença entre maiúsculas e minúsculas), a prioridade é **Alta**; caso contrário, é **Normal**.
3. A data precisa ser válida e o status deve ser um dos valores disponíveis: Pendente, Em andamento ou Concluída.
4. As demandas são armazenadas no SQLite e exibidas da mais recente para a mais antiga.

## Funcionalidades

- Cadastro de demandas com validação no servidor e campos obrigatórios na interface.
- Consulta das demandas cadastradas e filtro por status.
- Resumo visual opcional com total de demandas e contagem por status, setor e prioridade.

## Decisões técnicas

Foi escolhida uma aplicação web simples por permitir demonstração rápida. SQLite evita configurar um servidor de banco de dados. A regra de prioridade foi isolada na função `calcular_prioridade` para facilitar manutenção e testes. Consultas SQL usam parâmetros para receber valores do usuário. A aplicação mantém o escopo enxuto, priorizando lógica, funcionalidade e organização, conforme o enunciado.

## Testes

Para executar os testes automatizados:

```bash
python -m unittest discover -s tests -v
```

**Observação:** solução para execução local/demonstração técnica. Para publicação em produção, seriam necessários configuração segura da chave secreta, autenticação e configurações de servidor adequadas.
