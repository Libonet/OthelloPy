def clear() -> None: 
  print("\033[H\033[J", end="")

def main() -> None:
  print("// Aclaracion: el archivo de juego debe ser ingresado en la carpeta 'partidas'")
  path = input("Ingrese el nombre del archivo de juego: ")
  try:
    with open(f"partidas/{path}", "r") as f:
      partida = f.readlines()
      for row in range(len(partida)):
        partida[row] = partida[row].strip("\n")
  except OSError:
    print("Error al leer el archivo, intente de vuelta")
    main()
    return

  # almacenamos la información de cada jugador
  jugadorA = tuple(partida[0].split(",", 1))
  jugadorB = tuple(partida[1].split(",", 1))
  if jugadorA[1] == jugadorB[1]:
    print("Ambos jugadores no pueden ser del mismo color...")
    return

  # datos de juego
  # tablero

  for jugada in range(3, len(partida)):
    pass

if __name__ == "__main__":
  main()