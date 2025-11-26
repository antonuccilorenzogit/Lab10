from database.DB_connect import DBConnect
from model.hub import Hub
from model.spedizione import Spedizione


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """

    @staticmethod
    def readALLNodes():
        # funzione che interroga il DB con una query, legge e salva in oggetti di tipo hub le righe.
        # salva gli oggetti in una lista e la restituisce

        conn= DBConnect.get_connection()
        result= []

        #leggo tutti gli hub
        query= '''select *
                from hub h '''
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)

        for row in cursor:
            hub = Hub(row['id'],
                    row['codice'],
                    row['nome'],
                    row['citta'],
                    row['stato'],
                    row['latitudine'],
                    row['longitudine'])
            result.append(hub)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def readALLEdge():

        # funzione che interroga il DB con una query, legge e salva in oggetti di tipo spedizione tutte le righe risultate.
        # salva gli oggetti in una lista e la restituisce
        conn = DBConnect.get_connection()
        result = []
        query = '''select *
                    from spedizione s '''
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            spedizione = Spedizione(row['id'],
                      row['id_compagnia'],
                      row['numero_tracking'],
                      row['id_hub_origine'],
                      row['id_hub_destinazione'],
                      row['data_ritiro_programmata'],
                      row['distanza'],
                      row['data_consegna'],
                      row['valore_merce'])
            result.append(spedizione)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def guadagno_medio(hub_partenza : Hub, hub_arrivo: Hub):
        #Interroga il DB con una query che dati due hub ritorna il guadagno medio per quella tratta
        #in entrambi i sensi
        conn = DBConnect.get_connection()

        query = '''select AVG(s.valore_merce ) as guadagno_medio
                    from spedizione s
                    where (s.id_hub_origine = %s and s.id_hub_destinazione= %s) 
                    or  (s.id_hub_destinazione = %s and s.id_hub_origine= %s)  '''

        cursor = conn.cursor()
        cursor.execute(query,(hub_partenza.id, hub_arrivo.id,hub_arrivo.id,hub_partenza.id))
        row = cursor.fetchone()
        result= row[0]
        cursor.close()
        conn.close()
        return result



