Create Or Alter Procedure pFinalizarMeta (
	@login     Int,
	@idTabela  Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 27/12/2024
Descrição: Finalizar metas
******************************************************************/


Set Nocount On

Begin Try

	Update A
	Set
		status = 'E',
		dt_fim = Getdate(),
		dt_alteracao = Getdate()
	From meta_tb A
	Where login_id = login_id
	      And meta_id = @idTabela

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