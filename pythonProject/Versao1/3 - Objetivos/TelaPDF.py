from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from EmitirPDF import EmitirPDF

class TelaPDF(EmitirPDF):
    def __init__(self, root):
        self.root = root
        self.janela = Tk()
        self.tela()
        self.frame()
        self.atualizar_tela()

    def tela(self):
        self.janela.title("Relatório de Contas")
        self.janela.configure(background='#836FFF')
        self.janela.geometry("300x300")
        self.janela.resizable(False, False)

    def selecionar_caminho(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".pdf")
        if caminho:
            self.criar_pdf(caminho)

    def frame(self):
        self.framepdf = Frame(self.janela, bd=1, bg='#E6E6FA', highlightbackground='black', highlightthickness=2)
        self.framepdf.place(relx=0.05 , rely=0.05, relwidth=0.90, relheight=0.90)

        #Variável para armazenar a escolha do usuário
        self.escolha = tk.StringVar(value=" ")

        #Botões de opção
        self.opcao1 = tk.Radiobutton(self.framepdf, text="Emitir todas os objetivos", variable=self.escolha,
                                     value="Op1",command=self.atualizar_tela)
        self.opcao1.place(relx=0.10, rely=0.05, relwidth=0.55, relheight=0.10)

        self.opcao2 = tk.Radiobutton(self.framepdf, text="Emitir Todas os Objetivos Finalizadas", variable=self.escolha,
                                     value="Op2",command=self.atualizar_tela)
        self.opcao2.place(relx=0.10, rely=0.20, relwidth=0.80, relheight=0.10)

        self.opcao3 = tk.Radiobutton(self.framepdf, text="Emitir Todas os Objetivos Ativos", variable=self.escolha,
                                     value="Op3", command=self.atualizar_tela)
        self.opcao3.place(relx=0.10, rely=0.35, relwidth=0.75, relheight=0.10)

        self.opcao4 = tk.Radiobutton(self.framepdf, text="Emitir Todos os Objetivos pelo tipo", variable=self.escolha,
                                     value="Op4", command=self.atualizar_tela)
        self.opcao4.place(relx=0.10, rely=0.50, relwidth=0.80, relheight=0.10)

        #Label
        self.lbl1 = Label(self.framepdf, text="Tipo Objetivo:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl1.place(relx=0.05, rely=0.65)

        #Combo
        contas = self.carregarComboConta()
        contas_formatados = [f"{conta:10}" for conta in contas]
        self.cbConta = ttk.Combobox(self.framepdf, values=contas_formatados)
        self.cbConta.place(relx=0.35, rely=0.50, relwidth=0.60)

        #Botões
        self.emitir = Button(self.framepdf, text="Emitir PDF", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                                 command=self.selecionar_caminho)
        self.emitir.place(relx=0.15, rely=0.85, relwidth=0.30, relheight=0.10)

        self.voltar = Button(self.framepdf, text="Voltar", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                             command=self.janela.destroy)
        self.voltar.place(relx=0.50, rely=0.85, relwidth=0.30, relheight=0.10)

    def atualizar_tela(self):
        self.opcao_selecionada = self.escolha.get()

        if self.opcao_selecionada == "Op4":
            self.cbConta.place(relx=0.35, rely=0.65, relwidth=0.60)
            self.lbl1.place(relx=0.05, rely=0.65)
        else:
            self.cbConta.place_forget()
            self.lbl1.place_forget()

    def voltarTelaPrincipal(self):
        janelaPDF.iconify()
