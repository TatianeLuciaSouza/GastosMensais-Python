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
	@login_id    Int,
	@anoMes      Varchar(6),
	@error       Varchar(100)

Select @produto_id = produto_id From produto_tb Where nome = @produto
Select @tp_conta_id = tp_Produto_id From tp_produto_tb Where descricao = @tp_conta
Select @login_id = login_id From usuario_tb Where ativo = 1
Select @anoMes = Concat(Year(Getdate()),Month(Getdate()))

/*************************************************************************************/

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
		login_id,
		produto_id,
		valor,
		parcela,
		dt_inicio,
		dt_fim,
		dt_inclusao)
	Select
		@tp_conta_id,
		@login_id,
		@produto_id,
		@valor,
		@parcela,
		Dateadd(Month, 1,Getdate()),
		Dateadd(Month, @parcela,Getdate()),
		Getdate()
	
	Set @error = 'Erro ao atualizar tabela salario_tb'
	If @parcela = 1
	Begin
		Update A
		Set 
			gastos += @valor,
			sobra -= @valor
		From salario_tb A
		Where login_id = @login_id
			  And Concat(Year(dt_inclusao),Month(dt_inclusao)) = @anoMes
	End	      

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