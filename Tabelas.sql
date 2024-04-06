Create Table tp_produto_tb (
	tp_produto_id Int Identity(1,1) Not Null,
	descricao     Varchar(20)       Not Null,
	dt_inclusao   Datetime          Not Null,
	dt_alteracao  Datetime,
	Primary Key (tp_produto_id))

Create Table produto_tb (
	produto_id    Int Identity(1,1) Not Null,
	nome          Varchar(50)       Not Null,
	tp_produto_id Int				Not Null,
	dt_inclusao   Datetime          Not Null,
	dt_alteracao  Datetime,
	Primary Key (produto_id),
	Foreign Key (tp_produto_id) References tp_produto_tb(tp_produto_id),)

Create Index ix_tp_produto_id_tp_produto_tb On tp_produto_tb(tp_produto_id)


Create Table loja_tb (
	loja_id      Int Identity(1,1) Not Null,
	nome         Varchar(50)       Not Null,
	dt_inclusao  Datetime          Not Null,
	dt_alteracao Datetime,
	Primary Key (loja_id))

Create Table gastos_tb (
	gasto_id     Int Identity(1,1) Not Null,
	produto_id   Int               Not Null,
	loja_id      Int               Not Null,
	valor        Numeric(6,2)      Not Null,
	qtd          Int               Not Null,
	dt_inclusao  Datetime          Not Null,
	dt_alteracao Datetime,
	Primary Key(gasto_id),
	Foreign Key (produto_id) References produto_tb(produto_id),
	Foreign Key (loja_id) References loja_tb(loja_id))

Create Index ix_produto_id_produto_tb On produto_tb(produto_id)
Create Index ix_loja_id_loja_tb On loja_tb(loja_id)


Create Table contas_tb (
	conta_id     Int Identity(1,1) Not Null,
	tp_conta_id  Int               Not Null,
	produto_id   Int               Not Null,
	valor        Numeric(6,2)      Not Null,
	parcela      Int               Not Null,
	dt_inicio    Datetime          Not Null,
	dt_fim       Datetime,
	dt_inclusao  Datetime          Not Null,
	dt_alteracao Datetime,
	Primary Key(conta_id),
	Foreign Key (tp_conta_id) References tp_produto_tb(tp_produto_id),
	Foreign Key (produto_id) References produto_tb(produto_id))

Create Index ix_tp_conta_id_tp_produto_tb On tp_produto_tb(tp_produto_id)
Create Index ix2_produto_id_produto_tb On produto_tb(produto_id)


Create Table parcelas_tb (
	parcela_id Int Identity(1,1) Not Null,
	conta_id   Int				 Not Null,
	vl_parcela Numeric(6,2)      Not Null,
	parcela    Int               Not Null,
	dt_parcela Datetime          Not Null,
	Primary Key(parcela_id),
	Foreign Key (conta_id) References contas_tb(conta_id))

Create Index ix_conta_id_contas_tb On contas_tb(conta_id)


