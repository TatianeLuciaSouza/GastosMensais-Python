Create Or Alter Procedure pAlterar (
	@login     Int,
	@idTabela  Int,
	@valor     Numeric(10,2),
	@valor2    Numeric(10,2),
	@valor3    Varchar(100),
	@alteracao Int,
	@tipo      Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 22/01/2025
Descrição: Atualizar dados das tabelas
		   1 - Contas Mensais
		   2 - Metas
		   3 - Aportes
		   4 - Décimo Terceiro
Exec pAlterar 3, 9, 1, Null, Null, 5,3 
******************************************************************/

Declare 
	@parcela  Int,
	@vlMensal Numeric(10,2),
	@vlRend   Numeric(10,2),
	@qtdCota  Int

/*****************************************************************/

Set Nocount On

Begin Try

	If @tipo = 1
	Begin
		If @alteracao = 2
		Begin
			Set @parcela = Convert(Int, @valor2)
			Exec pAlterarConta @login, @idTabela, @parcela, Null, Null, @alteracao
		End
		Else If @alteracao = 3
		Begin
			Exec pAlterarConta @login, @idTabela, Null, Null, @valor3, @alteracao
		End
		Else If @alteracao = 4
		Begin
			Exec pAlterarConta @login, @idTabela, Null, @valor, Null, @alteracao
		End
	End

	If @tipo = 2
	Begin
		If @alteracao = 2
		Begin
			Exec pAlterarMeta @login, @idTabela, @valor, Null, Null, @alteracao
		End
		Else If @alteracao = 3
		Begin
			Exec pAlterarMeta @login, @idTabela, Null, @valor2, Null, @alteracao
		End
		Else If @alteracao = 4
		Begin
			Set @vlMensal = Convert(Numeric(10,2), @valor3)
			Exec pAlterarMeta @login, @idTabela, Null, Null, @vlMensal, @alteracao
		End
		Else If @alteracao = 9
		Begin
			Exec pAlterarMeta @login, @idTabela, Null, Null, Null, @alteracao
		End
	End

	If @tipo = 3
	Begin
		If @alteracao = 5
		Begin
			Exec pAlterarAporte @login, @idTabela, @valor, Null, Null, @alteracao
		End
		Else If @alteracao = 6
		Begin
			Exec pAlterarAporte @login, @idTabela, Null, @valor2, Null, @alteracao
		End
		Else If @alteracao = 8
		Begin
			Set @vlRend = Convert(Numeric(10,2), @valor3)
			Exec pAlterarAporte @login, @idTabela, Null, Null, @vlRend, @alteracao
		End
		Else If @alteracao = 9
		Begin
			Exec pAlterarAporte @login, @idTabela, Null, Null, Null, @alteracao
		End
	End

	If @tipo = 4
	Begin
		If @alteracao = 1
		Begin
			Exec pAlterarDecimo @login, @idTabela, @valor2, Null, @alteracao
		End
		Else If @alteracao = 2
		Begin
			Exec pAlterarDecimo @login, @idTabela, Null, @valor, @alteracao
		End
	End
	
/*******************************************************************************************/

End Try

Begin Catch

	Select
		Error_procedure() 'Error_procedure',
		Error_line()      'Error_line',
		Error_number()    'Error_number',
		Error_message()   'Error_message'

End Catch