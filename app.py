"""Aplicação de cadastro e acompanhamento de demandas internas."""
from datetime import date
from pathlib import Path
import sqlite3

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.config.update(
    SECRET_KEY="desafio-local-altere-para-producao",
    DATABASE=str(Path(__file__).resolve().parent / "demandas.db"),
)

STATUS_PERMITIDOS = ("Pendente", "Em andamento", "Concluída")


def conectar():
    conexao = sqlite3.connect(app.config["DATABASE"])
    conexao.row_factory = sqlite3.Row
    return conexao


def inicializar_banco():
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS demandas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                data_solicitacao TEXT NOT NULL,
                setor TEXT NOT NULL,
                status TEXT NOT NULL,
                prioridade TEXT NOT NULL
            )
        """)


def calcular_prioridade(descricao):
    """Regra do desafio: urgente/erro => Alta; caso contrário => Normal."""
    texto = descricao.casefold()
    return "Alta" if "urgente" in texto or "erro" in texto else "Normal"


def validar_demanda(dados):
    campos = ("titulo", "descricao", "data_solicitacao", "setor", "status")
    if any(not str(dados.get(campo, "")).strip() for campo in campos):
        return "Preencha todos os campos obrigatórios."
    try:
        date.fromisoformat(dados["data_solicitacao"])
    except ValueError:
        return "Informe uma data de solicitação válida."
    if dados["status"] not in STATUS_PERMITIDOS:
        return "Selecione um status válido."
    return None


@app.route("/", methods=["GET"])
def inicio():
    filtro_status = request.args.get("status", "")
    if filtro_status and filtro_status not in STATUS_PERMITIDOS:
        filtro_status = ""

    with conectar() as conexao:
        if filtro_status:
            demandas = conexao.execute(
                "SELECT * FROM demandas WHERE status = ? ORDER BY id DESC", (filtro_status,)
            ).fetchall()
        else:
            demandas = conexao.execute("SELECT * FROM demandas ORDER BY id DESC").fetchall()
        total = conexao.execute("SELECT COUNT(*) AS total FROM demandas").fetchone()["total"]
        por_status = conexao.execute(
            "SELECT status AS nome, COUNT(*) AS quantidade FROM demandas GROUP BY status ORDER BY status"
        ).fetchall()
        por_setor = conexao.execute(
            "SELECT setor AS nome, COUNT(*) AS quantidade FROM demandas GROUP BY setor ORDER BY setor"
        ).fetchall()
        por_prioridade = conexao.execute(
            "SELECT prioridade AS nome, COUNT(*) AS quantidade FROM demandas GROUP BY prioridade ORDER BY prioridade"
        ).fetchall()

    return render_template(
        "index.html", demandas=demandas, total=total,
        por_status=por_status, por_setor=por_setor,
        por_prioridade=por_prioridade, status_permitidos=STATUS_PERMITIDOS,
        filtro_status=filtro_status, data_hoje=date.today().isoformat(),
    )


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    dados = {campo: request.form.get(campo, "").strip() for campo in
             ("titulo", "descricao", "data_solicitacao", "setor", "status")}
    erro = validar_demanda(dados)
    if erro:
        flash(erro, "erro")
        return redirect(url_for("inicio"))

    prioridade = calcular_prioridade(dados["descricao"])
    with conectar() as conexao:
        conexao.execute("""
            INSERT INTO demandas (titulo, descricao, data_solicitacao, setor, status, prioridade)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (dados["titulo"], dados["descricao"], dados["data_solicitacao"],
              dados["setor"], dados["status"], prioridade))

    flash(f"Demanda cadastrada com sucesso! Prioridade: {prioridade}.", "sucesso")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=True)
