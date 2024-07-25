import datetime

import pyodbc

from Conexao import ConexaoBD
from tkinter import *
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class Interagir:
    def carregarData(self):
        conexao = ConexaoBD.conectar(self)
        login_id = self.usuario()
        comando = ("Select Distinct Concat(Year(dt_inclusao), "
                   "Case When Len(Month(dt_inclusao)) = 1 Then '0' End, "
                   "Month(dt_inclusao)) From gastos_tb Where login_id = ?")
        resultado = conexao.execute(comando, login_id)
        datas = resultado.fetchall()
        conexao.close()
        return [data[0] for data in datas]
    def carregarData13(self):
        conexao = ConexaoBD.conectar(self)
        login_id = self.usuario()
        comando = ("Select Distinct Year(dt_inclusao) From decimo_terceiro_tb Where login_id = ?")
        resultado = conexao.execute(comando, login_id)
        datas = resultado.fetchall()
        conexao.commit()
        conexao.close()
        return [data[0] for data in datas]
    def carregarComboProduto(self):
        conexao = ConexaoBD.conectar(self)
        resultado = conexao.execute("Select Concat(produto_id,' - ',nome) From produto_tb")
        produtos = resultado.fetchall()
        conexao.close()
        return [produto[0] for produto in produtos]

    def carregarComboProdutoConta(self, indice_conta):
        conexao = ConexaoBD.conectar(self)
        resultado = conexao.execute("Select Concat(produto_id,' - ',nome) From produto_tb Where tp_produto_id = ?",
                                         (indice_conta))
        produtos = resultado.fetchall()
        conexao.close()
        return [produto[0] for produto in produtos]

    def carregarComboTpProduto(self):
        conexao = ConexaoBD.conectar(self)
        resultado = conexao.execute("Select Concat(tp_produto_id,' - ',descricao) From tp_produto_tb")
        tpprodutos = resultado.fetchall()
        conexao.close()
        return [produto[0] for produto in tpprodutos]

    def carregarComboLoja(self):
        conexao = ConexaoBD.conectar(self)
        resultado = conexao.execute("Select Concat(loja_id,' - ',nome) From loja_tb")
        lojas = resultado.fetchall()
        conexao.close()
        return [loja[0] for loja in lojas]

    def carregarComboMeta(self):
        conexao = ConexaoBD.conectar(self)
        resultado = conexao.execute("Select Concat(meta_id,' - ',nome) From meta_tb")
        metas = resultado.fetchall()
        conexao.close()
        return [meta[0] for meta in metas]

    def carregarComboContaMeta(self):
        conexao = ConexaoBD.conectar(self)
        resultado = conexao.execute("Select Concat(tp.tp_produto_id,' - ',tp.descricao) From meta_tb o "
                                         "Inner Join tp_produto_tb tp On o.tp_meta_id = tp.tp_produto_id")
        tipoContas = resultado.fetchall()
        conexao.close()
        return [conta[0] for conta in tipoContas]

    def carregarComboTicker(self):
        login_id = self.usuario()
        conexao = ConexaoBD.conectar(self)
        comando = ("Select ticker From fundos_tb Where login_id = ?")
        resultado = conexao.execute(comando, login_id)
        tickers = resultado.fetchall()
        conexao.close()
        return [ticker[0] for ticker in tickers]

    def carregarComboTicker2(self, tipo):
        if tipo == 1:
            categoria = 'F'
        elif tipo == 2:
            categoria = 'A'
        elif tipo == 3:
            conexao = ConexaoBD.conectar(self)
            resultado = conexao.execute("Select Concat(fundo_id,' - ',ticker) From fundos_tb Where categoria In('F','A')")
            tickers = resultado.fetchall()
            conexao.close()
            return [ticker[0] for ticker in tickers]

        conexao = ConexaoBD.conectar(self)
        resultado = conexao.execute( "Select Concat(fundo_id,' - ',ticker) From fundos_tb Where categoria = '" + categoria + "'")
        tickers = resultado.fetchall()
        conexao.close()
        return [ticker[0] for ticker in tickers]

    def incluirGastos(self):
        comando = "pGastosMensais ?, ?, ?, ?, ?"
        conexao = ConexaoBD.conectar(comando)

        produto = self.cbProdutoGasto.get().strip()
        loja = self.cbLojaGasto.get().strip()
        valor = self.txtValorGasto.get()
        qtd = self.txtQtdGasto.get()
        tipo = self.cbTpProdutoGasto.get()

        if not produto:
            messagebox.showinfo("Erro", "O campo do produto está vazio! Favor preencher.")
            return

        if not tipo:
            messagebox.showinfo("Erro", "O campo tipo do produto está vazio! Favor preencher.")
            return

        if not loja:
            messagebox.showinfo("Erro", "O campo da loja está vazio! Favor preencher.")
            return

        if not qtd:
            messagebox.showinfo("Erro", "O campo quantidade está vazio! Favor preencher.")
            return

        if not valor:
            messagebox.showinfo("Erro", "O campo valor está vazio! Favor preencher.")
            return

        try:
            conexao.execute(comando, str(produto), valor, int(qtd), str(loja), str(tipo))
            conexao.commit()

            self.cbProdutoGasto.delete(0, END)
            self.cbLojaGasto.delete(0, END)
            self.txtQtdGasto.delete(0, END)
            self.txtValorGasto.delete(0, END)
            self.cbTpProdutoGasto.delete(0, END)

            self.carregarGridGastos(event=None)

            # Atualizar o combo data
            datas = self.carregarData()
            self.cbDataGasto['values'] = datas

            self.atualizarCombos(1)
            self.carregarMenu()

        except pyodbc.Error as e:
            conexao.rollback()
            messagebox.showerror("Erro", str(e))
            return
        finally:
            conexao.close()

    def carregarGridGastos(self, event):
        conexao = ConexaoBD.conectar(self)
        data_str = self.cbDataGasto.get().strip()

        login_id = self.usuario()

        if not data_str:
            self.gastos.delete(*self.gastos.get_children())  # Limpa os registros na Treeview
            return []

        # Verifica se a conexão está aberta
        if not hasattr(self, 'conexao') or conexao is None:
            conexao = ConexaoBD.conectar(self)

        comando = ("Select g.gasto_id, p.nome, g.qtd, g.valor, l.nome 'nomeLoja', g.dt_inclusao "
                   "From gastos_tb g Inner Join produto_tb p On g.produto_id = p.produto_id "
                   "Inner Join loja_tb l On g.loja_id = l.loja_id "
                   "Where g.login_id = ? And Concat(Year(g.dt_inclusao), "
                   "Case When Len(Month(g.dt_inclusao)) = 1 Then '0' End, "
                   "Month(g.dt_inclusao)) = ?")
        resultado = conexao.execute(comando, login_id, data_str)
        registros = resultado.fetchall()
        self.gastos.delete(*self.gastos.get_children())
        for registro in registros:
            gastoID, nome, qtd, valor, nomeLoja, dt_inclusao = registro

            gasto_ID = f'{gastoID:5}'
            produto_formatado = f'{nome:10}'
            qtd_formatado = f'{qtd:10}'
            valor_formatado = f'R$ {valor:.2f}'
            loja_formatada = f'{nomeLoja:10}'
            data_formatada = dt_inclusao.strftime('%d/%m/%Y')

            self.gastos.insert("", "end", values=(gasto_ID,produto_formatado, qtd_formatado, valor_formatado, loja_formatada,
                                                   data_formatada))

    def carregarGridConta(self, event):
        conexao = ConexaoBD.conectar(self)

        # Verifica se a conexão está aberta
        if not hasattr(self, 'conexao') or conexao is None:
            conexao = ConexaoBD.conectar(self)

        mes = str(datetime.date.today().month)
        ano = str(datetime.date.today().year)
        login_id = self.usuario()

        comando = ("Select prod.nome, c.valor, p.parcela From contas_tb c "
                   "Inner Join produto_tb prod On c.produto_id = prod.produto_id "
                   "Inner Join parcelas_tb p On p.conta_id = c.conta_id "
                   "Where Month(p.dt_parcela) = ? And Year(p.dt_parcela) = ? And c.login_id = ?")
        resultado = conexao.execute(comando, mes, ano, login_id)
        registros = resultado.fetchall()
        self.contas.delete(*self.contas.get_children())
        for registro in registros:
            nome, valor, parcela = registro

            produto_formatado = f'{nome:10}'
            valor_formatado = f'R$ {valor:.2f}'
            parcela_formatada = f'{parcela:10}'

            self.contas.insert("", "end", values=(produto_formatado, valor_formatado, parcela_formatada))

    def carregarGridMetas(self, event):
        conexao = ConexaoBD.conectar(self)

        #Verifica se a conexão está aberta
        if not hasattr(self, 'conexao') or conexao is None:
            conexao = ConexaoBD.conectar(self)

        login_id = self.usuario()
        comando = ("Select meta_id, nome, vl_total, vl_atual, descricao,"
                   "Case When ativo = 1 Then 'Ativo' Else 'Finalizado' End 'Status'"
                   "From meta_tb Where login_id = ?")
        resultado = conexao.execute(comando, login_id)
        registros = resultado.fetchall()
        conexao.close()
        self.metas.delete(*self.metas.get_children())
        for registro in registros:
            objetivo_id, nome, vl_total, vl_atual, descricao, Status = registro

            objetivo_id_formatado = f'{objetivo_id:10}'
            objetivo_formatado = f'{nome:10}'
            vl_total_formatado = f'R$ {vl_total:.2f}'
            vl_atual_formatada = f'R$ {vl_atual:.2f}'
            descricao_formatado = f'{descricao:10}'
            status_formatado = f'{Status:10}'

            self.metas.insert("", "end", values=(objetivo_id_formatado, objetivo_formatado, vl_total_formatado, vl_atual_formatada, descricao_formatado, status_formatado))

    def carregarGridFundo(self, opcao):

        if opcao == "A":
            tipo = 'A'
        elif opcao == "F":
            tipo = 'F'

        conexao = ConexaoBD.conectar(self)

        login_id = self.usuario()
        comando = ("Select f.nm_empresa 'Nome da Empresa', f.tipo_fundo 'Tipo do Fundo', f.ticker 'Ticker',"
                   "Case When f.categoria = 'F' Then fiis.nro_cota Else a.nro_cota End 'Total de Cotas',"
                   "Case When f.categoria = 'F' Then fiis.vl_investido Else a.vl_investido End 'Total Investido',"
                   "Isnull(p.qtd_cota, 0) 'Contas adquiridas',Isnull(p.vl_cota, 0) 'Valor da última cota', "
                   "Isnull(p.vl_total, 0) 'Investido no Mês', Isnull(p.mesAno, '') 'Mes/Ano'"
                   "From fundos_tb f Left Join fiis_tb fiis On f.fundo_id = fiis.fundo_id "
                   "Left Join acoes_tb a On f.fundo_id = a.fundo_id Left Join aportes_tb p On f.fundo_id = p.fundo_id "
                   "Where f.categoria = ? And f.login_id = ?")
        resultado = conexao.execute(comando, tipo, login_id)
        registros = resultado.fetchall()
        conexao.close()
        self.fundos.delete(*self.fundos.get_children())
        for registro in registros:
            nm_empresa, tp_fundo, ticker, tl_cotas, tl_investido, qtd_cota, vl_cota, vl_total, mesAno = registro

            nm_empresa_formatado = f'{nm_empresa:10}'
            tp_fundo_formatado = f'{tp_fundo:10}'
            ticker_formatado = f'{ticker:10}'
            tl_cotas_formatada = f'{tl_cotas:10}'
            tl_investido_formatado = f'R$ {tl_investido:.2f}'
            qtd_cota_formatado = f'{qtd_cota:10}'
            vl_cota_formatado = f'R$ {vl_cota:.2f}'
            vl_total_formatado = f'R$ {vl_total:.2f}'
            mesAno_formatado = f'{mesAno:10}'

            self.fundos.insert("", "end", values=(nm_empresa_formatado, tp_fundo_formatado, ticker_formatado,
                                                  tl_cotas_formatada, tl_investido_formatado, qtd_cota_formatado,
                                                  vl_cota_formatado, vl_total_formatado, mesAno_formatado))

    def carregarGrid13(self, event):
        conexao = ConexaoBD.conectar(self)

        ano = self.cbData13.get().strip()

        if not ano:
            self.despesas.delete(*self.despesas.get_children())  # Limpa os registros na Treeview
            return []

        # Verifica se a conexão está aberta
        if not hasattr(self, 'conexao') or conexao is None:
            conexao = ConexaoBD.conectar(self)

        login_id = self.usuario()

        comando = ("Select d.despesa_id, p.nome, d.descricao, d.valor "
                   "From despesas_tb d With (Nolock) "
                   "Inner Join produto_tb p With (Nolock) On d.produto_id = p.produto_id "
                   "Inner Join decimo_terceiro_tb d13 With (Nolock) On d.decimo_id = d13.decimo_id "
                   "Where Year(d.dt_inclusao) = ? And d13.login_id = ?")
        resultado = conexao.execute(comando, ano, login_id)
        registros = resultado.fetchall()
        conexao.commit()
        conexao.close()
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

    def carregar(self, event):
        conexao = ConexaoBD.conectar(self)
        ano = self.cbData13.get().strip()
        login_id = self.usuario()

        comando = ("Select vl_parcela1, vl_parcela2, vl_total, vl_sobra "
                   "From decimo_terceiro_tb "
                   "Where Year(dt_inclusao) = ? And login_id = ?")
        resultado = conexao.execute(comando, ano, login_id)
        registros = resultado.fetchall()

        for registro in registros:
            #Obtém os valores do registro
            vl_parcela1, vl_parcela2, vl_total, vl_sobra = registro

            if not vl_parcela2:
                vl_parcela2 = 0

            #Formata os valores conforme necessário
            valor1_formatado = f'R${vl_parcela1:.2f}'
            valor2_formatado = f'R${vl_parcela2:.2f}'
            valor3_formatado = f'R${vl_total:.2f}'
            valor4_formatado = f'R${vl_sobra:.2f}'

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
                self.config13()
            else:
                self.txtparcela1.config(state="disabled")
                self.txtVlTotal.config(state="disabled")
                self.txtSobra.config(state="disabled")
                self.config13()

            conexao.commit()
            conexao.close()

            self.carregarGrid13(event=None)
    def novaConta(self):
        comando = "pIncluirConta ?, ?, ?, ?"
        conexao = ConexaoBD.conectar(self)

        conta = self.cbConta.get().strip()
        produto =  self.cbProdutoConta.get().strip()
        valor = self.txtValorConta.get()
        parcela = self.cbParcelaConta.get()

        if not produto:
            messagebox.showinfo("Erro", "O campo produto está vazio! Favor preencher.")
            return

        if not conta:
            messagebox.showinfo("Erro", "O campo tipo do produto está vazio! Favor preencher.")
            return

        if not parcela:
            messagebox.showinfo("Erro", "O campo parcela está vazio! Favor preencher.")
            return

        if not valor:
            messagebox.showinfo("Erro", "O campo valor está vazio! Favor preencher.")
            return

        try:
            conexao.execute(comando, conta, produto, valor, int(parcela))
            conexao.commit()
            self.cbProdutoConta.delete(0, END)
            self.cbConta.delete(0, END)
            self.cbParcelaConta.delete(0, END)
            self.txtValorConta.delete(0, END)

            self.carregarGridConta(event=None)
            self.atualizarCombos(2)
        except pyodbc.Error as e:
            conexao.rollback()
            messagebox.showerror("Erro", str(e))
            return
        finally:
            conexao.close()
    def novaMeta(self):
        comando = "pIncluirMetas ?, ?, ?, ?, ?"
        conexao = ConexaoBD.conectar(self)

        meta = str(self.cbMetas.get().strip())
        conta = str(self.cbTipoMeta.get().strip())
        descricao = str(self.txtDescricaoMeta.get().strip())
        valorTotal = self.txtValorTotalMeta.get()
        valorInicial = self.txtValorInicialMeta.get()

        if not meta:
            messagebox.showinfo("Erro", "O campo Meta está vazio! Favor preencher.")
            return

        if not conta:
            messagebox.showinfo("Erro", "O campo tipo do Meta está vazio! Favor preencher.")
            return

        if not descricao:
            messagebox.showinfo("Erro", "O campo descrição está vazio! Favor preencher.")
            return

        if not valorInicial:
            valorInicial = 0

        try:
            conexao.execute(comando, conta, meta, descricao, valorTotal, valorInicial)
            conexao.commit()
            self.cbMetas.delete(0, END)
            self.cbTipoMeta.delete(0, END)
            self.txtDescricaoMeta.delete(0, END)
            self.txtValorTotalMeta.delete(0, END)
            self.txtValorInicialMeta.delete(0, END)

            self.carregarGridMetas(event=None)
            self.atualizarCombos(3)
        except pyodbc.Error as e:
            conexao.rollback()
            messagebox.showerror("Erro", str(e))
            return
        finally:
            conexao.close()

    def finalizarMeta(self, event):
        item_selecionado = self.metas.selection()

        if item_selecionado:
            valores = self.metas.item(item_selecionado)['values']

        meta_id = valores[0]
        login_id = self.usuario()

        conexao = ConexaoBD.conectar(self)
        comando = ("Update A Set ativo = 0 From meta_tb A Where meta_id = ? And login_id = ? ")
        conexao.execute(comando, meta_id, login_id)
        conexao.commit()
        conexao.close()

        self.carregarGridMetas(event=None)

    def DepositaMeta(self):
        comando = "pDepositaMetas ?, ?, ?, ?"
        conexao = ConexaoBD.conectar(self)

        indice_meta = self.cbMetas.get()

        meta = indice_meta[0]
        descricao = str(self.txtDescMeta.get().strip())
        vlDeposita = self.txtVlDeposita.get()
        vlSacar = self.txtVlSaca.get()

        if not meta:
            messagebox.showinfo("Erro", "O campo Meta está vazio! Favor preencher.")
            return

        if not descricao:
            descricao = None

        if not vlDeposita:
            vlDeposita = None
            if not vlSacar:
                messagebox.showinfo("Erro", "O campo Deposito está vazio! Favor preencher.")
                return

        if not vlSacar:
            if not vlDeposita:
                messagebox.showinfo("Erro", "O campo Sacar está vazio! Favor preencher.")
                return

        if not vlSacar:
            vlSacar = None

        try:
            conexao.execute(comando, meta, vlDeposita, vlSacar, descricao)
            conexao.commit()

            self.cbMetas.delete(0, END)
            self.cbTipoMeta.delete(0, END)
            self.txtDescMeta.delete(0, END)
            self.txtVlDeposita.delete(0, END)
            self.txtVlSaca.delete(0, END)

            self.carregarGridMetas(event=None)
            self.carregarMenu()
        except pyodbc.Error as e:
            conexao.rollback()
            messagebox.showerror("Erro", str(e))
            return
        finally:
            conexao.close()

    def incluirAporte(self):
        comando = "pIncluirAporte ?, ?, ?, ?"
        conexao = ConexaoBD.conectar(self)

        ticker = str(self.cbTicker.get().strip())
        cota = int(self.txtCota.get())
        vlCota = self.txtVlCota.get()
        rendimento = self.txtRendMes.get()

        if not ticker:
            messagebox.showinfo("Erro", "O campo Ticker está vazio! Favor preencher.")
            return

        if not cota:
            messagebox.showinfo("Erro", "O campo tipo do Quantidade de Cota está vazio! Favor preencher.")
            return

        if not vlCota:
            messagebox.showinfo("Erro", "O campo Valor da Cota está vazio! Favor preencher.")
            return

        if not rendimento:
            rendimento = None

        try:
            conexao.execute(comando, ticker, cota, vlCota, rendimento)
            conexao.commit()
            self.cbTicker.delete(0, END)
            self.txtCota.delete(0, END)
            self.txtVlCota.delete(0, END)
            self.txtRendMes.delete(0, END)

            self.atualizarCombos(4)
        except pyodbc.Error as e:
            conexao.rollback()
            messagebox.showerror("Erro", str(e))
            return
        finally:
            conexao.close()
    def incluirFundo(self):
        comando = "pIncluirFundo ?, ?, ?, ?"
        conexao = ConexaoBD.conectar(self)

        emp = str(self.txtempresa.get().strip())
        tipo = str(self.txttipo.get().strip())
        ticker = str(self.txtticker.get().strip())
        categora = str(self.txtescolha.get().strip())

        if not emp:
            messagebox.showinfo("Erro", "O campo Nome da Empresa está vazio! Favor preencher.")
            return

        if not tipo:
            messagebox.showinfo("Erro", "O campo tipo do Fundo está vazio! Favor preencher.")
            return

        if not ticker:
            messagebox.showinfo("Erro", "O campo Ticker está vazio! Favor preencher.")
            return

        if not categora:
            messagebox.showinfo("Erro", "Selecionar qual categoria do fundo, por favor!")
            return

        if categora == 'A':
            categora == 'A'
        elif categora == 'F':
            categora == 'F'
        else:
            messagebox.showinfo("Erro", "Digite F para FIIS ou A para Ações!")
            return

        try:
            conexao.execute(comando, emp, tipo, ticker, categora)
            conexao.commit()

            self.txtempresa.delete(0, END)
            self.txttipo.delete(0, END)
            self.txtticker.delete(0, END)
            self.txtescolha.delete(0, END)

            self.carregarGridFundo(categora)
            self.atualizarCombos(4)
        except pyodbc.Error as e:
            conexao.rollback()
            messagebox.showerror("Erro", str(e))
            return
        finally:
            conexao.close()

    def incluirParcela(self):
        conexao = ConexaoBD.conectar(self)
        vl1 = self.txtparcela1.get()
        vl2 = self.txtparcela2.get()
        sobra = self.txtSobra.get()
        login_id = self.usuario()

        vl1_formatado = "{:.2f}".format(float(vl1))

        if not vl2:
            vl2_formatado = 0
        else:
            vl2_formatado = "{:.2f}".format(float(vl2))

        data = datetime.date.today()
        formatted_date = data.strftime('%Y%m%d')

        if not vl2 and vl1 > '0':
            self.txtparcela2.config(state="normal")
            self.txtVlTotal.config(state="normal")
            self.txtSobra.config(state="normal")

            comando = ("Insert Into decimo_terceiro_tb (login_id, vl_parcela1, vl_total, vl_sobra, dt_inclusao) "
                       "Select ?, ?, ?, ?, ?")

            conexao.execute(comando, login_id, vl1, vl1, vl1, formatted_date)

            self.txtVlTotal.insert(0, vl1)
            self.txtSobra.insert(0, vl1)

            self.txtparcela1.config(state="disabled")
            self.txtVlTotal.config(state="disabled")
            self.txtSobra.config(state="disabled")

            conexao.commit()
            conexao.close()

            #Atualizar o combo data
            datas = self.carregarData13()
            self.cbData13['values'] = datas

        elif vl2 > '0':
            self.txtVlTotal.config(state="normal")
            self.txtSobra.config(state="normal")

            comando = ("Select Max(decimo_id) From decimo_terceiro_tb Where login_id = ?")
            resultado = conexao.execute(comando, login_id)
            id = resultado.fetchall()

            total = (float(vl1_formatado) + float(vl2_formatado))
            total_formatado = "R$ {:.2f}".format(total)
            resultado = (float(sobra) + float(vl2))
            sobra_formatada =  "R$ {:.2f}".format(resultado)
            decimo_id = id[0][0]

            comando = ("Update A Set vl_parcela2 = ?, vl_total = ?, vl_sobra = ?, dt_alteracao = ? "
                       "From decimo_terceiro_tb A Where decimo_id = ? And login_id = ?")

            self.txtVlTotal.delete(0, END)
            self.txtSobra.delete(0, END)

            self.txtVlTotal.insert(0, total_formatado)
            self.txtSobra.insert(0, sobra_formatada)

            self.txtVlTotal.config(state="disabled")
            self.txtSobra.config(state="disabled")
            self.txtparcela2.config(state="disabled")

            conexao.execute(comando, float(vl2), total, resultado, formatted_date, decimo_id, login_id)
            conexao.commit()
            conexao.close()
        else:
            messagebox.showinfo("Erro", "Informe o valor da parcela.")
            conexao.close()
            return

    def incluirDespesa(self):
        comando = "pIncluirDespesas13 ?, ?, ?, ?, ?"
        conexao = ConexaoBD.conectar(self)
        cursor = conexao.cursor()

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

        try:
            cursor.execute(comando, despesa, tpDespesa, loja, valor, desc)
            conexao.commit()

            self.txtValor.delete(0, END)
            self.txtDescricao.delete(0, END)
            self.cbDespesa.delete(0, END)
            self.cbTpDespesa.delete(0, END)
            self.cbLoja.delete(0, END)

            self.carregarGrid13(event=None)
            self.carregar(event=None)
            self.atualizarCombos(5)
        except pyodbc.Error as e:
            conexao.rollback()
            messagebox.showerror("Erro", str(e))
            return
        finally:
            conexao.close()
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
                    self.entry = Entry(self.despesas)
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
        comando = "pAlteracaoDespesas13 ?, ?, ?, ?"
        conexao = ConexaoBD.conectar(self)
        cursor = conexao.cursor()

        try:
            cursor.execute(comando, self.id, self.coluna_selecionada, novo_valor, "")
            conexao.commit()
        except pyodbc.Error as e:
            conexao.rollback()
            messagebox.showerror("Erro", str(e))
            return
        finally:
            conexao.close()

        #Remover o Entry após a edição
        self.entry.destroy()

        self.carregarGrid13(event=None)
        self.carregar(event=None)

    def excluir(self, event):
        global indice_selecionado
        indice_selecionado = self.despesas.identify_row(event.y)
        self.id = self.despesas.set(indice_selecionado, "#1")

        if indice_selecionado is not None:
            self.despesas.delete(indice_selecionado)
            indice_selecionado = None

        comando = "pAlteracaoDespesas13 ?, ?, ?, ?"
        conexao = ConexaoBD.conectar(self)
        cursor = conexao.cursor()

        try:
            cursor.execute(comando, self.id, "", "", "#5")
            conexao.commit()
        except pyodbc.Error as e:
            conexao.rollback()
            messagebox.showerror("Erro", str(e))
            return
        finally:
            conexao.close()

        conexao.commit()
        conexao.close()

        self.carregarGrid13(event=None)
        self.carregar(event=None)

    def criar_pdf(self, caminho):
        # Definir o tamanho da página e criar o objeto do documento
        doc = SimpleDocTemplate(caminho, pagesize=letter)

        # Definir o estilo do parágrafo
        styles = getSampleStyleSheet()
        estilo_titulo = styles["Title"]
        estilo_texto = ParagraphStyle(
            "estilo_texto",
            parent=styles["Normal"],
            fontSize=12,
            fontName="Helvetica-Bold"
        )

        if self.escolha.get() == 'Op1':
            texto = Paragraph("Relatório De Gastos Mensais",
                              estilo_texto)
            comando = "pRelatorios ?, ?, ?, ?, ?, ?, ?, ?"
            conexao = ConexaoBD.conectar(self)
            tipo = 1

            dt_inicio = self.data1.get()
            dt_fim = self.data2.get()
            produto = self.cbProdutoRelat.get()
            tpProduto = self.cbContaRelatorio.get()

            idProduto = int(produto.split()[0])

            if not tpProduto:
                idTpProduto = ""
            else:
                idTpProduto = int(tpProduto.split()[0])

            cursor = conexao.cursor()
            resultado = cursor.execute(comando, tipo, idProduto, idTpProduto, "", "", "", dt_inicio, dt_fim)

            if resultado.description == 1:
                message = cursor.fetchone()[0]
                messagebox.showerror("Erro", message)
                conexao.close()
                return

            colunas = [column[0] for column in resultado.description]
            dados = [colunas] + [list(row) for row in resultado]
            tabela = Table(dados, colWidths=[85, 100, 85])
            conexao.close()

        elif self.escolha.get() == 'Op2':
            texto = Paragraph("Relatório de Contas",
                              estilo_texto)
            comando = "pRelatorios ?, ?, ?, ?, ?, ?, ?, ?"
            conexao = ConexaoBD.conectar(self)
            tipo = 2
            if self.checkbox_value.get() == 1:
                status = 1
            else:
                status = 0

            dt_inicio = self.data1.get()
            dt_fim = self.data2.get()
            tpProduto = self.cbContaRelatorio.get()
            idTpProduto = int(tpProduto.split()[0])

            cursor = conexao.cursor()
            resultado = conexao.execute(comando, tipo, "", idTpProduto, "", status, "", dt_inicio, dt_fim)

            if resultado.description == 1:
                message = cursor.fetchone()[0]
                messagebox.showerror("Erro", message)
                conexao.close()
                return

            colunas = [column[0] for column in resultado.description]
            dados = [colunas] + [list(row) for row in resultado]
            tabela = Table(dados, colWidths=[85, 100, 85])
            conexao.close()

        elif self.escolha.get() == 'Op3':
            texto = Paragraph(
                "Relatório de Metas",
                estilo_texto)
            comando = "pRelatorios ?, ?, ?, ?, ?, ?, ?, ?"
            conexao = ConexaoBD.conectar(self)
            tipo = 3
            if self.checkbox_value.get() == 1:
                status = 1
            else:
                status = 0

            dt_inicio = self.data1.get()
            dt_fim = self.data2.get()
            tpProduto = self.cbContaRelatorio.get()
            idTpProduto = int(tpProduto.split()[0])

            cursor = conexao.cursor()
            resultado = cursor.execute(comando, tipo, "", idTpProduto, "", status, "", dt_inicio, dt_fim)

            if resultado.description != None:
                message = cursor.fetchone()[0]
                messagebox.showerror("Erro", message)
                conexao.close()
                return

            colunas = [column[0] for column in resultado.description]
            dados = [colunas] + [list(row) for row in resultado]
            tabela = Table(dados, colWidths=[85, 100, 85])
            conexao.close()

        elif self.escolha.get() == 'Op4':
            texto = Paragraph(
                "Relatório de Aportes",
                estilo_texto)
            comando = "pRelatorios ?, ?, ?, ?, ?, ?, ?, ?"
            conexao = ConexaoBD.conectar(self)
            tipo = 4
            if self.checkbox_value.get() == 1:
                status = 1
            else:
                status = 0

            dt_inicio = self.data1.get()
            dt_fim = self.data2.get()
            ticker = self.cbTicker.get().strip()
            fundo = self.cbFundo.get()
            id = int(fundo.split()[0])

            cursor = conexao.cursor()
            resultado = cursor.execute(comando, tipo, "", "", id, status, ticker, dt_inicio, dt_fim)

            if resultado.description != None:
                message = cursor.fetchone()[0]
                messagebox.showerror("Erro", message)
                conexao.close()
                return

            colunas = [column[0] for column in resultado.description]
            dados = [colunas] + [list(row) for row in resultado]
            tabela = Table(dados, colWidths=[85, 100, 85])
            conexao.close()

        # Lista para armazenar os elementos do documento
        elementos = []

        # Adicionar o título
        titulo = Paragraph("Relatório", estilo_titulo)
        elementos.append(titulo)

        elementos.append(texto)

        # Adicionar espaço entre o texto e a tabela
        espaco = Spacer(1, 20)
        elementos.append(espaco)

        # Adicionar uma tabela
        estilo_tabela = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        tabela.setStyle(estilo_tabela)
        elementos.append(tabela)

        # Construir o documento PDF
        doc.build(elementos)

    def alterarGastos(self, event):
        region = self.gastos.identify_region(event.x, event.y)
        if region == 'cell':
            item_id = self.gastos.identify_row(event.y)
            if item_id:
                self.item_selecionado = item_id
                self.coluna_selecionada = self.gastos.identify_column(event.x)
                self.id = self.gastos.set(item_id, "#1")

                # Verifica se a coluna selecionada é editável
                if self.coluna_selecionada == "#2" or self.coluna_selecionada == "#5":
                    messagebox.showwarning("Coluna Não Editável","Você clicou em uma coluna que não pode ser alterada.")
                else:
                    if self.item_selecionado and self.coluna_selecionada:
                        self.gastos.focus(self.item_selecionado)
                        self.gastos.selection_set(self.item_selecionado)

                        #Obter o valor atual da célula
                        valor_atual = self.gastos.set(self.item_selecionado, self.coluna_selecionada)

                        #Remover o valor atual da célula
                        self.gastos.set(self.item_selecionado, self.coluna_selecionada, "")

                        #Criação do Entry para a edição
                        self.entry = Entry(self.gastos)
                        self.entry.insert(0, valor_atual)
                        self.dt_alteracao = datetime.date.today()
                        self.entry.bind("<Return>", self.salvarGastos)

                        #Posicionar o Entry na célula selecionada
                        bbox = self.gastos.bbox(self.item_selecionado, column=self.coluna_selecionada)
                        x = bbox[0] + self.gastos.winfo_x() + 2
                        y = bbox[1] + self.gastos.winfo_y() + 2
                        self.gastos.update_idletasks()
                        self.entry.place(x=x, y=y, width=bbox[2] - bbox[0], height=bbox[3] - bbox[1])
                        self.entry.focus_set()
    def salvarGastos(self, event):
        novo_valor = self.entry.get()
        conexao = ConexaoBD.conectar(self)
        comando = "Exec pAlterarGastosMensais ?, ?, ?, ?"

        try:
            if self.coluna_selecionada == "#3":
                conexao.execute(comando, int(self.id), None, novo_valor, self.coluna_selecionada)
                conexao.commit()
            if self.coluna_selecionada == "#4":
                conexao.execute(comando, int(self.id), novo_valor, None, self.coluna_selecionada)
                conexao.commit()
                valor_formatado = 'R$ {:,.2f}'.format(float(novo_valor))
                self.gastos.set(self.item_selecionado, self.coluna_selecionada, valor_formatado)
        except pyodbc.Error as e:
            conexao.rollback()
            messagebox.showerror("Erro", str(e))
            return
        finally:
            conexao.close()

        # Remover o Entry após a edição
        self.entry.destroy()

        self.carregarMenu()

    def excluirGastos(self, event):
        global indice_selecionado
        indice_selecionado = self.gastos.identify_row(event.y)
        id = self.gastos.set(indice_selecionado, "#1")

        if indice_selecionado is not None:
            self.gastos.delete(indice_selecionado)
            indice_selecionado = None

        conexao = ConexaoBD.conectar(self)
        comando = ("Delete From gastos_tb Where gasto_id = " + id)
        conexao.execute(comando)
        conexao.commit()
        conexao.close()

        self.carregarMenu

    def carregarSalario(self):
        conexao = ConexaoBD.conectar(self)
        comando = ("Select salario, sobra, extra, gastos From salario_tb Where login_id = ?")

        login = self.usuario()

        resultado = self.conexao.execute(comando, login)
        registros = resultado.fetchall()

        for registro in registros:
            #Obtém os valores do registro
            salario, sobra, extra, gastos = registro

        salario_formatado = f'{salario:.2f}'
        sobra_formatado = f'{sobra:.2f}'
        extra_formatado = f'{extra:.2f}'
        gastos_formatado = f'{gastos:.2f}'

        if extra_formatado > 0:
            salario_formatado += extra_formatado
            sobra_formatado += extra_formatado

        self.txtSaldo.insert(0, salario_formatado)
        self.txtSobra.insert(0, sobra_formatado)
        self.txtGastos.insert(0, gastos_formatado)

    def usuario(self):
        comando = ("Select login_id From usuario_tb Where ativo = 1")
        conexao = ConexaoBD.conectar(self)
        cursor = conexao.cursor()
        resultado = cursor.execute(comando)

        id = resultado.fetchone()[0]
        login = id

        conexao.commit()
        conexao.close()

        return login

    def sair(self):
        login = self.usuario()

        update = ("Update A Set ativo = 0 From usuario_tb A Where login_id = ?")

        conexao = ConexaoBD.conectar(self)
        conexao.execute(update, login)
        conexao.commit()
        conexao.close()

        #self.janela.quit()
        self.janela.destroy()

    def carregarMenu(self):
        id = self.usuario()
        comando = ("Select l.nome 'nome', s.salario 'salario', s.sobra 'sobra', "
                   "s.gastos 'gastos', s.extra 'extra' From login_tb l "
                   "Inner Join salario_tb s On l.login_id = s.login_id "
                   "Inner Join usuario_tb u On l.login_id = u.login_id And u.ativo = 1 "
                   "Where l.login_id = ?")

        conexao = ConexaoBD.conectar(self)
        resultado = conexao.execute(comando, id)
        registros = resultado.fetchall()
        conexao.close()
        for registro in registros:
            nome, salario, sobra, gastos, extra = registro

            nome_formatado = f'{nome:10}'
            salario_formatado = f'R$ {salario:.2f}'
            sobra_formatado = f'R$ {sobra:.2f}'
            gastos_formatado = f'R$ {gastos:.2f}'
            extra_formatado = f'R$ {extra:.2f}'

        if not gastos_formatado:
            gastos_formatado = 0

        if not extra_formatado:
            extra_formatado = 0

        self.lblNome.config(text='Usuário: ' + nome_formatado)
        self.lblSalario.config(text='Sálario: ' + salario_formatado)
        self.lblGastos.config(text='Gastos: ' + gastos_formatado)
        self.lblSobra.config(text='Sobra: ' + sobra_formatado)
        self.lblExtra.config(text='Extra: ' + extra_formatado)

    def alterarSalario(self):
        salario = self.txtSalario.get()
        extra = self.txtExtra.get()

        comando = "Exec pAlteraSalario ?, ?"

        conexao = ConexaoBD.conectar(self)

        if not salario:
            salario_formatado = None
        else:
            salario_formatado = "R$ {:.2f}".format(float(salario))

        if not extra:
            extra_formatado = None
        else:
            extra_formatado = "R$ {:.2f}".format(float(extra))

        try:
            conexao.execute(comando, salario_formatado, extra_formatado)
            conexao.commit()
            self.txtSalario.delete(0, END)
            self.txtExtra.delete(0, END)
            self.carregarMenu()
        except pyodbc.Error as e:
            conexao.rollback()
            messagebox.showerror("Erro", str(e))
            return
        finally:
            conexao.close()

Interagir()