--Create Database GastosMensaisV2
--Use GastosMensaisV2
-----------------------------------------------------------

Create Table login_tb (
	login_id     Int Identity(1,1) Not Null,
	nome         Varchar(30)       Not Null,
	email        Varchar(50)       Not Null,
	senha        Varchar(10)       Not Null,
	dt_inclusao  Datetime          Not Null,
	dt_alteracao Datetime,
	Primary Key(login_id))

Create Table usuario_tb (
	login_id Int,
	ativo    Int,
	Primary Key(login_id),
	Foreign Key (login_id) References login_tb(login_id))

Create Table salario_tb (
	salario_id   Int Identity(1,1) Not Null,
	login_id     Int               Not Null,
	salario      Numeric(10,2)     Not Null,
	sobra        Numeric(10,2),
	gastos       Numeric(10,2),
	extra        Numeric(10,2),
	desccricao   Varchar(30),
	dt_inclusao  Datetime          Not Null,
	dt_alteracao Datetime,
	Primary Key(salario_id),
	Foreign Key (login_id) References login_tb(login_id))

Create Index ix_login_id_salario_tb On salario_tb(login_id)


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

Create Index ix_tp_produto_id_tp_produto_tb On produto_tb(tp_produto_id)


Create Table loja_tb (
	loja_id      Int Identity(1,1) Not Null,
	nome         Varchar(50)       Not Null,
	dt_inclusao  Datetime          Not Null,
	dt_alteracao Datetime,
	Primary Key (loja_id))

Create Table gastos_tb (
	gasto_id     Int Identity(1,1) Not Null,
	login_id     Int               Not Null,
	produto_id   Int               Not Null,
	loja_id      Int               Not Null,
	valor        Numeric(6,2)      Not Null,
	qtd          Int               Not Null,
	dt_inclusao  Datetime          Not Null,
	dt_alteracao Datetime,
	Primary Key(gasto_id),
	Foreign Key (produto_id) References produto_tb(produto_id),
	Foreign Key (loja_id) References loja_tb(loja_id),
	Foreign Key (login_id) References login_tb(login_id))

Create Index ix_produto_id_gastos_tb On gastos_tb(produto_id)
Create Index ix_loja_id_gastos_tb On gastos_tb(loja_id)
Create Index ix_login_id2_gastos_tb On gastos_tb(login_id)


Create Table contas_tb (
	conta_id     Int Identity(1,1) Not Null,
	login_id     Int               Not Null,
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
	Foreign Key (produto_id) References produto_tb(produto_id),
	Foreign Key (login_id) References login_tb(login_id))

Create Index ix_tp_conta_id_tp_contas_tb On contas_tb(tp_conta_id)
Create Index ix2_produto_id_contas_tb On contas_tb(produto_id)
Create Index ix_login_id3_contas_tb On contas_tb(login_id)


Create Table parcelas_tb (
	parcela_id Int Identity(1,1) Not Null,
	conta_id   Int				 Not Null,
	vl_parcela Numeric(6,2)      Not Null,
	parcela    Int               Not Null,
	dt_parcela Datetime          Not Null,
	dt_pag     Datetime,
	Primary Key(parcela_id),
	Foreign Key (conta_id) References contas_tb(conta_id))

Create Index ix_conta_id_parcelas_tb On parcelas_tb(conta_id)


Create Table meta_tb (
	meta_id      Int Identity(1,1) Not Null,
	login_id     Int               Not Null,
	tp_meta_id   Int               Not Null,
	nome         Varchar(20)       Not Null,
	descricao    Varchar(100)      Not Null,
	vl_total     Numeric(10,2),
	vl_atual     Numeric(10,2),
	ativo        Int               Not Null,
	dt_inicio    Datetime          Not Null,
	dt_fim       Datetime,
	dt_alteracao Datetime
	Primary Key(meta_id),
	Foreign Key (tp_meta_id) References tp_produto_tb(tp_produto_id),
	Foreign Key (login_id) References login_tb(login_id))

Create Index ix_meta_id_meta_tb On meta_tb(tp_meta_id)
Create Index ix_login_id4_meta_tb On meta_tb(login_id)


Create Table metaDescricao_tb (
	desc_id      Int Identity(1,1) Not Null,
	meta_id      Int               Not Null,
	descricao    Varchar(30)       Not Null,
	dt_inclusao  Datetime	       Not Null,
	dt_alteracao Datetime,
	Primary Key(desc_id),
	Foreign Key (meta_id) References meta_tb(meta_id))

Create Index ix_meta_id_metaDescricao_tb On metaDescricao_tb(meta_id)


Create Table fundos_tb (
	fundo_id     Int Identity(1,1) Not Null,
	login_id     Int               Not Null,
	nm_empresa   Varchar(60)       Not Null,
	tipo_fundo   Varchar(50)       Not Null,
	ticker       Varchar(10)       Not Null,
	categoria    Char(1)		   Not Null, --F - Fundos Imobiliarios / A - A��es
	status       Char(2), --VT - Venda Total / V - Venda de uma aprte das cotas 
	dt_inclusao  Datetime          Not Null,
	dt_alteracao Datetime,
	Primary Key(fundo_id),
	Foreign Key (login_id) References login_tb(login_id))

Create Index ix_login_id_fundos_tb On fundos_tb(login_id)


Create Table acoes_tb (
	acao_id		 Int Identity(1,1) Not Null,
	fundo_id	 Int               Not Null,
	nro_cota	 Int               Not Null,
	vl_investido Numeric(10,2)     Not Null,
	dt_inclusao  Datetime          Not Null,
	dt_altercao  Datetime,    
	Primary Key(acao_id),
	Foreign Key (fundo_id) References fundos_tb(fundo_id))

Create Index ix_fundo_id_acoes_tb On acoes_tb(fundo_id)


Create Table fiis_tb (
	fiis_id		 Int Identity(1,1) Not Null,
	fundo_id	 Int               Not Null,
	nro_cota	 Int               Not Null,
	vl_investido Numeric(10,2)     Not Null,
	dt_inclusao  Datetime          Not Null,
	dt_altercao  Datetime,
	Primary Key(fiis_id),
	Foreign Key (fundo_id) References fundos_tb(fundo_id))

Create Index ix_fundo_id2_fiis_tb On fiis_tb(fundo_id)


Create Table aportes_tb  (
	aporte_id	  Int Identity(1,1) Not Null,
	fundo_id	  Int               Not Null,
	qtd_cota	  Int               Not Null,
	vl_cota		  Numeric(6,2)      Not Null,
	vl_total	  Numeric(6,2)      Not Null,
	vl_rendimento Numeric(10,2),
	mesAno        Varchar(6)        Not Null,
	dt_inclusao   Datetime          Not Null,
	dt_altercao   Datetime,
	Primary Key(aporte_id),
	Foreign Key (fundo_id) References fundos_tb(fundo_id))

Create Index ix_fundo_id3_aportes_tb On aportes_tb(fundo_id)


Create Table venda_fundo_tb (
	venda_fundo_id Int Identity(1,1) Not Null,
	fundo_id       Int               Not Null,
	nro_cota       Int               Not Null,
	vl_cota        Numeric(6,2)      Not Null,
	vl_total       Numeric(10,2)     Not Null,
	dt_venda       Datetime          Not Null,
	Primary Key(venda_fundo_id),
	Foreign Key (fundo_id) References fundos_tb(fundo_id))

Create Index ix_fundo_id_venda_fundo_tb On venda_fundo_tb(fundo_id)

Create Table decimo_terceiro_tb (
	decimo_id    Int Identity(1,1) Not Null,
	login_id     Int               Not Null,
	vl_parcela1  Numeric(10,2),
	vl_parcela2  Numeric(10,2),
	vl_total     Numeric(10,2),
	vl_sobra     Numeric(10,2),
	dt_inclusao  Datetime          Not Null,
	dt_alteracao Datetime,
	Primary Key(decimo_id),
	Foreign Key (login_id) References login_tb(login_id))

Create Index ix_login_id_decimo_terceiro_tb On decimo_terceiro_tb(login_id)


Create Table despesas_tb (
	despesa_id   Int Identity(1,1) Not Null,
	produto_id   Int               Not Null,
	decimo_id    Int               Not Null,
	loja_id      Int               Not Null,
	descricao    Varchar(30)       Not Null,
	valor        Numeric(10,2)     Not Null,
	dt_inclusao  Datetime          Not Null,
	dt_alteracao Datetime,
	Primary key(despesa_id),
	Foreign Key (decimo_id) References decimo_terceiro_tb(decimo_id),
	Foreign Key (produto_id) References produto_tb(produto_id),
	Foreign Key (loja_id) References loja_tb(loja_id))

Create Index ix_decimo_id_despesas_tb On despesas_tb(decimo_id)
Create Index ix_loja_id_despesas_tb On despesas_tb(loja_id)
Create Index ix_produto_id_despesas_tb On despesas_tb(produto_id)




