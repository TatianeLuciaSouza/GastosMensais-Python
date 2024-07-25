Create Or Alter Procedure pIncluirAporte(
	@ticker		Varchar(10),
	@qtdCota    Int,
	@valor      Numeric(10,2),
	@rendimento Numeric(10,2))

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 16/04/2024
Descrição: Procedure para incluir novo aporto no mês.
******************************************************************/

Set Nocount On

--Declaração de Variáveis
Declare 
	@fundo_id      Int,
	@anoMesPassado Varchar(6),
	@tipo		   Char(1),
	@error         Varchar(100)

Set @error = 'Erro ao pegar os IDs'

Select @fundo_id = fundo_id, @tipo = categoria  From fundos_tb Where ticker = @ticker
Set @anoMesPassado = Concat(Month(Dateadd(Month, -1, Getdate())), Year(Getdate()))

/******************************************************************/

Begin Try

	If @rendimento > 0
	Begin 
		Set @error = 'Erro ao tentar atualizar a tabela aportes_tb'
		Update A
		Set vl_rendimento = @rendimento
		From aportes_tb A
		Where fundo_id = @fundo_id
		      And mesAno = @anoMesPassado
	End

	Set @error = 'Erro ao tentar inserir na tabela aportes_tb'
	Insert Into aportes_tb (
		fundo_id,
		qtd_cota,
		vl_cota,
		vl_total,
		mesAno,
		dt_inclusao) 
	Select
		@fundo_id,
		@qtdCota,
		@valor,
	   (@qtdCota * @valor),
	   @anoMesPassado,
	   Getdate()

	If @tipo = 'F'
	Begin
		Set @error = 'Erro ao tentar atualizar a tabela fiis_tb'
		Update A
		Set 
			nro_cota = nro_cota + @qtdCota,
			vl_investido = (@qtdCota * @valor),
			dt_altercao = Getdate()
		From fiis_tb A
		Where fundo_id = @fundo_id
	End

	If @tipo = 'A'
	Begin
		Set @error = 'Erro ao tentar atualizar a tabela acoes_tb'
		Update A
		Set 
			nro_cota = nro_cota + @qtdCota,
			vl_investido = (@qtdCota * @valor),
			dt_altercao = Getdate()
		From acoes_tb A
		Where fundo_id = @fundo_id
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