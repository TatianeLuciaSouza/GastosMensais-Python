from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from GerarPDF import EmitirPDF
from tkcalendar import DateEntry
from datetime import date


janelaPDF = Tk()
janelaPDF.iconify()

class TelaPDF(EmitirPDF):
    def __init__(self, root):
        self.root = root
        self.janela = janelaPDF
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
        self.opcao1 = tk.Radiobutton(self.framepdf, text="Emitir todas as Contas", variable=self.escolha,
                                     value="Op1",command=self.atualizar_tela)
        self.opcao1.place(relx=0.10, rely=0.05, relwidth=0.60, relheight=0.10)

        self.opcao2 = tk.Radiobutton(self.framepdf, text="Emitir Todas as Contas Finalizadas", variable=self.escolha,
                                     value="Op2",command=self.atualizar_tela)
        self.opcao2.place(relx=0.10, rely=0.20, relwidth=0.80, relheight=0.10)

        self.opcao3 = tk.Radiobutton(self.framepdf, text="Emitir Contas Especificas", variable=self.escolha,
                                     value="Op3", command=self.atualizar_tela)
        self.opcao3.place(relx=0.10, rely=0.35, relwidth=0.60, relheight=0.10)

        self.opcao4 = tk.Radiobutton(self.framepdf, text="Emitir Contas Por Período", variable=self.escolha,
                                     value="Op4", command=self.atualizar_tela)
        self.opcao4.place(relx=0.10, rely=0.50, relwidth=0.60, relheight=0.10)

        # Label
        self.lbl1 = Label(self.framepdf, text="Tipo Conta:", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl1.place(relx=0.05, rely=0.65)

        # Combo
        contas = self.carregarComboConta()
        contas_formatados = [f"{conta:10}" for conta in contas]
        self.cbConta = ttk.Combobox(self.framepdf, values=contas_formatados)
        self.cbConta.place(relx=0.35, rely=0.65, relwidth=0.60)

        # Obter a data atual
        data_atual = date.today()

        # Criar o DateEntry com o calendário
        self.data1 = DateEntry(self.framepdf, date_pattern='dd/mm/yyyy', width=12, background='darkblue',
                               foreground='white', borderwidth=2,
                               year=data_atual.year, month=data_atual.month, day=data_atual.day)
        self.data1.place(relx=0.05, rely=0.65)

        self.data2 = DateEntry(self.framepdf, date_pattern='dd/mm/yyyy', width=12, background='darkblue',
                               foreground='white', borderwidth=2,
                               year=data_atual.year, month=data_atual.month, day=data_atual.day)
        self.data2.place(relx=0.60, rely=0.65)

        # Label
        self.lbl2 = Label(self.framepdf, text="Até", bg='#E6E6FA', font=('verdana', 8, 'bold'))
        self.lbl2.place(relx=0.45, rely=0.65)


        #Botões
        self.emitir = Button(self.framepdf, text="Emitir PDF", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                                 command=self.selecionar_caminho)
        self.emitir.place(relx=0.15, rely=0.85, relwidth=0.30, relheight=0.10)

        self.voltar = Button(self.framepdf, text="Voltar", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                             command=self.voltarTelaPrincipal)
        self.voltar.place(relx=0.50, rely=0.85, relwidth=0.30, relheight=0.10)

    def atualizar_tela(self):
        self.opcao_selecionada = self.escolha.get()

        if self.opcao_selecionada == "Op3":
            self.lbl2.place_forget()
            self.data1.place_forget()
            self.data2.place_forget()
            self.cbConta.place(relx=0.35, rely=0.65, relwidth=0.60)
            self.lbl1.place(relx=0.05, rely=0.65)
        elif self.opcao_selecionada == "Op4":
            self.cbConta.place_forget()
            self.lbl1.place_forget()
            self.data1.place(relx=0.05, rely=0.65)
            self.lbl2.place(relx=0.45, rely=0.65)
            self.data2.place(relx=0.60, rely=0.65)
        else:
            self.lbl2.place_forget()
            self.data1.place_forget()
            self.data2.place_forget()
            self.cbConta.place_forget()
            self.lbl1.place_forget()

    def voltarTelaPrincipal(self):
        janelaPDF.iconify()
