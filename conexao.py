from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, VARCHAR, CHAR, NUMERIC, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import create_database, database_exists
import local_settings as settings



#Criando uma engine com os dados do arquivo local_settings
def get_engine (user, passwd, host, port, db ):
    url = f"oracle+cx_oracle://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine




def get_engine_from_settings(model: dict):
    keys = [model.user, model.passwd, model.host, model.port, model.db]
    if not all (key in keys for key in settings.keys()):
        raise Exception ('Bad config file')

    return get_engine(settings['user'],
                    settings['passwd'],
                    settings['host'],
                    settings['port'],
                    settings['db'])


#Iniciando uma sessão com o banco de dados
def get_session():
    engine = get_engine_from_settings()
    session = sessionmaker(bind=engine)()
    return session



engine_operacional = get_engine_from_settings(settings.banco_operacional)
session_operacional = get_session()
engine_dimensional = get_engine_from_settings(settings.banco_dimensional)
session_dimensional = get_session()
