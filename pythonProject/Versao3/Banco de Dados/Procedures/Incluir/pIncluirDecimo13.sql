Create Or Alter Procedure pIncluirDecimo13 (
	@login     Int,
	@valor     Numeric(14,2))

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 06/02/2025
Descrição: Incluir Priemira Parcela do Décimo Terceiro.
******************************************************************/

Set Nocount On

Begin Try

	Begin Tran
		Insert Into decimo_terceiro_tb (
			login_id,
			vl_parcela1,
			vl_parcela2,
			vl_total,
			vl_sobra,
			ano,
			dt_inclusao)
		Select
			@login,
			@valor,
			0,
			@valor,
			@valor,
			Year(Getdate()),
			Getdate() 
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