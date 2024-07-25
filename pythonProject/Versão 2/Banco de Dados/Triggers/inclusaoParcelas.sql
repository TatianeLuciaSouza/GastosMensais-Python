Create Or ALter Trigger inclusaoParcelas
On contas_tb For Insert
As
	Declare 
		@mes        Int = 0,
		@parcelas   Int,
		@conta_id   Int,
		@valor      Numeric(6,2),
		@vl_parcela Numeric(6,2)

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

		Insert Into parcelas_tb (
			conta_id,
			vl_parcela,
			parcela,
			dt_parcela)
		Select
			@conta_id,
			@vl_parcela,
			@mes,
			Dateadd(Month, @mes,Getdate())

		Set @parcelas -= 1
	End

	If @@Rowcount > 0
  	   Rollback Transaction
