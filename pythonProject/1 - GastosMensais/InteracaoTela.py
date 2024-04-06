import datetime
from SQLServer import ConexaoBD
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from TelaPDF import TelaPDF
class Interagir:
    def carregarData(self):
        self.conexao = ConexaoBD.conectar(self)
        resultado = self.conexao.execute("Select Distinct Concat(Year(dt_inclusao), "
                                         "Case When Len(Month(dt_inclusao)) = 1 Then '-0' End, "
                                         "Month(dt_inclusao)) "
                                         "From gastos_tb")
        datas = resultado.fetchall()
        self.conexao.close()
        return [data[0] for data in datas]


    def carregarGrid(self, event):
        self.conexao = ConexaoBD.conectar(self)
        data_str = self.cbData.get()
        if not data_str:
            self.compras.delete(*self.compras.get_children())  # Limpa os registros na Treeview
            return []

        # Verifica se a conexão está aberta
        if not hasattr(self, 'conexao') or self.conexao is None:
            self.conexao = ConexaoBD.conectar(self)

        resultado = self.conexao.execute("Select g.gasto_id, p.nome, g.qtd, g.valor, l.nome 'nomeLoja', g.dt_inclusao "
                                         "From gastos_tb g Inner Join produto_tb p On g.produto_id = p.produto_id "
                                         "Inner Join loja_tb l On g.loja_id = l.loja_id "
                                         "Where Concat(Year(g.dt_inclusao), "
                                         "Case When Len(Month(g.dt_inclusao)) = 1 Then '-0' End, "
                                         "Month(g.dt_inclusao)) = '" + data_str + "'")
        registros = resultado.fetchall()
        self.compras.delete(*self.compras.get_children())  # Limpa os registros na Treeview
        for registro in registros:
            # Obtém os valores do registro
            gastoID, nome, qtd, valor, nomeLoja, dt_inclusao = registro

            # Formata os valores conforme necessário
            gasto_ID = f'{gastoID:5}'
            produto_formatado = f'{nome:10}'
            qtd_formatado = f'{qtd:10}'
            valor_formatado = f'R$ {valor:.2f}'  # Exemplo: R$ 10.50
            loja_formatada = f'{nomeLoja:10}'
            data_formatada = dt_inclusao.strftime('%d/%m/%Y')  # Exemplo: 31/12/2023

            # Insere o registro formatado na Treeview
            self.compras.insert("", "end", values=(gasto_ID,produto_formatado, qtd_formatado, valor_formatado, loja_formatada,
                                                   data_formatada))


    def carregarComboProduto(self):
        self.conexao = ConexaoBD.conectar(self)
        resultado = self.conexao.execute("Select nome From produto_tb")
        produtos = resultado.fetchall()
        self.conexao.close()
        return [produto[0] for produto in produtos]

    def carregarComboTpProduto(self):
        self.conexao = ConexaoBD.conectar(self)
        resultado = self.conexao.execute("Select descricao From tp_produto_tb")
        tpprodutos = resultado.fetchall()
        self.conexao.close()
        return [produto[0] for produto in tpprodutos]


    def carregarComboLoja(self):
        self.conexao = ConexaoBD.conectar(self)
        resultado = self.conexao.execute("Select nome From loja_tb")
        lojas = resultado.fetchall()
        self.conexao.close()
        return [loja[0] for loja in lojas]


    def incluir(self):
        self.comando = "pGastosMensais ?, ?, ?, ?, ?"
        self.conexao = ConexaoBD.conectar(self.comando)

        produto = self.cbProduto.get()
        loja = self.cbLoja.get()
        valor = self.txtValor.get()
        qtd = self.txtQtd.get()
        tipo = self.cbTpProduto.get()

        self.conexao.execute(self.comando, str(produto), valor, int(qtd), str(loja), str(tipo))
        self.conexao.commit()
        self.conexao.close()

        self.cbProduto.delete(0, END)
        self.cbLoja.delete(0, END)
        self.txtQtd.delete(0, END)
        self.txtValor.delete(0, END)
        self.cbTpProduto.delete(0, END)

        # Atualizar o grid
        self.carregarGrid(event=None)

        # Atualizar o combo data
        datas = self.carregarData()
        self.cbData['values'] = datas


    def alterar(self, event):
        region = self.compras.identify_region(event.x, event.y)
        if region == 'cell':
            item_id = self.compras.identify_row(event.y)
            if item_id:
                self.item_selecionado = item_id
                self.coluna_selecionada = self.compras.identify_column(event.x)
                self.id = self.compras.set(item_id, "#1")

                # Verifica se a coluna selecionada é editável
                if self.coluna_selecionada == "#2" or self.coluna_selecionada == "#5":
                    messagebox.showwarning("Coluna Não Editável","Você clicou em uma coluna que não pode ser alterada.")
                else:
                    if self.item_selecionado and self.coluna_selecionada:
                        self.compras.focus(self.item_selecionado)
                        self.compras.selection_set(self.item_selecionado)

                        #Obter o valor atual da célula
                        valor_atual = self.compras.set(self.item_selecionado, self.coluna_selecionada)

                        #Remover o valor atual da célula
                        self.compras.set(self.item_selecionado, self.coluna_selecionada, "")

                        #Criação do Entry para a edição
                        self.entry = ttk.Entry(self.compras)
                        self.entry.insert(0, valor_atual)
                        self.dt_alteracao = datetime.date.today()
                        self.entry.bind("<Return>", self.salvar_edicao)

                        #Posicionar o Entry na célula selecionada
                        bbox = self.compras.bbox(self.item_selecionado, column=self.coluna_selecionada)
                        x = bbox[0] + self.compras.winfo_x() + 2
                        y = bbox[1] + self.compras.winfo_y() + 2
                        self.compras.update_idletasks()
                        self.entry.place(x=x, y=y, width=bbox[2] - bbox[0], height=bbox[3] - bbox[1])
                        self.entry.focus_set()
    def salvar_edicao(self, event):
        novo_valor = self.entry.get()
        self.conexao = ConexaoBD.conectar(self)
        self.data = datetime.date.today().strftime('%d/%m/%y')

        if self.coluna_selecionada == "#3":
            self.comando = ("Update A Set qtd = " + novo_valor + ", dt_alteracao = '" +
                            self.data + "' From gastos_tb A Where gasto_id = " + self.id)
            self.conexao.execute(self.comando)
            self.conexao.commit()
            self.conexao.close()

        if self.coluna_selecionada == "#4":
            self.comando = ("Update A Set valor = " + novo_valor + ", dt_alteracao = '" +
                            self.data + "' From gastos_tb A Where gasto_id = " + self.id)
            self.conexao.execute(self.comando)
            self.conexao.commit()
            self.conexao.close()

        # Atualizar o valor na célula selecionada
        self.compras.set(self.item_selecionado, self.coluna_selecionada, novo_valor)

        # Remover o Entry após a edição
        self.entry.destroy()

    def excluir(self, event):
        global indice_selecionado
        indice_selecionado = self.compras.identify_row(event.y)
        self.id = self.compras.set(indice_selecionado, "#1")

        if indice_selecionado is not None:
            self.compras.delete(indice_selecionado)
            indice_selecionado = None

        self.conexao = ConexaoBD.conectar(self)
        self.comando = ("Delete From gastos_tb Where gasto_id = " + self.id)
        self.conexao.execute(self.comando)
        self.conexao.commit()
        self.conexao.close()

    def telaRelatorio(self, valor):
        self.tela_pdf = TelaPDF(self)
        self.tela_pdf.janela.deiconify()

    def sair(self, valor):
        self.janela.quit()

Interagir()

