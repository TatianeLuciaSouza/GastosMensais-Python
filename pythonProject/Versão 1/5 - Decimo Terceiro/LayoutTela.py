import datetime
from tkinter import *
from tkinter import ttk
from Interacao import Interagir

janela = Tk()

class Applicacao(Interagir):
    def __init__(self, root):
        self.root = root
        self.janela = janela
        self.tela()
        self.frame()
        self.comboData()
        self.grid()
        self.botoes(),
        self.configuracoes()
        janela.mainloop()

    def tela(self):
        self.janela.title("Gastos Mensais")
        self.janela.configure(background='#836FFF')
        self.janela.geometry("600x600")
        self.janela.resizable(False, False)

    def limpar(self, event):
        if not self.cbData.get().strip():
            self.txtparcela1.config(state="normal")
            self.txtparcela2.config(state="normal")
            self.txtVlTotal.config(state="normal")
            self.txtSobra.config(state="normal")

            self.txtparcela1.delete(0, END)
            self.txtparcela2.delete(0, END)
            self.txtVlTotal.delete(0, END)
            self.txtSobra.delete(0, END)

            self.txtparcela2.config(state="disabled")
            self.txtVlTotal.config(state="disabled")
            self.txtSobra.config(state="disabled")

    def configuracoes(self):
        ano = self.cbData.get().strip()
        data = str(datetime.date.today().year)

        if ano == data:
            for widget in self.frame3.winfo_children():
                widget.configure(state="normal")
            self.btnDespesa.configure(state="normal")

            self.txtValor.delete(0, END)
            self.txtDescricao.delete(0, END)
            self.cbDespesa.delete(0, END)
            self.cbTpDespesa.delete(0, END)
            self.cbLoja.delete(0, END)

        else:
            self.txtValor.delete(0, END)
            self.txtDescricao.delete(0, END)
            self.cbDespesa.delete(0, END)
            self.cbTpDespesa.delete(0, END)
            self.cbLoja.delete(0, END)

            for widget in self.frame3.winfo_children():
                widget.configure(state="disabled")
            self.btnDespesa.configure(state="disabled")

    def frame(self):
        self.frame1 = Frame(self.janela, bd=1, bg='#E6E6FA', highlightbackground='black', highlightthickness=2)
        self.frame1.place(relx=0.15 , rely=0.08, relwidth=0.70, relheight=0.08)

        self.frame2 = Frame(self.janela, bd=1, bg='#E6E6FA', highlightbackground='black', highlightthickness=2)
        self.frame2.place(relx=0.27, rely=0.18, relwidth=0.45, relheight=0.06)

        self.frame3 = Frame(self.janela, bd=1, bg='#E6E6FA', highlightbackground='black', highlightthickness=2)
        self.frame3.place(relx=0.10, rely=0.77, relwidth=0.80, relheight=0.15)

        #Labels
        self.lbl1 = Label(self.frame1, text="1ºParcela:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl1.place(relx=0.02, rely=0.25)

        self.lbl2 = Label(self.frame1, text="2ºParcela:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl2.place(relx=0.20, rely=0.25, relwidth=0.65)

        self.lbl3 = Label(self.frame2, text="Total:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl3.place(relx=0.02, rely=0.20)

        self.lbl3 = Label(self.frame2, text="Sobra:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl3.place(relx=0.27, rely=0.20, relwidth=0.65)

        self.lbl4 = Label(self.frame3, text="Despesa:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl4.place(relx=0.01, rely=0.15)

        self.lbl5 = Label(self.frame3, text="Tipo:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl5.place(relx=0.38, rely=0.15)

        self.lbl6 = Label(self.frame3, text="Local:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl6.place(relx=0.69, rely=0.15)

        self.lbl7 = Label(self.frame3, text="Valor:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl7.place(relx=0.01, rely=0.60)

        self.lbl8 = Label(self.frame3, text="Descrição:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl8.place(relx=0.35, rely=0.60)

        #Botões
        self.btnok = Button(self.frame1, text="Ok", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                                 command=self.incluir)
        self.btnok.place(relx=0.86, rely=0.25, relwidth=0.10, relheight=0.50)

        #Textboxa
        self.txtparcela1 = Entry(self.frame1)
        self.txtparcela1.place(relx=0.20, rely=0.25, relwidth=0.20)

        self.txtparcela2 = Entry(self.frame1, state="disabled")
        self.txtparcela2.place(relx=0.61, rely=0.25, relwidth=0.20)

        self.txtVlTotal = Entry(self.frame2, state="disabled")
        self.txtVlTotal.place(relx=0.18, rely=0.20, relwidth=0.25)

        self.txtSobra = Entry(self.frame2, state="disabled")
        self.txtSobra.place(relx=0.69, rely=0.20, relwidth=0.25)

        self.txtValor = Entry(self.frame3)
        self.txtValor.place(relx=0.11, rely=0.60, relwidth=0.20)

        self.txtDescricao = Entry(self.frame3)
        self.txtDescricao.place(relx=0.51, rely=0.60, relwidth=0.47)

        #Combos
        despesas = self.carregarComboDespesas()
        despesas_formatados = [f"{despesa:10}" for despesa in despesas]
        self.cbDespesa = ttk.Combobox(self.frame3, values=despesas_formatados)
        self.cbDespesa.place(relx=0.15, rely=0.15, relwidth=0.20)

        tpdespesas = self.carregarComboTpDespesas()
        tpdespesas_formatados = [f"{tpdespesa:10}" for tpdespesa in tpdespesas]
        self.cbTpDespesa= ttk.Combobox(self.frame3, values=tpdespesas_formatados)
        self.cbTpDespesa.place(relx=0.46, rely=0.15, relwidth=0.20)

        lojas = self.carregarComboLoja()
        lojas_formatados = [f"{lojas:10}" for lojas in lojas]
        self.cbLoja = ttk.Combobox(self.frame3, values=lojas_formatados)
        self.cbLoja.place(relx=0.78, rely=0.15, relwidth=0.20)

        for widget in self.frame3.winfo_children():
            widget.configure(state="disabled")
    def comboData(self):
        datas = self.carregarData()
        datas_formatados = [f"{datas:10}" for datas in datas]
        self.cbData = ttk.Combobox(self.janela, values=datas_formatados)
        self.cbData.place(relx=0.40, rely=0.03, relwidth=0.20)
        self.cbData.bind("<KeyRelease-BackSpace>", self.limpar)

    def grid(self):
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview",font=("Arial", 8, 'bold'), foreground='black') #foreground='red'
        self.despesas = ttk.Treeview(self.janela, column=("ID", "Despesa", "Descrição", "Valor"), style="Custom.Treeview")
        self.style.map("Treeview",
                  foreground=[('selected', 'black')],
                  background=[('selected', 'white')])
        self.despesas.pack()
        colunas = ["ID", "Despesa", "Descrição", "Valor"]

        self.despesas.heading("#0", text="")
        self.despesas.column("#0", width=0, stretch=False)

        for coluna in colunas:
            self.despesas.heading(coluna, text=coluna)
            self.despesas.column(coluna, width=30)

        self.despesas.column("#1", width=0, stretch=False)
        self.despesas.place(relx=0.10, rely=0.26, relwidth=0.80, relheight=0.50)

        #Associa o evento ao combobox
        self.cbData.bind("<<ComboboxSelected>>", self.carregar)

        self.despesas.bind("<Double-1>", self.alterar)
        self.despesas.bind("<Delete>", self.excluir)


    def botoes(self):
        self.btnSair = Button(janela, text="Sair", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.btnSair.bind("<Button-1>", self.sair)
        self.btnSair.place(relx=0.91, rely=0.94, relwidth=0.08, relheight=0.05)

        self.btnDespesa = Button(janela, text="Incluir Despesa", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                                 command=self.incluirDespesa)
        self.btnDespesa.place(relx=0.40, rely=0.94, relwidth=0.18, relheight=0.05)


app = Applicacao(janela)
