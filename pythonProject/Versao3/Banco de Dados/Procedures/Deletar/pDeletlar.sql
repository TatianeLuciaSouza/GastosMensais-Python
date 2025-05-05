Create Or Alter Procedure pDeletlar (
	@login     Int,
	@idTabela  Int,
	@tipo      Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 06/12/2024
Descrição: Deletar ou finalizar:
		   1 - Gastos Mensais
		   2 - Metas
		   3 - Deletar gastos do Décimo Terceiro
		   4 - Excluir contas
******************************************************************/

Set Nocount On

Begin Try

	If @tipo = 1
	Begin	
		Exec pDeletarGasto @login, @idTabela
	End

	If @tipo = 2
	Begin
		Exec pFinalizarMeta @login, @idTabela
	End

	If @tipo = 3
	Begin
		Exec pDeletarGasto13 @login, @idTabela
	End

	If @tipo = 4
	Begin
		Exec pDeletarConta @login, @idTabela
	End
	
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