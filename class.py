from numbers import Number
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, VARCHAR, CHAR, NUMERIC, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.ext.declarative import declarative_base
from local_settings import postgresql as settings

#Criando uma engine com os dados do arquivo local_settings
def get_engine (user, passwd, host, port, db ):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine




def get_engine_from_settings():
    keys = ['pguser', 'pgpasswd', 'pghost', 'pgport', 'pgdb']
    if not all (key in keys for key in settings.keys()):
        raise Exception ('Bad config file')

    return get_engine(settings['pguser'],
                    settings['pgpasswd'],
                    settings['pghost'],
                    settings['pgport'],
                    settings['pgdb'])

#Iniciando uma sessão com o banco de dados
def get_session():
    engine = get_engine_from_settings()
    session = sessionmaker(bind=engine) ()
    return session

engine = get_engine_from_settings()
session = get_session()
session

Base = declarative_base()

#Declarando bases para construção das tabelas do banco de dados

class Artistas(Base):
    __tablename__= 'artistas'

    cod_art = Column(NUMERIC(4), primary_key=True)
    tpo_art = Column(CHAR(1))
    nac_bras = Column(CHAR(1))
    cod_grav = Column(NUMERIC(4), ForeignKey("gravadoras.cod_grav"))
    qtd_tit = Column(NUMERIC(4))
    med_anual = Column(NUMERIC(4,2))
    nom_art = Column(VARCHAR(40))
    gravadora = relationship('Gravadoras')


class Copias(Base):
    __tablename__= 'copias'

    cod_tit = Column(NUMERIC(6), ForeignKey("titulos.cod_tit"), primary_key=True )
    num_cop = Column(NUMERIC(2), primary_key=True)
    dat_aq = Column(Date)
    status = Column(CHAR(1))
    titulos = relationship('titulos')


class Gravadoras(Base):
    __tablename__= 'gravadoras'

    cod_grav= Column(NUMERIC(4), primary_key=True)
    uf_grav = Column(CHAR(2))
    nac_bras = Column(CHAR(1))
    nom_grav = Column(VARCHAR(40))
    artistas = relationship(Artistas, backref='gravadoras')


class Itens_Locacoes(Base):
    __tablename__= 'itens_locacoes'

    cod_soc = Column(NUMERIC(4),ForeignKey("locacoes.cod_soc"), primary_key=True)
    dat_loc = Column(Date,ForeignKey("locacoes.dat_loc"), primary_key=True)
    cod_tit = Column(NUMERIC(6), ForeignKey("copias.cod_tit"), primary_key=True)
    num_cop = Column(NUMERIC(2), ForeignKey("copias.num_cop"))
    dat_prev = Column(Date)
    val_loc = Column(NUMERIC(6,2))
    sta_mul = Column(CHAR(1))
    dat_dev = Column(Date)
    locacoes_soc= relationship('locacoes')


class Locacoes(Base):
    __tablename__= 'locacoes'

    cod_soc = Column(NUMERIC(4), ForeignKey("socios.cod_soc"), primary_key=True)
    dat_loc = Column(Date, primary_key=True)
    val_loc = Column(NUMERIC(5,2))
    dat_venc = Column(Date)
    sta_pgto = Column(CHAR(1))
    dat_pgto = Column(Date)
    locacoes = relationship(Itens_Locacoes, backref= 'locacoes')


class Socios(Base):
    __tablename__= 'socios'

    cod_soc = Column(NUMERIC(4), primary_key=True)
    dat_cad = Column(Date)
    cod_tps = Column(NUMERIC(4), ForeignKey("tipos_socios.cod_tps"))
    sta_soc = Column(CHAR(1))
    nom_soc = Column(VARCHAR(40))
    tipos_socio= relationship('tipos_socios')


class Tipos_Socios(Base):
    __tablename__ = 'tipos_socios'

    cod_tps = Column(NUMERIC(4), primary_key=True)
    lim_tit = Column(NUMERIC(2))
    val_base = Column(NUMERIC(6,2))
    dsc_tps = Column(VARCHAR(40))
    socios = relationship(Socios, backref= 'tipos_socios')


class Titulos(Base):
    __tablename__ = 'titulos'

    cod_tit = Column(NUMERIC(6), primary_key=True)
    tpo_tit = Column(CHAR(1))
    cla_tit = Column(CHAR(1))
    qtd_cop = Column(NUMERIC(3))
    dat_lanc = Column(Date)
    cod_art = Column(NUMERIC(4), ForeignKey("artistas.cod_art"))
    cod_grav = Column(NUMERIC(4), ForeignKey("gravadoras.cod_grav"))
    dsc_tit = Column(VARCHAR(40))
    copias = relationship(Copias, backref='titulos')


Base.metadata.create_all(engine)
