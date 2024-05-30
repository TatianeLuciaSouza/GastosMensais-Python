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
            self.comando = "pRelatorioaFundos ?, ?, ?, ?, ?"
            self.conexao = ConexaoBD.conectar(self)

            if self.cbOpcoes.index() == 1:
                texto = Paragraph("Relatório que contém todos os fundos existentes",
                                  estilo_texto)
                tipo = "F"
                opcao = 1

                resultado = self.conexao.execute(self.comando, tipo, opcao, "", "", "")

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 2:
                texto = Paragraph("Relatório que contém todos os fundos vendidos",
                                  estilo_texto)
                tipo = "F"  #FIIS
                opcao = 2

                resultado = self.conexao.execute(self.comando, tipo, opcao, "", "", "")

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 3:
                texto = Paragraph("Relatório que contém todos os Aportes",
                                  estilo_texto)
                tipo = "F"  #FIIS
                opcao = 3

                resultado = self.conexao.execute(self.comando, tipo, opcao, "", "", "")

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 4:
                texto = Paragraph("Relatório que contém todos os Rendimentos",
                                  estilo_texto)
                tipo = "F"  # FIIS
                opcao = 4

                dt_inicio = self.data1.get()
                dt_fim = self.data2.get()

                resultado = self.conexao.execute(self.comando, tipo, opcao, "", dt_inicio, dt_fim)

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 5:
                texto = Paragraph("Relatório que contém todos os Rendimentos Por Fundo",
                                  estilo_texto)
                tipo = "F"  # FIIS
                opcao = 5

                dt_inicio = self.data1.get()
                dt_fim = self.data2.get()

                indice_fundo = self.cbFundos.get()
                id = int(indice_fundo.split()[0])

                resultado = self.conexao.execute(self.comando, tipo, opcao, id, dt_inicio, dt_fim)

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 6:
                texto = Paragraph("Relatório que contém todos os Aportes por período",
                                  estilo_texto)
                tipo = "F"  #FIIS
                opcao = 6

                dt_inicio = self.data1.get()
                dt_fim = self.data2.get()

                resultado = self.conexao.execute(self.comando, tipo, opcao, "", dt_inicio, dt_fim)
                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 7:
                texto = Paragraph("Relatório que contém todos os Aportes por fundo",
                                  estilo_texto)
                tipo = "F"  #FIIS
                opcao = 7

                indice_fundo = self.cbFundos.get()
                id = int(indice_fundo.split()[0])

                resultado = self.conexao.execute(self.comando, tipo, opcao, id, "", "")

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 8:
                texto = Paragraph("Relatório que contém todos os Aportes por fundo e período",
                                  estilo_texto)
                tipo = "F"  #FIIS
                opcao = 8

                indice_fundo = self.cbFundos.get()
                id = int(indice_fundo.split()[0])

                dt_inicio = self.data1.get()
                dt_fim = self.data2.get()

                resultado = self.conexao.execute(self.comando, tipo, opcao, dt_inicio, dt_fim, id)

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
            self.comando = "pRelatorioaFundos ?, ?, ?, ?, ?"
            self.conexao = ConexaoBD.conectar(self)

            if self.cbOpcoes.index() == 1:
                texto = Paragraph("Relatório que contém todos as Ações existentes",
                                  estilo_texto)
                tipo = "A"  #Ações
                opcao = 1

                resultado = self.conexao.execute(self.comando, tipo, opcao, "", "", "")

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 2:
                texto = Paragraph("Relatório que contém todos as Ações vendidas",
                                  estilo_texto)
                tipo = "A"  #Ações
                opcao = 2

                resultado = self.conexao.execute(self.comando, tipo, opcao, "", "", "")

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 3:
                texto = Paragraph("Relatório que contém todos os Aportes",
                                  estilo_texto)
                tipo = "A"  #Ações
                opcao = 3

                resultado = self.conexao.execute(self.comando, tipo, opcao, "", "", "")

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 4:
                texto = Paragraph("Relatório que contém todos os Rendimentos",
                                  estilo_texto)
                tipo = "A"  # FIIS
                opcao = 4

                dt_inicio = self.data1.get()
                dt_fim = self.data2.get()

                resultado = self.conexao.execute(self.comando, tipo, opcao, "", dt_inicio, dt_fim)

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 5:
                texto = Paragraph("Relatório que contém todos os Rendimentos Por Ação",
                                  estilo_texto)
                tipo = "A"  # FIIS
                opcao = 5

                dt_inicio = self.data1.get()
                dt_fim = self.data2.get()

                indice_fundo = self.cbFundos.get()
                id = int(indice_fundo.split()[0])

                resultado = self.conexao.execute(self.comando, tipo, opcao, id, dt_inicio, dt_fim)

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 6:
                texto = Paragraph("Relatório que contém todos os Aportes por período",
                                  estilo_texto)
                tipo = "A"  #Ações
                opcao = 6

                dt_inicio = self.data1.get()
                dt_fim = self.data2.get()

                resultado = self.conexao.execute(self.comando, tipo, opcao, "", dt_inicio, dt_fim)

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 7:
                texto = Paragraph("Relatório que contém todos os Aportes por Ação",
                                  estilo_texto)
                tipo = "A"  #Ações
                opcao = 7

                indice_fundo = self.cbFundos.get()
                id = int(indice_fundo.split()[0])

                resultado = self.conexao.execute(self.comando, tipo, opcao, id, "", "")

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 8:
                texto = Paragraph("Relatório que contém todos os Aportes por Ação e Período",
                                  estilo_texto)
                tipo = "A"  #Ações
                opcao = 8

                indice_fundo = self.cbFundos.get()
                id = int(indice_fundo.split()[0])

                dt_inicio = self.data1.get()
                dt_fim = self.data2.get()

                resultado = self.conexao.execute(self.comando, tipo, opcao, dt_inicio, dt_fim, id)

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
            self.comando = "pRelatorioaFundos ?, ?, ?, ?, ?"
            self.conexao = ConexaoBD.conectar(self)

            if self.cbOpcoes.index() == 1:
                texto = Paragraph("Relatório que contém todos os Fundos e Ações existentes",
                                  estilo_texto)
                tipo = "0"  #Ambos
                opcao = 1

                resultado = self.conexao.execute(self.comando, tipo, opcao, "", "", "")

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 2:
                texto = Paragraph("Relatório que contém todos os Fundos e Ações vendidos",
                                  estilo_texto)
                tipo = "0"  ##Ambos
                opcao = 2

                resultado = self.conexao.execute(self.comando, tipo, opcao, "", "", "")

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 3:
                texto = Paragraph("Relatório que contém todos os Aportes",
                                  estilo_texto)
                tipo = "0"  #Ambos
                opcao = 3

                resultado = self.conexao.execute(self.comando, tipo, opcao, "", "", "")

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 4:
                texto = Paragraph("Relatório que contém todos os Aportes por período",
                                  estilo_texto)
                tipo = "0"  #Ambos
                opcao = 4

                dt_inicio = self.data1.get()
                dt_fim = self.data2.get()

                resultado = self.conexao.execute(self.comando, tipo, opcao, "", dt_inicio, dt_fim)

                if resultado.description != None:
                    message = self.conexao.fetchone()[0]
                    messagebox.showerror("Erro", message)
                    self.conexao.close()
                    return

                colunas = [column[0] for column in resultado.description]
                dados = [colunas] + [list(row) for row in resultado]
                tabela = Table(dados, colWidths=[85, 100, 85])
                self.conexao.close()

            elif self.cbOpcoes.index() == 5:
                texto = Paragraph("Relatório que contém os Rendimentos",
                                  estilo_texto)
                tipo = "0"  #Ambos
                opcao = 5

                dt_inicio = self.data1.get()
                dt_fim = self.data2.get()

                resultado = self.conexao.execute(self.comando, tipo, opcao, "", dt_inicio, dt_fim)

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

    def carregarComboFundo(self, tipo):
        self.conexao = ConexaoBD.conectar(self)

        resultado = self.conexao.execute("Select Concat(fundo_id,' - ',ticker) From fundos_tb Where categoria = '" + tipo + "'")

        fundos = resultado.fetchall()
        self.conexao.close()
        return [fundo[0] for fundo in fundos]



