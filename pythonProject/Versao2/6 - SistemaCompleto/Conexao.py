import pyodbc

class ConexaoBD():
    def conectar(self):
        dados_conexao = (
            "Driver={SQL Server};"
            "Server=DESKTOP-8RMSN4M\\SQLEXPRESS;"
            "Database=GastosMensaisV2;"
            "Trusted_Connection=yes;"
        )
        conexao = pyodbc.connect(dados_conexao)
        return conexao

