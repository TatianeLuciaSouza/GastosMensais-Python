Create Or Alter Procedure pDeletarConta (
	@login     Int,
	@idTabela  Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 24/01/2025
Descrição: Deletar conta.
******************************************************************/

Set Nocount On

Begin Try
	
	Update A
	Set situacao = 'Cancelada'
	From contas_tb A 
	Where login_id = @login 
			And conta_id = @idTabela

	Update A
	Set situacao = 'Cancelada'
	From parcelas_tb A
	Inner Join contas_tb c
		On A.conta_id = c.conta_id
	Where A.dt_parcela > Getdate()

	
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