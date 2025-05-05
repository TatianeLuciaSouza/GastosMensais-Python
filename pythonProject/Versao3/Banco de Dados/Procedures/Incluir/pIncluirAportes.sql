Create Or Alter Procedure pIncluirAportes (
	@login     Int,
	@idFundo   Int,
	@qtd       Int,
	@vlCota    Numeric(10,2),
	@vlRend    Numeric(10,2) = Null)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 07/01/2025
Descrição: Incluir aporte.
Exec pIncluirAportes 3, 5, 1, 50, 1
******************************************************************/

Declare 
	@vlTotal    Numeric(10,2),
	@mesAno     Varchar(6),
	@idInvet    Int     

Set @vlTotal = @qtd * @vlCota
Set @mesAno = Concat(Format(Month(Getdate()), '00'), Year(Getdate()))

Select @idInvet = investimento_id From investimentos_tb 
Where login_id = @login
	  And fundo_id = @idFundo

Set Nocount On

Begin Try

	Begin Tran

		Update A
		Set 
			nro_cota += @qtd,
			vl_investido += @vlTotal,
			vl_rendimento += @vlRend,
			dt_altercao = Getdate()
		From investimentos_tb A
		Where login_id = @login
		      And fundo_id = @idFundo

		Update A
		Set 
			sobra -= @vlTotal,
			dt_alteracao = Getdate()
		From salario_tb A 
		Where A.usuario_id = @login
				And A.mesAno = @mesAno

		Insert Into aportes_tb (
			investimento_id,
			qtd_cota,
			vl_cota,
			vl_total,
			vl_rendimento,
			mesAno,
			dt_inclusao)
		Select 
			@idInvet,
			@qtd,
			@vlCota,
			@vlTotal,
			@vlRend,
			@mesAno,
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