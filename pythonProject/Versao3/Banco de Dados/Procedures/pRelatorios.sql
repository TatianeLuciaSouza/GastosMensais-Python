Create Or ALter Procedure pRelatorios (
	@login      Int,
	@produto    Int         Null,
	@tpProduto  Int         Null,
	@meta       Int         Null,
	@loja       Int         Null,
	@tpLoja     Varchar(10) Null,
	@status     Varchar(10) Null,
	@ticker     Int			Null,
	@dtInicio   Date	    Null,
	@dtFim      Date	    Null,
	@tipo       Int)

As

/*******************************************************************
Autor....: Tatiane Lucia
Data.....: 13/03/2025
Descrição: Gerar relatórios:
			1 - Gastos Mensais
			2 - Contas do Mês
			3 - Metas
			4 - Aportes
			5 - Gastos do Décimo13
			6 - Décimo Terceiro
Exec pRelatorios 3, null, 10, Null, Null, Null, Null, Null, '20241206', '20250101',1
*******************************************************************/

Set Nocount On

Begin Try

	If @tipo = 1 --Gastos Mensais
	Begin
		Select
			p.nome 'Produto',
			tp.descricao 'Tipo do Produto',
			g.qtd 'Quantidade de Produto',
			g.valor 'Valor da Unidade',
			g.vlTotal 'Valor Total',
			l.nome 'Loja',
			Case When g.tpCompra = 'Online' Then 'Compra Online' Else 'Compra em Loja Física' End As 'Tipo de Compra',
			Convert(Date,g.dt_inclusao) 'Data da Compra'
		From gastos_tb g With (Nolock)
		Inner Join produto_tb p With (Nolock)
			On g.produto_id = p.produto_id
		Inner Join loja_tb l With (Nolock)
			On g.loja_id = l.loja_id
		Inner Join tp_produto_tb tp With (Nolock)
			On p.tp_produto_id = tp.tp_produto_id
		Where g.login_id = @login
			  And (p.produto_id = @produto Or @produto Is Null)
			  And (tp.tp_produto_id = @tpProduto Or @tpProduto Is Null)
			  And (l.loja_id = @loja Or @loja Is Null)
			  And (g.tpCompra= @tpLoja Or @tpLoja Is Null)
			  And Convert(Date,g.dt_inclusao) Between @dtInicio And @dtFim
	End
	Else If @tipo = 2 --Contas do Mês
	Begin
		If @status = 'Finalizado'
			Select
				p.nome 'Conta',
				tp.descricao 'Tipo da Conta',
				c.parcela 'Parcelas',
				(c.valor / c.parcela) 'Valor da Parcela',
				c.valor 'Valor Total',
				c.descricao 'Descriçãod a Conta',
				Convert(Date,c.dt_inclusao) 'Data da Conta'
			From contas_tb c With (Nolock)
			Inner Join produto_tb p With (Nolock)
				On c.produto_id = p.produto_id
				And c.tp_conta_id = p.tp_produto_id
			Inner Join tp_produto_tb tp With (Nolock)
				On p.tp_produto_id = tp.tp_produto_id
			Where c.login_id = @login
				  And (p.produto_id = @produto Or @produto Is Null)
				  And (tp.tp_produto_id = @tpProduto Or @tpProduto Is Null)
				  And c.situacao = 'Cancelado'
				  And Convert(Date,c.dt_inclusao) Between @dtInicio And @dtFim

		Else If @status = 'Ativo'
			Select
				p.nome 'Conta',
				tp.descricao 'Tipo da Conta',
				c.parcela 'Parcelas',
				(c.valor / c.parcela) 'Valor da Parcela',
				c.valor 'Valor Total',
				c.descricao 'Descriçãod a Conta',
				Convert(Date,c.dt_inclusao) 'Data da Conta'
			From contas_tb c With (Nolock)
			Inner Join produto_tb p With (Nolock)
				On c.produto_id = p.produto_id
				And c.tp_conta_id = p.tp_produto_id
			Inner Join tp_produto_tb tp With (Nolock)
				On p.tp_produto_id = tp.tp_produto_id
			Where c.login_id = @login
				  And (p.produto_id = @produto Or @produto Is Null)
				  And (tp.tp_produto_id = @tpProduto Or @tpProduto Is Null)
				  And c.situacao <> 'Cancelado'
				  And Convert(Date,c.dt_inclusao) Between @dtInicio And @dtFim

		Else
			Select
				p.nome 'Conta',
				tp.descricao 'Tipo da Conta',
				c.parcela 'Parcelas',
				(c.valor / c.parcela) 'Valor da Parcela',
				c.valor 'Valor Total',
				c.descricao 'Descriçãod a Conta',
				Case When c.situacao = 'Cancelada' Then c.situacao Else 'Ativa' End As 'Situação',
				Convert(Date,c.dt_inclusao) 'Data da Conta'
			From contas_tb c With (Nolock)
			Inner Join produto_tb p With (Nolock)
				On c.produto_id = p.produto_id
				And c.tp_conta_id = p.tp_produto_id
			Inner Join tp_produto_tb tp With (Nolock)
				On p.tp_produto_id = tp.tp_produto_id
			Where c.login_id = @login
				  And (p.produto_id = @produto Or @produto Is Null)
				  And (tp.tp_produto_id = @tpProduto Or @tpProduto Is Null)
				  And Convert(Date,c.dt_inclusao) Between @dtInicio And @dtFim	    
	End
	Else If @tipo = 3 --Metas
	Begin
		If @status = 'Finalizado'	
			Select
				nome 'Nome da Meta',
				vl_Mensal 'Aporte Mensal',
				vl_atual 'Valor Juntado',
				vl_final 'Valor Objetivo',
				Case When movimento = 1 Then 'Manual' 
					 When movimento = 2 Then 'Automático'
				End As 'Forma de Aporte',
				Case When status = 'E' Then 'Encerrado' Else 'Ativa' End As 'Status',
				Convert(Date,dt_inicio) 'Data da Meta'
			From meta_tb With (Nolock)
			Where login_id = @login
					And (nome = @meta Or @meta Is Null)
					And status = 'E'
					And Convert(Date,dt_inicio) Between @dtInicio And @dtFim

		Else If @status = 'Ativo'
			Select
				nome 'Nome da Meta',
				vl_Mensal 'Aporte Mensal',
				vl_atual 'Valor Juntado',
				vl_final 'Valor Objetivo',
				Case When movimento = 1 Then 'Manual' 
					 When movimento = 2 Then 'Automático'
				End As 'Forma de Aporte',
				Case When status = 'E' Then 'Encerrado' Else 'Ativa' End As 'Status',
				Convert(Date,dt_inicio) 'Data da Meta'
			From meta_tb With (Nolock)
			Where login_id = @login
					And (nome = @meta Or @meta Is Null)
					And status = 'A'
					And Convert(Date,dt_inicio) Between @dtInicio And @dtFim

		Else
			Select
				nome 'Nome da Meta',
				vl_Mensal 'Aporte Mensal',
				vl_atual 'Valor Juntado',
				vl_final 'Valor Objetivo',
				Case When movimento = 1 Then 'Manual' 
					 When movimento = 2 Then 'Automático'
				End As 'Forma de Aporte',
				Case When status = 'E' Then 'Encerrado' Else 'Ativa' End As 'Status',
				Convert(Date,dt_inicio) 'Data da Meta'
			From meta_tb With (Nolock)
			Where login_id = @login
					And (nome = @meta Or @meta Is Null)
					And Convert(Date,dt_inicio) Between @dtInicio And @dtFim
	End
	Else If @tipo = 4 --Aportes
	Begin
		If @status = 'Finalizado'
			Select
				a.qtd_cota 'Cotas',
				a.vl_cota 'Valor da Cota',
				a.vl_total 'Valor Total',
				a.vl_rendimento 'Rendimento',
				a.mesAno,
				Convert(Date,a.dt_inclusao) 'Data do Aporte'
			From investimentos_tb i With (Nolock)
			Inner Join fundos_tb f With (Nolock)
				On i.fundo_id = f.fundo_id
			Inner Join aportes_tb a With (Nolock)
				On i.investimento_id = a.investimento_id
			Where f.ticker = @ticker
				  --And f.categoria = @tpFundo
				  And i.status = 'V'
				  And Convert(Date,a.dt_inclusao) Between @dtInicio And @dtFim

		Else If @status = 'Ativo'
				Select
				a.qtd_cota 'Cotas',
				a.vl_cota 'Valor da Cota',
				a.vl_total 'Valor Total',
				a.vl_rendimento 'Rendimento',
				a.mesAno,
				Convert(Date,a.dt_inclusao) 'Data do Aporte'
			From investimentos_tb i With (Nolock)
			Inner Join fundos_tb f With (Nolock)
				On i.fundo_id = f.fundo_id
			Inner Join aportes_tb a With (Nolock)
				On i.investimento_id = a.investimento_id
			Where f.ticker = @ticker
				  --And f.categoria = @tpFundo
				  And i.status <> 'V'
				  And Convert(Date,a.dt_inclusao) Between @dtInicio And @dtFim

		Else
			Select
				a.qtd_cota 'Cotas',
				a.vl_cota 'Valor da Cota',
				a.vl_total 'Valor Total',
				a.vl_rendimento 'Rendimento',
				a.mesAno,
				Case When i.status = 'V' Then 'Ventido' Else 'Ativa' End As 'Status',
				Convert(Date,a.dt_inclusao) 'Data do Aporte'
			From investimentos_tb i With (Nolock)
			Inner Join fundos_tb f With (Nolock)
				On i.fundo_id = f.fundo_id
			Inner Join aportes_tb a With (Nolock)
				On i.investimento_id = a.investimento_id
			Where f.ticker = @ticker
				  --And f.categoria = @tpFundo
				  And Convert(Date,a.dt_inclusao) Between @dtInicio And @dtFim
	End

	Else If @tipo = 5 --Gastos do Décimo13
	Begin
		Select
			p.nome 'Produto',
			tp.descricao 'Tipo do Produto',
			g.qtd 'Quantidade de Produto',
			g.valor 'Valor Total',
			l.nome 'Loja',
			Case When g.tpCompra = 'Online' Then 'Compra Online' Else 'Compra em Loja Física' End As 'Tipo de Compra',
			Convert(Date,g.dt_inclusao) 'Data da Compra'
		From gastos13_tb g With (Nolock)
		Inner Join decimo_terceiro_tb d With (Nolock)
			On g.decimo_id = d.decimo_id
		Inner Join produto_tb p With (Nolock)
			On g.produto_id = p.produto_id
		Inner Join loja_tb l With (Nolock)
			On g.loja_id = l.loja_id
		Inner Join tp_produto_tb tp With (Nolock)
			On p.tp_produto_id = tp.tp_produto_id
		Where d.login_id = @login
			  And (p.produto_id = @produto Or @produto Is Null)
			  And (tp.tp_produto_id = @tpProduto Or @tpProduto Is Null)
			  And (l.loja_id = @loja Or @loja Is Null)
			  And (g.tpCompra= @tpLoja Or @tpLoja Is Null)
			  And Convert(Date,g.dt_inclusao) Between @dtInicio And @dtFim
	End

	Else If @tipo = 6 --Décimo terceiro
	Begin
		Select
			vl_parcela1 'Primeira Parcela',
			vl_parcela2 'Segunda Parcela',
			vl_total 'Valor Total',
			vl_sobra 'Valor da Sobra',
			ano 'Ano'
		From decimo_terceiro_tb
		Where login_id = @login
	End
/******************************************************************/

End Try

Begin Catch

	Select
		Error_procedure() 'Error_procedure',
		Error_line()      'Error_line',
		Error_number()    'Error_number',
		Error_message()   'Error_message'

End Catch
