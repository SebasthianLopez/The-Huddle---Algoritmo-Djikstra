import heapq
import random 
# --- Función para dibujar el mapa con emojis y coordenadas ---
def mostrar(tablero, camino):
    camino_set = set(camino)

    # Imprime los números de las columnas
    print("\n   ", end="")
    for i in range(len(tablero[0])): 
        print(f"{i:<2}", end="")    #reserva 2 espacios para alinear el número con el ancho del emoji
    print()

    for f in range(len(tablero)):
        # Imprime el número de la fila
        print(f"{f:<2} ", end="") 
        
        for c in range(len(tablero[0])):
            if (f, c) in camino_set:
                print("🟩", end="") # Camino verde
            else:
                val = tablero[f][c]
                if val == 0: 
                    print("⬜", end="") 
                elif val == 1:
                    print("🟥", end="") 
                elif val == 2:
                    print("🟦", end="") 
                elif val == 3:
                    print("🟥", end="") # Pared puesta por usuario
                elif val == 8:
                    print("🟨", end="") # meta
                elif val == 9:
                    print("🟧", end="") ## inicios
        print()
    print()

# --- Función que devuelve los movimientos vecinos válidos ---
def movimientos(f, c, filas, cols):
    movs = []
    direcciones = [(-1,0), (1,0), (0,-1), (0,1)]

    for df, dc in direcciones:
        nf = f + df
        nc = c + dc

        if 0 <= nf < filas and 0 <= nc < cols:
            movs.append((nf, nc))
    
    return movs

# --- Algoritmo Dijkstra: Encuentra la ruta de menor costo ---
def dijkstra(tablero, inicio, meta):
    filas = len(tablero)
    cols = len(tablero[0])
    
    cola = [ (0, inicio[0], inicio[1], [inicio]) ]      #Configuración inicial: Agregamos el punto de partida a la cola y creamos el set de memoria
    visitados = set()

    while len(cola) > 0:
        costo, f, c, camino = heapq.heappop(cola)    #Saca el camino con MENOR costo de la cola   

        if (f, c) == meta:
            return camino, costo

        if (f, c) in visitados: 
            continue
        visitados.add((f, c))

        for nf, nc in movimientos(f, c, filas, cols):   # Este bloque revisa los vecinos, calcula cuánto cuesta moverse a ellos 
                                                        # (el agua es más cara) y los agrega a la cola para visitarlos después
            terreno = tablero[nf][nc]
            peso = 0
            se_puede = False

            # Reglas de terreno
            if terreno == 0 or terreno == 8 or terreno == 9:
                peso = 1
                se_puede = True
            elif terreno == 2:
                peso = 5 
                se_puede = True
            
            if se_puede and (nf, nc) not in visitados:
                heapq.heappush(cola, (costo + peso, nf, nc, camino + [(nf, nc)]))       # gregar una nueva tarea a la lista
                        #Agenda el siguiente paso priorizando el menor costo
    return [], 0
    #Si la cola se vacía y nunca encontramos la meta, devolvemos camino vacío 
# --- Bloque Principal ---
def main():
    print("--- CALCULADORA DE RUTAS ---")

    try:
        dim = int(input("Tamaño del tablero (Ej: 6): "))
        tablero = [[0 for _ in range(dim)] for _ in range(dim)]
    except:
        print("Error. Usando 6x6.")
        tablero = [[0 for _ in range(6)] for _ in range(6)]

    # --- GENERACIÓN ALEATORIA DE OBSTÁCULOS ---
    try:
        # 1. Pedimos cuántos obstáculos quiere
        cantidad = int(input("\nCantidad de obstáculos aleatorios: "))
        
        creados = 0
        while creados < cantidad:
            # 2. Generamos coordenadas al azar
            rf = random.randint(0, dim - 1)
            rc = random.randint(0, dim - 1)

            # 3. Verificamos que el lugar esté vacío (sea 0) para no sobrescribir
            if tablero[rf][rc] == 0:
                # 4. Elegimos al azar: 1 (Pared) o 2 (Agua)
                tablero[rf][rc] = random.choice([1, 2])
                creados += 1
                
        print(f"✅ Se colocaron {cantidad} obstáculos.")
    except:
        print("Error en la cantidad. Se dejará el mapa vacío.")

    mostrar(tablero, [])

    try:
        ini_in = input("Inicio 🟧 (Fila Columna): ")
        inicio = tuple(map(int, ini_in.split()))
        
        fin_in = input("Meta   🟨 (Fila Columna): ")
        meta = tuple(map(int, fin_in.split()))
        
        tablero[inicio[0]][inicio[1]] = 9       
        tablero[meta[0]][meta[1]] = 8
    except: return

    # --- BUCLE DE JUEGO ---
    while True:
        # 1. Recalcular ruta con el estado actual
        ruta, esfuerzo = dijkstra(tablero, inicio, meta)

        # 2. Verificar si existe camino
        if not ruta:
            print("\n CAMINO BLOQUEADO. No quedan rutas posibles.")
            print("Así quedó el mapa final:")
            mostrar(tablero, []) # Mostramos el mapa una última vez
            break

        # 3. Mostrar resultado exitoso
        print(f"\n RUTA ENCONTRADA (Costo: {esfuerzo})")
        mostrar(tablero, ruta)
        print("Coordenadas:", ruta)

        # 4. Pedir bloqueo al usuario
        print("\nBloquear camino (pondrá una pared 1):")
        bloqueo = input("Coordenada > ")
        
        if bloqueo == "": break

        try:
            bf, bc = map(int, bloqueo.split())
            
            # Solo permite bloquear si es parte de la ruta y no es inicio/fin
            if (bf, bc) in ruta and (bf, bc) != inicio and (bf, bc) != meta:
                tablero[bf][bc] = 3 # Ponemos pared (3)
                print(" Pared colocada. Recalculando...")
                # Al terminar este 'if', el while vuelve a empezar y recalcula solo
            else:
                print(" Coordenada no válidas.")
        except: print("Error.")

if __name__ == "__main__":
    main()