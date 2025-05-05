--Exec pAdicionar 3, 'Soro do Caramelo', 11,  'Veterinario 24h', 'Física', 35, Null, NUll, 1, 1, Null
Create Or Alter Procedure pAdicionar (
	@login     Int,
	@produto   Varchar(50),
	@tpProduto Int = Null,
	@loja      Varchar(50) = Null,
	@tploja    Varchar(12) = Null,
	@valor     Numeric(10,2),
	@valor2    Numeric(10,2) = Null,
	@valor3    Numeric(10,2) = Null,
	@qtd       Int,
	@tipo      Int,
	@descricao Varchar(100) = Null)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 03/12/2024
Descrição: Adicionar as inclusões dos gastos, contas e metas.
		   1 - Gastos Mensais
		   2 - Contas Mensais
		   3 - Metas
		   4 - Gastos 13
		   5 - Décimo Terceiro
		   6 - Salário do Mês
******************************************************************/

--Declarar Variáveis
Declare
	@ano       Int,
	@mesAno	   Varchar(6),
	@idProduto Int

Set @ano = Year(Getdate())
Set @mesAno = Concat(Format(Month(Getdate()), '00'), Year(Getdate()))

/******************************************************************/

Set Nocount On

Begin Try

	If @tipo = 1
	Begin	
		If (Isnumeric(@produto) = 0) And (Not Exists(Select Top 1 1 From produto_tb Where nome = @produto))
		Begin
			Select 'entrou'
			Insert Into produto_tb (
				nome,
				tp_produto_id,
				dt_inclusao)
			Select
				@produto,
				@tpProduto,
				Getdate()

			Select @produto = produto_id From produto_tb Where nome = @produto
		End
		Else
		Begin
			Select @produto = produto_id From produto_tb Where nome = @produto
		End

		If (Isnumeric(@loja) = 0 And Not Exists(Select Top 1 1 From loja_tb Where nome = @loja))
		Begin
			Select 'entrou'
			Insert Into loja_tb (
				nome,
				dt_inclusao)
			Select
				@loja,
				Getdate()

			Select @loja = loja_id From loja_tb Where nome = @loja
		End
		Else
		Begin
			Select @loja = loja_id From loja_tb Where nome = @loja
		End

		Exec pIncluirGasto @login, @produto, @loja, @tploja, @valor, @qtd
	End

	Else If @tipo = 2
	Begin
		If (Isnumeric(@produto) = 0) And (Not Exists(Select Top 1 1 From produto_tb Where nome = @produto))
		Begin
			Select 'entrou'
			Insert Into produto_tb (
				nome,
				tp_produto_id,
				dt_inclusao)
			Select
				@produto,
				@tpProduto,
				Getdate()

			Select @produto = produto_id From produto_tb Where nome = @produto
		End
		Else
		Begin
			Select @produto = produto_id From produto_tb Where nome = @produto
		End

		Exec pIncluirConta @login, @produto, @tpProduto, @descricao, @valor, @qtd
	End

	If @tipo = 3
		Exec pIncluirMeta @login, @produto, @qtd, @valor, @valor2, @valor3

	If @tipo = 4
	Begin	
		If (Isnumeric(@produto) = 0) And (Not Exists(Select Top 1 1 From produto_tb Where nome = @produto))
		Begin
			Select 'entrou'
			Insert Into produto_tb (
				nome,
				tp_produto_id,
				dt_inclusao)
			Select
				@produto,
				@tpProduto,
				Getdate()

			Select @produto = produto_id From produto_tb Where nome = @produto
		End
		Else
		Begin
			Select @produto = produto_id From produto_tb Where nome = @produto
		End

		If (Isnumeric(@loja) = 0 And Not Exists(Select Top 1 1 From loja_tb Where nome = @loja))
		Begin
			Select 'entrou'
			Insert Into loja_tb (
				nome,
				dt_inclusao)
			Select
				@loja,
				Getdate()

			Select @loja = loja_id From loja_tb Where nome = @loja
		End
		Else
		Begin
			Select @loja = loja_id From loja_tb Where nome = @loja
		End

		Exec pIncluirGasto13 @login, @produto, @loja, @tploja, @valor, @qtd, @descricao
	End

	If @tipo = 5
	Begin
		If Not Exists(Select Top 1 1 From decimo_terceiro_tb Where ano = @ano And login_id = @login)
			Exec pIncluirDecimo13 @login, @valor
	End

	If @tipo = 6
	Begin
		If Not Exists(Select Top 1 1 From salario_tb Where mesAno = @mesAno And usuario_id = @login)
			Exec pIncluirSalario @login, @valor, @valor2, @mesAno
	End
	
/*******************************************************************************************/

End Try

Begin Catch

	If @@Rowcount > 0
		Rollback

	Select
		Error_procedure() 'Error_procedure',
		Error_line()      'Error_line',
		Error_number()    'Error_number',
		Error_message()   'Error_message'

End Catch