import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        genres = self._model.getAllGenres()
        for g in genres:
            self._view._ddGenre.options.append(ft.dropdown.Option(key=g.GenreId, text=g.Name, data = g))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        pass

    def handleCreaGrafo(self,e):
        pass

    def handleCammino(self,e):
        pass