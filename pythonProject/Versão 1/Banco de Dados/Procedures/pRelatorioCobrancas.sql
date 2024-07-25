Create Or ALter Procedure pRelatorioCobrancas (
	@tipo        Int,
	@dt_inicio   Datetime,
	@dt_fim      Datetime,
	@produto_id  Int,
	@tp_conta_id Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 05/04/2024
Descrição: Procedure para emitir relatório de cobranças.
******************************************************************/

Set Nocount On

--Declaração de Variáveis
Declare @error Varchar(100)


Begin Try
	Set @error = 'Erro ao consultar os dados'

	If @tipo = 1
	Begin
		Select 
			p.nome 'Nome do Produto',
			tp.descricao 'Tipo do Produto',
			l.nome 'Local da Compra',
			g.qtd 'Quantidade',
			g.valor 'Valor Total',
			Convert(Date,g.dt_inclusao) 'Data da Compra'
		From gastos_tb g
		Inner Join produto_tb p
			On g.produto_id = p.produto_id
		Inner Join tp_produto_tb tp
			On p.tp_produto_id = tp.tp_produto_id
		Inner Join loja_tb l
			On g.loja_id = l.loja_id
	End
	Else If @tipo = 2
	Begin
		Select 
			p.nome 'Nome do Produto',
			tp.descricao 'Tipo do Produto',
			l.nome 'Local da Compra',
			g.qtd 'Quantidade',
			g.valor 'Valor Total',
			Convert(Date,g.dt_inclusao) 'Data da Compra'
		From gastos_tb g
		Inner Join produto_tb p
			On g.produto_id = p.produto_id
			And p.produto_id = @produto_id
		Inner Join tp_produto_tb tp
			On p.tp_produto_id = tp.tp_produto_id
		Inner Join loja_tb l
			On g.loja_id = l.loja_id
	End
	Else If @tipo = 3
	Begin
		Select 
			p.nome 'Nome do Produto',
			tp.descricao 'Tipo do Produto',
			l.nome 'Local da Compra',
			g.qtd 'Quantidade',
			g.valor 'Valor Total',
			Convert(Date,g.dt_inclusao) 'Data da Compra'
		From gastos_tb g
		Inner Join produto_tb p
			On g.produto_id = p.produto_id
		Inner Join tp_produto_tb tp
			On p.tp_produto_id = tp.tp_produto_id
			And tp.tp_produto_id = @tp_conta_id
		Inner Join loja_tb l
			On g.loja_id = l.loja_id
	End
	Else If @tipo = 4
	Begin
		Select 
			p.nome 'Nome do Produto',
			tp.descricao 'Tipo do Produto',
			l.nome 'Local da Compra',
			g.qtd 'Quantidade',
			g.valor 'Valor Total',
			Convert(Date,g.dt_inclusao) 'Data da Compra'
		From gastos_tb g
		Inner Join produto_tb p
			On g.produto_id = p.produto_id
		Inner Join tp_produto_tb tp
			On p.tp_produto_id = tp.tp_produto_id
		Inner Join loja_tb l
			On g.loja_id = l.loja_id
		Where Convert(Date,g.dt_inclusao) Between @dt_inicio And @dt_fim
	End

/******************************************************************/

End Try

Begin Catch

	If @@Rowcount > 0
		Rollback

	Select 
		@error            'Local do Erro',
		Error_procedure() 'Error_procedure',
		Error_line()      'Error_line',
		Error_number()    'Error_number',
		Error_message()   'Error_message'

End Catch


