Create Or ALter Trigger inclusaoParcelas On contas_tb For Insert

As
	Declare 
		@mes        Int = 0,
		@parcelas   Int,
		@conta_id   Int,
		@valor      Numeric(6,2),
		@vl_parcela Numeric(6,2),
		@mesAno     Int,
		@ano        Int

	Select Top 1 
		@conta_id = conta_id, 
		@valor = valor, 
		@parcelas = parcela 
	From contas_tb 
	Order By conta_id Desc

	Set @vl_parcela = @valor/@parcelas

	While @parcelas > 0
	Begin
		Set @mes += 1

		 -- Calcular o ano de acordo com o número da parcela
        Set @ano = Year(Getdate()) + ((@mes + Month(Getdate()) - 1) / 12)
        Set @mesAno = (@mes - 1) % 12 + 1

		Insert Into parcelas_tb (
			conta_id,
			vl_parcela,
			parcela,
			dt_parcela,
			situacao,
			mesAno)
		Select
			@conta_id,
			@vl_parcela,
			@mes,
			Dateadd(Month, @mes,Getdate()),
			'Pendente',
			Concat(Format(@mesAno, '00'), @ano)

		Set @parcelas -= 1
	End
