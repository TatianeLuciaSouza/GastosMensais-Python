import datetime
from tkinter import *
from tkinter import ttk
from InteracaoTela import Interagir

janela = Tk()

class Tela(Interagir):
    def __init__(self, root):
        self.root = root
        self.janela = janela
        self.grid()
        self.tela()
        self.frame()
        self.botoes()
        janela.mainloop()

    def tela(self):
        self.janela.title("Contas Mensais")
        self.janela.configure(background='#836FFF')
        self.janela.geometry("600x300")
        self.janela.resizable(False, False)
        self.lblData = Label(text="Contas deste mês, " + str(datetime.date.today()), bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lblData.place(relx=0.10, rely=0.05)
        self.carregarGrid(event=None)

    def habilitar_combo(self,event):
        if self.cbConta.get() == -1:
            self.cbProduto["state"] = "disabled"
            self.cbProduto["value"] = ""
        else:
            self.cbProduto["state"] = "normal"
            indice_conta = self.cbConta.get()
            id = str(indice_conta.split()[0])
            produtos = self.carregarComboProduto(id)
            produtos_formatados = [f"{produto:10}" for produto in produtos]
            self.cbProduto['values'] = produtos_formatados
    def frame(self):
        self.frame1 = Frame(self.janela, bd=1, bg='#E6E6FA', highlightbackground='black', highlightthickness=2)
        self.frame1.place(relx=0.55 , rely=0.10, relwidth=0.43, relheight=0.80)

        #Labels
        self.lbl1 = Label(self.frame1, text="Tipo Conta:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl1.place(relx=0.02, rely=0.10)

        self.lbl4 = Label(self.frame1, text="Tipo:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl4.place(relx=0.02, rely=0.32)

        self.lbl2 = Label(self.frame1, text="Valor:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl2.place(relx=0.02, rely=0.55)

        self.lbl3 = Label(self.frame1, text="Parcela:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl3.place(relx=0.48, rely=0.55)

        #Botões
        self.btnConta = Button(self.frame1, text="Nova Conta", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                                 command=self.novaConta)
        self.btnConta.place(relx=0.35, rely=0.80, relwidth=0.35, relheight=0.12)
        self.btnConta.bind("<<ComboboxSelected>>", self.carregarGrid)

        #Combos
        contas = self.carregarComboConta()
        contas_formatados = [f"{conta:10}" for conta in contas]
        self.cbConta = ttk.Combobox(self.frame1, values=contas_formatados)
        self.cbConta.place(relx=0.33, rely=0.10, relwidth=0.63)


        selecao = self.cbConta.get()
        if len(selecao) > 0:
            self.indice_conta = selecao[0]
            produtos = self.carregarComboProduto(self.indice_conta)
            produtos_formatados = [f"{produto:10}" for produto in produtos]
            self.cbProduto = ttk.Combobox(self.frame1, values=produtos_formatados)
            self.cbProduto.place(relx=0.18, rely=0.32, relwidth=0.78)
            self.cbProduto["state"] = "disabled"
        else:
            self.cbProduto = ttk.Combobox(self.frame1)
            self.cbProduto.place(relx=0.18, rely=0.32, relwidth=0.78)
            self.cbProduto["state"] = "disabled"

        self.cbparcela = ttk.Combobox(self.frame1, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        self.cbparcela.place(relx=0.71, rely=0.55, relwidth=0.18)

        self.cbConta.bind("<<ComboboxSelected>>", self.habilitar_combo)

        #Textboxa
        self.txtValor = Entry(self.frame1)
        self.txtValor.place(relx=0.19, rely=0.55, relwidth=0.20)
    def grid(self):
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview", font=("Arial", 8, 'bold'), foreground='black')  # foreground='red'
        self.contas = ttk.Treeview(self.janela, column=("Nome", "Valor", "Parcela"), style="Custom.Treeview")
        self.contas.pack()
        colunas = ["Nome", "Valor", "Parcela"]

        self.contas.heading("#0", text="")
        self.contas.column("#0", width=0, stretch=False)

        for coluna in colunas:
            self.contas.heading(coluna, text=coluna)
            self.contas.column(coluna, width=30)

        self.contas.place(relx=0.02, rely=0.15, relwidth=0.50, relheight=0.74)

    def botoes(self):
        self.btnRelatorio = Button(janela, text="Relatório", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.btnRelatorio.bind("<Button-1>", self.telaRelatorio)
        self.btnRelatorio.place(relx=0.20, rely=0.91, relwidth=0.15, relheight=0.08)

        self.btnSair = Button(janela, text="Sair", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.btnSair.bind("<Button-1>", self.sair)
        self.btnSair.place(relx=0.90, rely=0.91, relwidth=0.08, relheight=0.08)

app = Tela(janela)
