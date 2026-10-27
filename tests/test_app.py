import os
import tempfile
import unittest

from app import app, calcular_prioridade, inicializar_banco


class TestDemandas(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        app.config.update(TESTING=True, DATABASE=os.path.join(self.temp.name, "teste.db"))
        inicializar_banco()
        self.cliente = app.test_client()

    def tearDown(self):
        self.temp.cleanup()

    def test_prioridade_alta(self):
        self.assertEqual(calcular_prioridade("ERRO no cadastro"), "Alta")
        self.assertEqual(calcular_prioridade("Solicitação Urgente"), "Alta")

    def test_prioridade_normal(self):
        self.assertEqual(calcular_prioridade("Atualização de rotina"), "Normal")

    def test_cadastro_e_consulta(self):
        resposta = self.cliente.post("/cadastrar", data={
            "titulo": "Atualizar processo", "descricao": "Correção de ERRO",
            "data_solicitacao": "2026-10-15", "setor": "TI", "status": "Pendente"
        }, follow_redirects=True)
        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"Atualizar processo", resposta.data)
        self.assertIn(b"Alta", resposta.data)

    def test_campos_obrigatorios(self):
        resposta = self.cliente.post("/cadastrar", data={
            "titulo": "  ", "descricao": "Teste", "data_solicitacao": "2026-10-15",
            "setor": "TI", "status": "Pendente"
        }, follow_redirects=True)
        self.assertIn("Preencha todos os campos obrigatórios".encode(), resposta.data)
        self.assertIn(b"Nenhuma demanda encontrada", resposta.data)

    def test_status_invalido(self):
        resposta = self.cliente.post("/cadastrar", data={
            "titulo": "Teste", "descricao": "Teste", "data_solicitacao": "2026-10-15",
            "setor": "TI", "status": "Inexistente"
        }, follow_redirects=True)
        self.assertIn("Selecione um status válido".encode(), resposta.data)


if __name__ == "__main__":
    unittest.main()
