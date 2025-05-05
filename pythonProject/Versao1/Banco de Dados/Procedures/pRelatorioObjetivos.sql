Create Or ALter Procedure pRelatorioObjetivos (
	@tipo      Int,
	@tp_conta  Int)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 09/04/2024
Descrição: Procedure para emitir relatório dos objetivos.
******************************************************************/

Set Nocount On


--Declaração de Variáveis
Declare @error Varchar(100)

Begin Try
	
	Set @error = 'Erro ao tentar consultar os dados'

	If @tipo = 1
	Begin
		Select 
			o.nome 'Nome do Objetivo',
			tp.descricao 'Tipo do Objetivo',
			o.vl_total 'Valor da Meta',
			o.vl_atual	'Valor Autal'
		From objetivo_tb o
		Inner Join tp_produto_tb tp
			On o.tp_objetivo_id = tp.tp_produto_id
	End
	Else If @tipo = 2
	Begin
		Select 
			o.nome 'Nome do Objetivo',
			tp.descricao 'Tipo do Objetivo',
			o.vl_total 'Valor da Meta',
			o.vl_atual	'Valor Autal'
		From objetivo_tb o
		Inner Join tp_produto_tb tp
			On o.tp_objetivo_id = tp.tp_produto_id
		Where o.ativo = 0
	End
	Else If @tipo = 3
	Begin
		Select 
			o.nome 'Nome do Objetivo',
			tp.descricao 'Tipo do Objetivo',
			o.vl_total 'Valor da Meta',
			o.vl_atual	'Valor Autal'
		From objetivo_tb o
		Inner Join tp_produto_tb tp
			On o.tp_objetivo_id = tp.tp_produto_id
		Where o.ativo = 1
	End
	Else If @tipo = 4
	Begin
		Select 
			o.nome 'Nome do Objetivo',
			o.vl_total 'Valor da Meta',
			o.vl_atual	'Valor Autal'
		From objetivo_tb o
		Inner Join tp_produto_tb tp
			On o.tp_objetivo_id = tp.tp_produto_id
			And tp.tp_produto_id = @tp_conta
	End

/******************************************************************/

End Try

Begin Catch

	If @@Rowcount > 0
		Rollback

	Select 
		@Error			  'Local do Erro',
		Error_procedure() 'Error_procedure',
		Error_line()      'Error_line',
		Error_number()    'Error_number',
		Error_message()   'Error_message'

End Catch

