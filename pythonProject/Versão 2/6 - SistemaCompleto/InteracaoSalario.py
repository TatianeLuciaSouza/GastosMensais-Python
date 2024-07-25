from tkinter import messagebox
import pyodbc
from Conexao import ConexaoBD

class NovoSalario:
    def salario(self):
        comando = "pIncluirSalario ?, ?, ?"

        salario = self.txtSalario.get()
        extra = self.txtValor.get()
        desc = self.txtDesc.get().strip()

        salario_formatado = "{:.2f}".format(float(salario))

        if not salario:
            messagebox.showerror("Atenção!", "Informe o novo salário deste mês!")
            return
        if not extra:
            extra_formatado = 0
        else:
            extra_formatado = "{:.2f}".format(float(extra))
        if not desc:
            desc = None

        conexao = ConexaoBD.conectar(self)
        cursor = conexao.cursor()

        try:
            cursor.execute(comando, salario_formatado, extra_formatado, desc)
            conexao.commit()
        except pyodbc.Error as e:
            conexao.rollback()
            messagebox.showerror("Erro", str(e))
            return
        finally:
            conexao.close()
            self.janela.destroy()
            import LayoutTela
            LayoutTela.Aplicacao()

NovoSalario()