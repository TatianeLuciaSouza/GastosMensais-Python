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
	@login_id Int,
	@fundo_id Int,
	@error    Varchar(100)

Select @login_id = login_id From usuario_tb Where ativo = 1

/******************************************************************/

Begin Try

	Set @error = 'Erro ao tentar inserir na tabela fundos_tb'
	Insert Into fundos_tb (
		login_id,
		nm_empresa,
		tipo_fundo,
		ticker,
		categoria,
		dt_inclusao) 
	Select
		@login_id,
		@emp,
		@tipo,
		@ticker,
		@categoria,
		Getdate()

	Select @fundo_id = Max(fundo_id) From fundos_tb Where login_id = @login_id

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