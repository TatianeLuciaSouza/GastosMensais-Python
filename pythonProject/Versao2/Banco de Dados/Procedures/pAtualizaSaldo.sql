Create Or Alter Procedure pAtualizaSaldo

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 28/06/2024
Descrição: Procedure para todo início de mês, desconta do salários
           as contas do mês.
******************************************************************/

Set Nocount On

--Declaração de Variáveis
Declare 
	@login_id    Int,
	@anoMes      Varchar(6),
	@error       Varchar(100)

Select @login_id = login_id From usuario_tb Where ativo = 1
Select @anoMes = Concat(Year(Getdate()),Month(Getdate()))

/**********************************************************/

--Tabela temporária
Create Table #contas (
	login_id   Int,
	vl_parcela Numeric(10,2),
	anoMes     Varchar(6))

/**********************************************************/

Begin Try

	Set @error = 'Erro ao inserir na tabela temporária'
	Insert Into #contas (
		login_id,
		vl_parcela)
	Select 
		c.login_id,
		Sum(p.vl_parcela) vl_parcela
	From contas_tb c With (Nolock)
	Inner Join parcelas_tb p With (Nolock)
		On c.conta_id = p.conta_id
		And Concat(Year(p.dt_parcela), Month(p.dt_parcela)) = @anoMes
	Where c.login_id = @login_id
	Group By c.login_id


	Set @error = 'Erro ao atualizar a tabela salario_tb'
	Update A
	Set 
		sobra -= c.vl_parcela,
		gastos += c.vl_parcela
	From salario_tb A
	Inner Join #contas c
		On A.login_id = c.login_id
	Where Concat(Year(A.dt_inclusao), Month(A.dt_inclusao)) = @anoMes

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