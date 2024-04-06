from tkinter import *
from tkinter import ttk
from InteracaoTela import Interagir

janela = Tk()

class Applicacao(Interagir):
    def __init__(self, root):
        self.root = root
        self.janela = janela
        self.tela()
        self.frame()
        self.comboBox()
        self.grid()
        self.botoes()
        janela.mainloop()

    def tela(self):
        self.janela.title("Gastos Mensais")
        self.janela.configure(background='#836FFF')
        self.janela.geometry("600x300")
        self.janela.resizable(False, False)

    def frame(self):
        self.frame1 = Frame(self.janela, bd=1, bg='#E6E6FA', highlightbackground='black', highlightthickness=2)
        self.frame1.place(relx=0.55 , rely=0.10, relwidth=0.43, relheight=0.80)  #0 - lado esquedo da tela / 1 - lado direito da tela

        #Labels
        self.lbl1 = Label(self.frame1, text="Produto:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl1.place(relx=0.02, rely=0.10)

        self.lbl4 = Label(self.frame1, text="Tipo:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl4.place(relx=0.02, rely=0.28)

        self.lbl2 = Label(self.frame1, text="Quantidade:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl2.place(relx=0.02, rely=0.45)

        self.lbl3 = Label(self.frame1, text="Valor:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl3.place(relx=0.59, rely=0.45)

        self.lbl3 = Label(self.frame1, text="Loja:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl3.place(relx=0.02, rely=0.62)

        #Botões
        self.btnIncluir = Button(self.frame1, text="Incluir", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                                 command=self.incluir)
        self.btnIncluir.place(relx=0.35, rely=0.85, relwidth=0.30, relheight=0.12)

        #Combos
        produtos = self.carregarComboProduto()
        produtos_formatados = [f"{produto:10}" for produto in produtos]
        self.cbProduto = ttk.Combobox(self.frame1, values=produtos_formatados)
        self.cbProduto.place(relx=0.18, rely=0.28, relwidth=0.78)

        tpprodutos = self.carregarComboTpProduto()
        tpprodutos_formatados = [f"{tpproduto:10}" for tpproduto in tpprodutos]
        self.cbTpProduto = ttk.Combobox(self.frame1, values=tpprodutos_formatados)
        self.cbTpProduto.place(relx=0.26, rely=0.10, relwidth=0.70)

        lojas = self.carregarComboLoja()
        lojas_formatados = [f"{lojas:10}" for lojas in lojas]
        self.cbLoja = ttk.Combobox(self.frame1, values=lojas_formatados)
        self.cbLoja.place(relx=0.18, rely=0.62, relwidth=0.78)

        #Textboxa
        self.txtQtd = Entry(self.frame1)
        self.txtQtd.place(relx=0.35, rely=0.45, relwidth=0.15)

        self.txtValor = Entry(self.frame1)
        self.txtValor.place(relx=0.76, rely=0.45, relwidth=0.20)
    def comboBox(self):
        datas = self.carregarData()
        datas_formatados = [f"{datas:10}" for datas in datas]
        self.cbData = ttk.Combobox(self.janela, values=datas_formatados)
        self.cbData.place(relx=0.17, rely=0.03, relwidth=0.20)

    def grid(self):
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview",font=("Arial", 8, 'bold'), foreground='black') #foreground='red'
        self.compras = ttk.Treeview(self.janela, column=("ID", "Produto", "Qtd", "Valor", "Loja", "Data"), style="Custom.Treeview")
        self.style.map("Treeview",
                  foreground=[('selected', 'black')],
                  background=[('selected', 'white')])
        self.compras.pack()
        colunas = ["ID", "Produto", "Qtd", "Valor", "Loja", "Data"]

        self.compras.heading("#0", text="")
        self.compras.column("#0", width=0, stretch=False)

        for coluna in colunas:
            self.compras.heading(coluna, text=coluna)
            self.compras.column(coluna, width=30)

        self.compras.column("#1", width=0, stretch=False)
        self.compras.place(relx=0.02, rely=0.15, relwidth=0.50, relheight=0.74)

        #Associa o evento ao combobox
        self.cbData.bind("<<ComboboxSelected>>", self.carregarGrid)
        self.compras.bind("<Double-1>", self.alterar)
        self.compras.bind("<Delete>", self.excluir)


    def botoes(self):
        self.btnRelatorio = Button(janela, text="Relatório", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.btnRelatorio.bind("<Button-1>", self.telaRelatorio)
        self.btnRelatorio.place(relx=0.20, rely=0.91, relwidth=0.15, relheight=0.08)

        self.btnSair = Button(janela, text="Sair", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.btnSair.bind("<Button-1>", self.sair)
        self.btnSair.place(relx=0.90, rely=0.91, relwidth=0.08, relheight=0.08)


app = Applicacao(janela)
