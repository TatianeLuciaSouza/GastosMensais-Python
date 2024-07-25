Create Or Alter Procedure pDepositaMetas(
	@meta_id    Int,
	@vlDeposita Numeric(10,2),
	@vlSaca     Numeric(10,2),
	@descricao  Varchar(30))

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 27/06/2024
Descrição: Procedure para depositar ou sacar o dinheira das metas.
******************************************************************/

Set Nocount On

--Declaração de Variáveis
Declare 
	@login_id    Int,
	@anoMes      Varchar(6),
	@error       Varchar(100)

Select @login_id = login_id From usuario_tb Where ativo = 1
Select @anoMes = Concat(Year(Getdate()),Month(Getdate()))

/*********************************************************************************/


Begin Try

	Set @error = 'Erro ao tentar alterar a tabela meta_tb ou salario_tb'
	If @vlDeposita > 0
	Begin
		Update A
		Set vl_atual += @vlDeposita
		From meta_tb A
		Where meta_id = @meta_id 
			  And login_id = @login_id

		Update A
		Set 
			gastos += @vlDeposita,
			sobra -= @vlDeposita
		From salario_tb A
		Where login_id = @login_id
			  And Concat(Year(dt_inclusao),Month(dt_inclusao)) = @anoMes
	End
	Else
	Begin
		Update A
		Set vl_atual -= @vlSaca
		From meta_tb A
		Where meta_id = @meta_id 
			  And login_id = @login_id

		Update A
		Set 
			gastos -= @vlSaca,
			sobra += @vlSaca
		From salario_tb A
		Where login_id = @login_id
			  And Concat(Year(dt_inclusao),Month(dt_inclusao)) = @anoMes

		Insert Into metaDescricao_tb (
			meta_id,
			descricao,
			dt_inclusao)
		Select
			@meta_id,
			@descricao,
			Getdate()
	End

/******************************************************************/

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