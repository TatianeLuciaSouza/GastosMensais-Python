import datetime
from Conexao import ConexaoBD
from tkinter import ttk, messagebox
from tkinter import *
from TelaPDF import TelaPDF
class Interagir:
    def carregarComboConta(self):
        self.conexao = ConexaoBD.conectar(self)
        resultado = self.conexao.execute("Select Concat(tp_produto_id,' - ',descricao) From tp_produto_tb")
        tipoContas = resultado.fetchall()
        self.conexao.close()
        return [conta[0] for conta in tipoContas]

    def carregarComboProduto(self,indice_conta):
        self.conexao = ConexaoBD.conectar(self)
        resultado = self.conexao.execute("Select Concat(produto_id,' - ',nome) From produto_tb Where tp_produto_id = ?", (indice_conta))
        produtos = resultado.fetchall()
        self.conexao.close()
        return [produto[0] for produto in produtos]

    def carregarGrid(self, event):
        self.conexao = ConexaoBD.conectar(self)

        #Verifica se a conexão está aberta
        if not hasattr(self, 'conexao') or self.conexao is None:
            self.conexao = ConexaoBD.conectar(self)

        self.mes = str(datetime.date.today().month)

        resultado = self.conexao.execute("Select prod.nome, c.valor, p.parcela From contas_tb c "
                                         "Inner Join produto_tb prod On c.produto_id = prod.produto_id "
                                         "Inner Join parcelas_tb p On p.conta_id = c.conta_id "
                                         "Where Month(p.dt_parcela) = '" + self.mes + "'")
        registros = resultado.fetchall()
        self.contas.delete(*self.contas.get_children())  # Limpa os registros na Treeview
        for registro in registros:
            #Obtém os valores do registro
            nome, valor, parcela = registro

            # Formata os valores conforme necessário
            produto_formatado = f'{nome:10}'
            valor_formatado = f'R$ {valor:.2f}'  # Exemplo: R$ 10.50
            parcela_formatada = f'{parcela:10}'

            # Insere o registro formatado na Treeview
            self.contas.insert("", "end", values=(produto_formatado, valor_formatado, parcela_formatada))


    def novaConta(self):
        self.comando = "pIncluirConta ?, ?, ?, ?"
        self.conexao = ConexaoBD.conectar(self)

        indice_conta = self.cbConta.get()
        indice_produto = self.cbProduto.get()

        produto = str(indice_produto[4:])
        conta = str(indice_conta[4:])
        valor = self.txtValor.get()
        parcela = self.cbparcela.get()

        if not produto:
            messagebox.showinfo("Erro", "O campo produto está vazio! Favor preencher.")
            return

        if not conta:
            messagebox.showinfo("Erro", "O campo tipo do produto está vazio! Favor preencher.")
            return

        if not parcela:
            messagebox.showinfo("Erro", "O campo parcela está vazio! Favor preencher.")
            return

        if not valor:
            messagebox.showinfo("Erro", "O campo valor está vazio! Favor preencher.")
            return

        resultado = self.conexao.execute(self.comando, conta, produto, valor, int(parcela))

        if resultado.description != None:
            message = self.conexao.fetchone()[0]
            messagebox.showerror("Erro", message)
            self.conexao.close()
            return

        self.conexao.commit()
        self.conexao.close()

        self.cbProduto.delete(0, END)
        self.cbConta.delete(0, END)
        self.cbparcela.delete(0, END)
        self.txtValor.delete(0, END)

        # Atualizar o grid
        self.carregarGrid(event=None)

    def telaRelatorio(self, valor):
        self.tela_pdf = TelaPDF(self)
        self.tela_pdf.janela.deiconify()

    def sair(self, valor):
        self.janela.quit()

Interagir()