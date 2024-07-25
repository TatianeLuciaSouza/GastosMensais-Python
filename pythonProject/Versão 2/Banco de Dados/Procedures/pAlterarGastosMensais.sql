Create Or Alter Procedure pAlterarGastosMensais(
	@gasto_id Int,
	@valor    Numeric(6,2) Null,
	@qtd      Int Null,
	@coluna   Char(2))

As

/******************************************************************
Autor....: Tatiane Lucia
Data.....: 17/07/2024
Descrição: Procedure para alterar os gastos no mês.
******************************************************************/

Set Nocount On

--Declaração de Variáveis
Declare 
	@login_id Int,
	@anoMes   Varchar(6),
	@vl       Numeric(10,2),
	@quant    Int,
	@error    Varchar(100)

Select @login_id = login_id From usuario_tb Where ativo = 1
Select @anoMes = Concat(Year(Getdate()),Month(Getdate()))
Select @vl = valor, @quant = qtd From gastos_tb Where login_id = @login_id And gasto_id = @gasto_id  

/*************************************************************************************/

Begin Try

	Set @error = 'Erro ao atualizar a tabela gastos_tb'
	If @coluna = '#3'
	Begin
		Update A 
		Set 
			qtd = @qtd,
			dt_alteracao = Getdate()
		From gastos_tb A
		Where login_id = @login_id  
		      And gasto_id = @gasto_id   

		Set @error = '2 - Erro ao atualizar tabela salario_tb'
		Update A
		Set 
			gastos += ((@qtd * @vl) - (@quant * @vl)),
			sobra -= ((@qtd * @vl) - (@quant * @vl))
		From salario_tb A
		Where login_id = @login_id
			  And Concat(Year(dt_inclusao),Month(dt_inclusao)) = @anoMes
	End

	If @coluna = '#4'
	Begin
		Update A 
		Set 
			valor = @valor,
			dt_alteracao = Getdate()
		From gastos_tb A
		Where login_id = @login_id  
		      And gasto_id = @gasto_id  
			  
		Set @error = '2 - Erro ao atualizar tabela salario_tb'
		Update A
		Set 
			gastos += Case When @vl > @valor Then (@quant * (@valor - @vl))
						   When @vl < @valor Then (@quant * (@valor - @vl))
					  End,
			sobra -= Case When @vl > @valor Then (@quant * (@valor - @vl))
						   When @vl < @valor Then (@quant * (@valor - @vl))
					  End
		From salario_tb A
		Where login_id = @login_id
			  And Concat(Year(dt_inclusao),Month(dt_inclusao)) = @anoMes
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