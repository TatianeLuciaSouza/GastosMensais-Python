Insert Into fundos_tb (
	nm_empresa,
	tipo_fundo,
	ticker,
	categoria,
	dt_inclusao)
Values('Iridium Recebíveis Imobiliários', 'Papéis',	'IRDM11', 'F', Getdate()),
	  ('Ourinvest Jpp',	'Papéis', 'OUJP11', 'F', Getdate()),
	  ('GGR Covepi Renda', 'Imóveis Industriais e Logísticos', 'GGRC11', 'F', Getdate()),
	  ('Rec Logística',	'Imóveis Industriais e Logísticos',	'RELG11', 'F', Getdate()),
	  ('CSHG Real Estate', 'Renda',	'HGRE11', 'F', Getdate()),
	  ('HSI Malls', 'Renda',	'HSML11', 'F', Getdate()),
	  ('XP Malls', 'Shoppings', 'XPML11', 'F', Getdate()),
	  ('Riza Terrax', 'Misto', 'RZTR11', 'F', Getdate()),
	  ('JS Real Estate Multigestão', 'Misto', 'JSRE11', 'F', Getdate()),
	  ('Caixa', 'Banco', 'CXSE3F', 'A', Getdate()),
	  ('Itaú', 'Banco',	'ITSA4F', 'A', Getdate()),
	  ('Bradesco', 'Banco', 'BBDC3F', 'A', Getdate())