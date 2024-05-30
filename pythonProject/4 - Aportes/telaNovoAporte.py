from tkinter import ttk
import tkinter as tk
from tkinter import *
from novoAporte import novoAporte

class TelaNovoAporte(novoAporte):
    def __init__(self, root):
        self.root = root
        self.janela = Tk()
        self.tela()
        self.frame()
        self.botoes()

    def tela(self):
        self.janela.title("Novo Aporte")
        self.janela.configure(background='#836FFF')
        self.janela.geometry("300x200")
        self.janela.resizable(False, False)

    def frame(self):
        self.frame1 = Frame(self.janela, bd=1, bg='#E6E6FA', highlightbackground='black', highlightthickness=2)
        self.frame1.place(relx=0.12 , rely=0.05, relwidth=0.75, relheight=0.60)

        #Labels
        self.lbl1 = Label(self.frame1, text="Ticker:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl1.place(relx=0.05, rely=0.10)
        self.lbl2 = Label(self.frame1, text="Qtd Cotas:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl2.place(relx=0.53, rely=0.10)
        self.lbl3 = Label(self.frame1, text="Valor cota:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl3.place(relx=0.05, rely=0.55)
        self.lbl4 = Label(self.frame1, text="Rendimento:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl4.place(relx=0.53, rely=0.55)

        #Combo
        tickers = self.carregarComboTicker()
        tickers_formatados = [f"{ticker:10}" for ticker in tickers]
        self.cbTicker = ttk.Combobox(self.frame1, values=tickers_formatados)
        self.cbTicker.place(relx=0.07, rely=0.25, relwidth=0.25)

        #Textboxs
        self.txtCota = Entry(self.frame1)
        self.txtCota.place(relx=0.60, rely=0.25, relwidth=0.20)

        self.txtVlCota = Entry(self.frame1)
        self.txtVlCota.place(relx=0.11, rely=0.70, relwidth=0.20)

        self.txtRendMes = Entry(self.frame1)
        self.txtRendMes.place(relx=0.62, rely=0.70, relwidth=0.20)


    def botoes(self):
        #Botões
        self.registrar = Button(self.janela, text="Registrar", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                                 command=self.incluirAporte)
        self.registrar.place(relx=0.28, rely=0.70, relwidth=0.22, relheight=0.12)

        self.voltar = Button(self.janela, text="Voltar", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                             command=self.janela.destroy)
        self.voltar.place(relx=0.53, rely=0.70, relwidth=0.16, relheight=0.12)

        self.fundo = Button(self.janela, text="Novo Fundo", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                             command=self.telaNovoFundo)
        self.fundo.place(relx=0.68, rely=0.86, relwidth=0.30, relheight=0.12)

    def voltarTelaPrincipal(self):
        self.janela.iconify()

