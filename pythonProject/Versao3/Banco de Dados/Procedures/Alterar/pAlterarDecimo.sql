Create Or Alter Procedure pAlterarDecimo (
	@login      Int,
	@idTabela   Int,
	@vlParcela1 Numeric(10,2),
	@vlParcela2 Numeric(10,2),
	@alteracao  Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 07/02/2025
Descrição: Alterar o Décimo Terceiro
******************************************************************/

--Variáveis
Declare 
	@valor1  Numeric(10,2),
	@valor2  Numeric(10,2),
	@vlDif   Numeric(10,2),
	@vlSobra Numeric(10,2),
	@sobra   Numeric(10,2)

Select 
	@valor1 = vl_parcela1,
	@valor2 = vl_parcela2,
	@vlSobra = vl_sobra
From decimo_terceiro_tb A
Where login_id = login_id
	  And decimo_id = @idTabela

/*********************************************************/

Set Nocount On

Begin Try
	
	If @alteracao = 1
	Begin
		If @vlParcela1 > @valor1
		Begin
			Set @vlDif = @vlParcela1 - @valor1
			Set @sobra = @vlSobra + @vlDif
		End
		Else If @valor1 > @vlParcela1
		Begin
			Set @vlDif = @valor1 - @vlParcela1
			Set @sobra = @vlSobra - @vlDif
		End

		Update A
		Set
			vl_parcela1 = @vlParcela1,
			vl_Total = @vlParcela1 + A.vl_parcela2,
			vl_sobra = @sobra, 
			dt_alteracao = Getdate()
		From decimo_terceiro_tb A
		Where login_id = @login
			  And decimo_id = @idTabela
	End
	Else 
	Begin
		If @valor2 = 0
		Begin
			Set @vlDif = @vlParcela2
			Set @sobra = @vlParcela2
		End
		Else If @vlParcela2 > @valor2
		Begin
			Set @vlDif = @vlParcela2 - @valor2
			Set @sobra = @vlSobra + @vlDif
		End
		Else If @valor2 > @vlParcela2
		Begin
			Set @vlDif = @valor2 - @vlParcela2
			Set @sobra = @vlSobra - @vlDif
		End

		Update A
		Set
			vl_parcela2 = @vlParcela2,
			vl_Total = @vlParcela2 + A.vl_parcela1,
			vl_sobra = @sobra, 
			dt_alteracao = Getdate()
		From decimo_terceiro_tb A
		Where login_id = @login
			  And decimo_id = @idTabela
	End

/*********************************************************/

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