""" Este módulo provee funciones para jugar Othello en consola """

import os

# clear(): Imprime caracteres de escape ANSI, que son interpretados para limpiar la terminal
# \033 es una secuencia de escape, \033[ indica que se introduce una secuencia de control
# \033[H mueve el cursor al principio, \033[J borra la terminal desde el cursor al final
# Funciona en la mayoria de terminales modernas

def clear() -> None:
    """Limpia la terminal"""

    print("\033[H\033[J", end="")

# ----------------------------------------------------------------

# obtenerAdyacentes(): Toma una posicion y devuelve una lista con sus adyacentes,
# lo cual utilizaremos para recorrer las 'lineas' y comprobar si una jugada es valida

def obtener_adyacentes(posicion: str, filas: int = 8, alfabeto: str = "ABCDEFGH") -> list[str]:
    """
    Crea una lista de posiciones adyacentes a una en específico

    Args:
      posicion:
        Una de las posibles posiciones en el tablero
      alfabeto:
        Un string con las letras de las columnas del tablero

    Returns:
      adyacentes:
        Una lista de posiciones adyacentes a la posicion ingresada
    """

    # el indice de la letra en el string 'alfabeto'
    indice_de_letra = (ord(posicion[0])-65)
    # el numero de la posicion transformado a un
    num_de_posicion = int(posicion[1])
    adyacentes = []
    for numero in range(num_de_posicion-1, num_de_posicion+2):
        for letra in range(indice_de_letra-1, indice_de_letra+2):
            if letra >= 0 and letra < len(alfabeto) and numero > 0 and numero <= filas:
                if alfabeto[letra]+str(numero) == posicion:
                    continue
                adyacentes.append(f"{alfabeto[letra]}{numero}")
            else:
                adyacentes.append(None)

    return adyacentes

# ----------------------------------------------------------------

# crearTablero(): Creamos un tablero de juego con la informacion necesaria de cada casilla:
# el valor que contiene y una lista de posiciones adyacentes.
# Estas posiciones adyacentes se utilizaran para determinar si una jugada es valida

def crear_tablero(filas: int = 8, columnas: str = "ABCDEFGH") -> \
        dict[str, tuple[(str | None, list[str])]]:
    """
    Crea un tablero de juego

    Args:
      filas:
        Numero de filas. Por defecto el tablero tiene 8 filas,
            pero quedamos abiertos a una mayor/menor cantidad
      columnas:
        String de los nombres de columnas. Por defecto el tablero tiene 8 columnas ('ABCDEFGH'),
            pero quedamos abiertos a una mayor/menor cantidad

    Returns:
      tablero:
        Un diccionario que contiene el valor de cada posicion y una lista de posiciones adyacentes
    """

# creamos la lista de posiciones por comprensión.
# Por cada numero de fila recorremos todas las columnas
    posiciones = [f"{letra}{numero}"
                  for numero in range(1, filas+1)
                  for letra in columnas]

    tablero = {}
    for posicion in posiciones:
        tablero[posicion] = (
            None, obtener_adyacentes(posicion, filas, columnas))

    # como estamos jugando Othello, el tablero comienza con 4 fichas en el centro del tablero
    centro_h = (len(columnas)//2)-1
    centro_v = filas//2
    tablero[columnas[centro_h]+str(centro_v)] = \
        ("B", tablero[columnas[centro_h]+str(centro_v)][1])
    tablero[columnas[centro_h+1] +
            str(centro_v)] = ("N", tablero[columnas[centro_h+1]+str(centro_v)][1])
    tablero[columnas[centro_h]+str(centro_v+1)] = ("N",
                                                   tablero[columnas[centro_h]+str(centro_v+1)][1])
    tablero[columnas[centro_h+1]+str(centro_v+1)] = \
        ("B", tablero[columnas[centro_h+1]+str(centro_v+1)][1])

    return tablero

# ----------------------------------------------------------------

# TODO: mostrar correctamente el tablero

def mostrar_tablero(tablero: dict[str, tuple[(str | None, list[str])]], filas: int = 8,
                    columnas: str = "ABCDEFGH") -> None:
    tablero_formateado = formatear_tablero(tablero, filas, columnas)

    print("Tablero:")
    print("  | A | B | C | D | E | F | G | H |")
    print("------------------------------------------------------")
    for indice, fila in enumerate(tablero_formateado):
        print(f"{indice+1} |", end="")
        for casilla in fila:
            print(f" {casilla} ", end="|")
        print("")

# ----------------------------------------------------------------

def formatear_tablero(tablero: dict[str, tuple[(str | None, list[str])]], filas: int = 8,
                      columnas: str = "ABCDEFGH") -> list[list[str]]:
    output = []
    for i in range(1, filas+1):
        fila = []
        for columna in columnas:
            if tablero[columna+str(i)][0] == "N":
                fila += "N"
            elif tablero[columna+str(i)][0] == "B":
                fila += "B"
            else:
                fila += " "
        output.append(fila)
    return output

# ----------------------------------------------------------------

def recorrer_adyacentes(tablero: dict[str, tuple[(str | None, list[str])]], posicion: int,
                        casilla: str, jugador_actual: str) -> bool:
    datos_casilla_actual = tablero[casilla]
    lista_de_adyacentes = datos_casilla_actual[1]
    casilla_adyacente = lista_de_adyacentes[posicion]
    if casilla_adyacente is not None:
        color_de_adyacente = tablero[casilla_adyacente][0]
    else:
        color_de_adyacente = None
    if color_de_adyacente == jugador_actual:
        return True
    elif color_de_adyacente is None:
        return False
    return recorrer_adyacentes(tablero, posicion, casilla_adyacente, jugador_actual)

# ----------------------------------------------------------------

def posibles_jugadas(tablero: dict[str, tuple[(str | None, list[str])]],
                   jugador_actual: str) -> dict[str, list[int]]:
    """
    Devuelve un diccionario con las posibles jugadas.
    Las llaves son casillas, y su valor es una lista de direcciones
    """
    posibles_casillas: set[str] = set()
    jugadas_validas: dict[str, list[int]] = {}

    for casilla in tablero:
        if tablero[casilla][0] is not None and tablero[casilla][0] != jugador_actual:
            for adyacente in tablero[casilla][1]:
                if adyacente is not None and tablero[adyacente][0] is None:
                    posibles_casillas.add(adyacente)

    for posible_casilla in posibles_casillas:
        direcciones: list[int] = []

        lista_de_adyacentes = tablero[posible_casilla][1]
        color_de_adyacentes = [tablero[adyacente][0] if adyacente is not None
                            else None for adyacente in lista_de_adyacentes]
        if (jugador_actual == "B" and "N" not in color_de_adyacentes) or \
                (jugador_actual == "N" and "B" not in color_de_adyacentes):
            continue

        for posicion, adyacente in enumerate(lista_de_adyacentes):
            if color_de_adyacentes[posicion] is None or color_de_adyacentes[posicion] == jugador_actual:
                continue
            valida = recorrer_adyacentes(
                tablero, posicion, adyacente, jugador_actual)
            if valida:
                direcciones.append(posicion)
        if len(direcciones)!=0:
            jugadas_validas[posible_casilla] = direcciones

    return jugadas_validas

# ----------------------------------------------------------------

def realizar_jugada(tablero: dict[str, tuple[(str | None, list[str])]], casilla: str,
                    direccion: int, jugador_actual: str) -> None:
    """
    Realizar jugada recibe una casilla en la que jugar,
    y una dirección, y modifica toda la linea de fichas
    al color del jugador actual

    Args:
        tablero:
        Un diccionario que contiene el valor de cada posicion y una lista de posiciones adyacentes

        casilla:
        La casilla en la que se quiere realizar la jugada

        direccion:
        El indice

    """
    casilla_actual = tablero.get(casilla, (None, []))
    lista_de_adyacentes = casilla_actual[1]
    casilla_adyacente = lista_de_adyacentes[direccion]
    if casilla_adyacente is not None:
        # este es el adyacente a la posicion que estamos checkeando actualmente
        color_de_adyacente = tablero[casilla_adyacente][0]
    else:
        color_de_adyacente = jugador_actual
    tablero[casilla] = (jugador_actual, lista_de_adyacentes)
    if color_de_adyacente == jugador_actual:
        return
    elif color_de_adyacente is not None:
        realizar_jugada(tablero, casilla_adyacente, direccion, jugador_actual)

# ----------------------------------------------------------------

# en caso que alguna de las jugadas encontradas en el archivo sea incorrectajugada_incorrecta
# debe indicarlo marcando qué jugador realizó esa jugada,
# mostrar el tablero hasta esa jugada (sin incluirla) y finalizar
# Necesito:
# Siempre: quién, tablero en su estado final
# Si hubo un error: posicion de jugada, número, tablero antes de cometer el error
# Jugada podría ser una tupla? (nº jugada, casilla)

def terminar_partida(jugador_actual: str, tablero: dict[str, tuple[(str | None, list[str])]],
                     jugador_a: tuple[str, str], jugador_b: tuple[str, str],
                     jugada_incorrecta: tuple[(int, str)] | str) -> None:
    """ Imprime el final de una partida. """

    fichas = "Blancas" if jugador_actual == "B" else "Negras"
    if jugador_a[1] == jugador_actual:
        jugador = f"{jugador_a[0]} de las fichas {fichas},"
    else:
        jugador = f"{jugador_b[0]} de las fichas {fichas},"

    if jugada_incorrecta == "Fin":
        determinar_ganador(tablero, jugador_a, jugador_b)
    elif jugada_incorrecta == "NoFin":
        print("La partida está incompleta.")
    else:
        explicacion = "(Turno salteado) " if jugada_incorrecta[1] == "" else \
            f"({jugada_incorrecta[1]} no es posible)"
        print(
            f"En la jugada nº{jugada_incorrecta[0]} ({jugada_incorrecta[1]}), el jugador {jugador}"
            f" realizó un movimiento inválido {explicacion}")

# ----------------------------------------------------------------

def determinar_ganador(tablero: dict[str, tuple[(str | None, list[str])]],
                       jugador_a: tuple[str, str], jugador_b: tuple[str, str]) -> None:
    cant_blancas = 0
    cant_negras = 0
    for clave in tablero:
        color = tablero[clave][0]
        if color == "B":
            cant_blancas += 1
        if color == "N":
            cant_negras += 1

    if jugador_a[1] == "B":
        mostrar_ganador(jugador_a, jugador_b, cant_blancas, cant_negras)
    else:
        mostrar_ganador(jugador_b, jugador_a, cant_blancas, cant_negras)

# ----------------------------------------------------------------

def mostrar_ganador(blancas: tuple[str, str], negras: tuple[str, str],
                    cant_blancas: int, cant_negras: int) -> None:
    if cant_blancas > cant_negras:
        print(f"Ganó {blancas[0]} de fichas Blancas, con {cant_blancas} puntos")
    elif cant_negras > cant_blancas:
        print(f"Ganó {negras[0]} de fichas Negras, con {cant_negras} puntos")
    else:
        print("La partida terminó en empate.")

# ----------------------------------------------------------------

def leer_partida_de_othello(filas: int = 8, columnas: str = "ABCDEFGH") -> None:
    """Lee una partida de Othello guardada en un archivo .txt"""

    print("// Aclaracion: el archivo de juego debe ser ingresado en la carpeta 'partidas'")
    path = input("Ingrese el nombre del archivo de juego (sin el .txt): ")
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f"partidas/{path}.txt")

    try:
        with open(filename, "r", encoding="utf8") as file:
            partida = file.readlines()
            for row, line in enumerate(partida):
                partida[row] = line.strip("\n")
    except OSError:
        clear()
        print("Error al leer el archivo, intente de vuelta")
        leer_partida_de_othello()
        return

    # almacenamos la información de cada jugador
    jugador_a = tuple(partida[0].split(",", 1))
    jugador_b = tuple(partida[1].split(",", 1))
    if jugador_a[1] == jugador_b[1]:
        print("Ambos jugadores no pueden ser del mismo color...")
        return

    # datos de juego
    tablero = crear_tablero()
    jugador_actual = partida[2]  # inicialmente es el que está en el archivo

    # inicia el loop de la partida (recorre las jugadas)
    for jugada in range(3, len(partida)):
        jugadas_validas = posibles_jugadas(tablero, jugador_actual)
        if jugadas_validas == {}:
            if partida[jugada] == "":
                if partida[jugada-1] == "":
                    terminar_partida(jugador_actual, tablero, jugador_a, jugador_b, "Fin")
                    mostrar_tablero(tablero, filas, columnas)
                    return
                continue
        if partida[jugada] in jugadas_validas:
            for posicion in jugadas_validas[partida[jugada]]:
                realizar_jugada(
                    tablero, partida[jugada], posicion, jugador_actual)
        else:
            terminar_partida(jugador_actual, tablero, jugador_a,
                             jugador_b, (jugada-2, partida[jugada]))
            mostrar_tablero(tablero, filas, columnas)
            return

        if jugador_actual == "B":
            jugador_actual = "N"
        elif jugador_actual == "N":
            jugador_actual = "B"

    # ocurre si no se termino la partida
    jugadas_validas = posibles_jugadas(tablero, jugador_actual)
    if jugadas_validas != {}:
        terminar_partida(jugador_actual, tablero, jugador_a, jugador_b, "NoFin")
        mostrar_tablero(tablero, filas, columnas)
    else:
        terminar_partida(jugador_actual, tablero, jugador_a, jugador_b, "Fin")
        mostrar_tablero(tablero, filas, columnas)


if __name__ == "__main__":
    leer_partida_de_othello()
