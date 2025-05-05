from tkinter import *
from InteracaoLogin import Login

janela = Tk()

global login_id

class Aplicacao(Login):
    def __init__(self, root):
        self.root = root
        self.janela = janela
        self.tela(),
        self.login(),
        janela.mainloop()

    def tela(self):
        self.janela.title("Login")
        self.janela.geometry("300x300")
        self.janela.resizable(False, False)

    def login(self):
        self.lblLogin = Label(janela, text='E-mail:', font=('verdana', 8, 'bold'))
        self.lblLogin.place(relx=0.40, rely=0.12, relwidth=0.20, relheight=0.30)
        self.lblSenha = Label(janela, text='Senha:', font=('verdana', 8, 'bold'))
        self.lblSenha.place(relx=0.40, rely=0.35, relwidth=0.20, relheight=0.20)
        self.lblCadastrar = Label(janela, text='Cadastrar', fg='#0000FF',  font=('verdana', 8, 'bold', "underline"),  cursor="hand2")
        self.lblCadastrar.bind_class(self.lblCadastrar, "<Button-1>", self.cadastrar)
        self.lblCadastrar.place(relx=0.37, rely=0.70, relwidth=0.25, relheight=0.05)
        self.lblEmail = Label(janela, text="E-mail:", font=('verdana', 8, 'bold'))

        self.txtLogin = Entry(janela)
        self.txtLogin.place(relx=0.15, rely=0.30, relwidth=0.70)
        self.txtSenha = Entry(janela, show="*")
        self.txtSenha.place(relx=0.37, rely=0.48, relwidth=0.25)
        self.txtEmail = Entry(janela)

        self.btnEntrar = Button(janela, text="Entrar", bd=2, font=('verdana', 8, 'bold'), command=self.logar)
        self.btnEntrar.place(relx=0.40, rely=0.60, relwidth=0.18, relheight=0.08)

        self.btnSair = Button(janela, text="Sair", bd=2, font=('verdana', 8, 'bold'), command=self.sair)
        self.btnSair.place(relx=0.85, rely=0.88, relwidth=0.13, relheight=0.10)

    def cadastrar(self, event):
        self.lblCadastrar.place_forget()
        self.txtLogin.place_forget()
        self.txtEmail.place_forget()
        self.lblEmail.place_forget()

        self.lblLogin.place(relx=0.40, rely=0.01, relwidth=0.20, relheight=0.30)
        self.lblLogin.config(text="Nome:")
        self.lblEmail.place(relx=0.40, rely=0.30, relwidth=0.20, relheight=0.05)
        self.lblSenha.place(relx=0.40, rely=0.45, relwidth=0.20, relheight=0.05)
        self.btnSair.config(text='Voltar', command=self.voltar)
        self.btnSair.place(relx=0.80, rely=0.88, relwidth=0.16, relheight=0.10)

        self.txtLogin.place(relx=0.25, rely=0.19, relwidth=0.50)
        self.txtEmail.place(relx=0.15, rely=0.35, relwidth=0.70)
        self.txtSenha.place(relx=0.37, rely=0.50, relwidth=0.25)

        self.btnEntrar.place(relx=0.35, rely=0.62, relwidth=0.28, relheight=0.08)
        self.btnEntrar.config(text='Cadastrar', command=self.cadastro)

    def voltar(self):
        self.lblEmail.place_forget()
        self.txtEmail.place_forget()
        self.lblEmail.place_forget()
        self.txtLogin.place_forget()

        self.lblCadastrar.config(text='Cadastrar')
        self.lblCadastrar.place(relx=0.37, rely=0.70, relwidth=0.25, relheight=0.05)
        self.lblCadastrar.bind_class(self.lblCadastrar, "<Button-1>", self.cadastrar)
        self.lblLogin.place(relx=0.40, rely=0.12, relwidth=0.20, relheight=0.30)
        self.lblLogin.config(text="E-mail:")
        self.lblSenha.place(relx=0.40, rely=0.35, relwidth=0.20, relheight=0.20)

        self.txtLogin.place(relx=0.15, rely=0.30, relwidth=0.70)
        self.txtSenha.place(relx=0.37, rely=0.48, relwidth=0.25)

        self.btnEntrar.place(relx=0.40, rely=0.60, relwidth=0.18, relheight=0.08)
        self.btnEntrar.config(text='Entrar', command=self.logar)
        self.btnSair.config(text='Sair', command=self.sair)
        self.btnSair.place(relx=0.85, rely=0.88, relwidth=0.13, relheight=0.10)

app = Aplicacao(janela)