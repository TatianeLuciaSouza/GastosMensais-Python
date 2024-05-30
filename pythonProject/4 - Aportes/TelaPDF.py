from datetime import date
from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkcalendar import DateEntry
from EmitirPDF import EmitirPDF

#janelaPDF = Tk()
#janelaPDF.destroy()

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

    def opcoes(self, event):
        if self.escolha.get() == "Op1":
            tipo = "F"

            if self.cbOpcoes.get() == "4 - Rendimentos":
                self.cbFundos.place_forget()
                self.lbl1.place_forget()

                self.lbl2.place(relx=0.45, rely=0.40)
                self.data1.place(relx=0.05, rely=0.40)
                self.data2.place(relx=0.60, rely=0.40)

            elif self.cbOpcoes.get() == "5 - Rendimentos por Fundo":

                self.lbl1.place(relx=0.05, rely=0.60)
                self.lbl2.place(relx=0.45, rely=0.40)

                self.data1.place(relx=0.05, rely=0.40)
                self.data2.place(relx=0.60, rely=0.40)
                self.cbFundos.place(relx=0.35, rely=0.60, relwidth=0.60)

                fundos = self.carregarComboFundo(tipo)
                fundos_formatados = [f"{fundo:10}" for fundo in fundos]
                self.cbFundos['values'] = fundos_formatados

            elif self.cbOpcoes.get() == "6 - Aportes por Período":
                self.cbFundos.place_forget()
                self.lbl1.place_forget()

                self.lbl2.place(relx=0.45, rely=0.40)
                self.data1.place(relx=0.05, rely=0.40)
                self.data2.place(relx=0.60, rely=0.40)

            elif self.cbOpcoes.get() == "7 - Aportes por Fundo":
                self.data1.place_forget()
                self.data2.place_forget()
                self.lbl2.place_forget()

                self.lbl1.place(relx=0.05, rely=0.40)
                self.cbFundos.place(relx=0.35, rely=0.40, relwidth=0.60)

                fundos = self.carregarComboFundo(tipo)
                fundos_formatados = [f"{fundo:10}" for fundo in fundos]
                self.cbFundos['values'] = fundos_formatados

            elif self.cbOpcoes.get() == "8 - Aportes por Fundo e Período":

                self.lbl1.place(relx=0.05, rely=0.60)
                self.lbl2.place(relx=0.45, rely=0.40)

                self.data1.place(relx=0.05, rely=0.40)
                self.data2.place(relx=0.60, rely=0.40)
                self.cbFundos.place(relx=0.35, rely=0.60, relwidth=0.60)

                fundos = self.carregarComboFundo(tipo)
                fundos_formatados = [f"{fundo:10}" for fundo in fundos]
                self.cbFundos['values'] = fundos_formatados

            else:
                self.cbFundos.place_forget()
                self.lbl1.place_forget()
                self.data1.place_forget()
                self.data2.place_forget()
                self.lbl2.place_forget()

        elif self.escolha.get() == "Op2":
            tipo = "A"

            if self.cbOpcoes.get() == "4 - Rendimentos":
                self.cbFundos.place_forget()
                self.lbl1.place_forget()

                self.lbl2.place(relx=0.45, rely=0.40)
                self.data1.place(relx=0.05, rely=0.40)
                self.data2.place(relx=0.60, rely=0.40)

            elif self.cbOpcoes.get() == "5 - Rendimentos por Ação":

                self.lbl1.place(relx=0.05, rely=0.60)
                self.lbl2.place(relx=0.45, rely=0.40)

                self.data1.place(relx=0.05, rely=0.40)
                self.data2.place(relx=0.60, rely=0.40)
                self.cbFundos.place(relx=0.35, rely=0.60, relwidth=0.60)

                fundos = self.carregarComboFundo(tipo)
                fundos_formatados = [f"{fundo:10}" for fundo in fundos]
                self.cbFundos['values'] = fundos_formatados

            elif self.cbOpcoes.get() == "6 - Aportes por Período":
                self.cbFundos.place_forget()
                self.lbl1.place_forget()

                self.lbl2.place(relx=0.45, rely=0.40)
                self.data1.place(relx=0.05, rely=0.40)
                self.data2.place(relx=0.60, rely=0.40)

            elif self.cbOpcoes.get() == "7 - Aportes por Ação":
                self.data1.place_forget()
                self.data2.place_forget()
                self.lbl2.place_forget()

                self.lbl1.place(relx=0.05, rely=0.40)
                self.cbFundos.place(relx=0.35, rely=0.40, relwidth=0.60)

                fundos = self.carregarComboFundo(tipo)
                fundos_formatados = [f"{fundo:10}" for fundo in fundos]
                self.cbFundos['values'] = fundos_formatados

            elif self.cbOpcoes.get() == "8 - Aportes por Ação e Período":

                self.lbl1.place(relx=0.05, rely=0.60)
                self.lbl2.place(relx=0.45, rely=0.40)

                self.data1.place(relx=0.05, rely=0.40)
                self.data2.place(relx=0.60, rely=0.40)
                self.cbFundos.place(relx=0.35, rely=0.60, relwidth=0.60)

                fundos = self.carregarComboFundo(tipo)
                fundos_formatados = [f"{fundo:10}" for fundo in fundos]
                self.cbFundos['values'] = fundos_formatados

            else:
                self.cbFundos.place_forget()
                self.lbl1.place_forget()
                self.data1.place_forget()
                self.data2.place_forget()
                self.lbl2.place_forget()

        elif self.escolha.get() == "Op3":

            if self.cbOpcoes.get() == "4 - Aportes de ambos por Período":
                self.cbFundos.place_forget()
                self.lbl1.place_forget()

                self.lbl2.place(relx=0.45, rely=0.40)
                self.data1.place(relx=0.05, rely=0.40)
                self.data2.place(relx=0.60, rely=0.40)

            elif self.cbOpcoes.get() == "5 - Rendimentos":
                self.cbFundos.place_forget()
                self.lbl1.place_forget()

                self.lbl2.place(relx=0.45, rely=0.40)
                self.data1.place(relx=0.05, rely=0.40)
                self.data2.place(relx=0.60, rely=0.40)
            else:
                self.cbFundos.place_forget()
                self.lbl1.place_forget()
                self.data1.place_forget()
                self.data2.place_forget()
                self.lbl2.place_forget()
        else:
            self.cbFundos.place_forget()
            self.lbl1.place_forget()
            self.data1.place_forget()
            self.data2.place_forget()
            self.lbl2.place_forget()
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
        self.opcao1 = tk.Radiobutton(self.framepdf, text="FIIS", variable=self.escolha,
                                     value="Op1",command=self.atualizar_tela)
        self.opcao1.place(relx=0.10, rely=0.05, relwidth=0.20, relheight=0.10)

        self.opcao2 = tk.Radiobutton(self.framepdf, text="Ações", variable=self.escolha,
                                     value="Op2",command=self.atualizar_tela)
        self.opcao2.place(relx=0.35, rely=0.05, relwidth=0.25, relheight=0.10)

        self.opcao3 = tk.Radiobutton(self.framepdf, text="Ambos", variable=self.escolha,
                                     value="Op3", command=self.atualizar_tela)
        self.opcao3.place(relx=0.65, rely=0.05, relwidth=0.25, relheight=0.10)

        #Botões
        self.emitir = Button(self.framepdf, text="Emitir PDF", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'),
                                 command=self.selecionar_caminho)
        self.emitir.place(relx=0.15, rely=0.85, relwidth=0.30, relheight=0.10)

        self.voltar = Button(self.framepdf, text="Voltar", bd=2, bg='#E6E6FA', font=('verdana', 8, 'bold'), command = self.janela.destroy)
        self.voltar.place(relx=0.50, rely=0.85, relwidth=0.30, relheight=0.10)

        # Obter a data atual
        data_atual = date.today()

        # Criar o DateEntry com o calendário
        self.data1 = DateEntry(self.framepdf, date_pattern='dd/mm/yyyy', width=12, background='darkblue',
                               foreground='white', borderwidth=2,
                               year=data_atual.year, month=data_atual.month, day=data_atual.day)


        self.data2 = DateEntry(self.framepdf, date_pattern='dd/mm/yyyy', width=12, background='darkblue',
                               foreground='white', borderwidth=2,
                               year=data_atual.year, month=data_atual.month, day=data_atual.day)

        self.lbl2 = Label(self.framepdf, text="Até", bg='#E6E6FA', font=('verdana', 8, 'bold'))

        self.cbFundos = ttk.Combobox(self.framepdf)

        self.lbl1 = Label(self.framepdf, text="Fundos:", bg='#E6E6FA', font=('verdana', 8, 'bold'))

        self.lbl0 = Label(self.framepdf, text="Opções:", bg='#E6E6FA', font=('verdana', 8, 'bold'))

        self.cbOpcoes = ttk.Combobox(self.framepdf)

    def atualizar_tela(self):
        self.opcao_selecionada = self.escolha.get()

        if self.opcao_selecionada == "Op1":
            self.cbFundos.place_forget()
            self.lbl1.place_forget()
            self.data1.place_forget()
            self.data2.place_forget()
            self.lbl2.place_forget()

            self.lbl0.place(relx=0.10, rely=0.20)

            self.cbOpcoes['values'] = ""
            self.cbOpcoes['values'] = ["1 - Todos os Fundos", "2 - Fundos Vendidos",
                                       "3 - Todos os Aportes", "4 - Rendimentos",
                                       "5 - Rendimentos por Fundo", "6 - Aportes por Período",
                                       "7 - Aportes por Fundo", "8 - Aportes por Fundo e Período"]
            self.cbOpcoes.place(relx=0.35, rely=0.20, relwidth=0.60)
            self.cbOpcoes.bind("<<ComboboxSelected>>", self.opcoes)

        elif self.opcao_selecionada == "Op2":
            self.cbFundos.place_forget()
            self.lbl1.place_forget()
            self.data1.place_forget()
            self.data2.place_forget()
            self.lbl2.place_forget()

            self.lbl0.place(relx=0.10, rely=0.20)

            self.cbOpcoes['values'] = ""
            self.cbOpcoes['values'] = ["1 - Todos as Ações", "2 - Ações Vendidas",
                                       "3 - Todos os Aportes", "4 - Rendimentos",
                                       "5 - Rendimentos por Ação", "6 - Aportes por Período",
                                       "7 - Aportes por Ação", "8 - Aportes por Ação e Período"]
            self.cbOpcoes.place(relx=0.35, rely=0.20, relwidth=0.60)
            self.cbOpcoes.bind("<<ComboboxSelected>>", self.opcoes)

        elif self.opcao_selecionada == "Op3":
            self.cbFundos.place_forget()
            self.lbl1.place_forget()
            self.data1.place_forget()
            self.data2.place_forget()
            self.lbl2.place_forget()

            self.lbl0.place(relx=0.10, rely=0.20)

            self.cbOpcoes['values'] = ""
            self.cbOpcoes['values'] = ["1 - Todos os Fundos e Ações", "2 - Fundos e Ações Vendidos",
                                       "3 - Todos os Aportes de Ambos", "4 - Aportes de ambos por Período",
                                       "5 - Rendimentos"]
            self.cbOpcoes.place(relx=0.35, rely=0.20, relwidth=0.60)
            self.cbOpcoes.bind("<<ComboboxSelected>>", self.opcoes)

    def voltarTelaPrincipal(self):
        janelaPDF.iconify()
