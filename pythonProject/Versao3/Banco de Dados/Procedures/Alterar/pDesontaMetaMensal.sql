Create Or Alter Procedure pDesontaMetaMensal (@login Int)

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
	
	Insert Into #metas(
		meta_id,
		login_id,
		vl_mensal)
	Select
		meta_id,
		login_id,
		vl_mensal
	From meta_tb
	Where status = 'A'
	      And movimento = 2
		  And (dt_alteracao Is Null Or dt_alteracao <> Getdate())

	Select @vlTotal = Sum(vl_mensal) From #metas
	
	If @vlTotal > 0
	Begin
		Begin Tran
			Update A
			Set 
				vl_atual += @vlTotal,
				dt_alteracao = Getdate()
			From meta_tb A 
			Inner Join #metas m
				On A.meta_id = m.meta_id
			Where A.login_id = @login

			Update A
			Set 
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