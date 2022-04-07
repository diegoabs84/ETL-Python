from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, VARCHAR, CHAR, NUMERIC, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import create_database, database_exists
import sqlalchemy
from local_settings import banco_operacional as bo
from local_settings import banco_dimensional as bd
from local_settings import postgres as post
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
metadata = MetaData(bind=None)
artistas = Table('artistas', metadata, autoload=True, autoload_with= engine)

#printa coluna da tabela

print("\n -- Tabelas na coluna 'artistas' --") 
for columns in artistas.columns: 
    print(columns.name)
'''
#Criando uma engine com os dados do arquivo local_settings
def get_engine (user, passwd, host, port, db ):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine




def get_engine_from_settings(model):
    keys = [model['user'], model['passwd'], model['host'], model['port'], model['db']]
    #if not all (key in keys for key in model.keys()):
       # raise Exception ('Bad config file')

    return get_engine(model['user'],
                    model['passwd'],
                    model['host'],
                    model['port'],
                    model['db'])


#Iniciando uma sessão com o banco de dados
def get_session():
    engine = get_engine_from_settings()
    session = sessionmaker(bind=engine)()
    return session



#engine_operacional = get_engine_from_settings(bo)
#session_operacional = get_session()
#engine_dimensional = get_engine_from_settings(bd)
#session_dimensional = get_session()
session = get_engine_from_settings(post)
'''