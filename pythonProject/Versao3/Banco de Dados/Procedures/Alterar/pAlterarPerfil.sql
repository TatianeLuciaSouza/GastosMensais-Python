Create Or Alter Procedure pAlterarPerfil (
	@login      Int,
	@novaSenha  Varchar(8) = Null,
	@senhaAtual Varchar(8) = Null)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 06/03/2025
Descrição: Alterar o nome ou senhad o perfil.
exec pAlterarPerfil 3, '123', '123'
******************************************************************/

Set Nocount On

Begin Try
	Begin Tran
		If Not Exists(Select Top 1 1 From usuario_tb A Where usuario_id = @login And senha = @senhaAtual)
		Begin
			Select 1 resultado
		End
		Else
		Begin
			Update A
			Set 
				senha = @novaSenha,
				dt_alteracao = Getdate()
			From usuario_tb A
			Where usuario_id = @login
					And senha = @senhaAtual

			Select 0 resultado
		End
	Commit
	
/****************************************************************/

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