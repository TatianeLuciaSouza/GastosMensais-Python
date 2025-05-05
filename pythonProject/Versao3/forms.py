from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.routing import ValidationError
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

#from pythonProject.Versao3.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")

class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    PrimeiroNome = StringField("Nome de usuário", validators=[DataRequired()])
    SegundoNome = StringField("último nome de usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    botao_confirmacao = SubmitField("Criar Conta")

    #def validate_email(self, email):
     #   usuario = Usuario.query.filter_by(email=email.data).first()
      #  if usuario:
       #     return ValidationError("E-mail já cadastrado, faça login para continuar")
