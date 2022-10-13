""" Este módulo está destinado a los tests de funciones de main.py """
from src.main import obtener_adyacentes, crear_tablero, posibles_jugadas, recorrer_adyacentes


class TestMainFunctions:
    """Testeo de funciones que usan el tablero inicial"""
    tableroInicial: dict[str, tuple[str | None, list[str]]] = {
        "A1": (None, obtener_adyacentes("A1")),
        "B1": (None, obtener_adyacentes("B1")),
        "C1": (None, obtener_adyacentes("C1")),
        "D1": (None, obtener_adyacentes("D1")),
        "E1": (None, obtener_adyacentes("E1")),
        "F1": (None, obtener_adyacentes("F1")),
        "G1": (None, obtener_adyacentes("G1")),
        "H1": (None, obtener_adyacentes("H1")),
        "A2": (None, obtener_adyacentes("A2")),
        "B2": (None, obtener_adyacentes("B2")),
        "C2": (None, obtener_adyacentes("C2")),
        "D2": (None, obtener_adyacentes("D2")),
        "E2": (None, obtener_adyacentes("E2")),
        "F2": (None, obtener_adyacentes("F2")),
        "G2": (None, obtener_adyacentes("G2")),
        "H2": (None, obtener_adyacentes("H2")),
        "A3": (None, obtener_adyacentes("A3")),
        "B3": (None, obtener_adyacentes("B3")),
        "C3": (None, obtener_adyacentes("C3")),
        "D3": (None, obtener_adyacentes("D3")),
        "E3": (None, obtener_adyacentes("E3")),
        "F3": (None, obtener_adyacentes("F3")),
        "G3": (None, obtener_adyacentes("G3")),
        "H3": (None, obtener_adyacentes("H3")),
        "A4": (None, obtener_adyacentes("A4")),
        "B4": (None, obtener_adyacentes("B4")),
        "C4": (None, obtener_adyacentes("C4")),
        "D4": ("B", obtener_adyacentes("D4")),
        "E4": ("N", obtener_adyacentes("E4")),
        "F4": (None, obtener_adyacentes("F4")),
        "G4": (None, obtener_adyacentes("G4")),
        "H4": (None, obtener_adyacentes("H4")),
        "A5": (None, obtener_adyacentes("A5")),
        "B5": (None, obtener_adyacentes("B5")),
        "C5": (None, obtener_adyacentes("C5")),
        "D5": ("N", obtener_adyacentes("D5")),
        "E5": ("B", obtener_adyacentes("E5")),
        "F5": (None, obtener_adyacentes("F5")),
        "G5": (None, obtener_adyacentes("G5")),
        "H5": (None, obtener_adyacentes("H5")),
        "A6": (None, obtener_adyacentes("A6")),
        "B6": (None, obtener_adyacentes("B6")),
        "C6": (None, obtener_adyacentes("C6")),
        "D6": (None, obtener_adyacentes("D6")),
        "E6": (None, obtener_adyacentes("E6")),
        "F6": (None, obtener_adyacentes("F6")),
        "G6": (None, obtener_adyacentes("G6")),
        "H6": (None, obtener_adyacentes("H6")),
        "A7": (None, obtener_adyacentes("A7")),
        "B7": (None, obtener_adyacentes("B7")),
        "C7": (None, obtener_adyacentes("C7")),
        "D7": (None, obtener_adyacentes("D7")),
        "E7": (None, obtener_adyacentes("E7")),
        "F7": (None, obtener_adyacentes("F7")),
        "G7": (None, obtener_adyacentes("G7")),
        "H7": (None, obtener_adyacentes("H7")),
        "A8": (None, obtener_adyacentes("A8")),
        "B8": (None, obtener_adyacentes("B8")),
        "C8": (None, obtener_adyacentes("C8")),
        "D8": (None, obtener_adyacentes("D8")),
        "E8": (None, obtener_adyacentes("E8")),
        "F8": (None, obtener_adyacentes("F8")),
        "G8": (None, obtener_adyacentes("G8")),
        "H8": (None, obtener_adyacentes("H8")),
    }

    def test_obtener_adyacentes(self):
        """obtener_adyacentes devuelve una lista de casillas adyacentes a la indicada"""
        posicion1 = "C4"
        posicion2 = "A5"
        posicion3 = "H8"
        posicion4 = "D1"
        assert obtener_adyacentes(posicion1) == [
            "B3", "C3", "D3", "B4", "D4", "B5", "C5", "D5"]
        assert obtener_adyacentes(posicion2) == [
            None, "A4", "B4", None, "B5", None, "A6", "B6"]
        assert obtener_adyacentes(posicion3) == [
            "G7", "H7", None, "G8", None, None, None, None]
        assert obtener_adyacentes(posicion4) == [
            None, None, None, "C1", "E1", "C2", "D2", "E2"]

    def test_crear_tablero(self):
        """crear_tablero devuelve un diccionario con todas las casillas como llave,
        guardando en cada una una tupla de su color y una lista de casillas adyacentes"""
        assert crear_tablero(8, "ABCDEFGH") == self.tableroInicial
        self.tableroInicial["D3"] = ("N", obtener_adyacentes("D3"))
        assert crear_tablero(8, "ABCDEFGH") != self.tableroInicial

        assert crear_tablero(3, "ABC") == {
            "A1": ("B", obtener_adyacentes("A1", 3, "ABC")),
            "B1": ("N", obtener_adyacentes("B1", 3, "ABC")),
            "C1": (None, obtener_adyacentes("C1", 3, "ABC")),
            "A2": ("N", obtener_adyacentes("A2", 3, "ABC")),
            "B2": ("B",  obtener_adyacentes("B2", 3, "ABC")),
            "C2": (None,  obtener_adyacentes("C2", 3, "ABC")),
            "A3": (None, obtener_adyacentes("A3", 3, "ABC")),
            "B3": (None,  obtener_adyacentes("B3", 3, "ABC")),
            "C3": (None,  obtener_adyacentes("C3", 3, "ABC")),
        }

    def test_posibles_jugadas(self):
        """posibles_jugadas checkea qué casillas son válidas para una jugada,
        y guarda en un diccionario como llave la casilla, y valor la lista
        de direcciones que modificar"""
        assert posibles_jugadas(self.tableroInicial, "B") == {
            "E3":[6],
            "F4":[3],
            "C5":[4],
            "D6":[1],
            }

    def test_recorrer_adyacentes(self):
        """Testeamos el recorrido de adyacentes para validar jugada"""
        assert recorrer_adyacentes(self.tableroInicial, 6, "D4", "N") is True
