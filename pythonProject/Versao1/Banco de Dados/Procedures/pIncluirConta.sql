Create Or Alter Procedure pIncluirConta(
	@tp_conta Varchar(20),
	@produto  Varchar(20),
	@valor    Numeric(6,2),
	@parcela  Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 01/04/2024
Descrição: Procedure para cadastrar uma nova conta.
******************************************************************/

Set Nocount On

--Declaração de Variáveis
Declare 
	@produto_id  Int,
	@tp_conta_id Int,
	@error       Varchar(100)

Select @produto_id = produto_id From produto_tb Where nome = Rtrim(@produto)
Select @tp_conta_id = tp_Produto_id From tp_produto_tb Where descricao = Rtrim(@tp_conta)


Begin Try

	Set @error = 'Erro ao pegar os IDs'

	If Isnull(@tp_conta_id,'') = ''
	Begin 
		Insert Into tp_produto_tb (descricao, dt_inclusao)
		Select @tp_conta, Getdate()
		Select @tp_conta_id = tp_Produto_id From tp_produto_tb Where descricao = @tp_conta
	End

	If Isnull(@produto_id,'') = ''
	Begin 
		Insert Into produto_tb (nome, tp_produto_id, dt_inclusao)
		Select @produto, @tp_conta_id, Getdate()
		Select @produto_id = produto_id From produto_tb Where nome = @produto
	End
	
/******************************************************************/

	Set @error = 'Erro ao tentar inserir na tabela contas_tb'

	Insert Into contas_tb (
		tp_conta_id, 
		produto_id,
		valor,
		parcela,
		dt_inicio,
		dt_fim,
		dt_inclusao)
	Select
		@tp_conta_id,
		@produto_id,
		@valor,
		@parcela,
		Dateadd(Month, 1,Getdate()),
		Dateadd(Month, @parcela,Getdate()),
		Getdate()

/******************************************************************/

End Try

Begin Catch

	If @@Rowcount > 0
		Rollback

	Select 
		@Error			  'Local do Erro',
		Error_procedure() 'Error_procedure',
		Error_line()      'Error_line',
		Error_number()    'Error_number',
		Error_message()   'Error_message'

End Catch