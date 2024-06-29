#This holds the configuration data for my database connection as well as the secret_key for the CSRF implementation
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will-never-guess-player'
    SQL_SERVER = 'TWORKSTATION'
    DATABASE = 'SportsCanvas'
    DRIVER = 'ODBC Driver 17 for SQL Server'
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://@localhost/SportsCanvas?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    SQLALCHEMY_TRACK_MODIFICATIOSN = False
