Create Or Alter Procedure pGastosMensais(
	@produto   Varchar(50),
	@valor     Numeric(6,2),
	@qtd       Int,
	@loja      Varchar(50),
	@tpProduto Varchar(20))

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 15/03/2024
Descrição: Procedure para cadastrar novos gastos no mês.
******************************************************************/

Set Nocount On

--Declaração de Variáveis
Declare 
	@produto_id    Int,
	@loja_id       Int,
	@tp_Produto_id Int,
	@login_id      Int,
	@anoMes        Varchar(6),
	@error         Varchar(100)

Select @produto_id = produto_id From produto_tb Where nome = @produto
Select @loja_id = loja_id From loja_tb Where nome = @loja
Select @tp_Produto_id = tp_Produto_id From tp_produto_tb Where descricao = @tpProduto
Select @login_id = login_id From usuario_tb Where ativo = 1
Select @anoMes = Concat(Year(Getdate()),Month(Getdate()))

/*************************************************************************************/

Begin Try

	Set @error = 'Erro ao pegar os IDs'

	If Isnull(@tp_Produto_id,'') = ''
	Begin 
	select 'entrou3'
		Insert Into tp_produto_tb (descricao, dt_inclusao)
		Select @tpProduto, Getdate()
		Select @tp_Produto_id = tp_Produto_id From tp_produto_tb Where descricao = @tpProduto
	End

	If Isnull(@produto_id,'') = ''
	Begin 
		Insert Into produto_tb (nome, dt_inclusao, tp_produto_id) Select @produto, Getdate(), @tp_Produto_id
		Select @produto_id = produto_id From produto_tb Where nome = @produto
		select @produto_id,@produto
	End

	If Isnull(@loja_id,'') = ''
	Begin 
	select 'entrou2'
		Insert Into loja_tb (nome, dt_inclusao)
		Select @loja, Getdate()
		Select @loja_id = loja_id From loja_tb Where nome = @loja
	End

/******************************************************************/

	Set @error = 'Erro ao inserir na tabela gastos_tb'
	Insert Into gastos_tb (
		login_id,
		produto_id,  
		loja_id,     
		valor,       
		qtd,         
		dt_inclusao) 
	Select
		@login_id,
		@produto_id,
		@loja_id,
		@valor,
		@qtd,
		Getdate()

	Set @error = 'Erro ao atualizar tabela salario_tb'
	Update A
	Set 
		gastos += @valor,
		sobra -= @valor
	From salario_tb A
	Where login_id = @login_id
	      And Concat(Year(dt_inclusao),Month(dt_inclusao)) = @anoMes
	      

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