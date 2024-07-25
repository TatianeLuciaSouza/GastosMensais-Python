from tkinter import messagebox

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from Conexao import ConexaoBD

class EmitirPDF:
    def criar_pdf(self, caminho):
        #Definir o tamanho da página e criar o objeto do documento
        doc = SimpleDocTemplate(caminho, pagesize=letter)

        #Definir o estilo do parágrafo
        styles = getSampleStyleSheet()
        estilo_titulo = styles["Title"]
        estilo_texto = ParagraphStyle(
            "estilo_texto",
            parent=styles["Normal"],
            fontSize=12,
            fontName="Helvetica-Bold"
        )

        if self.escolha.get() == 'Op1':
            texto = Paragraph("Relatório que contém todas os objetivos ativos e finalizados.",
                              estilo_texto)
            self.comando = "pRelatorioObjetivos ?, ?"
            self.conexao = ConexaoBD.conectar(self)
            tipo = 1
            resultado = self.conexao.execute(self.comando, tipo, "")

            if resultado.description != None:
                message = self.conexao.fetchone()[0]
                messagebox.showerror("Erro", message)
                self.conexao.close()
                return

            colunas = [column[0] for column in resultado.description]
            dados = [colunas] + [list(row) for row in resultado]
            tabela = Table(dados, colWidths=[85, 100, 85])
            self.conexao.close()

        elif self.escolha.get() == 'Op2':
            texto = Paragraph("Relatório que contém todas os obejtivos finalizados.",
                              estilo_texto)
            self.comando = "pRelatorioObjetivos ?, ?"
            self.conexao = ConexaoBD.conectar(self)
            tipo = 2
            resultado = self.conexao.execute(self.comando, tipo, "")

            if resultado.description != None:
                message = self.conexao.fetchone()[0]
                messagebox.showerror("Erro", message)
                self.conexao.close()
                return

            colunas = [column[0] for column in resultado.description]
            dados = [colunas] + [list(row) for row in resultado]
            tabela = Table(dados, colWidths=[85, 100, 85])
            self.conexao.close()

        elif self.escolha.get() == 'Op3':
            texto = Paragraph(
                "Relatório que contém todas os obejtivos ativos.",
                estilo_texto)
            self.comando = "pRelatorioObjetivos ?, ?"
            self.conexao = ConexaoBD.conectar(self)
            tipo = 3
            resultado = self.conexao.execute(self.comando, tipo, "")

            if resultado.description != None:
                message = self.conexao.fetchone()[0]
                messagebox.showerror("Erro", message)
                self.conexao.close()
                return

            colunas = [column[0] for column in resultado.description]
            dados = [colunas] + [list(row) for row in resultado]
            tabela = Table(dados, colWidths=[85, 100, 85])
            self.conexao.close()

        elif self.escolha.get() == 'Op4':
            texto = Paragraph(
                "Relatório que contém todas os obejtivos pelo tipo informado.",
                estilo_texto)
            self.comando = "pRelatorioObjetivos ?, ?"
            self.conexao = ConexaoBD.conectar(self)
            tipo = 4
            indice_conta = self.cbConta.get()
            id = int(indice_conta.split()[0])
            resultado = self.conexao.execute(self.comando, tipo, id)

            if resultado.description != None:
                message = self.conexao.fetchone()[0]
                messagebox.showerror("Erro", message)
                self.conexao.close()
                return

            colunas = [column[0] for column in resultado.description]
            dados = [colunas] + [list(row) for row in resultado]
            tabela = Table(dados, colWidths=[85, 100, 85])
            self.conexao.close()

        # Lista para armazenar os elementos do documento
        elementos = []

        #Adicionar o título
        titulo = Paragraph("Relatório objetivos a serem concluidos", estilo_titulo)
        elementos.append(titulo)

        elementos.append(texto)

        #Adicionar espaço entre o texto e a tabela
        espaco = Spacer(1, 20)
        elementos.append(espaco)

        #Adicionar uma tabela
        estilo_tabela = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        tabela.setStyle(estilo_tabela)

        elementos.append(tabela)
        doc.build(elementos)

    def carregarComboConta(self):
        self.conexao = ConexaoBD.conectar(self)
        resultado = self.conexao.execute("Select Concat(tp_produto_id,' - ',descricao) From tp_produto_tb")
        tipoContas = resultado.fetchall()
        self.conexao.close()
        return [conta[0] for conta in tipoContas]


