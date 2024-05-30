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
        self.janela.title("Objetivos")
        self.janela.configure(background='#836FFF')
        self.janela.geometry("600x300")
        self.janela.resizable(False, False)
        self.carregarGrid(event=None)

    def frame(self):
        self.frame1 = Frame(self.janela, bd=1, bg='#E6E6FA', highlightbackground='black', highlightthickness=2)
        self.frame1.place(relx=0.02, rely=0.05, relwidth=0.50, relheight=0.90)

        #Labels
        self.lbl1 = Label(self.frame1, text="Tipo Objetivo:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl1.place(relx=0.02, rely=0.05)

        self.lbl4 = Label(self.frame1, text="Objetivo:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl4.place(relx=0.02, rely=0.18)

        self.lbl2 = Label(self.frame1, text="Valor Total do Objetivo:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl2.place(relx=0.02, rely=0.30)

        self.lbl3 = Label(self.frame1, text="Valor Inicial:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl3.place(relx=0.02, rely=0.42)

        self.lbl4 = Label(self.frame1, text="Descrição:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl4.place(relx=0.02, rely=0.53)

        #Botões
        self.btnObjetivo = Button(self.frame1, text="Novo Objetivo", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                                 command=self.novoObjetivo)
        self.btnObjetivo.place(relx=0.30, rely=0.85, relwidth=0.35, relheight=0.12)

        self.btnFinalizar = Button(self.janela, text="Finalizar", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.btnFinalizar.place(relx=0.75, rely=0.88, relwidth=0.12, relheight=0.08)

        #Combos
        contas = self.carregarComboConta()
        contas_formatados = [f"{conta:10}" for conta in contas]
        self.cbConta = ttk.Combobox(self.frame1, values=contas_formatados)
        self.cbConta.place(relx=0.35, rely=0.05, relwidth=0.64)

        objetivos = self.carregarComboObjetivo()
        objetivos_formatados = [f"{objetivo:10}" for objetivo in objetivos]
        self.cbObjetivo = ttk.Combobox(self.frame1, values=objetivos_formatados)
        self.cbObjetivo.place(relx=0.24, rely=0.18, relwidth=0.75)

        #Textboxs
        self.txtDescricao = Entry(self.frame1)
        self.txtDescricao.place(relx=0.27, rely=0.53, relwidth=0.70, height=70)

        self.txtValorTotal = Entry(self.frame1)
        self.txtValorTotal.place(relx=0.56, rely=0.30, relwidth=0.20)

        self.txtValorInicial = Entry(self.frame1)
        self.txtValorInicial.place(relx=0.32, rely=0.42, relwidth=0.20)

    def grid(self):
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview", font=("Arial", 8, 'bold'), foreground='black')
        self.objetivos = ttk.Treeview(self.janela, column=("ID", "Objetivo", "Valor Final", "Valor Atual", "Descrição", "Status"), style="Custom.Treeview")
        self.objetivos.pack()
        colunas = ["ID", "Objetivo", "Valor Final", "Valor Atual", "Descrição", "Status"]

        self.objetivos.heading("#0", text="")
        self.objetivos.column("#0", width=0, stretch=False)

        for coluna in colunas:
            self.objetivos.heading(coluna, text=coluna)
            self.objetivos.column(coluna, width=30)

        self.objetivos.column("#1", width=0, stretch=False)
        self.objetivos.place(relx=0.53, rely=0.05, relwidth=0.46, relheight=0.80)
        self.objetivos.bind("<Double-1>", self.finalizarObjetivo)

    def botoes(self):
        self.btnRelatorio = Button(janela, text="Relatório", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.btnRelatorio.bind("<Button-1>", self.telaRelatorio)
        self.btnRelatorio.place(relx=0.62, rely=0.88, relwidth=0.12, relheight=0.08)

        self.btnSair = Button(janela, text="Sair", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.btnSair.bind("<Button-1>", self.sair)
        self.btnSair.place(relx=0.92, rely=0.88, relwidth=0.07, relheight=0.08)

app = Tela(janela)
