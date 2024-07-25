Create Or Alter Procedure pRelatorioaFundos(
	@tipo     Char(1),
	@opcao    Int,
	@fundo_id Varchar(10) = Null,
	@dt_incio Datetime = Null,
	@dt_fim   Datetime = Null)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 25/04/2024
Descrição: Procedure para extrair relatório dos fundos.
******************************************************************/


--Declarar Variáveis
Declare 
	@inicio Varchar(6),
	@fim    Varchar(6),
	@error  Varchar(100)

--Setar Variáveis
If @dt_incio Is Not Null
Begin
	Set @inicio = Concat(Month(@dt_incio), Year(@dt_incio))
	Set @fim = Concat(Month(@dt_fim), Year(@dt_fim))
End

/******************************************************************/

Set Nocount On

Begin Try
	
	Set @error = 'Erro ao tentar consultar os dados'

	If @tipo In('F', 'A')
	Begin
		If @opcao = 1
			 Select 
				nm_empresa 'Nome Empresa',
				tipo_fundo 'Tipo do Fundo',
				ticker,
				Case When categoria = 'F' Then 'FIIS'
					 When categoria = 'A' Then 'Ação'
				Else 'Categoria Inválida' End Categoria
			From fundos_tb
			Where categoria = @tipo

		If @opcao = 2
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
			Where f.categoria = @tipo

		If @opcao = 3
			 Select 
				nm_empresa 'Nome Empresa',
				tipo_fundo 'Tipo do Fundo',
				ticker,
				Case When categoria = 'F' Then 'FIIS'
					 When categoria = 'A' Then 'Ação'
				Else 'Categoria Inválida' End Categoria,
				a.qtd_cota 'Cotas',
				a.vl_cota 'Valor da Cota',
				a.vl_total 'Valor total'
			From fundos_tb f
			Inner Join aportes_tb a
				On f.fundo_id = a.fundo_id
			Where f.categoria = @tipo

		If @opcao = 4
			Select 
				nm_empresa 'Nome Empresa',
				tipo_fundo 'Tipo do Fundo',
				ticker,
				Case When categoria = 'F' Then 'FIIS'
					 When categoria = 'A' Then 'Ação'
				Else 'Categoria Inválida' End Categoria,
				a.vl_rendimento 'Rendimento',
				a.mesAno 'Mês e Ano'
			From fundos_tb f
			Inner Join aportes_tb a
				On f.fundo_id = a.fundo_id
				And a.mesAno Between @inicio ANd @fim
			Where f.categoria = @tipo

		If @opcao = 5
			Select 
				nm_empresa 'Nome Empresa',
				tipo_fundo 'Tipo do Fundo',
				ticker,
				Case When categoria = 'F' Then 'FIIS'
					 When categoria = 'A' Then 'Ação'
				Else 'Categoria Inválida' End Categoria,
				a.vl_rendimento 'Rendimento',
				a.mesAno 'Mês e Ano'
			From fundos_tb f
			Inner Join aportes_tb a
				On f.fundo_id = a.fundo_id
				And a.fundo_id = @fundo_id
				And a.mesAno Between @inicio ANd @fim 
			Where f.categoria = @tipo

		If @opcao = 6
			 Select 
				nm_empresa 'Nome Empresa',
				tipo_fundo 'Tipo do Fundo',
				ticker,
				Case When categoria = 'F' Then 'FIIS'
					 When categoria = 'A' Then 'Ação'
				Else 'Categoria Inválida' End Categoria,
				a.qtd_cota 'Cotas',
				a.vl_cota 'Valor da Cota',
				a.vl_total 'Valor total'
			From fundos_tb f
			Inner Join aportes_tb a
				On f.fundo_id = a.fundo_id
				And a.mesAno Between @inicio ANd @fim 
			Where f.categoria = @tipo

		If @opcao = 7
			 Select 
				nm_empresa 'Nome Empresa',
				tipo_fundo 'Tipo do Fundo',
				ticker,
				Case When categoria = 'F' Then 'FIIS'
					 When categoria = 'A' Then 'Ação'
				Else 'Categoria Inválida' End Categoria,
				a.qtd_cota 'Cotas',
				a.vl_cota 'Valor da Cota',
				a.vl_total 'Valor total'
			From fundos_tb f
			Inner Join aportes_tb a
				On f.fundo_id = a.fundo_id
				And a.fundo_id = @fundo_id
			Where f.categoria = @tipo

		If @opcao = 8
			 Select 
				nm_empresa 'Nome Empresa',
				tipo_fundo 'Tipo do Fundo',
				ticker,
				Case When categoria = 'F' Then 'FIIS'
					 When categoria = 'A' Then 'Ação'
				Else 'Categoria Inválida' End Categoria,
				a.qtd_cota 'Cotas',
				a.vl_cota 'Valor da Cota',
				a.vl_total 'Valor total'
			From fundos_tb f
			Inner Join aportes_tb a
				On f.fundo_id = a.fundo_id
				And a.mesAno Between @inicio ANd @fim 
				And a.fundo_id = @fundo_id
			Where f.categoria = @tipo
	End
	Else If @tipo = '0'
	Begin
		If @opcao = 1
			 Select 
				nm_empresa 'Nome Empresa',
				tipo_fundo 'Tipo do Fundo',
				ticker,
				Case When categoria = 'F' Then 'FIIS'
					 When categoria = 'A' Then 'Ação'
				Else 'Categoria Inválida' End Categoria
			From fundos_tb

		If @opcao = 2
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

		If @opcao = 3
			 Select 
				nm_empresa 'Nome Empresa',
				tipo_fundo 'Tipo do Fundo',
				ticker,
				Case When categoria = 'F' Then 'FIIS'
					 When categoria = 'A' Then 'Ação'
				Else 'Categoria Inválida' End Categoria,
				a.qtd_cota 'Cotas',
				a.vl_cota 'Valor da Cota',
				a.vl_total 'Valor total'
			From fundos_tb f
			Inner Join aportes_tb a
				On f.fundo_id = a.fundo_id

		If @opcao = 4
			Select 
				nm_empresa 'Nome Empresa',
				tipo_fundo 'Tipo do Fundo',
				ticker,
				Case When categoria = 'F' Then 'FIIS'
					 When categoria = 'A' Then 'Ação'
				Else 'Categoria Inválida' End Categoria,
				a.vl_rendimento 'Rendimento',
				a.mesAno 'Mês e Ano'
			From fundos_tb f
			Inner Join aportes_tb a
				On f.fundo_id = a.fundo_id
				And a.mesAno Between @inicio ANd @fim

		If @opcao = 5
			Select 
				nm_empresa 'Nome Empresa',
				tipo_fundo 'Tipo do Fundo',
				ticker,
				Case When categoria = 'F' Then 'FIIS'
					 When categoria = 'A' Then 'Ação'
				Else 'Categoria Inválida' End Categoria,
				a.vl_rendimento 'Rendimento',
				a.mesAno 'Mês e Ano'
			From fundos_tb f
			Inner Join aportes_tb a
				On f.fundo_id = a.fundo_id
				And a.mesAno Between @inicio ANd @fim 
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