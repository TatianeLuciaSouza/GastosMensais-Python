Create Or Alter Procedure pAlterarConta (
	@login     Int,
	@idTabela  Int,
	@parcela   Int,
	@valor     Numeric(6,2),
	@descricao Varchar(100),
	@alteracao Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 22/01/2025
Descrição: Alterar o valor da conta mensal
******************************************************************/

--Váriaveis
Declare 
	@parcelaMAX Int,
	@vlConta	Numeric(6,2),
	@vlParcela	Numeric(6,2),
	@difParcela Int,
	@mesAno     Int,
	@mes        Int,
	@ano        Int,
	@dtParcela  Datetime

/*****************************************************************/

Set Nocount On

Begin Try
	Begin Tran
		If @alteracao = 2
		Begin
			Select @parcelaMAX = parcela, @vlConta = valor From contas_tb 
			Where login_id = @login 
				  And conta_id = @idTabela

			If @parcela > @parcelaMAX
			Begin
				Set @difParcela = (Abs(@parcela - @parcelaMAX))
				Select 
					@mesAno = mesAno, 
					@dtParcela = dt_parcela 
				From parcelas_tb 
				Where conta_id = @idTabela 
				      And parcela = @parcelaMAX
				
				Select @vlParcela = @vlConta / (@parcelaMAX + @difParcela)

				Update A
				Set 
					parcela = @parcela,
					dt_alteracao = Getdate()
				From contas_tb A
				Where login_id = @login
					  And conta_id = @idTabela
			
				Update A
				Set vl_parcela = @vlParcela
				From parcelas_tb A
				Where conta_id = @idTabela

				Select @mes = Case When Len(@mesAno) = 5
							Then Concat('0', Substring(Convert(Varchar(6),@mesAno), 0, 2))
						Else Substring(Convert(Varchar(6),@mesAno), 1, 2) End
				Select @ano = Case When Len(@mesAno) = 5
							Then Substring(Convert(Varchar(6),@mesAno), 2, 4)
						Else Substring(Convert(Varchar(6),@mesAno), 3, 4) End
					
				While @difParcela > 0
				Begin
					Set @mes += 1
					Set @ano = @ano + (@mes / 12)
					Set @mes = (@mes - 1) % 12 + 1
					Set @dtParcela = Dateadd(Month, 1, @dtParcela)
					Set @parcelaMAX += 1

					Insert Into parcelas_tb (
						conta_id,
						vl_parcela,
						parcela,
						dt_parcela,
						mesAno)
					Select top 1
						@idTabela,
						@vlParcela,
						@parcelaMAX,
						@dtParcela,
						Concat(Format(@mes, '00'), @ano)
					From parcelas_tb 
					Where conta_id = @idTabela

					Set @difParcela -= 1
				End

			End
			Else
			Begin
				Set @difParcela = (Abs(@parcelaMAX - @parcela))
				Select @vlParcela = @vlConta / (@parcelaMAX - @difParcela)

				Update A
				Set 
					parcela = @parcela,
					dt_alteracao = Getdate()
				From contas_tb A
				Where login_id = @login
					  And conta_id = @idTabela
			
				Update A
				Set vl_parcela = @vlParcela
				From parcelas_tb A
				Where conta_id = @idTabela

				Set @difParcela = (Abs(@parcelaMAX - @parcela))
				Delete From parcelas_tb Where conta_id = @idTabela And parcela >= @difParcela
			End
		End
	
		If @alteracao = 3
		Begin
			Update A
			Set 
				descricao = @descricao,
				dt_alteracao = Getdate()
			From contas_tb A
			Where login_id = @login
				  And conta_id = @idTabela
		End

		If @alteracao = 4
		Begin
			Update A
			Set 
				valor = @valor,
				dt_alteracao = Getdate()
			From contas_tb A
			Where login_id = @login
				  And conta_id = @idTabela

			Set @vlParcela = @valor / (Select parcela From contas_tb Where login_id = @login And conta_id = @idTabela)

			Update A
			Set vl_parcela = @vlParcela
			From parcelas_tb A
			Where conta_id = @idTabela
		End

	Commit

/*******************************************************************************************/

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