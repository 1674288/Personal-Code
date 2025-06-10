import graph
import math
import sys
import queue
import heapq



# PythonSalesMan/dijkstra.py

def Dijkstra(g, start):
    import heapq

    for v in g.Vertices:
        v.DijkstraDistance = float('inf')
        v.DijkstraVisit = False
        v.DijkstraPrevious = None

    start.DijkstraDistance = 0
    heap = [(0, start)]

    while heap:
        _, current = heapq.heappop(heap)
        if current.DijkstraVisit:
            continue
        current.DijkstraVisit = True

        for edge in current.Edges:
            neighbor = edge.Destination
            new_distance = current.DijkstraDistance + edge.Length
            if new_distance < neighbor.DijkstraDistance:
                neighbor.DijkstraDistance = new_distance
                neighbor.DijkstraPrevious = current
                heapq.heappush(heap, (new_distance, neighbor))

    # Retornem els predecessors com a diccionari
    return {v: v.DijkstraPrevious for v in g.Vertices}

# DijkstraQueue ================================================================

def DijkstraQueue(g, start):
    cua = []
    for v in g.Vertices:
        v.DijkstraDistance = sys.float_info.max #inicializamos las distancias a infinito
        v.DijkstraVisit = False
    start.DijkstraDistance = 0
    heapq.heappush(cua, (0, start))  # Usamos heapq.heappush() para añadir elementos a la cola de prioridad
    while cua:
        dist, vActual = heapq.heappop(cua)  # Usamos heapq.heappop() para eliminar elementos de la cola de prioridad
        if dist > vActual.DijkstraDistance:
            continue
        if  vActual.DijkstraVisit:
              continue
        edges = vActual.Edges 
        for edge in edges:
            sum_actual = vActual.DijkstraDistance + edge.Length #sumamos la distancia actual mas la distancia de la aresta
            if edge.Destination.DijkstraDistance > sum_actual:
                edge.Destination.DijkstraDistance = sum_actual
                heapq.heappush(cua, (sum_actual, edge.Destination))  # Usamos heapq.heappush() para añadir elementos a la cola de prioridad
        vActual.DijkstraVisit = True

