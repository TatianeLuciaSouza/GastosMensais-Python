Create Or Alter Procedure pAlterarMeta (
	@login     Int,
	@idTabela  Int,
	@vlAtual   Numeric(10,2),
	@vlFinal   Numeric(10,2),
	@vlMensal  Numeric(10,2),
	@alteracao Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 30/01/2025
Descrição: Alterar o valor da meta
******************************************************************/

Set Nocount On

Begin Try
	Begin Tran
		If @alteracao = 2
			Update A
			Set 
				vl_atual = @vlAtual,
				dt_alteracao = Getdate()
			From meta_tb A
			Where login_id = @login
			      And meta_id = @idTabela

		If @alteracao = 3
			Update A
			Set 
				vl_final = @vlFinal,
				dt_alteracao = Getdate()
			From meta_tb A
			Where login_id = @login
			      And meta_id = @idTabela

		If @alteracao = 4
			Update A
			Set 
				vl_mensal = @vlMensal,
				dt_alteracao = Getdate()
			From meta_tb A
			Where login_id = @login
			      And meta_id = @idTabela

		If @alteracao = 5
			Update A
			Set 
				movimento = Case When movimento = 1 Then 2
				                 When movimento = 2 Then 1 End,
				dt_alteracao = Getdate()
			From meta_tb A
			Where login_id = @login
			      And meta_id = @idTabela
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