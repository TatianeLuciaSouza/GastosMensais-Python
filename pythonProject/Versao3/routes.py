import datetime
import traceback
import random
import string


from flask import render_template, request, redirect, jsonify, session, send_file
from flask_mail import Mail
from pythonProject.Versao3 import app, database
from pythonProject.Versao3.models import Usuario
from flask import send_from_directory
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

mail = Mail(app)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/", methods=["GET", "POST"])
def homepage():
    return render_template("homePage.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('lEmail')
        senha = request.form.get('lSenha')

        usuario = Usuario.query.with_entities(
            Usuario.usuario_id,
            Usuario.nome,
            Usuario.email,
            Usuario.senha
        ).filter_by(email=email).first()

        if usuario and usuario.senha == senha:
            session['user_id'] = usuario.usuario_id
            session['user_name'] = usuario.nome
            session['user_email'] = usuario.email
            return redirect("/menu")
        else:
            return render_template("login.html", error="Email ou senha inválidos.")

    return render_template("login.html")

def gerarCodigo(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

@app.route('/enviaCodigo', methods=['POST'])
def enviaCodigo():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"status": "error", "message": "Email não fornecido."}), 400

    codigo = gerarCodigo()

    message = Mail(
        from_email='tatiane.lucia1998@gmail.com',
        to_emails=email,
        subject='Seu Código',
        plain_text_content=f'Seu código é: {codigo}'
    )

    try:
        sg = SendGridAPIClient('chave da api')
        response = sg.send(message)
        return jsonify({"status": "success", "message": "Email enviado com sucesso!", "codigo": codigo}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        primeiroNome = request.form.get('primeiro_nome')
        segundoNome = request.form.get('segundo_nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        data = datetime.date.today()
        formatted_date = data.strftime('%Y%m%d')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario:
            error = "E-mail já cadastrado!"
            return render_template("login.html", error2=error)
        else:
            # Criar um novo objeto Usuario
            novo_usuario = Usuario(nome=f"{primeiroNome} {segundoNome}", email=email, senha=senha,
                                   dt_inclusao=formatted_date)
            try:
                database.session.add(novo_usuario)
                database.session.commit()
            except Exception as e:
                print(f"Erro ao salvar o usuário: {e}")
                database.session.rollback()

    return render_template("login.html")

@app.route("/esqueciSenha", methods=["GET", "POST"])
def esqueiciSenha():
    return render_template("esqueciSenha.html")

@app.route("/menu", methods=["GET", "POST"])
def menu():
    user_name = session.get('user_name')
    user_id = session.get('user_id')
    dadoGrid = []  # Inicializa a lista de dado
    if request.method == "GET":
        try:
            Usuario.jobDesconto(user_id)
            grid = Usuario.obterSalarios(user_id)

            if grid:
                dadoGrid = [
                    {
                        "Salario": row["salario"],
                        "Extra": row["extra"],
                        "Gastos": row["gastos"],
                        "Sobra": row["sobra"],
                        "mesano": row["mesano"],
                    }
                    for row in grid
                ]
            else:
                print("Nenhum dado encontrado para o usuário.")
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        return render_template("menu.html", user_name=user_name, dadoGrid=dadoGrid)


@app.route("/gastos", methods=["GET", "POST"])
def gastosMensais():
    user_name = session.get('user_name')
    user_id = session.get('user_id')
    dadoGrid = []
    combotpProduto = []
    comboLoja = []
    comboProduto = []

    if request.method == "GET":
        try:
            grid = Usuario.obterGastos(user_id)
            carregar = request.args.get('tipo')
            if not carregar:
                if grid:
                    dadoGrid = [
                        {
                            "ID": row["ID"],
                            "Produto": row["produto"],
                            "Loja": row["loja"],
                            "Valor": row["valor"],
                            "vlTotal": row["vlTotal"],
                            "Qtd": row["qtd"],
                            "vlTotal": row["vlTotal"]
                        }
                        for row in grid
                    ]
                else:
                    print("Nenhum dado encontrado para o usuário.")
            else:
                if grid:
                    dadoGrid = [
                        {
                            "ID": row["ID"],
                            "Produto": row["produto"],
                            "Loja": row["loja"],
                            "Valor": row["valor"],
                            "vlTotal": row["vlTotal"],
                            "Qtd": row["qtd"],
                            "vlTotal": row["vlTotal"]
                        }
                        for row in grid
                    ]
                    return jsonify({'dados': dadoGrid, 'mensagem': None}), 200
                else:
                    return jsonify({'dados': [], 'mensagem': 'Nenhuma gasto encontrada.'}), 200

            combotpProduto = Usuario.obterTpProduto()
            comboLoja = Usuario.obterLoja()
            comboProduto = Usuario.obterProduto()

            if combotpProduto:
                combotpProduto = [row['tpProduto'] for row in combotpProduto if 'tpProduto' in row]
            else:
                print("Nenhum dado encontrado")

            if comboLoja:
                comboLoja = [row['loja'] for row in comboLoja if 'loja' in row]
            else:
                print("Nenhum dado encontrado")

            if comboProduto:
                comboProduto = [row['produto'] for row in comboProduto if 'produto' in row]
            else:
                print("Nenhum dado encontrado")

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return render_template("gastosMensais.html", user_name=user_name, dadoGrid=dadoGrid, combotpProduto=combotpProduto, comboLoja=comboLoja, comboProduto=comboProduto)

@app.route("/contas", methods=["GET", "POST"])
def contas():
    user_name = session.get('user_name')
    user_id = session.get('user_id')
    dadoGrid = []
    comboConta = []
    combotpConta = []

    if request.method == "GET":
        try:
            grid = Usuario.obterContas(user_id)
            comboConta = Usuario.obterProduto()
            combotpConta = Usuario.obterTpProduto()

            if combotpConta:
                combotpConta = [row['tpProduto'] for row in combotpConta if 'tpProduto' in row]
            else:
                print("Nenhum dado encontrado")

            if comboConta:
                comboConta = [row['produto'] for row in comboConta if 'produto' in row]
            else:
                print("Nenhum dado encontrado")

            if grid:
                dadoGrid = [
                    {
                        "conta": row["conta"],
                        "parcela": row["parcela"],
                        "valor": row["valor"]
                    }
                    for row in grid
                ]
            else:
                print("Nenhum dado encontrado para o usuário.")
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return render_template("contas.html", user_name=user_name, combotpConta=combotpConta, comboConta=comboConta, dadoGrid=dadoGrid)

@app.route("/metas", methods=["GET", "POST"])
def metas():
    user_name = session.get('user_name')
    user_id = session.get('user_id')
    dadoGrid = []

    if request.method == "GET":
        try:
            tipo = request.args.get('tipo')
            if not tipo:
                tipo = 'A'
                grid = Usuario.obterMetas(user_id,tipo)
                if grid:
                    dadoGrid = [
                        {
                            "ID": row["ID"],
                            "meta": row["nome"],
                            "dtInicio": row["dt_inicio"],
                            "dtFinal": row["dt_fim"],
                            "vlAtual": row["vl_atual"],
                            "vlFinal": row["vl_final"]
                        }
                        for row in grid
                    ]
                else:
                    print("Nenhum dado encontrado para o usuário.")
            else:
                grid = Usuario.obterMetas(user_id, tipo)
                if grid:
                    dadoGrid = [
                        {
                            "ID": row["ID"],
                            "meta": row["nome"],
                            "dtInicio": row["dt_inicio"],
                            "dtFinal": row["dt_fim"],
                            "vlAtual": row["vl_atual"],
                            "vlFinal": row["vl_final"]
                        }
                        for row in grid
                    ]
                    return jsonify({'dados': dadoGrid, 'mensagem': None}), 200
                else:
                    return jsonify({'dados': [], 'mensagem': 'Nenhuma meta encontrada.'}), 200

        except Exception as e:
            # Captura o erro e imprime o traceback
            print("Erro ao processar a requisição:", str(e))
            print("Traceback:", traceback.format_exc())  # Imprime o traceback completo
            return jsonify({'error': str(e)}), 500

    return render_template("metas.html", user_name=user_name, dadoGrid=dadoGrid)

@app.route("/aportes", methods=["GET", "POST"])
def aportes():
    user_name = session.get('user_name')
    user_id = session.get('user_id')
    dadoGrid = []
    combo = []

    if request.method == "GET":
        try:
            fundo = request.args.get('fundo')
            if not fundo:
                combo = Usuario.obterTickers(user_id, 'T')
                if combo:
                    combo = [row['tickers'] for row in combo if 'tickers' in row]
                else:
                    print("Nenhum dado encontrado")
            else:
                combo = Usuario.obterTickers(user_id, fundo)
                if combo:
                    combo = [row['tickers'] for row in combo if 'tickers' in row]
                    return jsonify({'dados': combo, 'mensagem': None}), 200
                else:
                    return jsonify({'dados': [], 'mensagem': 'Nenhuma ticker encontrada.'}), 200

            categoria = request.args.get('tipo')
            if not categoria:
                grid = Usuario.obterFundos(user_id, 'T')
                if grid:
                    dadoGrid = [
                        {
                            "nm_empressa": row["nm_empressa"],
                            "tipo_fundo": row["tipo_fundo"],
                            "ticker": row["ticker"],
                            "vl_investido": row["vl_investido"],
                            "vl_rendimento": row["vl_rendimento"]
                        }
                        for row in grid
                    ]
                else:
                    print("Nenhum dado encontrado para o usuário.")
            else:
                grid = Usuario.obterFundos(user_id, categoria)

                if grid:
                    dadoGrid = [
                        {
                            "nm_empressa": row["nm_empressa"],
                            "tipo_fundo": row["tipo_fundo"],
                            "ticker": row["ticker"],
                            "vl_investido": row["vl_investido"],
                            "vl_rendimento": row["vl_rendimento"]
                        }
                        for row in grid
                    ]
                    return jsonify({'dados': dadoGrid, 'mensagem': None}), 200
                else:
                    return jsonify({'dados': [], 'mensagem': 'Nenhuma fundo encontrada.'}), 200

        except Exception as e:
            # Captura o erro e imprime o traceback
            print("Erro ao processar a requisição:", str(e))
            print("Traceback:", traceback.format_exc())  # Imprime o traceback completo
            return jsonify({'error': str(e)}), 500

    return render_template("aportes.html", user_name=user_name, combo=combo, dadoGrid=dadoGrid)

@app.route("/decimo", methods=["GET", "POST"])
def decimo():
    user_name = session.get('user_name')
    user_id = session.get('user_id')
    valor13 = 0
    dadoGrid = []
    cbTpProduto13 = []
    cbLocal13 = []
    cbProduto13 = []

    if request.method == "GET":
        try:
            cbTpProduto13 = Usuario.obterTpProduto()
            cbLocal13 = Usuario.obterLoja()
            cbProduto13 = Usuario.obterProduto()
            grid = Usuario.despesas13(user_id)
            resultado = Usuario.obterValor13(user_id)
            if not resultado:
                valor13 = 0
            else:
                valor13 = resultado[0]['vl_sobra']
            carregar = request.args.get('tipo')
            if not carregar:
                if grid:
                    dadoGrid = [
                        {
                            "ID": row["ID"],
                            "produto": row["produto"],
                            "descricao": row["descricao"],
                            "loja": row["loja"],
                            "valor": row["valor"],
                            "dt_inclusao": row["dt_inclusao"]
                        }
                        for row in grid
                    ]
                else:
                    print("Nenhum dado encontrado para o usuário.")
            else:
                if grid:
                    dadoGrid = [
                        {
                            "ID": row["ID"],
                            "produto": row["produto"],
                            "descricao": row["descricao"],
                            "loja": row["loja"],
                            "valor": row["valor"],
                            "dt_inclusao": row["dt_inclusao"]
                        }
                        for row in grid
                    ]
                    return jsonify({'dados': dadoGrid, 'valor13': valor13, 'user_name': user_name, 'mensagem': None}), 200

                else:
                    return jsonify({'dados': [], 'mensagem': 'Nenhuma gasto encontrada.'}), 200

            if cbTpProduto13:
                cbTpProduto13 = [row['tpProduto'] for row in cbTpProduto13 if 'tpProduto' in row]
            else:
                print("Nenhum dado encontrado")

            if cbLocal13:
                cbLocal13 = [row['loja'] for row in cbLocal13 if 'loja' in row]
            else:
                print("Nenhum dado encontrado")

            if cbProduto13:
                cbProduto13 = [row['produto'] for row in cbProduto13 if 'produto' in row]
            else:
                print("Nenhum dado encontrado")


        except Exception as e:
            print("Erro ao processar a requisição:", str(e))
            print("Traceback:", traceback.format_exc())
            return jsonify({'error': str(e)}), 500

    return render_template("decimo.html", user_name=user_name, valor13=float(valor13), dadoGrid=dadoGrid, cbTpProduto13=cbTpProduto13, cbLocal13=cbLocal13, cbProduto13=cbProduto13)

@app.route("/relatorio", methods=["GET", "POST"])
def relatorio():
    user_name = session.get('user_name')

    return render_template("relatorios.html", user_name=user_name)

@app.route("/gerarRelatorio", methods=["GET", "POST"])
def gerarRelatorio():
    user_name = session.get('user_name')
    user_id = session.get('user_id')
    montaDado = []

    if request.method == 'POST':
        data = request.json
        tipo = data.get('tipo')

        if tipo == 1:
            produto = data.get('cbProduto')
            tpProduto = data.get('cbTpProduto')
            loja = data.get('cbloja')

            dados = Usuario.consultaRelatorio(user_id, produto, tpProduto, loja)

        if dados:
            montaDado = [
                {
                    "ID": row["ID"],
                    "conta": row["conta"],
                    "tpConta": row["tpConta"],
                    "parcela": row["parcela"],
                    "desc": row["descricao"],
                    "vlTotal": row["vlTotal"],
                    "vlParcela": row["vlParcela"]
                }
                for row in dados
            ]
        else:
            return jsonify({'dados': [], 'mensagem': 'Nenhuma gasto encontrada.'}), 200

        Usuario.gerarGrafico(montaDado)
        pdf = Usuario.gerarPDF(montaDado)
        return send_file(pdf, as_attachment=True)

    return render_template("relatorios.html", user_name=user_name)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    user_id = session.get('user_id')

    try:
        data = request.json
        tipo = data.get('tipo')

        if tipo == 1:
            produto = data.get('cbProduto')
            tpProduto = data.get('cbTpProduto')
            loja = data.get('cbloja')
            tpLoja = data.get('cbTpLocal')
            valor = data.get('valor')
            quantidade = data.get('quantidade')
            tipo = data.get('tipo')

            Usuario.executaProcAdicionar(user_id, produto, tpProduto, loja, tpLoja, valor, None, None, quantidade, tipo, '')
            return {"status": "success", "message": "Produto incluido com sucesso."}, 200

        elif tipo == 2:
            cbContas = data.get('cbContas')
            cbTpContas = data.get('cbTpContas')
            desc = data.get('desc')
            parcelas = data.get('parcelas')
            valorConta = data.get('valorConta')
            tipo = data.get('tipo')

            Usuario.executaProcAdicionar(user_id, cbContas, cbTpContas, '', '', valorConta, None, None, parcelas, tipo, desc)
            return {"status": "success", "message": "Conta incluida com sucesso."}, 200

        elif tipo == 3:
            meta = data.get('meta')
            mov = data.get('mov')
            vlInicial = data.get('vlInicial')
            vlFinal = data.get('vlFinal')
            vlMensal = data.get('vlMensal')
            tipo = data.get('tipo')

            Usuario.executaProcAdicionar(user_id, meta, '','', '', vlInicial, vlFinal, vlMensal, mov, tipo, '')
            return {"status": "success", "message": "Meta incluida com sucesso."}, 200

        elif tipo == 4:
            produto = data.get('produto')
            tpProduto = data.get('tpProduto')
            loja = data.get('loja')
            tpLoja = data.get('tpLoja')
            valor = data.get('valor')
            qtd = data.get('qtd')
            desc = data.get('desc')

            Usuario.executaProcAdicionar(user_id, produto, tpProduto,loja, tpLoja, valor, None, None, qtd, tipo, desc)
            return {"status": "success", "message": "Gastos do décimo tereiro incluido com sucesso."}, 200

        elif tipo == 5:
            valor = data.get('valor')
            Usuario.executaProcAdicionar(user_id, None, None, None, None, valor, None, None, None, tipo, None)
            return {"status": "success", "message": "Décimo terceiro incluido com Sucesso."}, 200

        elif tipo == 6:
            salario = data.get('valor1')
            extra = data.get('valor2')

            if not extra:
                extra = 0

            Usuario.executaProcAdicionar(user_id, None, None, None, None, salario, extra, None, None, tipo, None)
            return {"status": "success", "message": "Salário deste mês incluido com Sucesso."}, 200

    except Exception as e:
        print(f"Erro ao adicionar item: {str(e)}")  # Logando o erro
        return {"status": "error", "message": str(e)}, 400


@app.route('/deletar', methods=['POST'])
def deletar():
    user_id = session.get('user_id')

    try:
        data = request.json
        idTabela = data.get('idTabela')
        tipo = data.get('tipo')
        print('user_id', user_id)
        print('tipo', tipo)
        for item_id in idTabela:
            print('idTabela', int(float(item_id)))
            Usuario.executaProcDeletar(user_id, int(float(item_id)), tipo)
        return {"status": "success", "message": "Exclusão processado com sucesso."}, 200

    except Exception as e:
        print(f"Erro ao excluir itens: {str(e)}")  # Logando o erro
        return {"status": "error", "message": str(e)}, 400


@app.route('/adicionaAporte', methods=['POST'])
def adicionaAporte():
    user_id = session.get('user_id')

    try:
        data = request.json
        idFundo = data.get('idFundo')
        qtd = data.get('qtd')
        vlCota = data.get('vlCota')
        vlRend  = data.get('vlRend')
        Usuario.incluirAporte(user_id, idFundo, qtd, vlCota, vlRend)
        return {"status": "success", "message": "Aporte incluido com sucesso."}, 200

    except Exception as e:
        print(f"Erro ao incluir aporte: {str(e)}")  # Logando o erro
        return {"status": "error", "message": str(e)}, 400

@app.route("/consultaRelatorio", methods=["GET", "POST"])
def consultaRelatorio():
    user_id = session.get('user_id')

    if request.method == "GET":
        try:
            tipo_relatorio = request.args.get('tipo_relatorio')
            if tipo_relatorio in ['rGastos', 'rContas', 'rGastos13']:
                produtos = Usuario.obterProduto()
                tpProdutos = Usuario.obterTpProduto()
                loja = Usuario.obterLoja()

                if produtos:
                    produtos = [row['produto'] for row in produtos if 'produto' in row]
                else:
                    print("Nenhum dado encontrado")

                if tpProdutos:
                    tpProdutos = [row['tpProduto'] for row in tpProdutos if 'tpProduto' in row]
                else:
                    print("Nenhum dado encontrado")

                if loja:
                    loja = [row['loja'] for row in loja if 'loja' in row]
                else:
                    print("Nenhum dado encontrado")

                return jsonify({'produtos': produtos, 'tpProdutos': tpProdutos, 'loja': loja}), 200

            elif tipo_relatorio == 'rMetas':
                metas = Usuario.cbMetas(user_id)
                if metas:
                    metas = [row['metas'] for row in metas if 'metas' in row]
                else:
                    print("Nenhum dado encontrado")
                return jsonify({'metas': metas}), 200

            elif tipo_relatorio == 'rAportes':
                tpFundo = request.args.get('fundo')
                tickers = Usuario.obterTickers(user_id, tpFundo)

                if tickers:
                    tickers = [row['tickers'] for row in tickers if 'tickers' in row]
                else:
                    print("Nenhum dado encontrado")
                return jsonify({'tickers': tickers}), 200

            return jsonify({'error': 'Tipo de relatório não reconhecido.'}), 400

        except Exception as e:
            print(f"Erro ao carregar selects: {str(e)}")
            return jsonify({'error': str(e)}), 500

@app.route("/pContas", methods=["GET", "POST"])
def perfilContas():
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    dadoGrid = []

    if request.method == "GET":
        try:
            grid = Usuario.perfilContas(user_id)
            carregar = request.args.get('tipo')
            if not carregar:
                if grid:
                    dadoGrid = [
                        {
                            "ID": row["ID"],
                            "conta": row["conta"],
                            "tpConta": row["tpConta"],
                            "parcela": row["parcela"],
                            "desc": row["descricao"],
                            "vlTotal": row["vlTotal"],
                            "vlParcela": row["vlParcela"]
                        }
                        for row in grid
                    ]
                else:
                    print("Nenhum dado encontrado para o usuário.")
            else:
                if grid:
                    dadoGrid = [
                        {
                            "ID": row["ID"],
                            "conta": row["conta"],
                            "tpConta": row["tpConta"],
                            "parcela": row["parcela"],
                            "desc": row["descricao"],
                            "vlTotal": row["vlTotal"],
                            "vlParcela": row["vlParcela"]
                        }
                        for row in grid
                    ]
                    return jsonify({'dados': dadoGrid, 'mensagem': None}), 200
                else:
                    return jsonify({'dados': [], 'mensagem': 'Nenhuma gasto encontrada.'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return render_template("Perfil/contas.html", user_name=user_name, dadoGrid=dadoGrid)


@app.route('/alterar', methods=['POST'])
def alterar():
    user_id = session.get('user_id')

    try:
        data = request.json
        idTabela = data.get('id')
        valor = data.get('valor')
        coluna = data.get('coluna')
        tipo = data.get('tipo')
        print('idTabela', idTabela)
        print('valor', valor)
        print('coluna', coluna)
        print('tipo', tipo)

        if coluna == 1:
            Usuario.executaProcAlterar(user_id, int(float(idTabela)), None, valor, None, coluna, tipo)
        elif coluna == 2:
            Usuario.executaProcAlterar(user_id, int(float(idTabela)), valor, None, None, coluna, tipo)
        elif coluna == 3:
            Usuario.executaProcAlterar(user_id, int(float(idTabela)), None, valor, None, coluna, tipo)
        elif coluna == 4:
            Usuario.executaProcAlterar(user_id, int(float(idTabela)), None, None, valor, coluna, tipo)
        elif coluna == 5:
            Usuario.executaProcAlterar(user_id, int(float(idTabela)), valor, None, None, coluna, tipo)
        elif coluna == 6:
            Usuario.executaProcAlterar(user_id, int(float(idTabela)), None, valor, None, coluna, tipo)
        elif coluna == 8:
            Usuario.executaProcAlterar(user_id, int(float(idTabela)), None, None, valor, coluna, tipo)
        else:
            for item_id in idTabela:
                print('user_id', user_id)
                print('idTabela', int(float(item_id)))
                Usuario.executaProcAlterar(user_id, int(float(item_id)), None, None, None, 9, tipo)
        return {"status": "success", "message": "Exclusão processado com sucesso."}, 200

    except Exception as e:
        print(f"Erro ao alterar item: {str(e)}")  # Logando o erro
        return {"status": "error", "message": str(e)}, 400

@app.route("/pMetas", methods=["GET", "POST"])
def perfilMetas():
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    dadoGrid = []

    if request.method == "GET":
        try:
            grid = Usuario.perfilMetas(user_id)
            carregar = request.args.get('tipo')
            if not carregar:
                if grid:
                    dadoGrid = [
                        {
                            "ID": row["ID"],
                            "meta": row["meta"],
                            "vlAtual": row["vlAtual"],
                            "vlFinal": row["vlFinal"],
                            "vlMensal": row["vlMensal"],
                            "tipo": row["tipo"]
                        }
                        for row in grid
                    ]
                else:
                    print("Nenhum dado encontrado para o usuário.")
            else:
                if grid:
                    dadoGrid = [
                        {
                            "ID": row["ID"],
                            "meta": row["meta"],
                            "vlAtual": row["vlAtual"],
                            "vlFinal": row["vlFinal"],
                            "vlMensal": row["vlMensal"],
                            "tipo": row["tipo"]
                        }
                        for row in grid
                    ]
                    return jsonify({'dados': dadoGrid, 'mensagem': None}), 200
                else:
                    return jsonify({'dados': [], 'mensagem': 'Nenhuma gasto encontrada.'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return render_template("Perfil/metas.html", user_name=user_name, dadoGrid=dadoGrid)


@app.route("/pAportes", methods=["GET", "POST"])
def perfilAportes():
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    dadoGrid = []

    if request.method == "GET":
        try:
            categoria = request.args.get('tipo')
            print('categoria', categoria)
            if not categoria:
                grid = Usuario.obterAportes(user_id, 'T')
                if grid:
                    dadoGrid = [
                        {
                            "ID": row["ID"],
                            "nm_empressa": row["nm_empressa"],
                            "tipo_fundo": row["tipo_fundo"],
                            "ticker": row["ticker"],
                            "vl_investido": row["vl_investido"],
                            "vl_cota": row["vl_cota"],
                            "vl_total": row["vl_total"],
                            "vl_rendimento": row["vl_rendimento"],
                            "qtd": row["qtd"]
                        }
                        for row in grid
                    ]
                else:
                    print("Nenhum dado encontrado para o usuário.")
            else:
                grid = Usuario.obterAportes(user_id, categoria)

                if grid:
                    dadoGrid = [
                        {
                            "ID": row["ID"],
                            "nm_empressa": row["nm_empressa"],
                            "tipo_fundo": row["tipo_fundo"],
                            "ticker": row["ticker"],
                            "vl_investido": row["vl_investido"],
                            "vl_cota": row["vl_cota"],
                            "vl_total": row["vl_total"],
                            "vl_rendimento": row["vl_rendimento"],
                            "qtd": row["qtd"]
                        }
                        for row in grid
                    ]
                    return jsonify({'dados': dadoGrid, 'mensagem': None}), 200
                else:
                    return jsonify({'dados': [], 'mensagem': 'Nenhuma aporte encontrada.'}), 200

        except Exception as e:
            # Captura o erro e imprime o traceback
            print("Erro ao processar a requisição:", str(e))
            print("Traceback:", traceback.format_exc())  # Imprime o traceback completo
            return jsonify({'error': str(e)}), 500

    return render_template("Perfil/aportes.html", user_name=user_name, dadoGrid=dadoGrid)


@app.route("/pDecimo13", methods=["GET", "POST"])
def perfilDecimo13():
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    dadoGrid = []

    if request.method == "GET":
        try:
            grid = Usuario.perfilDecimo13(user_id)
            carregar = request.args.get('tipo')
            if not carregar:
                if grid:
                    dadoGrid = [
                        {
                             "ID": row["ID"],
                             "vlParcela1": row["vlParcela1"],
                             "vlParcela2": row["vlParcela2"],
                             "vlTotal": row["vlTotal"],
                             "vlSobra": row["vlSobra"]
                        }
                        for row in grid
                    ]
                else:
                    print("Nenhum dado encontrado para o usuário.")
            else:
                if grid:
                    dadoGrid = [
                        {
                            "ID": row["ID"],
                            "vlParcela1": row["vlParcela1"],
                            "vlParcela2": row["vlParcela2"],
                            "vlTotal": row["vlTotal"],
                            "vlSobra": row["vlSobra"]
                        }
                        for row in grid
                    ]
                    return jsonify({'dados': dadoGrid, 'mensagem': None}), 200
                else:
                    return jsonify({'dados': [], 'mensagem': 'Nenhuma Décimo Terceiro encontrada.'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return render_template("Perfil/decimo13.html", user_name=user_name, dadoGrid=dadoGrid)

@app.route("/verificacao", methods=["GET", "POST"])
def verificar():
    user_id = session.get('user_id')

    if request.method == "GET":
        try:
            tipo = int(request.args.get('tipo'))
            if tipo == 1:
                salario = Usuario.obterSalario(user_id)
                if salario:
                    salario = [row['salario'] for row in salario if 'salario' in row]
                    return jsonify({'salario': salario}), 200
                else:
                    return jsonify({'salario': 0}), 200

            elif tipo == 2:
                saldo = Usuario.obterSaldo(user_id)
                if saldo:
                    saldo = [row['sobra'] for row in saldo if 'sobra' in row]
                    return jsonify({'saldo': saldo}), 200
                else:
                    return jsonify({'saldo': 0}), 200

            if tipo == 3:
                print('entrou')
                decimo = Usuario.obterDecimo(user_id)
                print('decimo', decimo)
                if decimo:
                    decimo = [row['decimo'] for row in decimo if 'decimo' in row]
                    print('decimo', decimo)
                    return jsonify({'decimo': decimo}), 200
                else:
                    return jsonify({'decimo': 0}), 200

            elif tipo == 4:
                saldo = Usuario.obterSaldoDecimo(user_id)
                if saldo:
                    saldo = [row['sobra'] for row in saldo if 'sobra' in row]
                    return jsonify({'saldo': saldo}), 200
                else:
                    return jsonify({'saldo': 0}), 200

            return jsonify({'error': 'Tipo não reconhecido.'}), 400

        except Exception as e:
            print(f"Erro ao carregar: {str(e)}")
            return jsonify({'error': str(e)}), 500

@app.route("/pSalario", methods=["GET", "POST"])
def perfilSalario():
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    dadoGrid = []
    if request.method == "GET":
        try:
            grid = Usuario.perfilSalario(user_id)
            carregar = request.args.get('tipo')
            if not carregar:
                if grid:
                    dadoGrid = [
                        {
                            "ID": row["ID"],
                            "salario": row["salario"],
                            "sobra": row["sobra"],
                            "gastos": row["gastos"],
                            "extra": row["extra"]
                        }
                        for row in grid
                    ]
                else:
                    print("Nenhum dado encontrado para o usuário.")
            else:
                if grid:
                    dadoGrid = [
                        {
                            "ID": row["ID"],
                            "salario": row["salario"],
                            "sobra": row["sobra"],
                            "gastos": row["gastos"],
                            "extra": row["extra"]
                        }
                        for row in grid
                    ]
                    return jsonify({'dados': dadoGrid, 'mensagem': None}), 200
                else:
                    return jsonify({'dados': [], 'mensagem': 'Nenhum salário encontrada este mês.'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return render_template("Perfil/salario.html", user_name=user_name, dadoGrid=dadoGrid)