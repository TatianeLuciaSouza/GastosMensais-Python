Create Or Alter Procedure pIncluirGasto13 (
	@login     Int,
	@produto   Varchar(50),
	@loja      Varchar(50),
	@tploja    Varchar(12),
	@valor     Numeric(14,2),
	@qtd       Int,
	@descricao Varchar(100))

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 10/01/2025
Descrição: Incluir os gastos do Décimo Terceiro.
******************************************************************/

Set Nocount On

Declare 
	@compra Varchar(8),
	@ano Varchar(4)

Set @ano = Format(Getdate(), 'yyyy')

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
			vl_sobra -= @valor,
			dt_alteracao = Getdate()
		From decimo_terceiro_tb A
		Where ano = @ano
			  And login_id = @login

		Insert Into gastos13_tb (
			produto_id,  
			decimo_id,   
			loja_id,     
			tpCompra,    
			descricao,  
			qtd,
			valor,       
			dt_inclusao)
		Select
			@produto,
			decimo_id,
			@loja,
			@compra,
			@descricao,
			@qtd,
			@valor,
			Getdate()
		From decimo_terceiro_tb With (Nolock)
		Where ano = @ano
			  And login_id = @login
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