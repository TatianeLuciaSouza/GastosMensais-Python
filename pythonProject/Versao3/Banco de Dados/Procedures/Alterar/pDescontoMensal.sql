Create Or Alter Procedure pDescontoMensal (@login Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 02/01/2025
Descrição: Descontar as contas e metas do mês.
******************************************************************/

Create Table #metas (
	meta_id   Int,
	login_id  Int,
	vl_mensal Numeric(6,2))

Create Table #contas (
	conta_id   Int,
	login_id   Int,
	parcela_id Int,
	vl_parcela Numeric(6,2))

Set Nocount On

Begin Try

	Exec pDesontaContaMensal @login
	
	Exec pDesontaMetaMensal @login
	
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