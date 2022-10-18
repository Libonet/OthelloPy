""" Este módulo provee funciones para jugar Othello en consola """

import os

# clear(): Imprime caracteres de escape ANSI, que son interpretados para limpiar la terminal
# \033 es una secuencia de escape, \033[ indica que se introduce una secuencia de control
# \033[H mueve el cursor al principio, \033[J borra la terminal desde el cursor al final
# Funciona en la mayoria de terminales modernas


def clear() -> None:
    """ Limpia la terminal """

    print("\033[H\033[J", end="")

# ----------------------------------------------------------------


def generar_tablero(filas: int = 8, columnas: str = "ABCDEFGH") \
                 -> tuple[dict[str, str | None], dict[str, list[str | None]]]:
    """ Crea un tablero de juego

    Args:
      filas:
        Numero de filas. Por defecto el tablero tiene 8 filas,
        pero quedamos abiertos a una mayor/menor cantidad
      columnas:
        String de los nombres de columnas. Por defecto el tablero tiene 8 columnas ('ABCDEFGH'),
        pero quedamos abiertos a una mayor/menor cantidad
    Returns:
      tablero:
        Una tupla de 2 diccionarios que contienen el color de cada posicion
        y una lista de posiciones adyacentes respectivamente """

    colores: dict[str, str | None] = {}
    adyacentes: dict[str, list[str | None]] = {}

    for numero in range(1, filas+1):
        for letra in columnas:
            posicion = f"{letra}{numero}"
            colores[posicion] = None
            adyacentes[posicion] = obtener_adyacentes(posicion)

    centro_h = (len(columnas)//2)-1
    centro_v = filas//2
    colores[columnas[centro_h]+str(centro_v)] = \
        colores[columnas[centro_h+1]+str(centro_v+1)] = "B"

    colores[columnas[centro_h]+str(centro_v+1)] =\
        colores[columnas[centro_h+1]+str(centro_v)] = "N"

    tablero = (colores, adyacentes)
    return tablero

# ----------------------------------------------------------------
# obtenerAdyacentes(): Toma una posicion y devuelve una lista con sus adyacentes,
# lo cual utilizaremos para recorrer las 'lineas' y comprobar si una jugada es valida


def obtener_adyacentes(posicion: str, filas: int = 8, columnas: str = "ABCDEFGH") \
        -> list[str | None]:
    """ Crea una lista de posiciones adyacentes a una en específico

    Args:
        posicion:
            Una casilla del tablero
        filas:
            Numero de filas. Por defecto el tablero tiene 8 filas
        columnas:
            String de los nombres de columnas. Por defecto el tablero tiene 8 columnas ('ABCDEFGH')
    Returns:
        adyacentes:
            Una lista con las casillas adyacentes a la ingresada.
            Los indices de la lista determinan una direccion en específico:
            0:NorOeste, 1:Norte, 2:NorEste, 3:Oeste, 4:Este, 5:SurOeste, 6:Sur, 7:SurEste """

    # el indice de la letra en el string 'alfabeto'
    indice_de_letra = (ord(posicion[0])-65)
    # el numero de la posicion transformado a un int
    num_de_posicion = int(posicion[1])
    adyacentes: list[str | None] = []
    for numero in range(num_de_posicion-1, num_de_posicion+2):
        for letra in range(indice_de_letra-1, indice_de_letra+2):
            if letra >= 0 and letra < len(columnas) and numero > 0 and numero <= filas:
                if columnas[letra]+str(numero) == posicion:
                    continue
                adyacentes.append(f"{columnas[letra]}{numero}")
            else:
                adyacentes.append(None)

    return adyacentes

# ----------------------------------------------------------------


# TODO: mostrar correctamente el tablero

def mostrar_tablero(tablero_de_colores: dict[str, str | None], filas: int = 8, \
                    columnas: str = "ABCDEFGH") -> None:
    """ Imprime el tablero en consola

    Args:
        tablero_de_colores:
            Diccionario con los colores de cada casilla
        filas:
            Numero de filas. Por defecto el tablero tiene 8 filas
        columnas:
            String de los nombres de columnas. Por defecto el tablero tiene 8 columnas ('ABCDEFGH')
    Returns: None """

    tablero_formateado = formatear_tablero(tablero_de_colores, filas, columnas)

    print("Tablero:")
    print("  | A | B | C | D | E | F | G | H |")
    print("------------------------------------------------------")
    for indice, fila in enumerate(tablero_formateado):
        print(f"{indice+1} |", end="")
        for casilla in fila:
            print(f" {casilla} ", end="|")
        print("")

# ----------------------------------------------------------------


def formatear_tablero(tablero_de_colores: dict[str, str | None], filas: int = 8, \
                      columnas: str = "ABCDEFGH") -> list[list[str]]:
    """ Reemplaza los valores que representan los colores para mostrar en consola

    Args:
        tablero_de_colores:
            Diccionario con los colores de cada casilla
        filas:
            Numero de filas. Por defecto el tablero tiene 8 filas
        columnas:
            String de los nombres de columnas. Por defecto el tablero tiene 8 columnas ('ABCDEFGH')
    Returns:
        output:
            Una lista cuyos elementos son strings representando los colores de cada fila """

    output = []
    for i in range(1, filas+1):
        fila = []
        for columna in columnas:
            if tablero_de_colores[columna+str(i)] == "N":
                fila += "⚫"
            elif tablero_de_colores[columna+str(i)] == "B":
                fila += "⚪"
            else:
                fila += " "
        output.append(fila)
    return output

# ----------------------------------------------------------------


def posibles_jugadas(tablero: tuple[(dict[str, str | None], dict[str, list[str | None]])], \
                     jugador_actual: str) -> dict[str, list[int]]:
    """
    Devuelve un diccionario con las posibles jugadas.
    Las llaves son casillas, y su valor es una lista de direcciones que modificar

    Args:

    """
    colores, adyacentes = tablero
    posibles_casillas: set[str] = set()
    jugadas_validas: dict[str, list[int]] = {}

    for casilla in colores:
        if colores[casilla] is not None and colores[casilla] != jugador_actual:
            for adyacente in adyacentes[casilla]:
                if adyacente is not None and colores[adyacente] is None:
                    posibles_casillas.add(adyacente)

    for posible_casilla in posibles_casillas:
        direcciones: list[int] = []

        # para que una jugada sea válida, el color de las fichas adyacentes a la jugada
        # tiene que ser el contrario al del jugador actual
        color_de_adyacentes = [colores[adyacente] if adyacente is not None
                               else None for adyacente in adyacentes[posible_casilla]]

        for direccion, adyacente in enumerate(adyacentes[posible_casilla]):
            color = color_de_adyacentes[direccion]
            if color is None or color == jugador_actual or adyacente is None:
                continue
            valida = validar_linea(tablero, direccion, adyacente, jugador_actual)
            if valida:
                direcciones.append(direccion)
        if len(direcciones) != 0:
            # se crea una clave que indica una posible jugada
            jugadas_validas[posible_casilla] = direcciones

    return jugadas_validas

# ----------------------------------------------------------------


def validar_linea(tablero: tuple[dict[str, str | None], dict[str, list[str | None]]], \
                  direccion: int, casilla: str, jugador_actual: str) -> bool:
    """ """

    colores, adyacentes = tablero
    lista_de_adyacentes = adyacentes[casilla]
    casilla_adyacente = lista_de_adyacentes[direccion]

    if casilla_adyacente is not None:
        if colores[casilla_adyacente] == jugador_actual:
            return True
        if colores[casilla_adyacente] is None:
            return False
    else:
        return False
    return validar_linea(tablero, direccion, casilla_adyacente, jugador_actual)

# ----------------------------------------------------------------

def realizar_jugada(tablero: tuple[dict[str, str | None], dict[str, list[str | None]]], \
                    casilla: str, direccion: int, jugador_actual: str) -> None:
    """ Realizar jugada recibe una casilla en la que jugar,
        y una dirección, y modifica toda la linea de fichas
        al color del jugador actual

    """
    colores, adyacentes = tablero
    lista_de_adyacentes = adyacentes[casilla]
    casilla_adyacente = lista_de_adyacentes[direccion]

    colores[casilla] = jugador_actual
    if casilla_adyacente is not None:
        if colores[casilla_adyacente] == jugador_actual:
            return
        elif colores[casilla_adyacente] is not None:
            realizar_jugada(tablero, casilla_adyacente, direccion, jugador_actual)


# ----------------------------------------------------------------

# en caso que alguna de las jugadas encontradas en el archivo sea incorrectajugada_incorrecta
# debe indicarlo marcando qué jugador realizó esa jugada,
# mostrar el tablero hasta esa jugada (sin incluirla) y finalizar
# Necesito:
# Siempre: quién, tablero en su estado final
# Si hubo un error: posicion de jugada, número, tablero antes de cometer el error
# Jugada podría ser una tupla? (nº jugada, casilla)


def terminar_partida(tablero: tuple[dict[str, str | None], dict[str, list[str | None]]],\
                     jugador_actual: str, jugador_a: tuple[str, str], jugador_b: tuple[str, str],\
                     jugada_incorrecta: tuple[(int, str)] | str) -> None:
    """ Imprime el final de una partida. """


    fichas = "Blancas" if jugador_actual == "B" else "Negras"
    if jugador_a[1] == jugador_actual:
        jugador = f"{jugador_a[0]} de las fichas {fichas},"
    else:
        jugador = f"{jugador_b[0]} de las fichas {fichas},"

    if jugada_incorrecta == "Fin":
        colores, _ = tablero
        determinar_ganador(colores, jugador_a, jugador_b)
    elif jugada_incorrecta == "NoFin":
        print("La partida está incompleta.")
    else:
        explicacion = "(Turno salteado) " if jugada_incorrecta[1] == "" else \
            f"({jugada_incorrecta[1]} no es posible)"
        print(
            f"En la jugada nº{jugada_incorrecta[0]} ({jugada_incorrecta[1]}), el jugador {jugador}"
            f" realizó un movimiento inválido {explicacion}")

# ----------------------------------------------------------------


def determinar_ganador(tablero_de_colores: dict[str, str | None],
                       jugador_a: tuple[str, str], jugador_b: tuple[str, str]) -> None:
    cant_blancas = 0
    cant_negras = 0
    for casilla in tablero_de_colores:
        color = tablero_de_colores[casilla]
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
        print(
            f"Ganó {blancas[0]} de fichas Blancas, con {cant_blancas} puntos")
    elif cant_negras > cant_blancas:
        print(f"Ganó {negras[0]} de fichas Negras, con {cant_negras} puntos")
    else:
        print("La partida terminó en empate.")

# ----------------------------------------------------------------


def leer_partida_de_othello(filas: int = 8, columnas: str = "ABCDEFGH") -> None:
    """Lee una partida de Othello guardada en un archivo .txt"""

    print("// Aclaracion: el archivo de juego debe ser ingresado en la carpeta 'partidas'")
    print("// Presione enter para probar una partida de ejemplo")
    ubicacion = input("Ingrese el nombre del archivo de juego (sin el .txt): ")
    dirname = os.path.dirname(__file__)
    if ubicacion != "":
        filename = os.path.join(dirname, f"partidas/{ubicacion}.txt")
    else:
        filename = os.path.join(dirname, "partidas/ejemplo.txt")

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
    tablero = generar_tablero()
    jugador_actual = partida[2]  # inicialmente es el que está en el archivo
    colores, _ = tablero

    # inicia el loop de la partida (recorre las jugadas)
    for jugada in range(3, len(partida)):
        jugadas_validas = posibles_jugadas(tablero, jugador_actual)
        if jugadas_validas == {}:
            if partida[jugada] == "":
                if partida[jugada-1] == "":
                    terminar_partida(tablero, jugador_actual,
                                     jugador_a, jugador_b, "Fin")
                    mostrar_tablero(colores, filas, columnas)
                    return
                continue
        if partida[jugada] in jugadas_validas:
            for posicion in jugadas_validas[partida[jugada]]:
                realizar_jugada(
                    tablero, partida[jugada], posicion, jugador_actual)
        else:
            terminar_partida(tablero, jugador_actual, jugador_a,
                             jugador_b, (jugada-2, partida[jugada]))
            mostrar_tablero(colores, filas, columnas)
            return

        if jugador_actual == "B":
            jugador_actual = "N"
        elif jugador_actual == "N":
            jugador_actual = "B"

    jugadas_validas = posibles_jugadas(tablero, jugador_actual)
    # ocurre si no se termino la partida
    if jugadas_validas != {}:
        terminar_partida(tablero, jugador_actual,
                         jugador_a, jugador_b, "NoFin")
        mostrar_tablero(colores, filas, columnas)
    else:
        terminar_partida(tablero, jugador_actual, jugador_a, jugador_b, "Fin")
        mostrar_tablero(colores, filas, columnas)


if __name__ == "__main__":
    leer_partida_de_othello()
