Create Or Alter Procedure pIncluirObjetivo(
	@tp_conta	  Varchar(20),
	@objetivo	  Varchar(20),
	@descricao    Varchar(100),
	@valorTotal   Numeric(10,2),
	@valorInicial Numeric(10,2))

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 08/04/2024
Descrição: Procedure para cadastrar um novo objetivo.
******************************************************************/

Set Nocount On

--Declaração de Variáveis
Declare 
	@tp_conta_id Int,
	@error       Varchar(100)

Select @tp_conta_id = tp_Produto_id From tp_produto_tb Where descricao = @tp_conta


Begin Try

	Set @error = 'Erro ao pegar os IDs'

	If Isnull(@tp_conta_id,'') = ''
	Begin 
		Insert Into tp_produto_tb (descricao, dt_inclusao)
		Select @tp_conta, Getdate()
		Select @tp_conta_id = tp_Produto_id From tp_produto_tb Where descricao = Rtrim(@tp_conta)
	End
	
/******************************************************************/

	Set @error = 'Erro ao tentar inserir na tabela objetivo_tb'

	Insert Into objetivo_tb (
		tp_objetivo_id,
		nome,
		descricao,
		vl_total,
		vl_atual,
		ativo,
		dt_inicio)
	Select
		@tp_conta_id,
		@objetivo,
		@descricao,
		@valorTotal,
		@valorInicial,
		1,
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