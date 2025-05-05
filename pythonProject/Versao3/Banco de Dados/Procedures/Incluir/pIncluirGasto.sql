Create Or Alter Procedure pIncluirGasto (
	@login     Int,
	@produto   Varchar(50),
	@loja      Varchar(50),
	@tploja    Varchar(12),
	@valor     Numeric(14,2),
	@qtd       Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 05/12/2024
Descrição: Incluir os gastos do mês.
******************************************************************/

Set Nocount On

Declare 
	@compra Varchar(8),
	@mesAno  Varchar(6)

Set @mesAno = Concat(Format(Month(Getdate()), '00'), Year(Getdate()))

If @tploja = 'lojaVirtual'
Begin 
	Set @compra = 'Online'
End
Else
Begin
	Set @compra = 'Física'
End

/*******************************************************************************************/

Begin Try
	Begin Tran
		Update A
		Set 
			sobra -= @valor,
			dt_alteracao = Getdate()
		From salario_tb A 
		Where A.usuario_id = @login
				And A.mesAno = @mesAno

		Insert Into gastos_tb (
			login_id,
			produto_id,
			loja_id,
			tpCompra,
			valor,
			vlTotal,
			qtd,
			dt_inclusao)
		Select
			@login,
			@produto,
			@loja,
			@compra,
			@valor,
			(@valor * @qtd),
			@qtd,
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