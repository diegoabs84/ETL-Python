from ast import Num
from numbers import Number
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, VARCHAR, CHAR, NUMERIC, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.ext.declarative import declarative_base
from local_settings import banco_operacional as settings
import conexao




Base = declarative_base()

#Declarando bases para referência das tabelas do banco de dados operacional

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


#Declarando bases para referência das tabelas do banco de dados dimensional

class Dim_artista(Base):
    __tablename__ = 'dm_artista'

    id_art = Column(Number(4), primary_key=True, nullable = False)
    tpo_art = Column(VARCHAR(40), nullable = False)
    nac_bras = Column(VARCHAR(40), nullable = False)
    nom_art = Column(VARCHAR(40), nullable = False)

    def __init__(self, artista : Artistas, id) -> None:
        super().__init__()
        self.id_art = id
        self.tpo_art = artista.tpo_art
        self.nac_bras = artista.nac_bras
        self.nom_art = artista.nom_art

class Dim_gravadora(Base):
    __tablename__ = 'dm_gravadora'

    id_grav = Column(Number(4), primary_key=True, nullable = False)
    uf_grav = Column(VARCHAR(50), nullable=False)
    nac_bras = Column(VARCHAR(30), nullable=False)
    nom_grav = Column(VARCHAR(40), nullable=False)

    def __init__(self, gravadora : Gravadoras, id) -> None:
        super().__init__()
        self.id_grav = id
        self.uf_grav = gravadora.uf_grav
        self.nac_bras = gravadora.nac_bras
        self.nom_grav = gravadora.nom_grav

class Dim_socio(Base):
    __tablename__ = 'dm_socio'

    id_soc = Column(Number(4), primary_key=True, nullable=False)
    nom_soc = Column(VARCHAR(40), nullable = False)
    tipo_socio = Column(VARCHAR(40), nullable=False)

    def __init__(self, socio : Socios, tipos : Tipos_Socios, id) -> None:
        super().__init__()
        self.id_soc = id
        self.nom_soc = socio.nom_soc
        self.tipo_socio = tipos.dsc_tps

class Dim_tempo(Base):
    __tablename__ = 'dm_tempo'

    id_tempo = Column(Number(6), primary_key=True, nullable=False )
    nu_ano = Column(Number(4),  nullable=False)
    nu_mes = Column(Number(2),  nullable=False)
    nu_anomes = Column(Number(7),  nullable=False)
    sg_mes = Column(CHAR(3),  nullable=False)
    nm_mesano = Column(CHAR(8),  nullable=False)
    nm_mes = Column(VARCHAR(15),  nullable=False)
    nu_dia= Column(Number(2),  nullable=False)
    dt_tempo = Column(Date,  nullable=False)
    nu_hora = Column(Number(2),  nullable=False)
    turno = Column(VARCHAR(30),  nullable=False)

    def __init__(self, locacoes : Locacoes, id) -> None:
        super().__init__()
        self.id_tempo = id
        self.nu_ano = locacoes.dat_loc.year
        self.nu_mes = locacoes.dat_loc.month
        self.nu_dia = locacoes.dat_loc.day
        

class Dim_titulo(Base):
    __tablename__ = 'dm_titulo'

    id_titulo = Column(Number(6), primary_key=True, nullable = False)
    tpo_titulo = Column(VARCHAR(40), nullable = False)
    cla_titulo = Column(VARCHAR(40), nullable = False)
    dsc_titulo = Column(VARCHAR(40), nullable = False)

    def __init__(self, titulo : Titulos, id) -> None:
        super().__init__()
        self.id_titulo = id
        self.tpo_titulo = titulo.tpo_tit
        self.cla_titulo = titulo.cla_tit
        self.dsc_titulo = titulo.dsc_tit

class FT_locacoes(Base):
    __tablename__ = 'ft_locacoes'

    id_soc = Column(Number(4), primary_key = True, nullable=False)
    id_titulo = Column(Number(6), primary_key = True, nullable=False)
    id_art = Column(Number(4), primary_key = True, nullable=False)
    id_grav = Column(Number(4), primary_key = True, nullable=False)
    id_tempo = Column(Number(6), primary_key = True, nullable=False)
    valor_arrecadado = Column(Number(10,2), nullable = False)
    tempo_devolucao = Column(Number(10,2), nullable = False)
    multa_atraso = Column(Number(10,2), nullable = False)

    def __init__(self, id_soc, id_titulo, id_art, id_grav,id_tempo, valor_arrecadado, tempo_devolucao, multa_atraso ) -> None:
        super().__init__()
        self.id_soc = id_soc
        self.id_titulo = id_titulo
        self.id_art = id_art
        self.id_grav = id_grav
        self.id_tempo = id_tempo
        self.valor_arrecadado = valor_arrecadado
        self.tempo_devolucao = tempo_devolucao
        self.multa_atraso = multa_atraso
