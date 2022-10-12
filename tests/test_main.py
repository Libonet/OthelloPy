from src.main import obtenerAdyacentes, crearTablero, validarJugada

class TestMainFunctions:
  tableroInicial = {
        "A1": (None, obtenerAdyacentes("A1")),
        "B1": (None, obtenerAdyacentes("B1")),
        "C1": (None, obtenerAdyacentes("C1")),
        "D1": (None, obtenerAdyacentes("D1")),
        "E1": (None, obtenerAdyacentes("E1")),
        "F1": (None, obtenerAdyacentes("F1")),
        "G1": (None, obtenerAdyacentes("G1")),
        "H1": (None, obtenerAdyacentes("H1")),
        "A2": (None, obtenerAdyacentes("A2")),
        "B2": (None, obtenerAdyacentes("B2")),
        "C2": (None, obtenerAdyacentes("C2")),
        "D2": (None, obtenerAdyacentes("D2")),
        "E2": (None, obtenerAdyacentes("E2")),
        "F2": (None, obtenerAdyacentes("F2")),
        "G2": (None, obtenerAdyacentes("G2")),
        "H2": (None, obtenerAdyacentes("H2")),
        "A3": (None, obtenerAdyacentes("A3")),
        "B3": (None, obtenerAdyacentes("B3")),
        "C3": (None, obtenerAdyacentes("C3")),
        "D3": (None, obtenerAdyacentes("D3")),
        "E3": (None, obtenerAdyacentes("E3")),
        "F3": (None, obtenerAdyacentes("F3")),
        "G3": (None, obtenerAdyacentes("G3")),
        "H3": (None, obtenerAdyacentes("H3")),
        "A4": (None, obtenerAdyacentes("A4")),
        "B4": (None, obtenerAdyacentes("B4")),
        "C4": (None, obtenerAdyacentes("C4")),
        "D4": ("B", obtenerAdyacentes("D4")),
        "E4": ("N", obtenerAdyacentes("E4")),
        "F4": (None, obtenerAdyacentes("F4")),
        "G4": (None, obtenerAdyacentes("G4")),
        "H4": (None, obtenerAdyacentes("H4")),
        "A5": (None, obtenerAdyacentes("A5")),
        "B5": (None, obtenerAdyacentes("B5")),
        "C5": (None, obtenerAdyacentes("C5")),
        "D5": ("N", obtenerAdyacentes("D5")),
        "E5": ("B", obtenerAdyacentes("E5")),
        "F5": (None, obtenerAdyacentes("F5")),
        "G5": (None, obtenerAdyacentes("G5")),
        "H5": (None, obtenerAdyacentes("H5")),
        "A6": (None, obtenerAdyacentes("A6")),
        "B6": (None, obtenerAdyacentes("B6")),
        "C6": (None, obtenerAdyacentes("C6")),
        "D6": (None, obtenerAdyacentes("D6")),
        "E6": (None, obtenerAdyacentes("E6")),
        "F6": (None, obtenerAdyacentes("F6")),
        "G6": (None, obtenerAdyacentes("G6")),
        "H6": (None, obtenerAdyacentes("H6")),
        "A7": (None, obtenerAdyacentes("A7")),
        "B7": (None, obtenerAdyacentes("B7")),
        "C7": (None, obtenerAdyacentes("C7")),
        "D7": (None, obtenerAdyacentes("D7")),
        "E7": (None, obtenerAdyacentes("E7")),
        "F7": (None, obtenerAdyacentes("F7")),
        "G7": (None, obtenerAdyacentes("G7")),
        "H7": (None, obtenerAdyacentes("H7")),
        "A8": (None, obtenerAdyacentes("A8")),
        "B8": (None, obtenerAdyacentes("B8")),
        "C8": (None, obtenerAdyacentes("C8")),
        "D8": (None, obtenerAdyacentes("D8")),
        "E8": (None, obtenerAdyacentes("E8")),
        "F8": (None, obtenerAdyacentes("F8")),
        "G8": (None, obtenerAdyacentes("G8")),
        "H8": (None, obtenerAdyacentes("H8")),
      }

  def test_obtenerAdyacentes(self):
    posicion1 = "C4"
    posicion2 = "A5"
    posicion3 = "H8"
    posicion4 = "D1"
    assert obtenerAdyacentes(posicion1) == ["B3", "C3", "D3", "B4", "D4", "B5", "C5", "D5"]
    assert obtenerAdyacentes(posicion2) == [None, "A4", "B4", None, "B5", None, "A6", "B6"]
    assert obtenerAdyacentes(posicion3) == ["G7", "H7", None, "G8", None, None, None, None]
    assert obtenerAdyacentes(posicion4) == [None, None, None, "C1", "E1", "C2", "D2", "E2"]

  def test_crearTablero(self):
      assert crearTablero(8, "ABCDEFGH") == self.tableroInicial
      self.tableroInicial["D3"] = ("N", obtenerAdyacentes("D3"))
      assert crearTablero(8, "ABCDEFGH") != self.tableroInicial

      assert crearTablero(3, "ABC") == {
          "A1": ("B", obtenerAdyacentes("A1", 3, "ABC")),
          "B1": ("N", obtenerAdyacentes("B1", 3, "ABC")),
          "C1": (None, obtenerAdyacentes("C1", 3, "ABC")),
          "A2": ("N", obtenerAdyacentes("A2", 3, "ABC")),
          "B2": ("B",  obtenerAdyacentes("B2", 3, "ABC")),
          "C2": (None,  obtenerAdyacentes("C2", 3, "ABC")),
          "A3": (None, obtenerAdyacentes("A3", 3, "ABC")),
          "B3": (None,  obtenerAdyacentes("B3", 3, "ABC")),
          "C3": (None,  obtenerAdyacentes("C3", 3, "ABC")),
      }

  def test_validarJugada(self):
    assert validarJugada(self.tableroInicial, "D3", "N")==(True, [1])
    assert validarJugada(self.tableroInicial, "A1", "B")==(False, [])