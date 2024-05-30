from tkinter import ttk
import tkinter as tk
from tkinter import *
from InteracaoTela import Interagir

janela = Tk()

class Tela(Interagir):
    def __init__(self, root):
        self.root = root
        self.janela = root
        self.tela()
        self.grid()
        self.frame()
        self.janela.mainloop()

    def tela(self):
        self.janela.title("Fundos de Investimentos")
        self.janela.configure(background='#000000')
        self.janela.geometry("600x300")
        self.janela.resizable(False, False)
        self.opcao = 0

    def frame(self):
        self.frame1 = Frame(self.janela, bd=1, bg='#E6E6FA', highlightbackground='black', highlightthickness=2)
        self.frame1.place(relx=0.02, rely=0.84, relwidth=0.955, relheight=0.14)

        #Variável para armazenar a escolha do usuário
        self.escolha = tk.StringVar(value=" ")


        #Botões de opção
        self.opcao1 = tk.Radiobutton(self.frame1, text="Ações", bg='#E6E6FA', variable=self.escolha,
                                     value="A", command=self.carregarGrid)
        self.opcao1.place(relx=0.27, rely=0.25, relwidth=0.11, relheight=0.50)

        self.opcao2 = tk.Radiobutton(self.frame1, text="FIIS", bg='#E6E6FA', variable=self.escolha,
                                     value="F", command=self.carregarGrid)
        self.opcao2.place(relx=0.42, rely=0.25, relwidth=0.11, relheight=0.50)

        #Botões
        self.btnaporte = Button(self.frame1, text="Novo Aporte", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                                 command=self.telaNovoAporte)
        self.btnaporte.place(relx=0.57, rely=0.25, relwidth=0.20, relheight=0.60)

        self.btnRelatorio = Button(self.frame1, text="Relatório", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.btnRelatorio.bind("<Button-1>", self.telaRelatorio)
        self.btnRelatorio.place(relx=0.03, rely=0.25, relwidth=0.12, relheight=0.60)

        self.btnSair = Button(self.frame1, text="Sair", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.btnSair.bind("<Button-1>", self.sair)
        self.btnSair.place(relx=0.90, rely=0.25, relwidth=0.07, relheight=0.60)

    def grid(self):
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview", font=("Arial", 8, 'bold'), foreground='black')
        self.fundos = ttk.Treeview(self.janela, column=("Nome da Empresa", "Tipo do Fundo", "Ticker",
                                                        "Total de Cotas", "Total Investido", "Contas adquiridas",
                                                        "Valor da última cota", "Investido no Mês", "Mes/Ano"), style="Custom.Treeview")
        self.fundos.pack()
        colunas = ["Nome da Empresa", "Tipo do Fundo", "Ticker",
                   "Total de Cotas", "Total Investido", "Contas adquiridas",
                   "Valor da última cota", "Investido no Mês", "Mes/Ano"]

        self.fundos.heading("#0", text="")
        self.fundos.column("#0", width=0, stretch=False)

        for coluna in colunas:
            self.fundos.heading(coluna, text=coluna)
            self.fundos.column(coluna, width=30)

        self.fundos.column("#1", width=0, stretch=False)
        self.fundos.place(relx=0.025, rely=0.05, relwidth=0.95, relheight=0.78)



app = Tela(janela)

