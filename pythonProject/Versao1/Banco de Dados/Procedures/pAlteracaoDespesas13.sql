Create Or Alter Procedure pAlteracaoDespesas13(
	@despesa_id Int,
	@tp_celula  Char(2) = Null,
	@dado       Varchar(50) = Null,
	@deletar    Char(2) = Null)

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 29/05/2024
Descrição: Alterar ou deletar as despesas do 13º.
******************************************************************/

Set Nocount On

--Declaração de Variáveis
Declare 
	@vl_anterior    Numeric(14,2),
	@id             Int,
	@idTipo         Int,
	@idTipoAnterior Int,
	@decimo_id      Int,
	@error         Varchar(100)

Begin Try

	Set @error = 'Erro ao tentar atualizar tabela despesas_tb'

	If @deletar = '#5'
	Begin
		Select 
			@vl_anterior = valor, 
			@decimo_id = decimo_id 
		From despesas_tb 
		Where despesa_id = @despesa_id

		Update A
		Set 
			vl_sobra = (A.vl_sobra + @vl_anterior),
			dt_alteracao = Getdate()
		From decimo_terceiro_tb A
		Where decimo_id = @decimo_id

		Delete From despesas_tb Where despesa_id = @despesa_id
	End
	Else
	Begin
		If @tp_celula = '#2'
		Begin	
			If Not Exists(Select Top 1 * From produto_tb Where nome = @dado)
			Begin
				Set @error = 'Produto não existe na base'
				select @error
			End
			Else
			Begin
				Select @idTipoAnterior = p.tp_produto_id From despesas_tb d With (Nolock)
				Inner Join produto_tb p With (Nolock) On d.produto_id = p.produto_id

				If Exists(Select Top 1 * From produto_tb Where nome = @dado And tp_produto_id = @idTipoAnterior)
				Begin
					Select @id = produto_id, @idTipo = tp_produto_id From produto_tb Where nome = @dado

					Update A
					Set 
						produto_id = @id,
						dt_alteracao = Getdate()
					From despesas_tb A
					Where despesa_id = @despesa_id
				End
				Else
				Begin
					Set @error = 'O tipo do produto atual não é o mesmo do anterior'
					select @error
				End
			End
		End

		If @tp_celula = '#3'
		Begin	
			Update A
			Set 
				descricao = @dado,
				dt_alteracao = Getdate()
			From despesas_tb A
			Where despesa_id = @despesa_id
		End

		If @tp_celula = '#4'
		Begin	
			Select 
				@vl_anterior = valor, 
				@decimo_id = decimo_id 
			From despesas_tb 
			Where despesa_id = @despesa_id

			Update A
			Set 
				vl_sobra = (A.vl_sobra + @vl_anterior) - @dado,
				dt_alteracao = Getdate()
			From decimo_terceiro_tb A
			Where decimo_id = @decimo_id

			Update A
			Set 
				valor = @dado,
				dt_alteracao = Getdate()
			From despesas_tb A
			Where despesa_id = @despesa_id
		End
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