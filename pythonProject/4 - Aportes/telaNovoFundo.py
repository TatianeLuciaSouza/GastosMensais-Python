from tkinter import *
from novoFundo import novoFundo

#janela = Tk()
#janela.iconify()

class TelaNovoFundo(novoFundo):
    def __init__(self, root):
        self.root = root
        self.janela = Tk()
        self.tela()
        self.frame()
        self.botoes()

    def tela(self):
        self.janela.title("Novo Aporte")
        self.janela.configure(background='#836FFF')
        self.janela.geometry("400x300")
        self.janela.resizable(False, False)

    def frame(self):
        self.frame1 = Frame(self.janela, bd=1, bg='#E6E6FA', highlightbackground='black', highlightthickness=2)
        self.frame1.place(relx=0.10 , rely=0.05, relwidth=0.80, relheight=0.80)

        #Labels
        self.lbl1 = Label(self.frame1, text="Nome da Empresa:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl1.place(relx=0.05, rely=0.10)
        self.lbl2 = Label(self.frame1, text="Tipo do Fundo:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl2.place(relx=0.05, rely=0.30)
        self.lbl3 = Label(self.frame1, text="Ticker:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl3.place(relx=0.05, rely=0.50)
        self.lbl4 = Label(self.frame1, text="Categoria:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl4.place(relx=0.05, rely=0.68)
        self.lbl5 = Label(self.frame1, text="(F - FIIS / A - Ações)", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl5.place(relx=0.30, rely=0.68)

        #Textboxs
        self.txtempresa = Entry(self.frame1)
        self.txtempresa.place(relx=0.48, rely=0.10, relwidth=0.50)

        self.txttipo = Entry(self.frame1)
        self.txttipo.place(relx=0.39, rely=0.30, relwidth=0.40)

        self.txtticker = Entry(self.frame1)
        self.txtticker.place(relx=0.23, rely=0.50, relwidth=0.20)

        self.txtescolha = Entry(self.frame1)
        self.txtescolha.place(relx=0.30, rely=0.80, relwidth=0.10)

    def botoes(self):
        #Botões
        self.registrar = Button(self.janela, text="Incluir", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                                 command=self.incluirFundo)
        self.registrar.place(relx=0.42, rely=0.88, relwidth=0.15, relheight=0.09)

        self.voltar = Button(self.janela, text="Voltar", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                             command=self.janela.destroy)
        self.voltar.place(relx=0.86, rely=0.89, relwidth=0.12, relheight=0.09)

    def voltarTelaPrincipal(self):
        self.janela.iconify()

