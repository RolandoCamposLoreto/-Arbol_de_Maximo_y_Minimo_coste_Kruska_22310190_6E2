# Se requiere instalar estas librerías antes de ejecutar el código:
# pip install matplotlib networkx

import networkx as nx           # Para manejar grafos
import matplotlib.pyplot as plt # Para graficar nodos y conexiones

# Clase para manejar el conjunto disjunto (Union-Find) que Kruskal necesita
class UnionFind:
    def __init__(self, n):
        # Inicializa cada nodo como su propio padre (representante)
        self.padre = list(range(n))
        # Tamaño del árbol para cada conjunto, para optimizar la unión
        self.tamano = [1] * n
    
    def encontrar(self, x):
        # Busca el representante del conjunto donde está x con compresión de caminos
        if self.padre[x] != x:
            self.padre[x] = self.encontrar(self.padre[x])
        return self.padre[x]
    
    def unir(self, x, y):
        # Une los conjuntos de x e y, si no están ya unidos
        raiz_x = self.encontrar(x)
        raiz_y = self.encontrar(y)
        if raiz_x == raiz_y:
            return False  # Ya están en el mismo conjunto
        # Unión por tamaño para mantener árbol balanceado
        if self.tamano[raiz_x] < self.tamano[raiz_y]:
            raiz_x, raiz_y = raiz_y, raiz_x
        self.padre[raiz_y] = raiz_x
        self.tamano[raiz_x] += self.tamano[raiz_y]
        return True

# Función que genera un grafo fijo con 7 oficinas para "Toroteo"
def generar_grafo_toroteo():
    # Diccionario con nodos y vecinos con costo de conexión (peso)
    # Nombres de oficinas: "Oficina 1" a "Oficina 7"
    grafo = {
        "Oficina 1": {"Oficina 2": 7, "Oficina 4": 5},
        "Oficina 2": {"Oficina 1": 7, "Oficina 3": 8, "Oficina 4": 9, "Oficina 5": 7},
        "Oficina 3": {"Oficina 2": 8, "Oficina 5": 5},
        "Oficina 4": {"Oficina 1": 5, "Oficina 2": 9, "Oficina 5": 15, "Oficina 6": 6},
        "Oficina 5": {"Oficina 2": 7, "Oficina 3": 5, "Oficina 4": 15, "Oficina 6": 8, "Oficina 7": 9},
        "Oficina 6": {"Oficina 4": 6, "Oficina 5": 8, "Oficina 7": 11},
        "Oficina 7": {"Oficina 5": 9, "Oficina 6": 11}
    }
    return grafo

# Función para mostrar gráficamente el grafo y el árbol mínimo resultante
def mostrar_arbol_kruskal(grafo, aristas_mst, titulo="Árbol Parcial Mínimo (Kruskal)"):
    G = nx.Graph()  # Grafo NetworkX
    
    # Agrega todas las aristas con pesos
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos.items():
            G.add_edge(nodo, vecino, weight=peso)
    
    pos = nx.spring_layout(G, seed=42)  # Posiciones fijas
    
    # Dibuja nodos y etiquetas
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=800, font_size=10)
    
    # Etiquetas de pesos para todas las aristas
    etiquetas = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas)
    
    # Dibuja las aristas del MST con color rojo y más ancho
    nx.draw_networkx_edges(G, pos, edgelist=aristas_mst, edge_color='red', width=3)
    
    plt.title(titulo)
    plt.show()

# Función que implementa el algoritmo de Kruskal mostrando pasos
def kruskal_con_pasos(grafo):
    # Lista para guardar todas las aristas únicas (sin duplicados)
    aristas = []
    nodos = list(grafo.keys())
    nodo_idx = {nodo: idx for idx, nodo in enumerate(nodos)}  # Índices para Union-Find
    
    # Construye lista de aristas (peso, nodo_origen, nodo_destino)
    visitado = set()
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos.items():
            # Para evitar aristas duplicadas: ordenar tupla (nodo, vecino)
            if (vecino, nodo) not in visitado:
                aristas.append((peso, nodo, vecino))
                visitado.add((nodo, vecino))
    
    # Ordena aristas por peso ascendente
    aristas.sort(key=lambda x: x[0])
    
    print("\n=== GRAFO ORIGINAL ===")
    for peso, desde, hasta in aristas:
        print(f"Arista: {desde} --({peso})--> {hasta}")
    print("======================\n")
    
    uf = UnionFind(len(nodos))  # Estructura Union-Find para ciclos
    mst = []                    # Lista de aristas en el árbol mínimo
    costo_total = 0             # Acumula costos
    
    print(">>> INICIO DEL ALGORITMO DE KRUSKAL")
    
    for peso, desde, hasta in aristas:
        idx_desde = nodo_idx[desde]
        idx_hasta = nodo_idx[hasta]
        # Si unir no genera ciclo, agregar arista al MST
        if uf.unir(idx_desde, idx_hasta):
            mst.append((desde, hasta))
            costo_total += peso
            print(f"✔ Se agrega arista: {desde} --({peso})--> {hasta}")
        else:
            print(f"✘ Se omite arista: {desde} --({peso})--> {hasta} (crea ciclo)")
    
    print("\n===== ÁRBOL PARCIAL MÍNIMO FINAL =====")
    for desde, hasta in mst:
        peso = grafo[desde][hasta]
        print(f"  - {desde} --({peso})--> {hasta}")
    print(f"\n💰 Costo total de interconexión para Toroteo: {costo_total}")
    print("=======================================\n")
    
    return mst

# ------------------- EJECUCIÓN PRINCIPAL ---------------------

grafo_toroteo = generar_grafo_toroteo()      # Grafo fijo de oficinas
resultado_mst = kruskal_con_pasos(grafo_toroteo)  # Ejecuta Kruskal paso a paso
mostrar_arbol_kruskal(grafo_toroteo, resultado_mst) # Muestra graficamente resultado
