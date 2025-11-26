from database import dao
from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._diz_nodes = {}
        self._edges = []
        self._set_edges= set()
        self.G = nx.Graph()

    def costruisci_grafo(self, guadagno):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """

        #inizializzo tutte le variabili
        self._nodes = None
        self._diz_nodes = {}
        self._edges = []
        self._set_edges = set()
        self.G = nx.Graph()

        #chiamo la funzione getALLNodes che crea una lista di oggetti di tipo HUB e li salva in self._nodes
        self.getALLNodes()

        #Creo dei nodi per ogni hub
        for hub in self._nodes:
            self.G.add_node(hub)

        #chiamo la funzione createEdge che crea tutti gli archi che abbiano un guadagno maggiore o uguale al guadagno
        #in input
        self.createEdge(guadagno)

    def getALLNodes(self):
        #crea una lista di tutti gli oggetti di tipo HUB e li salva in self._nodes
        self._nodes= DAO.readALLNodes()
        for hub in self._nodes:
            self._diz_nodes[hub.id] = hub

    def createEdge(self, guadagno):

        # popola la lista _edges con [hub_origine, hub_arrivo, guadagno medio]
        lista_connessioni = DAO.readALLEdge()
        for spedizione in lista_connessioni:
            hub_partenza = self._diz_nodes[spedizione.id_hub_origine]
            hub_arrivo = self._diz_nodes[spedizione.id_hub_destinazione]

            # crea tuple di hub partenza e arrivo e il loro inverso
            edge = (hub_partenza.id, hub_arrivo.id)
            edge_reverse = (hub_arrivo.id, hub_partenza.id)

            # verifica che quella tratta non sia gia stata presa in considerazione e neanche la sua invesra
            if edge not in self._set_edges and edge_reverse not in self._set_edges:

                # chiama una funzione che restituisce il guadagno medio per la tratta e la sua inversa senza distinzione
                guadagno_medio = self.calcola_guadagno_medio(hub_partenza, hub_arrivo)

                # verifica che il guadagno medio sia maggiore o uguale a quello richiesto
                if guadagno_medio >= guadagno:
                    # crea un arco tra i due hub con il guadagno medio
                    self.G.add_edge(hub_partenza, hub_arrivo, guadagno_medio=guadagno_medio)

                    self._edges.append([hub_partenza, hub_arrivo, guadagno_medio])
                    self._set_edges.add(edge)

    def calcola_guadagno_medio(self, hub_partenza, hub_arrivo):
        #chiama il dao che restituisce il guadagno medio per quella tratta e per la sua inversa
        return DAO.guadagno_medio(hub_partenza, hub_arrivo)

    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """
        return len(self._set_edges)

    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """
        return len(self._nodes)

    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        return self._edges

