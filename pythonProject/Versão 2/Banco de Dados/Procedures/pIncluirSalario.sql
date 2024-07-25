Create Or Alter Procedure pIncluirSalario(
	@salario Numeric(10,2),
	@extra   Numeric(10,2) Null,
	@desc    Varchar(30)   Null)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 26/06/2024
Descrição: Procedure para incluir salário do mês.
******************************************************************/

Set Nocount On

--Declarar Variável
Declare 
	@error    Varchar(100),
	@login_id Int

/******************************************************************/

--Pegar o ID do usuário que logou
Select @login_id = login_id From usuario_tb Where ativo = 1

/******************************************************************/

Begin Try

	Set @error = 'Erro ao tentar inserir na salario_tb'
	Insert Into salario_tb (
		login_id,
		salario,
		sobra,
		gastos,
		extra,
		desccricao,
		dt_inclusao) 
	Select
		@login_id,
		@salario,
		@salario,
		0.00,
		@extra,
		@desc,
		Getdate()

	Set @error = 'Erro ao tentar executar a procedure pAtualizaSaldo'
	Exec pAtualizaSaldo

/******************************************************************/

End Try

Begin Catch

	Return
		Select 
			@Error			  'Local do Erro',
			Error_procedure() 'Error_procedure',
			Error_line()      'Error_line',
			Error_number()    'Error_number',
			Error_message()   'Error_message'

End Catch