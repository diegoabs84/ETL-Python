from classes import (Artistas, Copias, Gravadoras, Itens_Locacoes, Locacoes, Socios, Tipos_Socios, Titulos, Dim_artista, Dim_gravadora, Dim_socio, Dim_tempo, Dim_titulo, Base)
from conexao import (session)
from inspect import Traceback

#Extração dos dados do modelo operacional

def ext_op():

    try:
        locadora_dict = {
            "artistas" : [i for i in session.query(Artistas).all()],
            "copias" : [i for i in session.query(Copias).all()],
            "gravadoras" : [i for i in session.query(Gravadoras).all()],
            "itensLocados" : [i for i in session.query(Itens_Locacoes).all()],
            "locacoes" : [i for i in session.query(Locacoes).all()],
            "socios" : [i for i in session.query(Socios).all()],
            "tiposSocios" : [i for i in session.query(Tipos_Socios).all()],
            "titulos" : [i for i in session.query(Titulos).all()],


        }
    except Exception as e:
        Traceback(e)
    
    return locadora_dict

#Processo de alteração e preenchimento dos dados

def tl_dim_locadora(locadora : dict):

    dim_locadora = { "dm_artista" : [], "dm_socio" : [], "dm_gravadora" : [], "dm_tempo" : [], "dm_titulo" : [], "ft_locacoes" : []}


    try:
        #Preparando para preencher a tabela dimensional artista
        count = 0
        for a in locadora["artistas"]:
            count+=1
            art = Dim_artista(a,count)
            dim_locadora["dm_artista"].append(art)
            session.add(art)

        #Preparando para preencher a tabela dimensional socio
        for soc in locadora["socios"]:
            for tip in locadora["tiposSocios"]:
                if tip.cod_tps == soc.cod_tps:
                    ss = Dim_socio(soc, tip)
                    dim_locadora["dm_socio"].append(ss)
                    session.add(ss)
        
        #Preparando para preencher a tabela dimensional gravadora
        count = 0
        for g in locadora["gravadoras"]:
            count+=1
            grv = Dim_gravadora(g,count)
            dim_locadora["dm_artista"].append(grv)
            session.add(grv)
        
        #Preparando para preencher a tabela dimensional titulo
        count = 0
        for t in locadora["titulos"]:
            count+=1
            tit = Dim_titulo(t,count)
            dim_locadora["dm_titulo"].append(tit)
            session.add(tit)

    except Exception as e:
        Traceback(e)    

        session.commit()
       

def main():
     loc = ext_op()
     tl_dim_locadora(loc)

if __name__ == '__main__':
     main()
     
     
    
    
