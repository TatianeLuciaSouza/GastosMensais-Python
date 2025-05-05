Create Or ALter Procedure pRelatorios (
	@tipo       Int,
	@produto    Int      Null,
	@tp_produto Int      Null,
	@tp_fundo   Int      Null,
	@ativo      Int      Null,
	@ticker     Int      Null,
	@dt_inicio  Datetime Null,
	@dt_fim     Datetime Null)

As

/*******************************************************************
Autor....: Tatiane Lucia
Data.....: 18/06/2024
Descrição: Procedure que gera os dados para emissão dos relatórios.
*******************************************************************/

Set Nocount On


--Declaração de Variáveis
Declare 
	@login_id Int,
	@error    Varchar(100)

Select @login_id = login_id From usuario_tb Where ativo = 1

/******************************************************************/

Begin Try

	Set @error = 'Erro ao tentar consultar os dados'

	If @tipo = 1 --Gastos Mensais
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
		Where g.login_id = @login_id
		      And p.produto_id = @produto 
		      And ((tp.tp_produto_id = @tp_produto)
			  And (Convert(Date,g.dt_inclusao) Between @dt_inicio And @dt_fim))
	End
	Else If @tipo = 2 --Contas do Mês
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
		Where c.login_id = @login_id
		      And tp.tp_produto_id = @tp_produto
			  And ((@ativo = 1) Or (@ativo = 0))
			  And (Convert(Date,c.dt_inclusao) Between @dt_inicio And @dt_fim)	    
	End
	Else If @tipo = 3 --Metas
	Begin
		Select 
			m.nome 'Nome do Objetivo',
			tp.descricao 'Tipo do Objetivo',
			m.vl_total 'Valor da Meta',
			m.vl_atual	'Valor Autal'
		From meta_tb m
		Inner Join tp_produto_tb tp
			On m.tp_meta_id = tp.tp_produto_id
		Where m.login_id = @login_id
		      And tp.tp_produto_id = @tp_produto
			  And ((@ativo = 1) Or (@ativo = 0))
			  And (Convert(Date,m.dt_inicio) Between @dt_inicio And @dt_fim)
	End
	Else If @tipo = 2 --Aportes
	Begin
		If @ativo = 1
		Begin
			If @tp_fundo In(1,2)
			Begin
				Select 
					nm_empresa 'Nome Empresa',
					tipo_fundo 'Tipo do Fundo',
					ticker,
					Case When categoria = 'F' Then 'FIIS'
						 When categoria = 'A' Then 'Ação'
					End Fundo,
					a.qtd_cota 'Cotas',
					a.vl_cota 'Valor da Cota',
					a.vl_total 'Valor total Investido'
				From fundos_tb f
				Inner Join aportes_tb a
					On f.fundo_id = a.fundo_id
				Where f.login_id = @login_id
				      And f.categoria = Case When @tp_fundo = 1 Then 'F'
										     When @tp_fundo = 2 Then 'A' End
					  And ((f.ticker = @ticker)
					  And (Convert(Date,a.dt_inclusao) Between @dt_inicio And @dt_fim))
			End
			Else If @tp_fundo In(3)
			Begin
				Select 
					nm_empresa 'Nome Empresa',
					tipo_fundo 'Tipo do Fundo',
					ticker,
					Case When categoria = 'F' Then 'FIIS'
						 When categoria = 'A' Then 'Ação'
					End Fundo,
					a.qtd_cota 'Cotas',
					a.vl_cota 'Valor da Cota',
					a.vl_total 'Valor total Investido'
				From fundos_tb f
				Inner Join aportes_tb a
					On f.fundo_id = a.fundo_id
				Where f.login_id = @login_id
				      And f.ticker = @ticker
				      Or (Convert(Date,a.dt_inclusao) Between @dt_inicio And @dt_fim)
			End
		End
		Else If @ativo = 0
		Begin 
			If @tp_fundo In(1,2)
			Begin
				Select 
					f.nm_empresa 'Nome Empresa',
					f.tipo_fundo 'Tipo do Fundo',
					f.ticker,
					Case When f.categoria = 'F' Then 'FIIS'
						 When f.categoria = 'A' Then 'Ação'
					Else 'Categoria Inválida' End Categoria,
					vf.nro_cota 'Cotas Vendidas',
					vf.vl_cota 'Valor da Cota',
					vf.vl_total 'Valor Total',
					vf.dt_venda 'Data da Venda'
				From fundos_tb f
				Inner Join venda_fundo_tb vf
					On f.fundo_id = vf.fundo_id
				Where f.login_id = @login_id
				      And f.categoria = Case When @tp_fundo = 1 Then 'F'
										     When @tp_fundo = 2 Then 'A' End
					  And ((f.ticker = @ticker)
					  And (Convert(Date,vf.dt_venda) Between @dt_inicio And @dt_fim))
			End
			Else If @tp_fundo In(3)
			Begin
				Select 
					f.nm_empresa 'Nome Empresa',
					f.tipo_fundo 'Tipo do Fundo',
					f.ticker,
					Case When f.categoria = 'F' Then 'FIIS'
						 When f.categoria = 'A' Then 'Ação'
					Else 'Categoria Inválida' End Categoria,
					vf.nro_cota 'Cotas Vendidas',
					vf.vl_cota 'Valor da Cota',
					vf.vl_total 'Valor Total',
					vf.dt_venda 'Data da Venda'
				From fundos_tb f
				Inner Join venda_fundo_tb vf
					On f.fundo_id = vf.fundo_id
				Where f.login_id = @login_id
				      And f.ticker = @ticker
				      Or Convert(Date,vf.dt_venda) Between @dt_inicio And @dt_fim
			End
		End
	End
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
