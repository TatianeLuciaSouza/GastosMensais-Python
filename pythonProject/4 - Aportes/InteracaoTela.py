from Conexao import ConexaoBD
from tkinter import ttk, messagebox
from TelaPDF import TelaPDF
from telaNovoAporte import TelaNovoAporte

class Interagir:
    def carregarGrid(self):

        if self.opcao % 2 == 0:
            tipo = 'A'
        else:
            tipo = 'F'
        self.conexao = ConexaoBD.conectar(self)

        resultado = self.conexao.execute("Select f.nm_empresa 'Nome da Empresa', f.tipo_fundo 'Tipo do Fundo', f.ticker 'Ticker',"
                                         "Case When f.categoria = 'F' Then fiis.nro_cota Else a.nro_cota End 'Total de Cotas',"
                                         "Case When f.categoria = 'F' Then fiis.vl_investido Else a.vl_investido End 'Total Investido',"
                                         "p.qtd_cota 'Contas adquiridas', p.vl_cota 'Valor da última cota', p.vl_total 'Investido no Mês',"
                                         "p.mesAno 'Mes/Ano' From fundos_tb f Left Join fiis_tb fiis On f.fundo_id = fiis.fundo_id "
                                         "Left Join acoes_tb a On f.fundo_id = a.fundo_id Inner Join aportes_tb p On f.fundo_id = p.fundo_id "
                                         "Where f.categoria = '"+ tipo + "'")
        registros = resultado.fetchall()
        self.conexao.close()
        self.fundos.delete(*self.fundos.get_children())
        for registro in registros:
            #Obtém os valores do registro
            nm_empresa, tp_fundo, ticker, tl_cotas, tl_investido, qtd_cota, vl_cota, vl_total, mesAno = registro

            #Formata os valores conforme necessário
            nm_empresa_formatado = f'{nm_empresa:10}'
            tp_fundo_formatado = f'{tp_fundo:10}'
            ticker_formatado = f'{ticker:10}'
            tl_cotas_formatada = f'{tl_cotas:10}'
            tl_investido_formatado = f'R$ {tl_investido:.2f}'
            qtd_cota_formatado = f'{qtd_cota:10}'
            vl_cota_formatado = f'R$ {vl_cota:.2f}'
            vl_total_formatado = f'R$ {vl_total:.2f}'
            mesAno_formatado = f'{mesAno:10}'

            #Insere o registro formatado na Treeview
            self.fundos.insert("", "end", values=(nm_empresa_formatado, tp_fundo_formatado, ticker_formatado,
                                                  tl_cotas_formatada, tl_investido_formatado, qtd_cota_formatado,
                                                  vl_cota_formatado, vl_total_formatado, mesAno_formatado))


        self.opcao += 1
    def telaRelatorio(self, valor):
        self.tela_pdf = TelaPDF(self)
        self.tela_pdf.janela.deiconify()

    def telaNovoAporte(self):
        self.telaNovoAporte = TelaNovoAporte(self)
        self.telaNovoAporte.janela.deiconify()

    def sair(self, valor):
        self.janela.quit()



