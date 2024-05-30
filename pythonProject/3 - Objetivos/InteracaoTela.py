from Conexao import ConexaoBD
from tkinter import ttk, messagebox
from tkinter import *
from TelaPDF import TelaPDF
class Interagir:
    def carregarComboConta(self):
        self.conexao = ConexaoBD.conectar(self)
        resultado = self.conexao.execute("Select Concat(tp.tp_produto_id,' - ',tp.descricao) From objetivo_tb o "
                                         "Inner Join tp_produto_tb tp On o.tp_objetivo_id = tp.tp_produto_id")
        tipoContas = resultado.fetchall()
        self.conexao.close()
        return [conta[0] for conta in tipoContas]

    def carregarComboObjetivo(self):
        self.conexao = ConexaoBD.conectar(self)
        resultado = self.conexao.execute("Select nome From objetivo_tb")
        objetivos = resultado.fetchall()
        self.conexao.close()
        return [objetivo[0] for objetivo in objetivos]

    def carregarGrid(self, event):
        self.conexao = ConexaoBD.conectar(self)

        #Verifica se a conexão está aberta
        if not hasattr(self, 'conexao') or self.conexao is None:
            self.conexao = ConexaoBD.conectar(self)

        resultado = self.conexao.execute("Select objetivo_id, nome, vl_total, vl_atual, descricao,"
                                         "Case When ativo = 1 Then 'Ativo' Else 'Finalizado' End 'Status'"
                                         "From objetivo_tb")
        registros = resultado.fetchall()
        self.conexao.close()
        self.objetivos.delete(*self.objetivos.get_children())
        for registro in registros:
            #Obtém os valores do registro
            objetivo_id, nome, vl_total, vl_atual, descricao, Status = registro

            #Formata os valores conforme necessário
            objetivo_id_formatado = f'{objetivo_id:10}'
            objetivo_formatado = f'{nome:10}'
            vl_total_formatado = f'R$ {vl_total:.2f}'
            vl_atual_formatada = f'R$ {vl_atual:.2f}'
            descricao_formatado = f'{descricao:10}'
            status_formatado = f'{Status:10}'

            #Insere o registro formatado na Treeview
            self.objetivos.insert("", "end", values=(objetivo_id_formatado, objetivo_formatado, vl_total_formatado, vl_atual_formatada, descricao_formatado, status_formatado))

    def novoObjetivo(self):
        self.comando = "pIncluirObjetivo ?, ?, ?, ?, ?"
        self.conexao = ConexaoBD.conectar(self)


        objetivo = str(self.cbObjetivo.get())
        conta = str(self.cbConta.get())
        descricao = str(self.txtDescricao.get())
        valorTotal = self.txtValorTotal.get()
        valorInicial = self.txtValorInicial.get()

        if not objetivo:
            messagebox.showinfo("Erro", "O campo objetivo está vazio! Favor preencher.")
            return

        if not conta:
            messagebox.showinfo("Erro", "O campo tipo do objetivo está vazio! Favor preencher.")
            return

        if not descricao:
            messagebox.showinfo("Erro", "O campo descrição está vazio! Favor preencher.")
            return

        if not valorInicial:
            valorInicial = 0

        resultado = self.conexao.execute(self.comando, conta, objetivo, descricao, valorTotal, valorInicial)

        if resultado.description != None:
            message = self.conexao.fetchone()[0]
            messagebox.showerror("Erro", message)
            self.conexao.close()
            return

        self.conexao.commit()
        self.conexao.close()

        self.cbObjetivo.delete(0, END)
        self.cbConta.delete(0, END)
        self.txtDescricao.delete(0, END)
        self.txtValorTotal.delete(0, END)
        self.txtValorInicial.delete(0, END)

        #Atualizar o grid
        self.carregarGrid(event=None)

    def finalizarObjetivo(self, event):
        # Obtém a linha selecionada
        item_selecionado = self.objetivos.selection()

        # Verifica se algum item foi selecionado
        if item_selecionado:
            # Obtém os valores da linha selecionada
            valores = self.objetivos.item(item_selecionado)['values']

        objetivo_id = valores[0]

        self.conexao = ConexaoBD.conectar(self)
        self.conexao.execute("Update A Set ativo = 0 From objetivo_tb A Where objetivo_id = " + str(objetivo_id))
        self.conexao.commit()
        self.conexao.close()

        #Atualizar o grid
        self.carregarGrid(event=None)

    def telaRelatorio(self, valor):
        self.tela_pdf = TelaPDF(self)
        self.tela_pdf.janela.deiconify()

    def sair(self, valor):
        self.janela.quit()

Interagir()