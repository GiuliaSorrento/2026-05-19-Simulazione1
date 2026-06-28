import itertools
from collections import defaultdict

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._artists = []
        self._idMapA= {}

    def getAllGenres(self):
        return DAO.getAllGenres()

    def buildGraph(self, genreId):
        self._artists= DAO.getAllNodes(genreId)
        self._graph.add_nodes_from(self._artists)
        for a in self._artists:
            self._idMapA[a.ArtistId] = a

        """Esiste un arco tra l’artista A e l’artista B se almeno un cliente ha acquistato brani di
entrambi gli artisti, con verso da A verso B se la popolarità di A è maggiore della popolarità di B. In caso i
nodi A e B abbiano la stessa popolarità, aggiungere due archi in entrambi i versi. Si calcoli la popolarità di un
artista come la somma di tutti i brani acquistati di quell’artista. Usare le tabelle invoceline e invoce per
determinare gli acquisti dei clienti. Il peso dell’arco tra l’artista A e l’artista B è la somma delle rispettive
popolarità."""

        #DEFAULT DICT: RISOLVE IL PROBLEMA DELLA GESTIONE DELLE CHIAVI MANCANTI
        #SE TI RENDI CONTO CHE HAI PROBLEMI PERCHE PRIMA DOVRESTI INIZIALIZZARE TUTTE LE CHIAVI MANUALMENTE E POI
        #METTERE I VALORI, USA DEFAULTDICT
        #MOLTO UTILE PER DIZONARI NIDIFICATI
        cliente_artista = defaultdict(dict)

        #NB. DEVO RACCOGLIERE IL NUMERO DI BRANI NON I BRANI NELLA QUERY
        cliente_artista_brano = DAO.cliente_artista_numbrani(genreId)  #lista di tuple (cliente artista NUMEROBRANI)
        for cliente, artista_id, numeroBrani in cliente_artista_brano:
                cliente_artista[cliente][artista_id] = numeroBrani


        artista_popolarita = defaultdict(int)

        for cliente, artisti in cliente_artista.items():
            for artista_id, numeroBrani in artisti.items():
                artista_popolarita[artista_id] += numeroBrani


        for cliente, artisti in cliente_artista.items(): #SCORRE IL DOPPIO DIZIONARIO
            #PRENDE LA LISTA DI ARTISTI.KEYS() E PRENDE COPPIE DA ITERTOOLS DI ARTISTI
            for a_id1, a_id2 in itertools.combinations(artisti.keys(),2): #PUOI PRENDERE DUE ELEMENTI ALL'INTERNO DI UN ITERTOOLS.COMBINATIONS(LISTA, 2)
                        pop1 = artista_popolarita[a_id1]
                        pop2 = artista_popolarita[a_id2]
                        if pop1 > pop2:
                            self._graph.add_edge(self._idMapA[a_id1], self._idMapA[a_id2], weight=pop1+pop2)
                        elif pop1 < pop2:
                            self._graph.add_edge(self._idMapA[a_id2], self._idMapA[a_id1], weight=pop1 + pop2)
                        else:
                            self._graph.add_edge(self._idMapA[a_id1], self._idMapA[a_id2], weight=pop1 + pop2)
                            self._graph.add_edge(self._idMapA[a_id2], self._idMapA[a_id1], weight=pop1 + pop2)


    def getGraphDetails(self):
            return len(self._graph.nodes), len(self._graph.edges)

    def getDettagli(self):
        """L’influenza di un artista è calcolata come: peso archi uscenti − peso archi entranti. Inoltre, si visualizzino i 5
            archi con peso maggiore, in ordine decrescente."""
        infMax = 0
        nodoInf = None
        for a in self._graph.nodes():
            uscenti = self._graph.out_edges(a, data=True) #data= true per prendere il peso
            entranti = self._graph.in_edges(a, data=True)
            sommaUscenti = sum(dati["weight"] for u,v,dati in uscenti)
            sommaEntranti = sum(dati["weight"] for u,v,dati in entranti)
            influenza=sommaUscenti - sommaEntranti
            if influenza > infMax:
                infMax = influenza
                nodoInf = a

        edges = sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)
        return nodoInf, infMax, edges[:5]

