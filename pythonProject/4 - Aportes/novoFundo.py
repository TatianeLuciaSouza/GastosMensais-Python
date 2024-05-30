from tkinter import messagebox, END
from Conexao import ConexaoBD
class novoFundo:
    def incluirFundo(self):
        self.comando = "pIncluirFundo ?, ?, ?, ?"
        self.conexao = ConexaoBD.conectar(self)

        emp = str(self.txtempresa.get())
        tipo = str(self.txttipo.get())
        ticker = str(self.txtticker.get())
        categora = str(self.txtescolha.get())

        if not emp:
            messagebox.showinfo("Erro", "O campo Nome da Empresa está vazio! Favor preencher.")
            return

        if not tipo:
            messagebox.showinfo("Erro", "O campo tipo do Fundo está vazio! Favor preencher.")
            return

        if not ticker:
            messagebox.showinfo("Erro", "O campo Ticker está vazio! Favor preencher.")
            return

        if not categora:
            messagebox.showinfo("Erro", "OSelecionar qual categoria do fundo, por favor!")
            return

        if categora != "A" or categora != "F":
            messagebox.showinfo("Erro", "Digite F para FIIS ou A para Ações!")
            return

        resultado = self.conexao.execute(self.comando, emp, tipo, ticker, categora)

        if resultado.description != None:
            message = self.conexao.fetchone()[0]
            messagebox.showerror("Erro", message)
            self.conexao.close()
            return

        self.conexao.commit()
        self.conexao.close()

        self.txtempresa.delete(0, END)
        self.txttipo.delete(0, END)
        self.txtticker.delete(0, END)
        self.txtescolha.delete(0, END)


novoFundo()