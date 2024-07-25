Create Or Alter Procedure pCadastroUsuario(
	@nome  Varchar(30),
	@email Varchar(50),
	@senha Varchar(10))

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 24/06/2024
Descrição: Procedure para cadastrar um novo usuário.
******************************************************************/

Set Nocount On

--Declarar Variável
Declare @error    Varchar(100)

/******************************************************************/

--Verificação de E-mail
If Exists(Select 1 From login_tb Where email = @email)
Begin
	 Select 'E-mail existente'
	 Return
End

/******************************************************************/

Begin Try

	Set @error = 'Erro ao tentar inserir na login_tb'
	Insert Into login_tb (
		nome,
		email,
		senha,
		dt_inclusao) 
	Select
		@nome,
		@email,
		@senha,
		Getdate()

/******************************************************************/

End Try

Begin Catch

	Return
		Select @error 
		Select 
			@Error			  'Local do Erro',
			Error_procedure() 'Error_procedure',
			Error_line()      'Error_line',
			Error_number()    'Error_number',
			Error_message()   'Error_message'

End Catch