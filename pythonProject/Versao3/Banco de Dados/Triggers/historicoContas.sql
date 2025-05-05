Create Or ALter Trigger historicoContas On contas_tb For Delete

As
	Insert Into contasHist_tb (
		conta_id,   
		login_id,   
		tp_conta_id,
		produto_id, 
		valor,      
		parcela,    
		descricao,  
		dt_canc)
	Select 
		conta_id,   
		login_id,   
		tp_conta_id,
		produto_id, 
		valor,      
		parcela,    
		descricao,  
		Getdate()
	From deleted del

	Update A
	Set situacao = 'Cancelada'
	From parcelas_tb A
	Inner Join deleted DEL
		On A.conta_id = DEL.conta_id
	Where A.dt_parcela > Getdate()

	