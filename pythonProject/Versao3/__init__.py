from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = secrets.token_hex(16)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mssql+pyodbc:///?odbc_connect="
    "Driver={SQL Server};"
    "Server=DESKTOP-8RMSN4M\\SQLEXPRESS;"
    "Database=GastosMensaisV3;"
    "Trusted_Connection=yes;"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do SQLAlchemy
database = SQLAlchemy(app)

from pythonProject.Versao3 import routes
from pythonProject.Versao3.models import Usuario
