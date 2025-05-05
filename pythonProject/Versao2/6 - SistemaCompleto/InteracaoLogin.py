import datetime
from tkinter import messagebox, END
from Conexao import ConexaoBD

global loginID
class Login:

    def logar(self):
        anoAtual = datetime.date.today().year

        conexao = ConexaoBD.conectar(self)

        email = self.txtLogin.get().strip()
        senha = self.txtSenha.get().strip()

        if not email:
            messagebox.showwarning("Atenção!", "Informe o E-mail.")
            return

        if not senha:
            messagebox.showwarning("Atenção!", "Informe a senha.")
            return

        comando = ("Select login_id From login_tb Where email = '" + email + "' And senha = '" + senha + "'")
        login = conexao.execute(comando)
        if login.rowcount == 0 :
            messagebox.showwarning("Atenção!", "Email ou senha inválido.")
            self.txtLogin.delete(0, END)
            self.txtSenha.delete(0, END)
            return
        else:
            res = login.fetchone()
            loginID = int(res[0])
            comando = ("Select Isnull(Max(Year(dt_inclusao)), 0) From salario_tb Where login_id = ?")
            result = conexao.cursor()
            result.execute(comando, loginID)

            data = result.fetchone()
            ano = int(data[0])

            conexao.commit()

            if ano == anoAtual:
                update = ("Update A Set ativo = 1 From usuario_tb A Where login_id = ?")
                conexao.execute(update, loginID)
                conexao.commit()
                conexao.close()

                self.janela.destroy()
                import LayoutTela
                LayoutTela.Aplicacao()
            else:
                update = ("Update A Set ativo = 1 From usuario_tb A Where login_id = ?")
                conexao.execute(update, loginID)
                conexao.commit()
                conexao.close()

                self.janela.destroy()
                import TelaSalario
                TelaSalario.Salario()

    def cadastro(self):
        comando = "pCadastroUsuario ?, ?, ?"
        conexao = ConexaoBD.conectar(self)

        nome = self.txtLogin.get().strip()
        email = self.txtEmail.get().strip()
        senha = self.txtSenha.get().strip()

        cursor = conexao.cursor()
        resultado = cursor.execute(comando, nome, email, senha)

        if resultado.description != None:
            message = cursor.fetchone()[0]
            messagebox.showerror("Erro", message)
            conexao.close()
            return

        self.txtLogin.delete(0, END)
        self.txtEmail.delete(0, END)
        self.txtSenha.delete(0, END)

        conexao.commit()
        conexao.close()

    def telaSalario(self):
        self.TelaSalario = self.Salario(self)
        self.TelaSalario.janela.deiconify()

    def telaPrincipal(self):
        self.LayoutTela = self.Aplicacao(self)
        self.LayoutTela.janela.deiconify()

    def sair(self):
        self.janela.quit()

Login()