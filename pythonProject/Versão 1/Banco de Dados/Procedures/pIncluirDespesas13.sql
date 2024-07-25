Create Or Alter Procedure pIncluirDespesas13(
	@despesa   Varchar(50),
	@tpDespesa Varchar(20),
	@loja      Varchar(50),
	@valor     Numeric(6,2),
	@desc      Varchar(30))

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 24/05/2024
Descrição: Incluir despesas do 13º.
******************************************************************/

Set Nocount On

--Declaração de Variáveis
Declare 
	@despesa_id    Int,
	@loja_id       Int,
	@tp_despesa_id Int,
	@descimo_id    Int,
	@vl_desps      Numeric(14,2),
	@error         Varchar(100)

Select @despesa_id = produto_id From produto_tb Where nome = @despesa
Select @loja_id = loja_id From loja_tb Where nome = @loja
Select @tp_despesa_id = tp_Produto_id From tp_produto_tb Where descricao = @tpDespesa
Select @descimo_id = decimo_id From decimo_terceiro_tb Where Year(dt_inclusao) = Year(Getdate())

Begin Try

	Set @error = 'Erro ao pegar os IDs'
	If Isnull(@tp_despesa_id,'') = ''
	Begin 
		Insert Into tp_produto_tb (descricao, dt_inclusao)
		Select @tpDespesa, Getdate()
		Select @tp_despesa_id = tp_Produto_id From tp_produto_tb Where descricao = @tpDespesa

	End

	If Isnull(@despesa_id,'') = ''
	Begin 
		Insert Into produto_tb (nome, dt_inclusao, tp_produto_id)
		Select @despesa, Getdate(), @tp_despesa_id
		Select @despesa_id = produto_id From produto_tb Where nome = @despesa
	End

	If Isnull(@loja_id,'') = ''
	Begin 
		Insert Into loja_tb (nome, dt_inclusao)
		Select @loja, Getdate()
		Select @loja_id = loja_id From loja_tb Where nome = @loja
	End

/******************************************************************/

	Set @error = 'Erro ao inserir na tabela despesas_tb'
	Insert Into despesas_tb (
		decimo_id,
		produto_id,
		loja_id,
		descricao,
		valor,
		dt_inclusao)
	Select
		@descimo_id,
		@despesa_id,
		@loja_id,
		@desc,
		@valor,
		Getdate()

	Set @vl_desps = (Select Sum(valor) From despesas_tb Where decimo_id = @descimo_id)

	Set @error = 'Erro ao tentar atualizar a tabela decimo_terceiro_tb'
	Update A
	Set
		vl_total = A.vl_parcela1 + A.vl_parcela2,
		vl_sobra = A.vl_total - @vl_desps
	From decimo_terceiro_tb A
	Where decimo_id = @descimo_id


/******************************************************************/
End Try

Begin Catch

	Select 
		@Error			  'Local do Erro',
		Error_procedure() 'Error_procedure',
		Error_line()      'Error_line',
		Error_number()    'Error_number',
		Error_message()   'Error_message'

End Catch