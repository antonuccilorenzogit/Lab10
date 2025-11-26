import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_tratte(self, e):
        """
        Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
        popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Hub presenti
        * Numero di Tratte
        * Lista di Tratte che superano il costo indicato come soglia
        """
        self._view.lista_visualizzazione.clean()

        #prendo il valore in input sul valore minimo per la ricerca
        guadagno_medio_minimo = self._view.guadagno_medio_minimo.value
        print(guadagno_medio_minimo)
        #Pongo =0 il guadagno minimo se non è stato inserito
        if guadagno_medio_minimo =='':
            self._view.show_alert('Inserire un guadagno medio soglia')
        else:
            guadagno_medio_minimo = float(guadagno_medio_minimo)

            if guadagno_medio_minimo < 0:
                guadagno_medio_minimo= 0

            #chiamo il model per costruire il grafico
            self._model.costruisci_grafo(guadagno_medio_minimo)

            #aggiungo i risultati alla listview
            self._view.lista_visualizzazione.controls.append(ft.Text(f'Numero di Hubs {self._model.get_num_nodes()}'))
            self._view.lista_visualizzazione.controls.append(ft.Text(f'Numero di tratte {self._model.get_num_edges()}')),
            i=1
            for edge in self._model.get_all_edges():
                hub_origine= edge[0]
                hub_arrivo= edge[1]
                guadagno_medio= edge[2]
                self._view.lista_visualizzazione.controls.append(ft.Text(f'{i}) [{hub_origine} -> {hub_arrivo}] -- guadagno medio per spedizione: ${guadagno_medio}'))
                i+=1
            self._view.update()

