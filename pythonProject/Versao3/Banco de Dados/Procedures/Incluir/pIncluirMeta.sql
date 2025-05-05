Create Or Alter Procedure pIncluirMeta (
	@login     Int,
	@meta      Varchar(20),
	@Movimento Int,  -- 1 - Manual / 2 - Automático 
	@vlInicial Numeric(10,2) = Null,
	@vlFinal   Numeric(10,2) = Null,
	@vlMensal  Numeric(10,2) = Null)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 17/12/2024
Descrição: Incluir Metas.
******************************************************************/

Set Nocount On

Begin Try

	Insert Into meta_tb (
		login_id,
		nome,
		vl_mensal,
		vl_final,
		vl_atual,
		status,
		movimento,
		dt_inicio)
	Select
		@login,
		@meta,
		@vlMensal,
		@vlFinal,
		@vlInicial,
		'A',
		@Movimento,
		Getdate()
	
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