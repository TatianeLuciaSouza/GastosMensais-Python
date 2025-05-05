Create Or Alter Procedure pDeletarGasto (
	@login     Int,
	@idTabela  Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 06/12/2024
Descrição: Deletar os gastos do mês.
******************************************************************/

Set Nocount On

Declare 
	@mesAno  Varchar(6),
	@vlTotal Numeric(6,2)

Set @mesAno = Concat(Format(Month(Getdate()), '00'), Year(Getdate()))
Select @vlTotal = valor From gastos_tb Where login_id = @login And gasto_id = @idTabela

/*******************************************************************************************/

Begin Try
	Begin Tran

		Update A
		Set 
			sobra += @vlTotal,
			dt_alteracao = Getdate()
		From salario_tb A 
		Where A.usuario_id = @login
				And A.mesAno = @mesAno

		Delete From gastos_tb 
		Where login_id = @login 
			  And gasto_id = @idTabela
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