Create Or Alter Procedure pDeletarGasto13 (
	@login     Int,
	@idTabela  Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 14/01/2025
Descrição: Deletar os gastos do décimo terceiro.
******************************************************************/

Set Nocount On

Declare 
	@ano Varchar(4),
	@vlTotal Numeric(6,2)

Set @ano = Format(Getdate(), 'yyyy')
Select @vlTotal = valor From gastos13_tb Where gasto13_id = @idTabela

/*******************************************************************************************/

Begin Try
	Begin Tran

		Update A
		Set 
			vl_sobra += @vlTotal,
			dt_alteracao = Getdate()
		From decimo_terceiro_tb A
		Where ano = @ano
			  And login_id = @login

		Delete From gastos13_tb 
		Where gasto13_id = @idTabela

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