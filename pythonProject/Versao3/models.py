import datetime
import matplotlib.pyplot as plt

from datetime import datetime
from sqlalchemy import text
from pythonProject.Versao3 import database
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model):
    __tablename__ = 'usuario_tb'

    usuario_id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(60), nullable=False)
    email = database.Column(database.String(50), nullable=False, unique=True)
    senha = database.Column(database.String(6), nullable=False)
    dt_inclusao = database.Column(database.DateTime, nullable=False)

    @staticmethod
    def saldoSalario(user_id):
        today = datetime.now()
        mesAno = today.strftime('%m%Y')

        with database.session() as session:
            dados = session.execute(
                 text("""
                    Select 
                        salario, 
                        extra, 
                        sobra, 
                        gastos
                    From salario_tb
                    Where usuario_id = :user_id
                          And mesAno = :mesAno
                """),
                {'user_id': user_id, 'mesAno': mesAno}
        ).fetchall()

        if dados:
            resultado = {
                "salario": float(dados[0][0]),  # Converter Decimal para float
                "extra": float(dados[0][1]),
                "sobra": float(dados[0][2]),
                "gastos": float(dados[0][3])
            }
            return resultado
        return None

    @staticmethod
    def obterSalarios(user_id):
        with database.session() as session:
            dados = session.execute(
                text("""
                        Select 
                            salario, 
                            extra, 
                            sobra, 
                            gastos,
                            mesAno
                        From salario_tb
                        Where usuario_id = :user_id
                    """),
                {'user_id': user_id}
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "salario": float(row[0]),
                    "extra": float(row[1]),
                    "sobra": float(row[2]),
                    "gastos": float(row[3]),
                    "mesano": row[4]
                })
            return resultado  # Retorna a lista de dicionários
        return None

    @staticmethod
    def obterSalario(user_id):
        today = datetime.now()
        mesAno = today.strftime('%m%Y')

        with database.session() as session:
            dados = session.execute(
                text("""
                           Select Top 1 1 salario
                           From salario_tb
                           Where usuario_id = :user_id
                                 And mesAno = :mesAno
                       """),
                {'user_id': user_id, 'mesAno': mesAno}
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({"salario": row[0]})
            return resultado
        return None

    @staticmethod
    def obterDecimo(user_id):
        today = datetime.now()
        ano = today.strftime('%Y')

        with database.session() as session:
            dados = session.execute(
                text("""
                             Select Top 1 1 decimo
                             From decimo_terceiro_tb
                             Where login_id = :user_id
                                   And ano = :ano
                         """),
                {'user_id': user_id, 'ano': ano}
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({"decimo": row[0]})
            return resultado
        return None

    @staticmethod
    def obterSaldo(user_id):
        today = datetime.now()
        mesAno = today.strftime('%m%Y')

        with database.session() as session:
            dados = session.execute(
                text("""
                               Select sobra 
                               From salario_tb
                               Where usuario_id = :user_id
                                     And mesAno = :mesAno
                           """),
                {'user_id': user_id, 'mesAno': mesAno}
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({"sobra": row[0]})
            return resultado
        return None

    @staticmethod
    def obterSaldoDecimo(user_id):
        today = datetime.now()
        ano = today.strftime('%Y')

        with database.session() as session:
            dados = session.execute(
                text("""
                                   Select vl_sobra 
                                   From decimo_terceiro_tb
                                   Where login_id = :user_id
                                         And ano = :ano
                               """),
                {'user_id': user_id, 'ano': ano}
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({"sobra": row[0]})
            return resultado
        return None

    @staticmethod
    def obterGastos(user_id):
        today = datetime.now()
        mesAno = today.strftime('%m%Y')

        with database.session() as session:
            dados = session.execute(
                text("""
                        Select 
                            g.gasto_id As ID,
                            p.nome As produto,
                            l.nome As loja,
                            g.valor,
                            g.vlTotal,
                            g.qtd,
                            g.vlTotal
                        From gastos_tb g With (Nolock)
                        Inner Join produto_tb p
                            On g.produto_id = p.produto_id
                        Inner Join loja_tb l With (Nolock)
                            On g.loja_id = l.loja_id
                        Where g.login_id = :user_id
                              And Format(g.dt_inclusao, 'MMyyyy') = :mesAno
                    """),
                {'user_id': user_id, 'mesAno': mesAno}
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "ID": float(row[0]),
                    "produto": row[1],
                    "loja": row[2],
                    "valor": float(row[3]),
                    "vlTotal": float(row[4]),
                    "qtd": row[5],
                })
            return resultado  # Retorna a lista de dicionários
        return None

    @staticmethod
    def obterTpProduto():
        with database.session() as session:
            dados = session.execute(
                text("""
                           Select 
                               Concat(tp_produto_id, ' - ', descricao) tpProduto
                           From tp_produto_tb With (Nolock)
                       """),
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "tpProduto": row[0]
                })
            return resultado  # Retorna a lista de dicionários
        return None

    @staticmethod
    def obterLoja():
        with database.session() as session:
            dados = session.execute(
                text("""
                               Select 
                                   Concat(loja_id, ' - ', nome) loja
                               From loja_tb With (Nolock)
                           """),
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "loja": row[0]
                })
            return resultado  # Retorna a lista de dicionários
        return None

    @staticmethod
    def obterProduto():
        with database.session() as session:
            dados = session.execute(
                text("""
                                 Select 
                                     Concat(produto_id, ' - ', nome) produto
                                 From produto_tb With (Nolock)
                             """),
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "produto": row[0]
                })
            return resultado  # Retorna a lista de dicionários
        return None

    @staticmethod
    def executaProcAdicionar(user, produto, tpProduto, loja, tpLoja, valor, valor2, valor3, qtd, tipo, desc):
        with database.session() as session:
            session.execute(
                text("""
                        EXEC pAdicionar :user, :produto, :tpProduto, :loja, :tpLoja, :valor, :valor2, :valor3, :qtd, :tipo, :desc
                    """),
                {
                    'user': user,
                    'produto': produto,
                    'tpProduto': tpProduto,
                    'loja': loja,
                    'tpLoja': tpLoja,
                    'valor': valor,
                    'valor2': valor2,
                    'valor3': valor3,
                    'qtd': qtd,
                    'tipo': tipo,
                    'desc': desc
                }
            )
            session.commit()
        return None

    @staticmethod
    def executaProcDeletar(user, idTabela, tipo):
        print('entrou delete')
        with database.session() as session:
            session.execute(
                text("""
                        EXEC pDeletlar :user, :idTabela, :tipo
                    """),
                {
                    'user': user,
                    'idTabela': idTabela,
                    'tipo': tipo
                }
            )
            session.commit()
        return None

    @staticmethod
    def obterContas(user_id):
        today = datetime.now()
        mesAno = today.strftime('%m%Y')

        with database.session() as session:
            dados = session.execute(
                text("""
                        Select 
	                        prod.nome As conta,
                            p.parcela, 
                            p.vl_parcela As valor
                        From contas_tb c With (Nolock)
                        Inner Join parcelas_tb p With (Nolock)
                            On c.conta_id = p.conta_id
                            And p.mesAno = :mesAno
                        Inner Join produto_tb prod With (Nolock)
                            On c.produto_id = prod.produto_id
                        Where c.login_id = :user_id
                              And c.situacao Is Null
                       """),
                {'user_id': user_id, 'mesAno': mesAno}
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "conta": row[0],
                    "parcela": row[1],
                    "valor": float(row[2])
                })
            return resultado  # Retorna a lista de dicionários
        return None

    @staticmethod
    def obterMetas(user_id, status):
        with database.session() as session:
            dados = session.execute(
                text("""
                        Select 
                            meta_id As ID,
                            nome,
                            Cast(dt_inicio As Date),
                            Cast(dt_fim As Date),
                            vl_atual,
                            vl_final
                           From meta_tb  With (Nolock)
                           Where login_id = :user_id
                                 And status = :status
                       """),
                {'user_id': user_id, 'status': status}
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "ID": row[0],
                    "nome": row[1],
                    "dt_inicio": row[2],
                    "dt_fim": row[3],
                    "vl_atual": float(row[4]),
                    "vl_final": float(row[5])
                })
            return resultado  # Retorna a lista de dicionários
        return None

    def jobDesconto(user):
        today = datetime.now()
        if today.day == 3:
            with database.session() as session:
                session.execute(
                    text(""" EXEC pDescontoMensal :user """),
                    { 'user': user }
                )
                session.commit()
            return None

    @staticmethod
    def obterTickers(user_id, fundo):
        if fundo == 'T':
            with database.session() as session:
                dados = session.execute(
                    text("""
                            Select Concat(f.fundo_id, ' - ', f.ticker) tickers
                            From fundos_tb f With (Nolock)
                            Inner Join investimentos_tb i With (Nolock)
                                On f.fundo_id = i.fundo_id
                                And i.login_id = :user_id
                        """),
                        {'user_id': user_id}
                ).fetchall()
        else:
            with database.session() as session:
                dados = session.execute(
                    text("""
                            Select Concat(f.fundo_id, ' - ', f.ticker) tickers
                            From fundos_tb f With (Nolock)
                            Inner Join investimentos_tb i With (Nolock)
            	                On f.fundo_id = i.fundo_id
            	                And i.login_id = :user_id
            	            Where f.categoria = :fundo
                                """),
                    {'user_id': user_id, 'fundo': fundo}
                ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "tickers": row[0]
                })
            return resultado  # Retorna a lista de dicionários
        return None

    @staticmethod
    def obterFundos(user_id, categoria):
        if categoria == 'T':
            with database.session() as session:
                dados = session.execute(
                    text("""
                            Select
                                f.nm_empresa,
                                f.tipo_fundo,
                                f.ticker,
                                i.vl_investido,
                                i.vl_rendimento
                            From investimentos_tb i With (Nolock)
                            Inner Join fundos_tb f With (Nolock)
                                On i.fundo_id = f.fundo_id
                            Where i.login_id = :user_id
                        """),
                    {'user_id': user_id}
                ).fetchall()
        else:
            with database.session() as session:
                dados = session.execute(
                    text("""
                            Select
                                f.nm_empresa,
                                f.tipo_fundo,
                                f.ticker,
                                i.vl_investido,
                                i.vl_rendimento
                            From investimentos_tb i With (Nolock)
                            Inner Join fundos_tb f With (Nolock)
                                On i.fundo_id = f.fundo_id
                                And f.categoria = :categoria
                            Where i.login_id = :user_id
                        """),
                    {'user_id': user_id, 'categoria': categoria}
                ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "nm_empressa": row[0],
                    "tipo_fundo": row[1],
                    "ticker": row[2],
                    "vl_investido": float(row[3]),
                    "vl_rendimento": float(row[4])
                })
            return resultado  # Retorna a lista de dicionários
        return None

    @staticmethod
    def incluirAporte(login, idFundo, qtd, vlCota, vlRend):

        if vlRend == None:
            vlRend = 0

        with database.session() as session:
            session.execute(
                text("""
                        EXEC pIncluirAportes :login, :idFundo, :qtd, :vlCota, :vlRend
                    """),
                {
                    'login': login,
                    'idFundo': idFundo,
                    'qtd': qtd,
                    'vlCota': vlCota,
                    'vlRend': vlRend
                }
            )
            session.commit()
        return None

    @staticmethod
    def obterValor13(user_id):
        today = datetime.now()
        ano = today.strftime('%Y')

        with database.session() as session:
            dados = session.execute(
                text("""
                        Select vl_sobra
                        From decimo_terceiro_tb  With (Nolock)
                        Where login_id = :user_id
                            And ano = :ano
                           """),
                {'user_id': user_id, 'ano': ano}
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "vl_sobra": row[0]
                })
            return resultado  # Retorna a lista de dicionários
        return None

    @staticmethod
    def despesas13(user_id):
        today = datetime.now()
        ano = today.strftime('%Y')

        with database.session() as session:
            dados = session.execute(
                text("""
                        Select 
                            desp.gasto13_id As ID,
                            p.nome As produto,
                            desp.descricao,
                            l.nome As loja,
                            desp.valor,
                            Convert(Date, desp.dt_inclusao) As dt_inclusao
                        From decimo_terceiro_tb d With (Nolock)
                        Inner Join gastos13_tb desp With (Nolock)
                            On desp.decimo_id = d.decimo_id
                        Inner Join loja_tb l With (Nolock)
                            On desp.loja_id = l.loja_id
                        Inner Join produto_tb p With (Nolock)
                            On desp.produto_id = p.produto_id
                        Where d.ano = :ano
                              And d.login_id = :user_id
                            """),
                {'user_id': user_id, 'ano': ano}
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "ID": row[0],
                    "produto": row[1],
                    "descricao": row[2],
                    "loja": row[3],
                    "valor": float(row[4]),
                    "dt_inclusao": row[5]
                })
            return resultado  # Retorna a lista de dicionários
        return None

    @staticmethod
    def cbMetas(user_id):
        with database.session() as session:
            dados = session.execute(
                text("""
                           Select 
                               Concat(meta_id, ' - ', nome) metas
                           From meta_tb With (Nolock)
                           Where login_id = :user_id
                       """),
                {'user_id': user_id}
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "metas": row[0]
                })
            return resultado  # Retorna a lista de dicionários
        return None

    @staticmethod
    def perfilContas(user_id):
        with database.session() as session:
            dados = session.execute(
                text("""
    	                Select 
    	                    c.conta_id As ID,
                            prod.nome As conta,
                            tpProd.descricao As tpConta,
                            c.parcela, 
                            c.descricao,
                            c.valor As vlTotal,
                            Convert(Numeric(10,2),(c.valor/c.parcela)) As vlParcela
                        From contas_tb c With (Nolock)
                        Inner Join produto_tb prod With (Nolock)
                            On c.produto_id = prod.produto_id
                        Inner Join tp_produto_tb tpProd With (Nolock)
                            On prod.tp_produto_id = tpProd.tp_produto_id
                        Where c.login_id = :user_id
                              And c.dt_fim >= Getdate()
                              And c.situacao Is Null
                       """),
                    {'user_id': user_id}
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "ID": row[0],
                    "conta": row[1],
                    "tpConta": row[2],
                    "parcela": row[3],
                    "descricao": row[4],
                    "vlTotal": float(row[5]),
                    "vlParcela": float(row[6])
                })
            return resultado  # Retorna a lista de dicionários
        return None

    @staticmethod
    def perfilMetas(user_id):
        with database.session() as session:
            dados = session.execute(
                text("""
    	                Select
                            meta_id ID,
                            nome meta,
                            vl_atual vlAtual,
                            vl_final vlFinal,
                            vl_Mensal vlMensal,
                            Case When movimento = 1 Then 'Manual' Else 'Automático' End tipo
                        From meta_tb
                        Where login_id = :user_id
                              And status = 'A'
                       """),
                    {'user_id': user_id}
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "ID": row[0],
                    "meta": row[1],
                    "vlAtual": float(row[2]),
                    "vlFinal": float(row[3]),
                    "vlMensal": float(row[4]),
                    "tipo": row[5]
                })
            return resultado  # Retorna a lista de dicionários
        return None

    @staticmethod
    def executaProcAlterar(user, idTabela, valor, valor2, valor3, alteracao, tipo):
        with database.session() as session:
            session.execute(
                text("""
                          EXEC pAlterar :user, :idTabela, :valor, :valor2, :valor3, :alteracao, :tipo
                      """),
                {
                    'user': user,
                    'idTabela': idTabela,
                    'valor': valor,
                    'valor2': valor2,
                    'valor3': valor3,
                    'alteracao': alteracao,
                    'tipo': tipo
                }
            )
            session.commit()
        return None

    @staticmethod
    def obterAportes(user_id, categoria):
        today = datetime.now()
        mesAno = today.strftime('%m%Y')

        if categoria == 'T':
            with database.session() as session:
                dados = session.execute(
                    text("""
                                Select
                                    a.aporte_id ID,
                                    f.nm_empresa,
                                    f.tipo_fundo,
                                    f.ticker,
                                    i.vl_investido,
                                    i.vl_rendimento,
                                    a.vl_cota,
                                    a.vl_total,
                                    a.vl_rendimento
                                From investimentos_tb i With (Nolock)
                                Inner Join fundos_tb f With (Nolock)
                                    On i.fundo_id = f.fundo_id
                                Inner Join aportes_tb a With (Nolock)
                                    On i.investimento_id = a.investimento_id
                                    And a.mesAno = :mesAno
                                Where i.login_id = :user_id
                                      And i.status Is Null
                            """),
                    {'user_id': user_id, 'mesAno': mesAno}
                ).fetchall()
        else:
            with database.session() as session:
                dados = session.execute(
                    text("""
                                Select
                                    a.aporte_id ID,
                                    f.nm_empresa,
                                    f.tipo_fundo,
                                    f.ticker,
                                    i.vl_investido,
                                    a.vl_cota,
                                    a.vl_total,
                                    a.vl_rendimento,
                                    a.qtd_cota qtd
                                From investimentos_tb i With (Nolock)
                                Inner Join fundos_tb f With (Nolock)
                                    On i.fundo_id = f.fundo_id
                                    And f.categoria = :categoria
                                Inner Join aportes_tb a With (Nolock)
                                    On i.investimento_id = a.investimento_id
                                    And a.mesAno = :mesAno
                                Where i.login_id = :user_id
                                      And i.status Is Null
                            """),
                    {'user_id': user_id, 'categoria': categoria, 'mesAno': mesAno}
                ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "ID": row[0],
                    "nm_empressa": row[1],
                    "tipo_fundo": row[2],
                    "ticker": row[3],
                    "vl_investido": float(row[4]),
                    "vl_cota": float(row[5]),
                    "vl_total": float(row[6]),
                    "vl_rendimento": float(row[7]),
                    "qtd": row[8]
                })
            return resultado
        return None

    @staticmethod
    def perfilDecimo13(user_id):
        today = datetime.now()
        ano = today.strftime('%Y')

        with database.session() as session:
            dados = session.execute(
                text("""
       	                Select
                               decimo_id ID,
                               vl_parcela1 vlParcela1,
                               vl_parcela2 vlParcela2,
                               vl_total vlTotal,
                               vl_sobra vlSobra
                           From decimo_terceiro_tb
                           Where login_id = :user_id
                                 And ano = :ano
                          """),
                {'user_id': user_id, 'ano': ano}
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "ID": row[0],
                    "vlParcela1": row[1],
                    "vlParcela2": float(row[2]) if row[2] is not None else 0.0,
                    "vlTotal": float(row[3]) if row[3] is not None else 0.0,
                    "vlSobra": float(row[4]) if row[4] is not None else 0.0
                })
            return resultado  # Retorna a lista de dicionários
        return None

    @staticmethod
    def perfilSalario(user_id):
        today = datetime.now()
        mesAno = today.strftime('%m%Y')

        with database.session() as session:
            dados = session.execute(
                text("""
          	            Select
                            salario_id,
                            salario,
                            sobra,
                            gastos,
                            extra
                        From salario_tb
                        Where usuario_id = :user_id
                            And mesAno = :mesAno
                             """),
                {'user_id': user_id, 'mesAno': mesAno}
            ).fetchall()
        resultado = []
        if dados:
            for row in dados:
                resultado.append({
                    "ID": row[0],
                    "salario": float(row[1]) if row[1] is not None else 0.0,
                    "sobra": float(row[2]) if row[2] is not None else 0.0,
                    "gastos": float(row[3]) if row[3] is not None else 0.0,
                    "extra": float(row[4]) if row[4] is not None else 0.0
                })
            return resultado  # Retorna a lista de dicionários
        return None

    def gerarGrafico(dados):
        plt.figure(figsize=(10, 6))
        plt.bar(dados['Coluna1'], dados['Coluna2'])  # Ajuste conforme necessário
        plt.title('Gráfico de Dados')
        plt.xlabel('Eixo X')
        plt.ylabel('Eixo Y')
        plt.savefig('static/grafico.png')  # Salvar como imagem
        plt.close()

    def gerarPDF(dados):
        pdf_file = "relatorio.pdf"
        c = canvas.Canvas(pdf_file, pagesize=letter)
        width, height = letter

        c.drawString(100, height - 50, "Relatório de Dados")
        y = height - 70
        for index, row in dados.iterrows():
            c.drawString(100, y, str(row.to_dict()))  # Formato das linhas
            y -= 20  # Espaço entre linhas

        c.save()
        return pdf_file