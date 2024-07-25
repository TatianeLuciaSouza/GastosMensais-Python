from tkinter import *
import tkinter as tk
from InteracaoSalario import NovoSalario


janela = Tk()

class Salario(NovoSalario):
    def __init__(self, root):
        self.root = root
        self.janela = janela
        self.tela(),
        self.salarioMes(),
        janela.mainloop()

    def tela(self):
        self.janela.title("Novo Salário Deste Mês")
        self.janela.geometry("300x200")
        self.janela.resizable(False, False)

    def salarioMes(self):
        self.lblSalario = Label(janela, text='Salário deste mês:', font=('verdana', 8, 'bold'))
        self.lblSalario.place(relx=0.30, rely=0.02, relwidth=0.40, relheight=0.10)
        self.lblExtra = Label(janela, text='Algum Extra?', font=('verdana', 8, 'bold'))
        self.lblExtra.place(relx=0.35, rely=0.30, relwidth=0.28, relheight=0.10)
        self.lblValor = Label(janela, text='Valor:', font=('verdana', 8, 'bold'))
        self.lblDesc = Label(janela, text='Descrição:', font=('verdana', 8, 'bold'))

        self.txtSalario = Entry(janela)
        self.txtSalario.place(relx=0.37, rely=0.11, relwidth=0.25)
        self.txtValor = Entry(janela)
        self.txtDesc = Entry(janela)

        self.checkbox_value = tk.BooleanVar()
        self.checkSim = tk.Checkbutton(janela, text="Sim", variable=self.checkbox_value)
        self.checkSim.grid(row=10, column=10, padx=200, pady=57, sticky=tk.E)
        self.checkSim.bind("<Button-1>", self.extra)

        self.btnIncluir = Button(janela, text="Incluir", bd=2, font=('verdana', 8, 'bold'), command=self.salario)
        self.btnIncluir.place(relx=0.40, rely=0.50, relwidth=0.18, relheight=0.10)

    def extra(self, event):
        if self.checkbox_value.get() == 0:
            self.lblValor.place(relx=0.20, rely=0.45, relwidth=0.25, relheight=0.10)
            self.lblDesc.place(relx=0.20, rely=0.60, relwidth=0.25, relheight=0.10)

            self.txtValor.place(relx=0.40, rely=0.45, relwidth=0.25)
            self.txtDesc.place(relx=0.45, rely=0.60, relwidth=0.50)
            self.btnIncluir.place(relx=0.40, rely=0.84, relwidth=0.18, relheight=0.10)
        else:
            self.lblValor.place_forget()
            self.lblDesc.place_forget()
            self.txtValor.place_forget()
            self.txtDesc.place_forget()

            self.btnIncluir.place(relx=0.40, rely=0.50, relwidth=0.18, relheight=0.10)


app = Salario(janela)