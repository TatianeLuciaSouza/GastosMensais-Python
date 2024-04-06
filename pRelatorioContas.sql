Create Or ALter Procedure pRelatorioContas (
	@tipo      Int,
	@dt_inicio Datetime,
	@dt_fim    Datetime,
	@tp_conta  Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 05/04/2024
Descrição: Procedure para emitir relatório de contas.
******************************************************************/

Set Nocount On

Begin Try
	If @tipo = 1
	Begin
		Select 
			prod.nome 'Nome do Produto',
			tp.descricao 'Tipo da Conta',
			p.vl_parcela 'Valor da Parcela',
			p.parcela 'Nro. Parcela Atual',
			Convert(Date,p.dt_parcela) 'Data Parcela Atual',
			c.parcela 'Total de Parcelas',
			c.valor	'Valor Total'
		From contas_tb c
		Inner Join produto_tb prod
			On c.produto_id = prod.produto_id
		Inner Join tp_produto_tb tp
			On prod.tp_produto_id = tp.tp_produto_id
		Inner Join parcelas_tb p
			On c.conta_id = p.conta_id
			And Concat(Year(p.dt_parcela),Month(p.dt_parcela)) = Concat(Year(Getdate()),Month(Getdate()))
	End
	Else If @tipo = 2
	Begin
		Select 
			prod.nome 'Nome do Produto',
			tp.descricao 'Tipo da Conta',
			c.parcela 'Total de Parcelas',
			c.valor	'Valor Total'
		From contas_tb c
		Inner Join produto_tb prod
			On c.produto_id = prod.produto_id
		Inner Join tp_produto_tb tp
			On prod.tp_produto_id = tp.tp_produto_id
	End
	Else If @tipo = 3
	Begin
		Select 
			prod.nome 'Nome do Produto',
			tp.descricao 'Tipo da Conta',
			p.vl_parcela 'Valor da Parcela',
			p.parcela 'Nro. Parcela Atual',
			Convert(Date,p.dt_parcela) 'Data Parcela Atual',
			c.parcela 'Total de Parcelas',
			c.valor	'Valor Total'
		From contas_tb c
		Inner Join produto_tb prod
			On c.produto_id = prod.produto_id
			And prod.tp_produto_id = @tp_conta
		Inner Join tp_produto_tb tp
			On prod.tp_produto_id = tp.tp_produto_id
		Inner Join parcelas_tb p
			On c.conta_id = p.conta_id
			And Concat(Year(p.dt_parcela),Month(p.dt_parcela)) = Concat(Year(Getdate()),Month(Getdate()))
	End
	Else If @tipo = 4
	Begin
		Select 
			prod.nome 'Nome do Produto',
			tp.descricao 'Tipo da Conta',
			p.vl_parcela 'Valor da Parcela',
			p.parcela 'Nro. Parcela Atual',
			Convert(Date,p.dt_parcela) 'Data Parcela Atual',
			c.parcela 'Total de Parcelas',
			c.valor	'Valor Total'
		From contas_tb c
		Inner Join produto_tb prod
			On c.produto_id = prod.produto_id
		Inner Join tp_produto_tb tp
			On prod.tp_produto_id = tp.tp_produto_id
		Inner Join parcelas_tb p
			On c.conta_id = p.conta_id
			And Convert(Date,p.dt_parcela) Between @dt_inicio And @dt_fim
	End

/******************************************************************/

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

