Create Or Alter Procedure pAlterarAporte (
	@login     Int,
	@idTabela  Int,
	@qtdCota   Int,
	@vlCota    Numeric(10,2),
	@vlRend    Numeric(10,2),
	@alteracao Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 30/01/2025
Descrição: Alterar o valor da meta
******************************************************************/

--Variaveis
Declare 
	@vlTotal       Numeric(10,2),
	@vlCotaAntigo  Numeric(10,2),
	@vlInvestido   Numeric(10,2),
	@vlTotalAntigo Numeric(10,2),
	@vlRendiemnto  Numeric(10,2),
	@vlrendAntigo  Numeric(10,2),
	@nroCotaAntigo Int,
	@qtdCotaAntigo Int,
	@nroCota       Int

Select 
	@vlTotal       = i.vl_investido,
	@vlRendiemnto  = i.vl_rendimento,
	@nroCotaAntigo = i.nro_cota,
	@vlTotalAntigo = a.vl_total,
	@vlCotaAntigo  = a.vl_cota,
	@nroCota       = a.qtd_cota,
	@vlrendAntigo  = a.vl_rendimento
From aportes_tb a With (Nolock)
Inner Join investimentos_tb i With (Nolock)
	On i.investimento_id = a.investimento_id
	And i.login_id = @login
Where a.aporte_id = @idTabela

/****************************************************************/

Set Nocount On

Begin Try
	Begin Tran
		If @alteracao = 5
		Begin
			Set @vlInvestido =  @vlTotal - @vlTotalAntigo
			Set @qtdCotaAntigo = @nroCotaAntigo - @nroCota
			
			Update A
			Set 
				qtd_cota = @qtdCota,
				vl_total = @vlCotaAntigo * @qtdCota,
				dt_altercao = Getdate()
			From aportes_tb A 
			Inner Join investimentos_tb i With (Nolock)
				On i.investimento_id = a.investimento_id
				And i.login_id = @login
			Where a.aporte_id = @idTabela

			Update i
			Set 
				nro_cota = @qtdCotaAntigo,
				vl_investido = @vlInvestido + (@vlCotaAntigo * @qtdCota),
				dt_altercao = Getdate()
			From aportes_tb A With (Nolock)
			Inner Join investimentos_tb i 
				On i.investimento_id = a.investimento_id
				And i.login_id = @login
			Where a.aporte_id = @idTabela
		End

		If @alteracao = 6
		Begin
			Set @vlInvestido =  @vlTotal - @vlTotalAntigo
			
			Update A
			Set 
				vl_cota = @vlCota,
				vl_total = @vlCota * @nroCota,
				dt_altercao = Getdate()
			From aportes_tb A 
			Inner Join investimentos_tb i With (Nolock)
				On i.investimento_id = a.investimento_id
				And i.login_id = @login
			Where a.aporte_id = @idTabela

			Update i
			Set 
				vl_investido = @vlInvestido + (@vlCota * @nroCota),
				dt_altercao = Getdate()
			From aportes_tb A With (Nolock)
			Inner Join investimentos_tb i 
				On i.investimento_id = a.investimento_id
				And i.login_id = @login
			Where a.aporte_id = @idTabela
		End

		If @alteracao = 8
		Begin
			Set @vlRendiemnto =  @vlRendiemnto - @vlrendAntigo
			
			Update A
			Set 
				vl_rendimento = @vlRend,
				dt_altercao = Getdate()
			From aportes_tb A 
			Inner Join investimentos_tb i With (Nolock)
				On i.investimento_id = a.investimento_id
				And i.login_id = @login
			Where a.aporte_id = @idTabela

			Update i
			Set 
				vl_rendimento = @vlRendiemnto + @vlRend,
				dt_altercao = Getdate()
			From aportes_tb A With (Nolock)
			Inner Join investimentos_tb i 
				On i.investimento_id = a.investimento_id
				And i.login_id = @login
			Where a.aporte_id = @idTabela
		End

		If @alteracao = 9
			Update i
			Set 
				status = 'V',
				dt_altercao = Getdate()
			From aportes_tb A With (Nolock)
			Inner Join investimentos_tb i 
				On i.investimento_id = a.investimento_id
				And i.login_id = @login
			Where a.aporte_id = @idTabela
	Commit

/****************************************************************/

End Try

Begin Catch

	Select
		Error_procedure() 'Error_procedure',
		Error_line()      'Error_line',
		Error_number()    'Error_number',
		Error_message()   'Error_message'

End Catch