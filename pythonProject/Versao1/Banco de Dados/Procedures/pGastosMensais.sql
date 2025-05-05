Create Or Alter Procedure pGastosMensais(
	@produto   Varchar(50),
	@valor     Numeric(6,2),
	@qtd       Int,
	@loja      Varchar(50),
	@tpProduto Varchar(20))

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 15/03/2024
Descri��o: Procedure para cadastrar novos gastos no m�s.
******************************************************************/

Set Nocount On

--Declara��o de Vari�veis
Declare 
	@produto_id    Int,
	@loja_id       Int,
	@tp_Produto_id Int,
	@error         Varchar(100)

Select @produto_id = produto_id From produto_tb Where nome = @produto
Select @loja_id = loja_id From loja_tb Where nome = @loja
Select @tp_Produto_id = tp_Produto_id From tp_produto_tb Where descricao = @tpProduto

Begin Try

	Set @error = 'Erro ao pegar os IDs'
	If Isnull(@produto_id,'') = ''
	Begin 
		Insert Into produto_tb (nome, dt_inclusao)
		Select @produto, Getdate()
		Select @produto_id = produto_id From produto_tb Where nome = @produto
	End

	If Isnull(@loja_id,'') = ''
	Begin 
		Insert Into loja_tb (nome, dt_inclusao)
		Select @loja, Getdate()
		Select @loja_id = loja_id From loja_tb Where nome = @loja
	End

	If Isnull(@tp_Produto_id,'') = ''
	Begin 
		Insert Into tp_produto_tb (descricao, dt_inclusao)
		Select @tpProduto, Getdate()
		Select @tp_Produto_id = tp_Produto_id From tp_produto_tb Where descricao = @tpProduto

	End

/******************************************************************/

	Set @error = 'Erro ao inserir na tabela gastos_tb'
	Insert Into gastos_tb (
		produto_id,  
		loja_id,     
		valor,       
		qtd,         
		dt_inclusao) 
	Select
		@produto_id,
		@loja_id,
		@valor,
		@qtd,
		Getdate()

/******************************************************************/
End Try

Begin Catch

	Select 
		@Error			  'Local do Erro',
		Error_procedure() 'Error_procedure',
		Error_line()      'Error_line',
		Error_number()    'Error_number',
		Error_message()   'Error_message'

End Catch