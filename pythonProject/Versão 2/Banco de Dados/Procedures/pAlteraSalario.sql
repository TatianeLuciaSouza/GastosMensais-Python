Create Or Alter Procedure pAlteraSalario (
	@salario Numeric(10,2) Null,
	@extra Numeric(10,2) Null)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 12/07/2024
Descrição: Procedure para alterar o salário ou extra.
******************************************************************/

Set Nocount On

--Declaração de Variáveis
Declare 
	@login_id Int,
	@anoMes    Varchar(6),
	@vlExtra   Numeric(10,2),
	@vlSalario Numeric(10,2), 
	@sobra     Numeric(10,2) = 0,
	@resutado  Numeric(10,2) = 0,
	@error     Varchar(100)

Select @login_id = login_id From usuario_tb Where ativo = 1
Select @anoMes = Concat(Year(Getdate()),Month(Getdate()))

/*******************************************************************************************/

Begin Try
	If (@extra Is Null And @salario > 0)
	Begin
		Select @vlExtra = s.extra
		From salario_tb s 
		Where s.login_id = @login_id And Concat(Year(s.dt_inclusao), Month(s.dt_inclusao)) = @anoMes

		Set @sobra = (@salario + @vlExtra)

		Set @error = '1 - Erro ao atualizar a tabela salario_tb'
		Update A
		Set 
			salario = @salario,
			sobra = @sobra,
			dt_alteracao = Getdate()
		From salario_tb A
		Where A.login_id = @login_id 
			  And Concat(Year(A.dt_inclusao), Month(A.dt_inclusao)) = @anoMes
	End

	If (@salario Is Null And @extra > 0)
	Begin
		Select @vlExtra = s.extra 
		From salario_tb s 
		Where s.login_id = @login_id And Concat(Year(s.dt_inclusao), Month(s.dt_inclusao)) = @anoMes

		If @vlExtra > @extra
		Begin
			Set @resutado = (@vlExtra - @extra)
			Set @sobra -= @resutado
		End

		If @vlExtra < @extra
		Begin
			Set @resutado = (@extra - @vlExtra)
			Set @sobra += @resutado
		End
		
		Set @error = '2 - Erro ao atualizar a tabela salario_tb'
		Update A
		Set 
			extra = @extra,
			sobra += @sobra,
			dt_alteracao = Getdate()
		From salario_tb A
		Where A.login_id = @login_id 
			  And Concat(Year(A.dt_inclusao), Month(A.dt_inclusao)) = @anoMes
	End

	If (@salario > 0 And @extra > 0)
	Begin
		Select @vlExtra = Case When s.extra > @extra Then (s.extra - @extra)
							   When s.extra < @extra Then @extra 
						  Else s.extra End
		From salario_tb s 
		Where s.login_id = @login_id And Concat(Year(s.dt_inclusao), Month(s.dt_inclusao)) = @anoMes

		Set @sobra = (@salario + @vlExtra)
		
		Set @error = '3 - Erro ao atualizar a tabela salario_tb'
		Update A
		Set 
			salario = @salario,
			extra = @vlExtra,
			sobra = @sobra,
			dt_alteracao = Getdate()
		From salario_tb A
		Where A.login_id = @login_id 
			  And Concat(Year(A.dt_inclusao), Month(A.dt_inclusao)) = @anoMes
	End

/*******************************************************************************************/

End Try

Begin Catch

	If @@Rowcount > 0
		Rollback

	Select
		@Error			  'Local do Erro',
		Error_procedure() 'Error_procedure',
		Error_line()      'Error_line',
		Error_number()    'Error_number',
		Error_message()   'Error_message'

End Catch