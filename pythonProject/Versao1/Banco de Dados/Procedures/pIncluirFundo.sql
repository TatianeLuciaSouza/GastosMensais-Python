Create Or Alter Procedure pIncluirFundo(
	@emp       Varchar(30),
	@tipo      Varchar(20),
	@ticker    Varchar(10),
	@categoria Char(1))

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 16/04/2024
Descrição: Procedure para incluir novo fundo.
******************************************************************/

Set Nocount On

--Declarar Variável
Declare 
	@fundo_id Int,
	@error    Varchar(100)

/******************************************************************/

Begin Try

	Set @error = 'Erro ao tentar inserir na tabela fundos_tb'
	Insert Into fundos_tb (
		nm_empresa,
		tipo_fundo,
		ticker,
		categoria,
		dt_inclusao) 
	Select
		@emp,
		@tipo,
		@ticker,
		@categoria,
		Getdate()

	Select @fundo_id = Max(fundo_id) From fundos_tb

	If @categoria = 'F'
	Begin
		Set @error = 'Erro ao tentar inserir na tabela fiis_tb'
		Insert into fiis_tb (
			fundo_id,
			nro_cota,
			vl_investido,
			dt_inclusao)
		Select
			@fundo_id,
			0,
			0,
			Getdate()
	End

	If @categoria = 'A'
	Begin
		Set @error = 'Erro ao tentar inserir na tabela acoes_tb'
		Insert into acoes_tb (
			fundo_id,
			nro_cota,
			vl_investido,
			dt_inclusao)
		Select
			@fundo_id,
			0,
			0,
			Getdate()
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