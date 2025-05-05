Create Or Alter Procedure pIncluirSalario (
	@login   Int,
	@salario Numeric(14,2),
	@extra   Numeric(14,2),
	@mesAno  Varchar(6))

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 07/03/2054
Descrição: Incluir saslário do mês.
******************************************************************/

Set Nocount On

Begin Try
	Begin Tran

		Insert Into salario_tb (
			usuario_id,
			salario,
			sobra,
			gastos,
			extra,
			mesAno,
			dt_inclusao)
		Select
			@login,
			@salario,
			@salario,
			0,
			@extra,
			@mesAno,
			Getdate()
	Commit
	
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