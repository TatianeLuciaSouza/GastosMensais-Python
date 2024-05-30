from tkinter import messagebox, END
from Conexao import ConexaoBD
from telaNovoFundo import TelaNovoFundo

class novoAporte:
    def carregarComboTicker(self):
        self.conexao = ConexaoBD.conectar(self)
        resultado = self.conexao.execute("Select ticker From fundos_tb")
        tickers = resultado.fetchall()
        self.conexao.close()
        return [ticker[0] for ticker in tickers]

    def incluirAporte(self):
        self.comando = "pIncluirAporte ?, ?, ?, ?"
        self.conexao = ConexaoBD.conectar(self)

        ticker = str(self.cbTicker.get())
        cota = int(self.txtCota.get())
        vlCota = self.txtVlCota.get()
        rendimento = self.txtRendMes.get()

        if not ticker:
            messagebox.showinfo("Erro", "O campo Ticker está vazio! Favor preencher.")
            return

        if not cota:
            messagebox.showinfo("Erro", "O campo tipo do Quantidade de Cota está vazio! Favor preencher.")
            return

        if not vlCota:
            messagebox.showinfo("Erro", "O campo Valor da Cota está vazio! Favor preencher.")
            return

        if not rendimento:
            rendimento = 0

        resultado = self.conexao.execute(self.comando, ticker, cota, vlCota, rendimento)

        if resultado.description != None:
            message = self.conexao.fetchone()[0]
            messagebox.showerror("Erro", message)
            self.conexao.close()
            return

        self.conexao.commit()
        self.conexao.close()

        self.cbTicker.delete(0, END)
        self.txtCota.delete(0, END)
        self.txtVlCota.delete(0, END)
        self.txtRendMes.delete(0, END)

    def telaNovoFundo(self):
        self.TelaNovoFundo = TelaNovoFundo(self)
        self.TelaNovoFundo.janela.deiconify()

novoAporte()