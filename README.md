# 📋 Sistema de Gestão de Demandas

Aplicação web desenvolvida como parte de um **desafio técnico para Analista de Desenvolvimento Júnior**, com o objetivo de facilitar o cadastro, a consulta e o acompanhamento de demandas internas.

O projeto prioriza **funcionalidade, validação de dados, organização do código e aplicação de regras de negócio**, com uma interface simples e objetiva.

## 🚀 Funcionalidades

- Cadastro de demandas com título, descrição, data de solicitação, setor e status.
- Validação dos campos obrigatórios, da data e do status informado.
- Definição **automática da prioridade** de cada demanda.
- Consulta das demandas cadastradas, com filtro por status.
- Painel de indicadores com total de demandas e agrupamentos por status, setor e prioridade.
- Persistência local dos dados usando SQLite.
- Mensagens de sucesso e de erro após o envio do formulário.

## 🛠️ Tecnologias utilizadas

| Tecnologia | Utilização |
| --- | --- |
| Python | Lógica da aplicação e regras de negócio |
| Flask | Rotas HTTP e processamento dos formulários |
| SQLite | Armazenamento das demandas |
| HTML | Estrutura da interface |
| CSS | Estilização da interface |
| `unittest` | Testes automatizados |

## 🧠 Regras de negócio

### Validação do cadastro

O sistema não permite cadastrar uma demanda com campos obrigatórios vazios. Também verifica se a data está em um formato válido e se o status pertence às opções permitidas: **Pendente**, **Em andamento** ou **Concluída**.

### Prioridade automática

A prioridade é calculada a partir da descrição da demanda:

- Se a descrição contiver **"urgente"** ou **"erro"**, a prioridade será **Alta**.
- Caso contrário, a prioridade será **Normal**.

A comparação não diferencia letras maiúsculas e minúsculas. O usuário não precisa informar a prioridade manualmente.

```python
def calcular_prioridade(descricao):
    texto = descricao.casefold()
    return "Alta" if "urgente" in texto or "erro" in texto else "Normal"
```

## 🏗️ Estrutura do projeto

```text
desafio_demandas/
├── app.py                 # Rotas, validações, regras de negócio e acesso ao banco
├── requirements.txt       # Dependências Python
├── templates/
│   └── index.html         # Formulário, listagem e indicadores
├── static/
│   └── style.css          # Estilos da interface
├── tests/
│   └── test_app.py        # Testes automatizados
└── README.md              # Documentação
```

O banco `demandas.db` é gerado localmente na primeira execução da aplicação.

### Organização do código

O projeto adota uma organização simples por responsabilidades: a interface fica nos arquivos HTML/CSS, as rotas são tratadas pelo Flask, e funções específicas executam validações e cálculo de prioridade. O acesso ao SQLite também está implementado em `app.py`.

Essa estrutura foi escolhida para atender ao escopo do desafio sem adicionar camadas ou abstrações desnecessárias.

## ⚙️ Como executar

**Pré-requisito:** Python instalado no computador.

1. Clone o repositório e acesse a pasta do projeto:

   ```bash
   git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
   cd SEU-REPOSITORIO
   ```

   > Substitua os valores acima pelo endereço e nome reais do seu repositório.

2. Instale as dependências:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Execute a aplicação:

   ```bash
   python app.py
   ```

4. Acesse no navegador:

   ```text
   http://127.0.0.1:5000
   ```

> A configuração atual utiliza o servidor de desenvolvimento do Flask, destinado ao uso local. Para publicação em produção, são necessários ajustes de segurança e implantação.

## 🧪 Testes automatizados

O projeto contém testes com `unittest` para verificar:

- Atribuição da prioridade Alta e Normal.
- Cadastro e consulta de demandas.
- Rejeição de campos obrigatórios não preenchidos.
- Rejeição de status inválido.

Para executar os testes a partir da raiz do projeto:

```bash
python -m unittest discover -s tests -v
```

## 📊 Indicadores

O painel apresenta:

- **Total de demandas:** quantidade geral cadastrada.
- **Demandas por status:** distribuição entre os status registrados.
- **Demandas por setor:** distribuição por área solicitante.
- **Demandas por prioridade:** comparação entre prioridades Alta e Normal.

Os indicadores são obtidos por consultas SQL com `COUNT(*)` e `GROUP BY`.

## 💡 Decisões técnicas

- **Flask:** framework leve para implementar uma aplicação web de pequeno porte.
- **SQLite:** permite persistência de dados sem a necessidade de instalar um servidor de banco de dados.
- **SQL parametrizado:** utilizado nas consultas com valores fornecidos pelo usuário, evitando concatená-los diretamente ao SQL.
- **Funções específicas:** a validação e a definição de prioridade foram separadas em funções para facilitar testes e manutenção.
- **Escopo objetivo:** prioridade para os requisitos do desafio, sem funcionalidades adicionais que aumentassem a complexidade.

## 🔮 Possíveis melhorias

- Edição e exclusão de demandas.
- Autenticação e controle de acesso.
- Histórico de mudanças de status.
- Paginação e filtros adicionais.
- Separação da persistência em um módulo próprio e migração para um banco de dados servidor, se necessário.

## 📌 Contexto

Projeto desenvolvido para demonstrar conhecimentos de **lógica de programação, validação de dados, regras de negócio, SQL e desenvolvimento web com Python**.
