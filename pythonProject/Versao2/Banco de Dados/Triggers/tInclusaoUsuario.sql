Create Or ALter Trigger tInclusaoUsuario
On login_tb For Insert
As
	Declare 
		@login_id Int = 0,
		@ativo    Int

	Select Top 1 @login_id = login_id From login_tb Order By dt_inclusao Desc

	Insert Into usuario_tb (
			login_id,
			ativo)
		Select
			@login_id,
			0
