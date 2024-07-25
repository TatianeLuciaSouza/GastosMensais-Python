import datetime

from Conexao import ConexaoBD
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

class Interagir:
    def carregarData(self):
        self.conexao = ConexaoBD.conectar(self)
        resultado = self.conexao.execute("Select Distinct Year(dt_inclusao) "
                                         "From decimo_terceiro_tb")
        datas = resultado.fetchall()
        self.conexao.commit()
        self.conexao.close()
        return [data[0] for data in datas]


    def carregarGrid(self, event):
        self.conexao = ConexaoBD.conectar(self)

        ano = self.cbData.get().strip()

        if not ano:
            self.despesas.delete(*self.despesas.get_children())  # Limpa os registros na Treeview
            return []

        # Verifica se a conexão está aberta
        if not hasattr(self, 'conexao') or self.conexao is None:
            self.conexao = ConexaoBD.conectar(self)

        resultado = self.conexao.execute("Select d.despesa_id, p.nome, d.descricao, d.valor"
                                         " From despesas_tb d With (Nolock)"
                                         " Inner Join produto_tb p With (Nolock) On d.produto_id = p.produto_id"
                                         " Where Year(d.dt_inclusao) = '" + ano + "'")
        registros = resultado.fetchall()
        self.conexao.commit()
        self.conexao.close()
        self.despesas.delete(*self.despesas.get_children())
        for registro in registros:
            ID, nome, Descricao, Valor = registro

            # Formata os valores conforme necessário
            ID = f'{ID:5}'
            nome_formatado = f'{nome:10}'
            desc_formatado = f'{Descricao:10}'
            valor_formatado = f'R$ {Valor:.2f}'  # Exemplo: R$ 10.50

            # Insere o registro formatado na Treeview
            self.despesas.insert("", "end", values=(ID, nome_formatado, desc_formatado, valor_formatado))

    def carregarComboDespesas(self):
        self.conexao = ConexaoBD.conectar(self)
        resultado = self.conexao.execute("Select nome From produto_tb")
        despesas = resultado.fetchall()
        self.conexao.commit()
        self.conexao.close()
        return [despesa[0] for despesa in despesas]

    def carregarComboTpDespesas(self):
        self.conexao = ConexaoBD.conectar(self)
        resultado = self.conexao.execute("Select descricao From tp_produto_tb")
        tpdespesas = resultado.fetchall()
        self.conexao.commit()
        self.conexao.close()
        return [tpdespesa[0] for tpdespesa in tpdespesas]

    def carregarComboLoja(self):
        self.conexao = ConexaoBD.conectar(self)
        resultado = self.conexao.execute("Select nome From loja_tb")
        lojas = resultado.fetchall()
        self.conexao.commit()
        self.conexao.close()
        return [loja[0] for loja in lojas]

    def carregar(self, event):
        self.conexao = ConexaoBD.conectar(self)
        ano = self.cbData.get().strip()
        resultado = self.conexao.execute("Select vl_parcela1, vl_parcela2, vl_total, vl_sobra "
                                         "From decimo_terceiro_tb "
                                         "Where Year(dt_inclusao) = " + ano)
        registros = resultado.fetchall()

        for registro in registros:
            #Obtém os valores do registro
            vl_parcela1, vl_parcela2, vl_total, vl_sobra = registro

            if not vl_parcela2:
                vl_parcela2 = 0

            #Formata os valores conforme necessário
            valor1_formatado = f'{vl_parcela1:.2f}'
            valor2_formatado = f'{vl_parcela2:.2f}'
            valor3_formatado = f'{vl_total:.2f}'
            valor4_formatado = f'{vl_sobra:.2f}'

            self.txtparcela1.config(state="normal")
            self.txtparcela2.config(state="normal")
            self.txtVlTotal.config(state="normal")
            self.txtSobra.config(state="normal")

            self.txtparcela1.delete(0, END)
            self.txtparcela2.delete(0, END)
            self.txtVlTotal.delete(0, END)
            self.txtSobra.delete(0, END)

            self.txtparcela1.insert(0, valor1_formatado)
            self.txtparcela2.insert(0, valor2_formatado)
            self.txtVlTotal.insert(0, valor3_formatado)
            self.txtSobra.insert(0, valor4_formatado)

            if vl_parcela1 > 0 and vl_parcela2 > 0:
                self.txtparcela1.config(state="disabled")
                self.txtparcela2.config(state="disabled")
                self.txtVlTotal.config(state="disabled")
                self.txtSobra.config(state="disabled")
                self.configuracoes()
            else:
                self.txtparcela1.config(state="disabled")
                self.txtVlTotal.config(state="disabled")
                self.txtSobra.config(state="disabled")
                self.configuracoes()

            self.conexao.commit()
            self.conexao.close()

            self.carregarGrid(event=None)
    def incluir(self):
        self.conexao = ConexaoBD.conectar(self)
        vl1 = self.txtparcela1.get()
        vl2 = self.txtparcela2.get()

        vl1_formatado = "{:.2f}".format(float(vl1))
        vl2_formatado = "{:.2f}".format(float(vl2))

        data = datetime.date.today()
        ano = datetime.date.today().year
        formatted_date = data.strftime('%Y%m%d')

        res = self.conexao.execute("Select Max(Year(dt_inclusao)) From decimo_terceiro_tb")
        ano2 = res.fetchall()
        max_year = ano2[0][0]

        if not vl2 and vl1 > '0':
            self.txtparcela2.config(state="normal")
            self.txtVlTotal.config(state="normal")
            self.txtSobra.config(state="normal")

            self.conexao.execute("Insert Into decimo_terceiro_tb (vl_parcela1, vl_total, vl_sobra, dt_inclusao) Select " +
                            vl1 + ", " + vl1 + ", " + vl1 + ", '" + formatted_date + "'")

            self.txtVlTotal.insert(0, vl1)
            self.txtSobra.insert(0, vl1)

            self.txtparcela1.config(state="disabled")
            self.txtVlTotal.config(state="disabled")
            self.txtSobra.config(state="disabled")

            self.conexao.commit()
            self.conexao.close()

            #Atualizar o combo data
            datas = self.carregarData()
            self.cbData['values'] = datas

        elif vl2 > '0':
            self.txtVlTotal.config(state="normal")
            self.txtSobra.config(state="normal")

            resultado = self.conexao.execute("Select Max(decimo_id) From decimo_terceiro_tb")
            id = resultado.fetchall()

            total = float(vl1_formatado) + float(vl2_formatado)
            total_formatado = "{:.2f}".format(total)

            self.comando = ("Update A Set vl_parcela2 = " + vl2_formatado + " , vl_total = " + total_formatado + ", vl_sobra = " + total_formatado +
                            ", dt_alteracao = '" + formatted_date + "' From decimo_terceiro_tb A Where decimo_id = " + str(id[0][0]))

            self.txtVlTotal.insert(0, total_formatado)
            self.txtSobra.insert(0, total_formatado)

            self.txtVlTotal.config(state="disabled")
            self.txtSobra.config(state="disabled")
            self.txtparcela2.config(state="disabled")

            self.conexao.execute(self.comando)
            self.conexao.commit()
            self.conexao.close()
        else:
            messagebox.showinfo("Erro", "Informe o valor da parcela.")
            self.conexao.close()
            return

    def incluirDespesa(self):
        self.comando = "pIncluirDespesas13 ?, ?, ?, ?, ?"
        self.conexao = ConexaoBD.conectar(self)
        cursor = self.conexao.cursor()

        despesa = self.cbDespesa.get().strip()
        tpDespesa =  self.cbTpDespesa.get().strip()
        loja = self.cbLoja.get().strip()
        valor =  self.txtValor.get()
        desc = self.txtDescricao.get().strip()

        if not despesa:
            messagebox.showinfo("Erro", "Insira qual é a despesa gasta.")
            return

        if not tpDespesa:
            messagebox.showinfo("Erro", "Insira qual o tipo da despesa gasta.")
            return

        if not loja:
            messagebox.showinfo("Erro", "Insira qual foi a loja em que a despesa foi comprada.")
            return

        if not valor:
            messagebox.showinfo("Erro", "Insira o valor da despesa gasta.")
            return

        if not desc:
            messagebox.showinfo("Erro", "Insira o porquê da despesa gasta.")
            return

        result = cursor.execute(self.comando, despesa, tpDespesa, loja, valor, desc)

        if result.description != None:
            message = cursor.fetchone()[0]
            messagebox.showerror("Erro", message)
            self.conexao.close()
            return

        self.conexao.commit()
        self.conexao.close()

        self.txtValor.delete(0, END)
        self.txtDescricao.delete(0, END)
        self.cbDespesa.delete(0, END)
        self.cbTpDespesa.delete(0, END)
        self.cbLoja.delete(0, END)

        self.carregarGrid(event=None)
        self.carregar(event=None)


    def alterar(self, event):
        region = self.despesas.identify_region(event.x, event.y)
        if region == 'cell':
            item_id = self.despesas.identify_row(event.y)
            if item_id:
                self.item_selecionado = item_id
                self.coluna_selecionada = self.despesas.identify_column(event.x)

                self.id = self.despesas.set(item_id, "#1").strip()

                if self.item_selecionado and self.coluna_selecionada:
                    self.despesas.focus(self.item_selecionado)
                    self.despesas.selection_set(self.item_selecionado)

                    #Obter o valor atual da célula
                    valor_atual = self.despesas.set(self.item_selecionado, self.coluna_selecionada)

                    #Remover o valor atual da célula
                    self.despesas.set(self.item_selecionado, self.coluna_selecionada, "")

                    #Criação do Entry para a edição
                    self.entry = ttk.Entry(self.despesas)
                    self.entry.insert(0, valor_atual)
                    self.entry.bind("<Return>", self.salvar_edicao)

                    #Posicionar o Entry na célula selecionada
                    bbox = self.despesas.bbox(self.item_selecionado, column=self.coluna_selecionada)
                    x = bbox[0] + self.despesas.winfo_x() + 2
                    y = bbox[1] + self.despesas.winfo_y() + 2
                    self.despesas.update_idletasks()
                    self.entry.place(x=x, y=y, width=bbox[2] - bbox[0], height=bbox[3] - bbox[1])
                    self.entry.focus_set()
    def salvar_edicao(self, event):
        novo_valor = self.entry.get().strip()
        self.comando = "pAlteracaoDespesas13 ?, ?, ?, ?"
        self.conexao = ConexaoBD.conectar(self)
        cursor = self.conexao.cursor()

        result = cursor.execute(self.comando, self.id, self.coluna_selecionada, novo_valor, "")

        if result.description != None:
            message = cursor.fetchone()[0]
            messagebox.showerror("Erro", message)
            self.conexao.close()
            self.carregarGrid(event=None)
            return

        self.conexao.commit()
        self.conexao.close()

        #Remover o Entry após a edição
        self.entry.destroy()

        self.carregarGrid(event=None)
        self.carregar(event=None)

    def excluir(self, event):
        global indice_selecionado
        indice_selecionado = self.despesas.identify_row(event.y)
        self.id = self.despesas.set(indice_selecionado, "#1")

        if indice_selecionado is not None:
            self.despesas.delete(indice_selecionado)
            indice_selecionado = None

        self.comando = "pAlteracaoDespesas13 ?, ?, ?, ?"
        self.conexao = ConexaoBD.conectar(self)
        cursor = self.conexao.cursor()

        result = cursor.execute(self.comando, self.id, "", "", "#5")

        if result.description != None:
            message = cursor.fetchone()[0]
            messagebox.showerror("Erro", message)
            self.conexao.close()
            self.carregarGrid(event=None)
            return

        self.conexao.commit()
        self.conexao.close()

        self.carregarGrid(event=None)
        self.carregar(event=None)

    def sair(self, valor):
        self.janela.quit()

Interagir()

