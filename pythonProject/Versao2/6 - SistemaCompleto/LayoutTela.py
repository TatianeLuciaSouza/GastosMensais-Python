import datetime
from tkinter import *
from tkinter import ttk, filedialog
import tkinter as tk
from datetime import date
from tkcalendar import DateEntry
from Interacao import Interagir

janela = Tk()

class Aplicacao(Interagir):
    def __init__(self, root):
        self.root = root
        self.janela = janela
        self.tela()
        self.menu()
        self.gastosMensais()
        self.contas()
        self.metas()
        self.aportes()
        self.decimoTerceiro()
        self.relatorios()
        self.config()
        self.exibirFrame()
        janela.mainloop()

    def tela(self):
        self.janela.title("Projeto Completo")
        self.janela.geometry("600x300")
        self.janela.resizable(False, False)
        abas = ttk.Notebook(self.janela)
        abas.pack(padx=10, pady=10, fill='both', expand=True)

        self.aba1 = ttk.Frame(abas)
        self.aba2 = ttk.Frame(abas)
        self.aba3 = ttk.Frame(abas)
        self.aba4 = ttk.Frame(abas)
        self.aba5 = ttk.Frame(abas)
        self.aba6 = ttk.Frame(abas)
        self.aba7 = ttk.Frame(abas)

        abas.add(self.aba1, text='Menu')
        abas.add(self.aba2, text='Gastos Mensais')
        abas.add(self.aba3, text='Contas no Mês')
        abas.add(self.aba4, text='Metas')
        abas.add(self.aba5, text='Aportes')
        abas.add(self.aba6, text='Décimo Terceiro')
        abas.add(self.aba7, text='Relatórios')

    def menu(self):
        #Frame - Início
        self.frameAlterarSalario = Frame(self.aba1, bd=1, highlightbackground='black', highlightthickness=2)
        self.frameAlterarSalario.place(relx=0.20, rely=0.40, relwidth=0.60, relheight=0.55)
        #Frame - Fim

        #Labels - Início
        lblData = Label(self.aba1, text='Data: ' + str(datetime.date.today()), font=('verdana', 8, 'bold'))
        lblData.place(relx=0.25, rely=0.06, relwidth=0.20, relheight=0.05)

        self.lblNome = Label(self.aba1,  font=('verdana', 8, 'bold'))
        self.lblNome.place(relx=0.55, rely=0.06, relwidth=0.20, relheight=0.05)

        self.lblSalario = Label(self.aba1, font=('verdana', 8, 'bold'))
        self.lblSalario.place(relx=0.10, rely=0.20, relwidth=0.30, relheight=0.05)

        self.lblGastos = Label(self.aba1, font=('verdana', 8, 'bold'))
        self.lblGastos.place(relx=0.39, rely=0.20, relwidth=0.30, relheight=0.05)

        self.lblSobra = Label(self.aba1, font=('verdana', 8, 'bold'))
        self.lblSobra.place(relx=0.35, rely=0.32, relwidth=0.30, relheight=0.05)

        self.lblExtra = Label(self.aba1, font=('verdana', 8, 'bold'))
        self.lblExtra.place(relx=0.65, rely=0.20, relwidth=0.30, relheight=0.05)

        self.lblExtraF = Label(self.frameAlterarSalario, text='Extra: ', font=('verdana', 8, 'bold'))
        self.lblExtraF.place(relx=0.60, rely=0.15, relwidth=0.15, relheight=0.10)

        self.lblSalarioF = Label(self.frameAlterarSalario, text='Salário: ',  font=('verdana', 8, 'bold'))
        self.lblSalarioF.place(relx=0.15, rely=0.15, relwidth=0.15, relheight=0.10)
        #Labels - Fim

        #Textboxs - Início
        self.txtSalario = Entry(self.frameAlterarSalario)
        self.txtSalario.place(relx=0.15, rely=0.30, relwidth=0.20)
        self.txtExtra = Entry(self.frameAlterarSalario)
        self.txtExtra.place(relx=0.60, rely=0.30, relwidth=0.20)
        #Textboxs - Fim

        #Botões - Início
        self.btnAlterar = Button(self.frameAlterarSalario, text="Alterar", bd=2, font=('verdana', 8, 'bold'), command=self.alterarSalario)
        self.btnAlterar.place(relx=0.37, rely=0.60, relwidth=0.20, relheight=0.25)

        self.btnSair = Button(self.aba1, text="Sair", bd=2,font=('verdana', 8, 'bold'), command=self.sair)
        self.btnSair.place(relx=0.91, rely=0.88, relwidth=0.08, relheight=0.10)
        #Botões - Fim

        self.carregarMenu()

        for widget in self.frameAlterarSalario.winfo_children():
            widget.configure(state="disabled")

        # checkbox - Início
        self.checkAlteracao = tk.BooleanVar()
        self.checkAlteracao_value = tk.Checkbutton(self.aba1, text="Alterar Salário",
                                                   variable=self.checkAlteracao, command=self.desabilitar)
        self.checkAlteracao_value.pack()
        self.checkAlteracao_value.place(x=465, y=100)
        # checkbox - Fim
    def gastosMensais(self):
        #Labels - Início
        lblProduto = Label(self.aba2, text="Produto:", font=('verdana', 8, 'bold'))
        lblProduto.place(relx=0.02, rely=0.15)

        lblTipo = Label(self.aba2, text="Tipo:", font=('verdana', 8, 'bold'))
        lblTipo.place(relx=0.02, rely=0.28)

        lblValor = Label(self.aba2, text="Valor:", font=('verdana', 8, 'bold'))
        lblValor.place(relx=0.02, rely=0.41)

        lblQdt = Label(self.aba2, text="QTD:", font=('verdana', 8, 'bold'))
        lblQdt.place(relx=0.02, rely=0.52)

        lblLoja = Label(self.aba2, text="Loja:", font=('verdana', 8, 'bold'))
        lblLoja.place(relx=0.02, rely=0.65)
        #Labels - Fim

        # Combobox - Início
        produtos = self.carregarComboProduto()
        produtos_formatados = [f"{produto:10}" for produto in produtos]
        self.cbProdutoGasto = ttk.Combobox(self.aba2, values=produtos_formatados)
        self.cbProdutoGasto.place(relx=0.13, rely=0.15, relwidth=0.25)

        tpprodutos = self.carregarComboTpProduto()
        tpprodutos_formatados = [f"{tpproduto:10}" for tpproduto in tpprodutos]
        self.cbTpProdutoGasto = ttk.Combobox(self.aba2, values=tpprodutos_formatados)
        self.cbTpProdutoGasto.place(relx=0.09, rely=0.28, relwidth=0.25)

        lojas = self.carregarComboLoja()
        lojas_formatados = [f"{lojas:10}" for lojas in lojas]
        self.cbLojaGasto = ttk.Combobox(self.aba2, values=lojas_formatados)
        self.cbLojaGasto.place(relx=0.09, rely=0.65, relwidth=0.25)

        datas = self.carregarData()
        datas_formatados = [f"{datas:10}" for datas in datas]
        self.cbDataGasto = ttk.Combobox(self.aba2, values=datas_formatados)
        self.cbDataGasto.place(relx=0.60, rely=0.03, relwidth=0.20)
        # Combobox - Fim

        #Textbox - Início
        self.txtQtdGasto = Entry(self.aba2)
        self.txtQtdGasto.place(relx=0.09, rely=0.52, relwidth=0.20)

        self.txtValorGasto = Entry(self.aba2)
        self.txtValorGasto.place(relx=0.10, rely=0.41, relwidth=0.10)
        #Textbox - Fim

        #BTN - Início
        self.btnIncluir = Button(self.aba2, text="Incluir", bd=2, font=('verdana', 8, 'bold'), command=self.incluirGastos)
        self.btnIncluir.place(relx=0.12, rely=0.83, relwidth=0.10, relheight=0.12)
        #BTN - Fim

        #Grid - Início
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 8, 'bold'), foreground='black')
        self.gastos = ttk.Treeview(self.aba2, column=("ID", "Produto", "Qtd", "Valor", "Loja", "Data"),
                                    style="Custom.Treeview")
        style.map("Treeview",
                       foreground=[('selected', 'black')],
                       background=[('selected', 'white')])
        self.gastos.pack()
        colunas = ["ID", "Produto", "Qtd", "Valor", "Loja", "Data"]

        self.gastos.heading("#0", text="")
        self.gastos.column("#0", width=0, stretch=False)

        for coluna in colunas:
            self.gastos.heading(coluna, text=coluna)
            self.gastos.column(coluna, width=30)

        self.gastos.column("#1", width=0, stretch=False)
        self.gastos.place(relx=0.40, rely=0.15, relwidth=0.60, relheight=0.80)

        #Associa o evento ao combobox
        self.cbDataGasto.bind("<<ComboboxSelected>>", self.carregarGridGastos)
        self.gastos.bind("<Double-1>", self.alterarGastos)
        self.gastos.bind("<Delete>", self.excluirGastos)
        #Grid - Fim

    def contas(self):
        # Labels - Início
        lblData = Label(self.aba3, text="Contas deste mês, " + str(datetime.date.today()),
                        font=('verdana', 8, 'bold'))
        lblData.place(relx=0.30, rely=0.05)

        lblTproduto = Label(self.aba3, text="Tipo Conta:", font=('verdana', 8, 'bold'))
        lblTproduto.place(relx=0.02, rely=0.25)

        lblTipo = Label(self.aba3, text="Tipo:", font=('verdana', 8, 'bold'))
        lblTipo.place(relx=0.02, rely=0.38)

        lblValor = Label(self.aba3, text="Valor:", font=('verdana', 8, 'bold'))
        lblValor.place(relx=0.02, rely=0.51)

        lblParcela = Label(self.aba3, text="Parcela:", font=('verdana', 8, 'bold'))
        lblParcela.place(relx=0.02, rely=0.64)
        # Labels - Fim

        # Textbox - Início
        self.txtValorConta = Entry(self.aba3)
        self.txtValorConta.place(relx=0.10, rely=0.51, relwidth=0.10)
        # Textbox - Fim

        # Combobox - Início
        contas = self.carregarComboTpProduto()
        contas_formatados = [f"{conta:10}" for conta in contas]
        self.cbConta = ttk.Combobox(self.aba3, values=contas_formatados)
        self.cbConta.place(relx=0.16, rely=0.25, relwidth=0.20)

        selecao = self.cbConta.get()
        if len(selecao) > 0:
            indice_conta = selecao[0]
            produtos = self.carregarComboProdutoConta(indice_conta)
            produtos_formatados = [f"{produto:10}" for produto in produtos]
            self.cbProdutoConta = ttk.Combobox(self.aba3, values=produtos_formatados)
            self.cbProdutoConta.place(relx=0.09, rely=0.38, relwidth=0.28)
            self.cbProdutoConta["state"] = "disabled"
        else:
            self.cbProdutoConta = ttk.Combobox(self.aba3)
            self.cbProdutoConta.place(relx=0.09, rely=0.38, relwidth=0.25)
            #self.cbProdutoConta["state"] = "disabled"

        self.cbParcelaConta = ttk.Combobox(self.aba3, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        self.cbParcelaConta.place(relx=0.12, rely=0.64, relwidth=0.07)
        self.cbConta.bind("<<ComboboxSelected>>", self.habilitar_combo)
        # Combobox - Fim

        #BTN - Início
        self.btnConta = Button(self.aba3, text="Nova Conta", bd=2, font=('verdana', 8, 'bold'),
                               command=self.novaConta)
        self.btnConta.place(relx=0.10, rely=0.83, relwidth=0.18, relheight=0.12)
        #BTN - Fim

        # Grid - Início
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 8, 'bold'), foreground='black')
        self.contas = ttk.Treeview(self.aba3, column=("Nome", "Valor", "Parcela"), style="Custom.Treeview")
        self.contas.pack()
        colunas = ["Nome", "Valor", "Parcela"]

        self.contas.heading("#0", text="")
        self.contas.column("#0", width=0, stretch=False)

        for coluna in colunas:
            self.contas.heading(coluna, text=coluna)
            self.contas.column(coluna, width=30)

        self.contas.place(relx=0.40, rely=0.15, relwidth=0.60, relheight=0.80)
        # Grid - Fim

        # Carregar o grid no início
        self.carregarGridConta(event=None)

    def metas(self):
        # Escolha de frames - Início
        self.escolhaFrameMeta = tk.StringVar(value=" ")

        self.opcao1 = tk.Radiobutton(self.aba4, text="Nova Meta", variable=self.escolhaFrameMeta,
                                     value="Op1", command=self.exibirFrameMeta)
        self.opcao1.place(relx=0.01, rely=0.03, relwidth=0.15, relheight=0.10)

        self.opcao2 = tk.Radiobutton(self.aba4, text="Depositar ou Sacar Meta", variable=self.escolhaFrameMeta,
                                     value="Op2", command=self.exibirFrameMeta)
        self.opcao2.place(relx=0.18, rely=0.03, relwidth=0.25, relheight=0.10)
        # Escolha de frames - Fim

        # Labels - Início
        self.lblTpMeta = Label(self.aba4, text="Tipo da Meta:", font=('verdana', 8, 'bold'))
        self.lblMeta = Label(self.aba4, text="Meta:", font=('verdana', 8, 'bold'))
        self.lblVlTotalMeta = Label(self.aba4, text="Valor Total da Meta:", font=('verdana', 8, 'bold'))
        self.lblVlInicial = Label(self.aba4, text="Valor Inicial:", font=('verdana', 8, 'bold'))
        self.lblDesc = Label(self.aba4, text="Descrição:", font=('verdana', 8, 'bold'))
        self.lblDepositar = Label(self.aba4, text="Depositar:", font=('verdana', 8, 'bold'))
        self.lblSacar = Label(self.aba4, text="Sacar:", font=('verdana', 8, 'bold'))
        self.lblDescMeta = Label(self.aba4, text="Descrição:", font=('verdana', 8, 'bold'))
        # Labels - Fim

        # Textbox - Início
        self.txtDescricaoMeta = Entry(self.aba4)
        self.txtValorTotalMeta = Entry(self.aba4)
        self.txtValorInicialMeta = Entry(self.aba4)
        self.txtVlDeposita = Entry(self.aba4)
        self.txtVlSaca = Entry(self.aba4)
        self.txtDescMeta = Entry(self.aba4)
        # Textbox - Fim

        # Combobox - Início
        tipoMetas = self.carregarComboContaMeta()
        tipoMeta_formatados = [f"{tipoMeta:10}" for tipoMeta in tipoMetas]
        self.cbTipoMeta = ttk.Combobox(self.aba4, values=tipoMeta_formatados)

        metas = self.carregarComboMeta()
        metas_formatados = [f"{meta:10}" for meta in metas]
        self.cbMetas = ttk.Combobox(self.aba4, values=metas_formatados)
        # Combobox - Fim

        # BTN - Início
        self.btnMeta = Button(self.aba4, text="Nova Meta", bd=2, font=('verdana', 8, 'bold'),command=self.novaMeta)
        # BTN - Fim

        # Grid - Início
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 8, 'bold'), foreground='black')
        self.metas = ttk.Treeview(self.aba4,column=("ID", "Meta", "Valor Final", "Valor Atual", "Descrição", "Status"),style="Custom.Treeview")
        self.metas.pack()
        colunas = ["ID", "Meta", "Valor Final", "Valor Atual", "Descrição", "Status"]

        self.metas.heading("#0", text="")
        self.metas.column("#0", width=0, stretch=False)

        for coluna in colunas:
            self.metas.heading(coluna, text=coluna)
            self.metas.column(coluna, width=30)

        self.metas.column("#1", width=0, stretch=False)
        self.metas.place(relx=0.48, rely=0.05, relwidth=0.50, relheight=0.90)
        self.metas.bind("<Double-1>", self.finalizarMeta)
        # Grid - Fim

        # Carregar o grid no início
        self.carregarGridMetas(event=None)

    def aportes(self):
        #Tipo de escolha - Início
        self.escolhaFrame = tk.StringVar(value=" ")

        self.opcao1 = tk.Radiobutton(self.aba5, text="Novo Aporte", variable=self.escolhaFrame,
                                value="Op1", command=self.exibirFrame)
        self.opcao1.place(relx=0.60, rely=0.05, relwidth=0.15, relheight=0.10)

        self.opcao2 = tk.Radiobutton(self.aba5, text="Novo Fundo", variable=self.escolhaFrame,
                                value="Op2", command=self.exibirFrame)
        self.opcao2.place(relx=0.80, rely=0.05, relwidth=0.15, relheight=0.10)

        self.escolhaFundo = tk.StringVar(value=" ")

        self.opcao3 = tk.Radiobutton(self.aba5, text="FIIS", variable=self.escolhaFundo,
                                     value="F", command=self.tipoFundo)
        self.opcao3.place(relx=0.13, rely=0.88, relwidth=0.15, relheight=0.10)

        self.opcao4 = tk.Radiobutton(self.aba5, text="Ações", variable=self.escolhaFundo,
                                     value="A", command=self.tipoFundo)
        self.opcao4.place(relx=0.25, rely=0.88, relwidth=0.15, relheight=0.10)
        #Tipo de escolha - Fim

        #Frames - Início
        self.frameFundo = Frame(self.aba5, bd=1, highlightbackground='black', highlightthickness=2)

        self.frameAporte = Frame(self.aba5, bd=1, highlightbackground='black', highlightthickness=2)
        #Frames - Fim


        # Labels - Início
        self.lbl1 = Label(self.frameFundo, text="Nome da Empresa:", font=('verdana', 8, 'bold'))
        self.lbl1.place(relx=0.05, rely=0.10)
        self.lbl2 = Label(self.frameFundo, text="Tipo do Fundo:", font=('verdana', 8, 'bold'))
        self.lbl2.place(relx=0.05, rely=0.30)
        self.lbl3 = Label(self.frameFundo, text="Ticker:", font=('verdana', 8, 'bold'))
        self.lbl3.place(relx=0.05, rely=0.50)
        self.lbl4 = Label(self.frameFundo, text="Categoria:", font=('verdana', 8, 'bold'))
        self.lbl4.place(relx=0.05, rely=0.68)
        self.lbl5 = Label(self.frameFundo, text="(F - FIIS / A - Ações)", font=('verdana', 8, 'bold'))
        self.lbl5.place(relx=0.30, rely=0.68)

        self.lbl6 = Label(self.frameAporte, text="Ticker:", font=('verdana', 8, 'bold'))
        self.lbl6.place(relx=0.05, rely=0.10)
        self.lbl7 = Label(self.frameAporte, text="Qtd Cotas:", font=('verdana', 8, 'bold'))
        self.lbl7.place(relx=0.53, rely=0.10)
        self.lbl8 = Label(self.frameAporte, text="Valor cota:", font=('verdana', 8, 'bold'))
        self.lbl8.place(relx=0.05, rely=0.55)
        self.lbl9 = Label(self.frameAporte, text="Rendimento:", font=('verdana', 8, 'bold'))
        self.lbl9.place(relx=0.53, rely=0.55)
        # Labels - Fim

        # Textbox - Início
        self.txtempresa = Entry(self.frameFundo)
        self.txtempresa.place(relx=0.48, rely=0.10, relwidth=0.50)
        self.txttipo = Entry(self.frameFundo)
        self.txttipo.place(relx=0.39, rely=0.30, relwidth=0.40)
        self.txtticker = Entry(self.frameFundo)
        self.txtticker.place(relx=0.23, rely=0.50, relwidth=0.20)
        self.txtescolha = Entry(self.frameFundo)
        self.txtescolha.place(relx=0.30, rely=0.80, relwidth=0.10)


        self.txtCota = Entry(self.frameAporte)
        self.txtCota.place(relx=0.60, rely=0.25, relwidth=0.20)
        self.txtVlCota = Entry(self.frameAporte)
        self.txtVlCota.place(relx=0.11, rely=0.70, relwidth=0.20)
        self.txtRendMes = Entry(self.frameAporte)
        self.txtRendMes.place(relx=0.62, rely=0.70, relwidth=0.20)
        # Textbox - Fim

        # Combobox - Início
        tickers = self.carregarComboTicker()
        tickers_formatados = [f"{ticker:10}" for ticker in tickers]
        self.cbTicker = ttk.Combobox(self.frameAporte, values=tickers_formatados)
        self.cbTicker.place(relx=0.07, rely=0.25, relwidth=0.25)
        # Combobox - Fim

        # BTN - Início
        self.btnAportes = Button(self.aba5, text="Novo Aporte", bd=2, font=('verdana', 8, 'bold'))
        # BTN - Fim

        # Grid - Início
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview", font=("Arial", 8, 'bold'), foreground='black')
        self.fundos = ttk.Treeview(self.aba5, column=("Nome da Empresa", "Tipo do Fundo", "Ticker",
                                                        "Total de Cotas", "Total Investido", "Contas adquiridas",
                                                        "Valor da última cota", "Investido no Mês", "Mes/Ano"),
                                   style="Custom.Treeview")
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
        self.fundos.place(relx=0.021, rely=0.03, relwidth=0.50, relheight=0.80)
        # Grid - Fim

    def decimoTerceiro(self):
        #Frames - Início
        self.frame1 = Frame(self.aba6, bd=1, highlightbackground='black', highlightthickness=2)
        self.frame1.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.20)

        self.frame2 = Frame(self.aba6, bd=1, highlightbackground='black', highlightthickness=2)
        self.frame2.place(relx=0.05, rely=0.68, relwidth=0.90, relheight=0.30)
        #Frames - Fim

        # Labels - Início
        lblParcela1 = Label(self.frame1, text="1ºParcela:", font=('verdana', 8, 'bold'))
        lblParcela1.place(relx=0.02, rely=0.05)

        lblParcela2 = Label(self.frame1, text="2ºParcela:", font=('verdana', 8, 'bold'))
        lblParcela2.place(relx=0.33, rely=0.05)

        lblTotal = Label(self.frame1, text="Total:", font=('verdana', 8, 'bold'))
        lblTotal.place(relx=0.02, rely=0.50)

        lblSobra = Label(self.frame1, text="Sobra:", font=('verdana', 8, 'bold'))
        lblSobra.place(relx=0.33, rely=0.50)

        lblDespesa = Label(self.frame2, text="Despesa:", font=('verdana', 8, 'bold'))
        lblDespesa.place(relx=0.02, rely=0.05)

        lblTpDespesa = Label(self.frame2, text="Tipo:", font=('verdana', 8, 'bold'))
        lblTpDespesa.place(relx=0.38, rely=0.02)

        lblLocal = Label(self.frame2, text="Local:", font=('verdana', 8, 'bold'))
        lblLocal.place(relx=0.68, rely=0.02)

        lblValor = Label(self.frame2, text="Valor:", font=('verdana', 8, 'bold'))
        lblValor.place(relx=0.40, rely=0.60)

        lblDesc = Label(self.frame2, text="Descrição:", font=('verdana', 8, 'bold'))
        lblDesc.place(relx=0.02, rely=0.60)
         # Labels - Fim

        # Textbox - Início
        self.txtparcela1 = Entry(self.frame1)
        self.txtparcela1.place(relx=0.16, rely=0.05, relwidth=0.15)

        self.txtparcela2 = Entry(self.frame1, state="disabled")
        self.txtparcela2.place(relx=0.47, rely=0.05, relwidth=0.15)

        self.txtVlTotal = Entry(self.frame1, state="disabled")
        self.txtVlTotal.place(relx=0.10, rely=0.50, relwidth=0.15)

        self.txtSobra = Entry(self.frame1, state="disabled")
        self.txtSobra.place(relx=0.42, rely=0.50, relwidth=0.15)

        self.txtValor = Entry(self.frame2)
        self.txtValor.place(relx=0.49, rely=0.60, relwidth=0.10)

        self.txtDescricao = Entry(self.frame2)
        self.txtDescricao.place(relx=0.17, rely=0.60, relwidth=0.20)
        # Textbox - Fim

        # Combobox - Início
        datas = self.carregarData13()
        datas_formatados = [f"{datas:10}" for datas in datas]
        self.cbData13 = ttk.Combobox(self.aba6, values=datas_formatados)
        self.cbData13.place(relx=0.73, rely=0.12, relwidth=0.20)
        self.cbData13.bind("<KeyRelease-BackSpace>", self.limpar)

        despesas = self.carregarComboProduto()
        despesas_formatados = [f"{despesa:10}" for despesa in despesas]
        self.cbDespesa = ttk.Combobox(self.frame2, values=despesas_formatados)
        self.cbDespesa.place(relx=0.15, rely=0.06, relwidth=0.20)

        tpdespesas = self.carregarComboTpProduto()
        tpdespesas_formatados = [f"{tpdespesa:10}" for tpdespesa in tpdespesas]
        self.cbTpDespesa = ttk.Combobox(self.frame2, values=tpdespesas_formatados)
        self.cbTpDespesa.place(relx=0.46, rely=0.06, relwidth=0.20)

        lojas = self.carregarComboLoja()
        lojas_formatados = [f"{lojas:10}" for lojas in lojas]
        self.cbLoja = ttk.Combobox(self.frame2, values=lojas_formatados)
        self.cbLoja.place(relx=0.77, rely=0.06, relwidth=0.20)
        # Combobox - Fim

        # BTN - Início
        self.btnOk = Button(self.frame1, text="Ok", bd=2, font=('verdana', 8, 'bold'),
                            command=self.incluirParcela)
        self.btnOk.place(relx=0.64, rely=0.06, relwidth=0.06, relheight=0.40)

        self.btnDespesa = Button(self.frame2, text="Incluir Despesa", bd=2, font=('verdana', 8, 'bold'),
                                 command=self.incluirDespesa)
        self.btnDespesa.place(relx=0.70, rely=0.55, relwidth=0.22, relheight=0.30)
        # BTN - Fim

        # Grid - Início
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 8, 'bold'), foreground='black')
        self.despesas = ttk.Treeview(self.aba6, column=("ID", "Despesa", "Descrição", "Valor"),
                                     style="Custom.Treeview")
        style.map("Treeview",
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
        self.despesas.place(relx=0.05, rely=0.30, relwidth=0.90, relheight=0.30)

        self.cbData13.bind("<<ComboboxSelected>>", self.carregar)

        self.despesas.bind("<Double-1>", self.alterar)
        self.despesas.bind("<Delete>", self.excluir)
        # Grid - Fim

        #Configurações - Início
        for widget in self.frame2.winfo_children():
            widget.configure(state="disabled")

        ano = self.cbData13.get().strip()
        data = str(datetime.date.today().year)

        if ano == data:
            for widget in self.frame2.winfo_children():
                widget.configure(state="normal")

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

            for widget in self.frame2.winfo_children():
                widget.configure(state="disabled")
        #Configurações - Fim
    def relatorios(self):
        # Frames - Início
        frame1 = Frame(self.aba7, bd=1, highlightbackground='black', highlightthickness=2)
        frame1.place(relx=0.02, rely=0.22, relwidth=0.40, relheight=0.50)

        frame2 = Frame(self.aba7, bd=1, highlightbackground='black', highlightthickness=2)
        frame2.place(relx=0.48, rely=0.10, relwidth=0.50, relheight=0.80)
        # Frames - Fim

        #Opções de relatório - início
        self.escolha = tk.StringVar(value=" ")

        opcao1 = tk.Radiobutton(frame1, text="Emitir Relatório - Gastos Mensais", variable=self.escolha,
                                     value="Op1", command=self.config)
        opcao1.place(relx=0.02, rely=0.05, relwidth=0.85, relheight=0.10)

        opcao2 = tk.Radiobutton(frame1, text="Emitir Relatório - Contas do mês", variable=self.escolha,
                                     value="Op2", command=self.config)
        opcao2.place(relx=0.02, rely=0.30, relwidth=0.85, relheight=0.10)

        opcao3 = tk.Radiobutton(frame1, text="Emitir Relatório - Metas", variable=self.escolha,
                                     value="Op3", command=self.config)
        opcao3.place(relx=0.02, rely=0.55, relwidth=0.65, relheight=0.10)

        opcao4 = tk.Radiobutton(frame1, text="Emitir Relatório - Aportes", variable=self.escolha,
                                     value="Op4", command=self.config)
        opcao4.place(relx=0.02, rely=0.80, relwidth=0.68, relheight=0.10)
        #Opções de relatório - Fim

        # Labels - Início
        self.lblProduto = Label(frame2, text="Produto:", font=('verdana', 8, 'bold'))
        self.lblTpConta = Label(frame2, text="Tipo Conta:", font=('verdana', 8, 'bold'))
        self.lblAte = Label(frame2, text="Até", font=('verdana', 8, 'bold'))
        self.lblTpFundo = Label(frame2, text="Tipo de Fundo:", font=('verdana', 8, 'bold'))
        self.lblTicker = Label(frame2, text="Ticker:", font=('verdana', 8, 'bold'))
        # Labels - Fim

        # Combobox - Início
        produtos = self.carregarComboProduto()
        produtos_formatados = [f"{produto:10}" for produto in produtos]
        self.cbProdutoRelat = ttk.Combobox(frame2, values=produtos_formatados)

        contas = self.carregarComboTpProduto()
        contas_formatados = [f"{conta:10}" for conta in contas]
        self.cbContaRelatorio = ttk.Combobox(frame2, values=contas_formatados)

        #Obter a data atual
        data_atual = date.today()

        # Criar o DateEntry com o calendário
        self.data1 = DateEntry(frame2, date_pattern='dd/mm/yyyy', width=12, background='darkblue',
                               foreground='white', borderwidth=2,
                               year=data_atual.year, month=data_atual.month, day=data_atual.day)
        self.data2 = DateEntry(frame2, date_pattern='dd/mm/yyyy', width=12, background='darkblue',
                               foreground='white', borderwidth=2,
                               year=data_atual.year, month=data_atual.month, day=data_atual.day)
        self.cbFundo = ttk.Combobox(frame2, values=["FIIS", "Ações", "Ambos"])
        self.cbTicker2 = ttk.Combobox(frame2)
        self.cbFundo.bind("<<ComboboxSelected>>", self.opcoes)
        # Combobox - Fim

        # BTN - Início
        self.emitir = Button(frame2, text="Emitir PDF", bd=2, font=('verdana', 8, 'bold'),
                             command=self.selecionar_caminho)
        # BTN - Fim

        #checkbox - Início
        self.checkbox_value = tk.BooleanVar()
        self.checkAtivo = tk.Checkbutton(frame2, text="Ativo", variable=self.checkbox_value)
        self.checkAtivo.pack()
        # checkbox - Fim

    ####################################################################################################################

    #Funções
    def config(self):
        opcao_selecionada = self.escolha.get()
        if opcao_selecionada == "Op1": #Gastos Mensais
            self.lblTpFundo.place_forget()
            self.cbFundo.place_forget()
            self.cbContaRelatorio.place_forget()
            self.checkAtivo.config(state="disabled")
            self.checkAtivo.pack_forget()
            self.lblTicker.place_forget()
            self.cbTicker2.place_forget()

            self.lblProduto.place(relx=0.05, rely=0.10)
            self.lblTpConta.place(relx=0.05, rely=0.30)
            self.lblTpConta.config(text="Tipo de Conta:")
            self.data1.place(relx=0.05, rely=0.53)
            self.lblAte.place(relx=0.45, rely=0.53)
            self.data2.place(relx=0.60, rely=0.53)
            self.cbProdutoRelat.place(relx=0.27, rely=0.08, relwidth=0.30)
            self.cbContaRelatorio.place(relx=0.40, rely=0.30, relwidth=0.30)
            self.emitir.place(relx=0.35, rely=0.80, relwidth=0.30, relheight=0.12)
        elif opcao_selecionada == "Op2": #Contas
            self.lblTpFundo.place_forget()
            self.cbFundo.place_forget()
            self.cbProdutoRelat.place_forget()
            self.cbContaRelatorio.place_forget()
            self.lblProduto.place_forget()
            self.cbTicker2.place_forget()
            self.lblTicker.place_forget()
            self.checkAtivo.config(state="normal")

            self.lblTpConta.place(relx=0.05, rely=0.10)
            self.lblTpConta.config(text="Tipo de Conta:")
            self.data1.place(relx=0.05, rely=0.45)
            self.lblAte.place(relx=0.45, rely=0.45)
            self.data2.place(relx=0.60, rely=0.45)
            self.cbContaRelatorio.place(relx=0.40, rely=0.08, relwidth=0.30)
            self.checkAtivo.place(x=200, y=15)
            self.emitir.place(relx=0.35, rely=0.80, relwidth=0.30, relheight=0.12)
        elif opcao_selecionada == "Op3": #Metas
            self.lblTpFundo.place_forget()
            self.cbFundo.place_forget()
            self.cbProdutoRelat.place_forget()
            self.cbContaRelatorio.place_forget()
            self.lblProduto.place_forget()
            self.cbTicker2.place_forget()
            self.lblTicker.place_forget()
            self.checkAtivo.config(state="normal")

            self.lblTpConta.place(relx=0.05, rely=0.10)
            self.lblTpConta.config(text="Tipo de Meta:")
            self.data1.place(relx=0.05, rely=0.45)
            self.lblAte.place(relx=0.45, rely=0.45)
            self.data2.place(relx=0.60, rely=0.45)
            self.cbContaRelatorio.place(relx=0.38, rely=0.08, relwidth=0.30)
            self.checkAtivo.place(x=200, y=15)
            self.emitir.place(relx=0.35, rely=0.80, relwidth=0.30, relheight=0.12)
        elif opcao_selecionada == "Op4": #Aportes
            self.cbProdutoRelat.place_forget()
            self.cbContaRelatorio.place_forget()
            self.lblProduto.place_forget()
            self.lblTpConta.place_forget()
            self.checkAtivo.config(state="normal")

            self.lblTpFundo.place(relx=0.05, rely=0.10)
            self.cbFundo.place(relx=0.41, rely=0.10, relwidth=0.30)
            self.data1.place(relx=0.05, rely=0.53)
            self.lblAte.place(relx=0.45, rely=0.53)
            self.data2.place(relx=0.60, rely=0.53)
            self.checkAtivo.place(x=210, y=18)
            self.emitir.place(relx=0.35, rely=0.80, relwidth=0.30, relheight=0.12)
            self.cbTicker2.place(relx=0.24, rely=0.30, relwidth=0.30)
            self.lblTicker.place(relx=0.05, rely=0.30)
        else:
            self.cbContaRelatorio.place_forget()
            self.data1.place_forget()
            self.data2.place_forget()
            self.cbProdutoRelat.place_forget()
            self.cbContaRelatorio.place_forget()
            self.lblProduto.place_forget()
            self.lblAte.place_forget()
            self.lblTpFundo.place_forget()
            self.cbFundo.place_forget()
            self.lblTpConta.place_forget()
            self.checkAtivo.pack_forget()
            self.emitir.place_forget()
            self.cbTicker2.place_forget()
            self.lblTicker.place_forget()

    def exibirFrame(self):
        opcaoFrame_selecionada = self.escolhaFrame.get()
        if opcaoFrame_selecionada == "Op1":
            self.frameFundo.place_forget()
            self.frameAporte.place(relx=0.53, rely=0.24, relwidth=0.45, relheight=0.50)
            self.btnAportes.place(relx=0.65, rely=0.83, relwidth=0.18, relheight=0.10)
            self.btnAportes.config(text="Novo Aporte", command=self.incluirAporte)
            self.fundos.place(relx=0.021, rely=0.03, relwidth=0.50, relheight=0.80)
        elif opcaoFrame_selecionada == "Op2":
            self.frameAporte.place_forget()
            self.frameFundo.place(relx=0.44, rely=0.23, relwidth=0.55, relheight=0.60)
            self.btnAportes.place(relx=0.63, rely=0.87, relwidth=0.16, relheight=0.10)
            self.btnAportes.config(text="Novo Fundo", command=self.incluirFundo)
            self.fundos.place(relx=0.021, rely=0.03, relwidth=0.40, relheight=0.80)
        else:
            self.frameFundo.place_forget()
            self.frameAporte.place_forget()
            self.btnAportes.place_forget()

    def exibirFrameMeta(self):
        opcaoFrameMeta_selecionada = self.escolhaFrameMeta.get()
        if opcaoFrameMeta_selecionada == "Op1":
            self.lblDepositar.place_forget()
            self.lblSacar.place_forget()
            self.lblDescMeta.place_forget()
            self.txtVlDeposita.place_forget()
            self.txtVlSaca.place_forget()
            self.txtDescMeta.place_forget()

            self.lblTpMeta.place(relx=0.02, rely=0.15)
            self.lblMeta.place(relx=0.02, rely=0.28)
            self.lblVlTotalMeta.place(relx=0.02, rely=0.41)
            self.lblVlInicial.place(relx=0.02, rely=0.55)
            self.lblDesc.place(relx=0.02, rely=0.71)
            self.txtDescricaoMeta.place(relx=0.15, rely=0.71, relwidth=0.30, height=30)
            self.txtValorTotalMeta.place(relx=0.26, rely=0.41, relwidth=0.20)
            self.txtValorInicialMeta.place(relx=0.18, rely=0.56, relwidth=0.20)
            self.cbTipoMeta.place(relx=0.18, rely=0.15, relwidth=0.25)
            self.cbMetas.place(relx=0.09, rely=0.28, relwidth=0.25)
            self.btnMeta.place(relx=0.15, rely=0.88, relwidth=0.15, relheight=0.10)
            self.btnMeta.config(text='Nova Meta', command=self.novaMeta)
        elif opcaoFrameMeta_selecionada == "Op2":
            self.lblVlTotalMeta.place_forget()
            self.lblVlInicial.place_forget()
            self.lblDesc.place_forget()
            self.txtDescricaoMeta.place_forget()
            self.txtValorTotalMeta.place_forget()
            self.txtValorInicialMeta.place_forget()

            self.lblTpMeta.place(relx=0.02, rely=0.15)
            self.lblMeta.place(relx=0.02, rely=0.28)
            self.lblDepositar.place(relx=0.02, rely=0.41)
            self.lblSacar.place(relx=0.02, rely=0.55)
            self.lblDescMeta.place(relx=0.02, rely=0.71)
            self.txtVlDeposita.place(relx=0.15, rely=0.41, relwidth=0.20)
            self.txtVlSaca.place(relx=0.10, rely=0.56, relwidth=0.20)
            self.txtDescMeta.place(relx=0.15, rely=0.71, relwidth=0.30, height=30)
            self.cbTipoMeta.place(relx=0.18, rely=0.15, relwidth=0.25)
            self.cbMetas.place(relx=0.09, rely=0.28, relwidth=0.25)
            self.btnMeta.place(relx=0.13, rely=0.88, relwidth=0.20, relheight=0.10)
            self.btnMeta.config(text='Atualizar Saldo', command=self.DepositaMeta)
        else:
            self.lblTpMeta.place_forget()
            self.lblMeta.place_forget()
            self.lblVlTotalMeta.place_forget()
            self.lblVlInicial.place_forget()
            self.lblDesc.place_forget()
            self.txtDescricaoMeta.place_forget()
            self.txtValorTotalMeta.place_forget()
            self.txtValorInicialMeta.place_forget()
            self.cbTipoMeta.place_forget()
            self.cbMetas.place_forget()
            self.btnMeta.place_forget()
            self.lblDepositar.place_forget()
            self.lblSacar.place_forget()
            self.lblDescMeta.place_forget()
            self.txtVlDeposita.place_forget()
            self.txtVlSaca.place_forget()
            self.txtDescMeta.place_forget()
    def habilitar_combo(self, event):
        if self.cbConta.get() == -1:
            self.cbProdutoConta["state"] = "disabled"
            self.cbProdutoConta["value"] = ""
        else:
            self.cbProdutoConta["state"] = "normal"
            indice_conta = self.cbConta.get()
            id = str(indice_conta.split()[0])
            produtos = self.carregarComboProdutoConta(id)
            produtos_formatados = [f"{produto:10}" for produto in produtos]
            self.cbProdutoConta['values'] = produtos_formatados

    def tipoFundo(self):
        opcaoFundo_selecionado = self.escolhaFundo.get()

        if opcaoFundo_selecionado == 'F':
            self.carregarGridFundo("F")
        elif opcaoFundo_selecionado == 'A':
            self.carregarGridFundo("A")

    def limpar(self, event):
        if not self.cbData13.get().strip():
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

    def config13(self):
        ano = self.cbData13.get().strip()
        data = str(datetime.date.today().year)

        if ano == data:
            for widget in self.frame2.winfo_children():
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

            for widget in self.frame2.winfo_children():
                widget.configure(state="disabled")
            self.btnDespesa.configure(state="disabled")

    def opcoes(self, event):
        escolha_fundo =  self.cbFundo.get()
        if escolha_fundo == 'FIIS':
            fundos = self.carregarComboTicker2(1)
            fundos_formatados = [f"{fundo:10}" for fundo in fundos]
            self.cbTicker2['values'] = fundos_formatados
        elif escolha_fundo == 'Ações':
            fundos = self.carregarComboTicker2(2)
            fundos_formatados = [f"{fundo:10}" for fundo in fundos]
            self.cbTicker2['values'] = fundos_formatados
        elif escolha_fundo == 'Ambos':
            fundos = self.carregarComboTicker2(3)
            fundos_formatados = [f"{fundo:10}" for fundo in fundos]
            self.cbTicker2['values'] = fundos_formatados

    def selecionar_caminho(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".pdf")
        if caminho:
            self.criar_pdf(caminho)

    def desabilitar(self):
        if self.checkAlteracao.get() == 1:
            for widget in self.frameAlterarSalario.winfo_children():
                widget.configure(state="normal")
        else:
            for widget in self.frameAlterarSalario.winfo_children():
                widget.configure(state="disabled")

    def atualizarCombos(self, qual):
        if qual == 1: #Gastos
            produtos = self.carregarComboProduto()
            produtos_formatados = [f"{produto:10}" for produto in produtos]
            self.cbProdutoGasto.config(values=produtos_formatados)

            tpprodutos = self.carregarComboTpProduto()
            tpprodutos_formatados = [f"{tpproduto:10}" for tpproduto in tpprodutos]
            self.cbTpProdutoGasto.config(values=tpprodutos_formatados)

            lojas = self.carregarComboLoja()
            lojas_formatados = [f"{lojas:10}" for lojas in lojas]
            self.cbLojaGasto.config(values=lojas_formatados)

        elif qual == 2: #Contas
            contas = self.carregarComboTpProduto()
            contas_formatados = [f"{conta:10}" for conta in contas]
            self.cbConta.config(values=contas_formatados)

            selecao = self.cbConta.get()
            if len(selecao) > 0:
                indice_conta = selecao[0]
                produtos = self.carregarComboProdutoConta(indice_conta)
                produtos_formatados = [f"{produto:10}" for produto in produtos]
                self.cbProdutoConta.config(values=produtos_formatados)
                self.cbProdutoConta["state"] = "disabled"
        elif qual == 3: #Metas
            tipoMetas = self.carregarComboContaMeta()
            tipoMeta_formatados = [f"{tipoMeta:10}" for tipoMeta in tipoMetas]
            self.cbTipoMeta.config(values=tipoMeta_formatados)

            metas = self.carregarComboMeta()
            metas_formatados = [f"{meta:10}" for meta in metas]
            self.cbMetas.config(values=metas_formatados)
        elif qual == 4: #Aportes
            tickers = self.carregarComboTicker()
            tickers_formatados = [f"{ticker:10}" for ticker in tickers]
            self.cbTicker.config(values=tickers_formatados)
        elif qual == 5: #Décimo13
            despesas = self.carregarComboProduto()
            despesas_formatados = [f"{despesa:10}" for despesa in despesas]
            self.cbDespesa.config(values=despesas_formatados)

            tpdespesas = self.carregarComboTpProduto()
            tpdespesas_formatados = [f"{tpdespesa:10}" for tpdespesa in tpdespesas]
            self.cbTpDespesa.config(values=tpdespesas_formatados)

            lojas = self.carregarComboLoja()
            lojas_formatados = [f"{lojas:10}" for lojas in lojas]
            self.cbLoja.config(values=lojas_formatados)
    ####################################################################################################################
app = Aplicacao(janela)