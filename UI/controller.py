import flet as ft
from UI.view import View
from model.model import Model

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: Model):
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        self.biblioteca_selezionata = None
        self.genere_selezionato = None

        self.popola_dropdown()

    def popola_dropdown(self):
        """Popola i menu a tendina della view prendendo i dati dal model."""
        # 1. Popola dropdown biblioteche
        biblioteche = self._model.get_biblioteche()
        # Aggiungiamo l'opzione "Nessun filtro" (con valore None o stringa vuota)
        self._view.dd_biblioteca.options.append(ft.dropdown.Option(key=None, text="Nessun filtro"))
        for biblio in biblioteche:
            # Usiamo l'ID come key e il nome (o nome + indirizzo) come text
            self._view.dd_biblioteca.options.append(ft.dropdown.Option(key=str(biblio.id), text=biblio.nome))

        # 2. Popola dropdown generi
        generi = self._model.get_generi()
        self._view.dd_genere.options.append(ft.dropdown.Option(key=None, text="Nessun filtro"))
        for genere in generi:
            if genere:  # Evitiamo generi vuoti/None
                self._view.dd_genere.options.append(ft.dropdown.Option(key=str(genere), text=str(genere)))

        self._view.update()

    def read_biblioteca(self, e):
        """Callback eseguita quando l'utente seleziona una biblioteca dal dropdown."""
        valore = e.control.value
        # Se l'utente seleziona "Nessun filtro" (key=None), impostiamo None, altrimenti convertiamo in int
        if valore is None or valore == "None":
            self.biblioteca_selezionata = None
        else:
            self.biblioteca_selezionata = int(valore)

    def read_genere(self, e):
        """Callback eseguita quando l'utente seleziona un genere dal dropdown."""
        valore = e.control.value
        if valore is None or valore == "None":
            self.genere_selezionato = None
        else:
            self.genere_selezionato = str(valore)

    def handle_mostra_libri(self, e):
        """Gestisce il click sul pulsante 'Mostra Libri', filtrando e visualizzando i risultati."""
        # Pulisci la ListView attuale
        self._view.list_view.controls.clear()

        # Interroga il model passando i filtri correnti
        libri = self._model.get_libri_filtrati(self.biblioteca_selezionata, self.genere_selezionato)

        if not libri:
            # Se la lista è vuota, mostra un alert
            self._view.show_alert("Nessun libro trovato con i criteri di filtraggio selezionati.")
        else:
            # Popola la ListView con i libri trovati
            for libro in libri:
                self._view.list_view.controls.append(
                    ft.Text(f"{libro.titolo} - {libro.autore} ({libro.genere}, {libro.anno_pubblicazione})")
                )

        self._view.update()
