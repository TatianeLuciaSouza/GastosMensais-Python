Create Or Alter Procedure pDesontaContaMensal (@login Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 02/01/2025
Descrição: Descontar as metas do mês.
******************************************************************/

Declare 
	@mesAno  Varchar(6),
	@vlTotal Numeric(6,2)

Set @mesAno = Concat(Format(Month(Getdate()), '00'), Year(Getdate()))

Set Nocount On

Begin Try
	
	Insert Into #contas(
		conta_id,
		login_id,
		parcela_id,
		vl_parcela)
	Select
		c.conta_id,
		@login,
		p.parcela_id,
		p.vl_parcela
	From contas_tb c With (Nolock)
	Inner Join parcelas_tb p With (Nolock)
		On c.conta_id = p.conta_id
		And p.mesAno = @mesAno
		And p.dt_pag Is Null
	Where c.login_id = @login

	Select @vlTotal = Sum(vl_parcela) From #contas
	
	If @vlTotal > 0
	Begin
		Begin Tran
			Update A
			Set dt_pag = Getdate()
			From parcelas_tb A 
			Inner Join #contas c
				On A.conta_id = c.conta_id
				And A.parcela_id = c.parcela_id
			Where c.login_id = @login

			Update A
			Set 
				gastos += @vlTotal,
				sobra -= @vlTotal,
				dt_alteracao = Getdate()
			From salario_tb A 
			Where A.usuario_id = @login
				  And A.mesAno = @mesAno
		Commit
	End

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