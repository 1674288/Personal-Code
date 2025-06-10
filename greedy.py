

import copy
import graph
import math
import sys
import queue
import dijkstra

def SalesmanTrackGreedy(g,visits):
    t = graph.Track(g)
    v = visits.Vertices.pop(0) #eliminamos el primer elemento
    ultim_visits = visits.Vertices.pop()
    candidats = visits.Vertices #guardamos la lista de nodos candidatos, nodos a visitar

    while candidats: 
        diccionari = dijkstra.Dijkstra(g, v)  #llamamos a la funcion dijkstra para que nos calcule el camino de menor distancia
        v1 = min(candidats, key=lambda v: v.DijkstraDistance) #guardamos la distancia minima es decir, el camino mas corto
        candidats.remove(v1) #eliminamos el nodo con menor distancia de la lista de candidatos, asi no lo volvemos a recorrer
        ##encontrar camino entre un nodo y otro en el diccionario que devuelve la funcion dijkstra 
        llista_path = donaPath(g, v, v1, diccionari)
        t.Append(llista_path)
        v = v1
    diccionari = dijkstra.Dijkstra(g, v)
    llista_path = donaPath(g, v, ultim_visits, diccionari) #llamamos a dona path para buscar el camino entre dos nodos 
    t.Append(llista_path) #añadimos la lista de camino  
    #ultim_candidat = results[-1]
    #path = Dijkstra_amb_llista(g, ultim_visits, ultim_candidat)
    
    return t  #devolvemos el camino (track)

def donaPath(g, n1, n2, visitat):
    t = graph.Track(g)
    llista = [n2]  # Comenzamos desde el nodo final n2
    v2 = n2
    while v2 is not n1:  # Mientras no lleguemos al nodo inicial        
        if visitat[v2] == None:
            break
        llista.append(visitat[v2])  # Agregamos el predecesor del último nodo a la lista
        v2 = visitat[v2]
    llista.reverse()  # Invertimos la lista para que esté en el orden correcto
    for i in range(len(llista) - 1):
        for edge in llista[i].Edges:
            if edge.Destination == llista[i + 1]:
                t.AddLast(edge)
                break
    return t