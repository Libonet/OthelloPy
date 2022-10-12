# clear(): Imprime caracteres de escape ANSI, que son interpretados para limpiar la terminal
# \033 es una secuencia de escape, \033[ indica que se introduce una secuencia de control
# \033[H mueve el cursor al principio, \033[J borra la terminal desde el cursor al final
# Funciona en la mayoria de terminales modernas
def clear() -> None: 
  """Limpia la terminal"""

  print("\033[H\033[J", end="")

# obtenerAdyacentes(): Toma una posicion y devuelve una lista con sus adyacentes,
# lo cual utilizaremos para recorrer las 'lineas' y comprobar si una jugada es valida
def obtenerAdyacentes(posicion: str, alfabeto: str) -> list[str]:
  """
  Crea una lista de posiciones adyacentes a una en específico

  Args:
    posicion: str
      Una de las posibles posiciones en el tablero
    alfabeto: str
      Un string con las letras de las columnas del tablero
  
  Returns:
    adyacentes: list[str]
      Una lista de posiciones adyacentes a la posicion ingresada
  """

  adyacentes = []
  for numero in range(int(posicion[1])-1, int(posicion[1])+2):
    for letra in range((ord(posicion[0])-65)-1, (ord(posicion[0])-65)+2):
      try:
        adyacentes.append(f"{alfabeto[letra]}{numero}")
      except IndexError:
        adyacentes.append(None)

  return adyacentes

# crearTablero(): Creamos un tablero de juego con la informacion necesaria de cada casilla: el valor que contiene y una lista de posiciones adyacentes.
# Estas posiciones adyacentes se utilizaran para determinar si una jugada es valida
def crearTablero(filas: int=8, columnas: str="ABCDEFGH") -> dict:
  """
  Crea un tablero de juego

  Args:
    filas: int
      Numero de filas. Por defecto el tablero tiene 8 filas, pero quedamos abiertos a una mayor/menor cantidad
    columnas: str
      String de los nombres de columnas. Por defecto el tablero tiene 8 columnas ('ABCDEFGH'), pero quedamos abiertos a una mayor/menor cantidad

  Returns:
    tablero: dict
      Un diccionario que contiene el valor de cada posicion y una lista de posiciones adyacentes
  """

  # creamos la lista de posiciones por comprensión. Por cada numero de fila recorremos todas las columnas
  posiciones = [f"{letra}{numero}" 
                  for numero in range(1, filas+1) 
                    for letra in columnas]
  
  tablero = {}
  for posicion in posiciones:
    tablero[posicion] = (None, obtenerAdyacentes(posicion, columnas))

  return tablero

def leerPartida() -> None:
  """Lee una partida de Othello"""
  
  print("// Aclaracion: el archivo de juego debe ser ingresado en la carpeta 'partidas'")
  path = input("Ingrese el nombre del archivo de juego (sin el .txt): ")
  try:
    with open(f"partidas/{path}.txt", "r") as f:
      partida = f.readlines()
      for row in range(len(partida)):
        partida[row] = partida[row].strip("\n")
  except OSError:
    clear()
    print("Error al leer el archivo, intente de vuelta")
    leerPartida()
    return

  # almacenamos la información de cada jugador
  jugadorA = tuple(partida[0].split(",", 1))
  jugadorB = tuple(partida[1].split(",", 1))
  if jugadorA[1] == jugadorB[1]:
    print("Ambos jugadores no pueden ser del mismo color...")
    return

  # datos de juego
  tablero = crearTablero()

  for jugada in range(3, len(partida)):
    print(partida[jugada])

if __name__ == "__main__":
  leerPartida()