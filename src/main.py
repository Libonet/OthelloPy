import os

# clear(): Imprime caracteres de escape ANSI, que son interpretados para limpiar la terminal
# \033 es una secuencia de escape, \033[ indica que se introduce una secuencia de control
# \033[H mueve el cursor al principio, \033[J borra la terminal desde el cursor al final
# Funciona en la mayoria de terminales modernas
def clear() -> None: 
  """Limpia la terminal"""

  print("\033[H\033[J", end="")

# obtenerAdyacentes(): Toma una posicion y devuelve una lista con sus adyacentes,
# lo cual utilizaremos para recorrer las 'lineas' y comprobar si una jugada es valida
def obtenerAdyacentes(posicion: str, filas: int=8, alfabeto: str="ABCDEFGH") -> list[str]:
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

  indiceDeLetra = (ord(posicion[0])-65) # el indice de la letra en el string 'alfabeto'
  numDePosicion = int(posicion[1]) # el numero de la posicion transformado a un
  adyacentes = []
  for numero in range(numDePosicion-1, numDePosicion+2):
    for letra in range(indiceDeLetra-1, indiceDeLetra+2):
      if letra>=0 and letra<len(alfabeto) and numero>0 and numero<=filas:
        if alfabeto[letra]+str(numero) == posicion:
          continue
        adyacentes.append(f"{alfabeto[letra]}{numero}")
      else:
        adyacentes.append(None)

  return adyacentes

# crearTablero(): Creamos un tablero de juego con la informacion necesaria de cada casilla: el valor que contiene y una lista de posiciones adyacentes.
# Estas posiciones adyacentes se utilizaran para determinar si una jugada es valida
def crearTablero(filas: int=8, columnas: str="ABCDEFGH") -> dict[str, tuple[(str|None, list[str])]]:
  """
  Crea un tablero de juego

  Args:
    filas: int
      Numero de filas. Por defecto el tablero tiene 8 filas, pero quedamos abiertos a una mayor/menor cantidad
    columnas: str
      String de los nombres de columnas. Por defecto el tablero tiene 8 columnas ('ABCDEFGH'), pero quedamos abiertos a una mayor/menor cantidad

  Returns:
    tablero: dict[str, list[None | str | list[str]]]
      Un diccionario que contiene el valor de cada posicion y una lista de posiciones adyacentes
  """

  # creamos la lista de posiciones por comprensión. Por cada numero de fila recorremos todas las columnas
  posiciones = [f"{letra}{numero}" 
                  for numero in range(1, filas+1) 
                    for letra in columnas]
  
  tablero = {}
  for posicion in posiciones:
    tablero[posicion] = (None, obtenerAdyacentes(posicion, filas, columnas))
  
  # como estamos jugando Othello, el tablero comienza con 4 fichas en el centro del tablero
  centroH = (len(columnas)//2)-1
  centroV = filas//2
  tablero[columnas[centroH]+str(centroV)] = ("B", tablero[columnas[centroH]+str(centroV)][1]) # en un 8x8: D4
  tablero[columnas[centroH+1]+str(centroV)] = ("N", tablero[columnas[centroH+1]+str(centroV)][1]) #        E4
  tablero[columnas[centroH]+str(centroV+1)] = ("N", tablero[columnas[centroH]+str(centroV+1)][1]) #        D5
  tablero[columnas[centroH+1]+str(centroV+1)] = ("B", tablero[columnas[centroH+1]+str(centroV+1)][1]) #    E5

  return tablero

def mostrarTablero(tablero: dict[str, tuple[(str|None, list[str])]], filas: int = 8, columnas: str = "ABCDEFGH") -> None: # TODO: mostrar correctamente el tablero
  tableroFormateado = formatearTablero(tablero, filas, columnas)

  print("Tablero:")
  print("  |A|B|C|D|E|F|G|H|")
  print("--------------------")
  for indice, fila in enumerate(tableroFormateado):
    print(f"{indice+1} |", end="")
    for casilla in fila:
      print(casilla, end="|")
    print("")

def formatearTablero(tablero: dict[str, tuple[(str|None, list[str])]], filas: int = 8, columnas: str = "ABCDEFGH") -> list[list[str]]:
    output = []
    for i in range(1, filas+1):
      fila = []
      for j in range(len(columnas)):
        if tablero[columnas[j]+str(i)][0] == "N":
          fila += "N"
        elif tablero[columnas[j]+str(i)][0] == "B":
          fila += "B"
        else:
          fila += " "
      output.append(fila)
    return output

def recorrerAdyacentes(tablero: dict[str, tuple[(str | None, list[str])]], posicion: int, casilla: str, jugadorActual: str) -> bool:
  datosCasillaActual = tablero[casilla]
  listaDeAdyacentes = datosCasillaActual[1]
  casillaAdyacente = listaDeAdyacentes[posicion]
  if casillaAdyacente!=None:
    colorDeAdyacente, adyacentes = tablero[casillaAdyacente]
  else:
    colorDeAdyacente = None
  if colorDeAdyacente==jugadorActual:
    return True
  elif colorDeAdyacente==None:
    return False
  return recorrerAdyacentes(tablero, posicion, casillaAdyacente, jugadorActual)

def validarJugada(tablero: dict[str, tuple[(str | None, list[str])]], casilla: str, jugadorActual: str) -> tuple[(bool, list[int])]:
  validos = []
  if tablero.get(casilla, "")[0] != None:
    return (False, [])

  listaDeAdyacentes = tablero[casilla][1]
  colorDeAdyacentes = [tablero[adyacente][0] if adyacente!=None else None for adyacente in listaDeAdyacentes]
  if (jugadorActual == "B" and "N" not in colorDeAdyacentes) or (jugadorActual == "N" and "B" not in colorDeAdyacentes):
    return (False, [])
  
  for posicion, adyacente in enumerate(listaDeAdyacentes):
    if colorDeAdyacentes[posicion] == None or colorDeAdyacentes[posicion] == jugadorActual:
      continue
    valida = recorrerAdyacentes(tablero, posicion, adyacente, jugadorActual)
    if valida:
      validos.append(posicion)
      
  if len(validos)!=0:
    return (True, validos)
  else:
    return (False, [])

def realizarJugada(tablero: dict[str, tuple[(str|None, list[str])]], casilla: str, posicion: int, jugadorActual: str) -> None:
  casillaActual = tablero.get(casilla, (None, []))
  listaDeAdyacentes = casillaActual[1]
  casillaAdyacente = listaDeAdyacentes[posicion]
  if casillaAdyacente != None:
    colorDeAdyacente, dobleAdyacentes = tablero[casillaAdyacente] # este es el adyacente a la posicion que estamos checkeando actualmente
  else:
    colorDeAdyacente = jugadorActual
  tablero[casilla] = (jugadorActual, listaDeAdyacentes)
  if colorDeAdyacente==jugadorActual:
    return
  elif colorDeAdyacente!=None:
    realizarJugada(tablero, casillaAdyacente, posicion, jugadorActual)

# en caso que alguna de las jugadas encontradas en el archivo sea incorrecta debe indicarlo marcando qué jugador realizó esa jugada,
# mostrar el tablero hasta esa jugada (sin incluirla) y finalizar
# Necesito:
# Siempre: quién, tablero en su estado final
# Si hubo un error: posicion de jugada, número, tablero antes de cometer el error
# Jugada podría ser una tupla? (nº jugada, casilla)
def terminarPartida(jugadorActual: str, tablero: dict[str, tuple[(str|None, list[str])]], jugadorA: tuple[str, str], jugadorB: tuple[str, str], 
    jugadaIncorrecta: tuple[(int, str)] | None = None) -> None:
  """ Imprime el final de una partida. """

  if jugadorActual=="B":
    fichas="Blancas"
  else:
    fichas="Negras"
  if jugadaIncorrecta != None:
    print(f"En la jugada nº{jugadaIncorrecta[0]}, posición {jugadaIncorrecta[1]} el jugador de las fichas {fichas} realizó un movimiento inválido")
    return
  for clave in tablero:
    color = tablero[clave][0]
    if color==None:
      print("La partida no fue terminada.")
      return
  if jugadaIncorrecta == None:
    determinarGanador(tablero, jugadorA, jugadorB)

def determinarGanador(tablero: dict[str, tuple[(str|None, list[str])]], jugadorA: tuple[str, str], jugadorB: tuple[str, str]):
  cantBlancas = 0
  cantNegras = 0
  for clave in tablero:
    color = tablero[clave][0]
    print(color)
    print(cantBlancas)
    print(cantNegras)
    if color == "B":
      cantBlancas+=1
    if color == "N":
      cantNegras+=1
  print(cantBlancas)

  if jugadorA[1]=="B":
    mostrarGanador(jugadorA, jugadorB, cantBlancas, cantNegras)
  else:
    mostrarGanador(jugadorB, jugadorA, cantBlancas, cantNegras)

def mostrarGanador(blancas: tuple[str, str], negras: tuple[str, str], cantBlancas: int, cantNegras: int):
    if cantBlancas>cantNegras:
      print(f"Ganó {blancas[0]}, con {cantBlancas} puntos")
    elif cantNegras>cantBlancas:
      print(f"Ganó {negras[0]}, con {cantNegras} puntos")
    else:
      print(f"La partida terminó en empate.")



def leerPartidaDeOthello(filas: int = 8, columnas: str = "ABCDEFGH") -> None:
  """Lee una partida de Othello guardada en un archivo .txt"""
  
  print("// Aclaracion: el archivo de juego debe ser ingresado en la carpeta 'partidas'")
  path = input("Ingrese el nombre del archivo de juego (sin el .txt): ")
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, f"partidas/{path}.txt")

  try:
    with open(filename, "r") as f:
      partida = f.readlines()
      for row in range(len(partida)):
        partida[row] = partida[row].strip("\n")
  except OSError:
    clear()
    print("Error al leer el archivo, intente de vuelta")
    leerPartidaDeOthello()
    return

  # almacenamos la información de cada jugador
  jugadorA = tuple(partida[0].split(",", 1))
  jugadorB = tuple(partida[1].split(",", 1))
  if jugadorA[1] == jugadorB[1]:
    print("Ambos jugadores no pueden ser del mismo color...")
    return

  # datos de juego
  tablero = crearTablero()
  jugadorActual = partida[2] # inicialmente es el que está en el archivo

  valida = False
  # inicia el loop de la partida (recorre las jugadas)
  for jugada in range(3, len(partida)):
    # para debugging:
    mostrarTablero(tablero, filas, columnas)
    valida, adyacentes = validarJugada(tablero, partida[jugada], jugadorActual)
    if not valida:
      terminarPartida(jugadorActual, tablero, jugadorA, jugadorB, (jugada-2, partida[jugada]))
      mostrarTablero(tablero, filas, columnas)
      return
    if valida:
      for posicion in adyacentes:
        realizarJugada(tablero, partida[jugada], posicion, jugadorActual)

    if jugadorActual == "B":
      jugadorActual = "N"
    elif jugadorActual == "N":
      jugadorActual = "B"
  
  terminarPartida(jugadorActual, tablero, jugadorA, jugadorB)
  mostrarTablero(tablero, filas, columnas)

if __name__ == "__main__":
  leerPartidaDeOthello()