Create Or Alter Procedure pIncluirConta (
	@login     Int,
	@conta     Int,
	@tpConta   Int,
	@descricao Varchar(100),
	@valor     Numeric(14,2),
	@parcela   Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 11/12/2024
Descrição: Incluir os contas.
******************************************************************/

Declare 
	@dtInicio Datetime,
	@dtFim    Datetime

Set @dtInicio = Getdate()
Set @dtFim = Dateadd(Month, Case When @parcela = 1 Then 0 else @parcela End, @dtInicio)

Set Nocount On

Begin Try

	Insert Into contas_tb (
		login_id,
		tp_conta_id,
		produto_id,
		valor,
		parcela,
		descricao,
		dt_inicio,
		dt_fim,
		dt_inclusao)
	Select
		@login,
		@tpConta,
		@conta,
		@valor,
		@parcela,
		@descricao,
		@dtInicio,
		@dtFim,
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