from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, VARCHAR, CHAR, NUMERIC, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import create_database, database_exists
import sqlalchemy
from sqlalchemy import create_engine, select, MetaData, Table, asc
import cx_Oracle




import local_settings

def connect_db():
  print("Abrindo conexão com o banco!")
  DIALECT = 'oracle'
  SQL_DRIVER = 'cx_oracle'
  USERNAME = 'locadora' #enter your username
  PASSWORD = 'locadora' #enter your password
  HOST = 'oracle-74894-0.cloudclusters.net' #enter the oracle db host url
  PORT = 12512 # enter the oracle port number
  SERVICE = 'XE' # enter the oracle db service name
  ENGINE_PATH_WIN_AUTH = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD +'@' + HOST + ':' + str(PORT) + '/?service_name=' + SERVICE

  engine = sqlalchemy.create_engine(ENGINE_PATH_WIN_AUTH)
  return engine
  


engine = connect_db()

session = sessionmaker(bind=engine,autoflush=True)()
