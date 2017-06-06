import sys
sys.path.append("/Users/stefanopica/tutoraggio_IA")
from priorityQueue.PQbinaryHeap import PQbinaryHeap as PriorityQueue
from graph.Graph_IncidenceList import GraphIncidenceList as Graph
from graph.elements import Edge
from mst.tree.CmpEdge import CmpEdge
from mst.GraphHelper import GraphHelper
from __init__ import printSwitch
from dictionary_tree.dictionary.dictTrees.trees.treeArrayList\
        import TreeArrayListNode
from mst.tree.TreeMod import TreeMod
from mst.tree.TreeNodeMod import  TreeNodeMod
import argparse
import random

Dump = printSwitch.dumpOperations
INFINITE = float("inf")

class ShortestPaths:
    @staticmethod
    def BellmanFord(graph, root):
        nodes = len(graph.nodes)
        dist = nodes * [INFINITE]
        dist[root] = 0
        for i in range(nodes):    #iterazioni pari al numero di nodi
            for j in range(len(graph.inc)):   #scorri tutti gli archi del grafo
                currNode = graph.inc[j].getFirstRecord()
                while currNode != None:
                    edge = currNode.elem
                    if dist[edge.tail] + edge.weight < dist[edge.head]:
                        #esegui rilassamento arco
                        dist[edge.head] = dist[edge.tail] + edge.weight
                    currNode = currNode.next
        return dist

    @staticmethod
    def FloydWarshall(graph):
        nodes = len(graph.nodes)
        dist = [[INFINITE]*nodes for i in range(nodes)]   #array muldimensionale nxn
        #inizializza la matrice con i valori degli archi esistenti
        for j in range(nodes):   #scorri tutti gli archi del grafo
            dist[j][j] = 0
            currNode = graph.inc[j].getFirstRecord()
            while currNode != None:
                edge = currNode.elem
                tail = edge.tail
                head = edge.head
                dist[tail][head] = edge.weight   #assegna il valore dell'arco
                currNode = currNode.next
        #print("stampa inizializzazione")
        #for i in range(len(dist)):
        #    print("\t", dist[i])

        for i in range(nodes):   #iterazioni pari al numero di nodi
            for x in range(nodes):
                for y in range(nodes):
                    #se possibile applicare il rilassamento sulla distanza x->y
                    #passando per il nodo i-esimo
                    if dist[x][i] + dist[i][y] < dist[x][y]:
                        dist[x][y] = dist[x][i] + dist[i][y]
        #    print("iterazione numero ", i)
        #    for i in range(len(dist)):
        #        print("\t", dist[i])
        return dist

      
    @staticmethod
    def Dijkstra(graph, root):
        n = len(graph.nodes)
        currentWeight = n * [INFINITE]  #imposta il peso degli archi a infinito
        pq = PriorityQueue()   #rappresenta la frontiera dell'albero generato
        currentWeight[root] = 0

        mstNodes = set()  #insieme dei nodi correnti inclusi nella soluzione

        #inizializzazione dell'albero
        treeNode = TreeArrayListNode(root)
        tree = TreeMod(treeNode)
        mstNodes.add(root)

        #inizializzazione pq
        pq.insert((root,Edge(root,root,0)), 0)  #triviale
        mstWeight = 0

        while not pq.isEmpty():
            vertex = pq.findMin()
            pq.deleteMin()
            if(vertex[0]) not in mstNodes:   #nodo non ancora aggiunto
                #aggiornare albero e peso mst
                connectingEdge = vertex[1]
                treeNode = TreeArrayListNode(vertex[0])
                father = tree.foundNodeByElem(connectingEdge.tail)
                father.sons.append(treeNode)
                treeNode.father = father
                mstNodes.add(vertex[0])
                mstWeight += connectingEdge.weight
            #print(currentWeight)

            currNode = graph.inc[vertex[0]].getFirstRecord()
            while currNode != None:    #scorre tutti gli archi incidenti
                #semplici variabili per semplificare il codice
                edge = currNode.elem
                head = edge.head
                tail = edge.tail
                weight = edge.weight
                currWeight = currentWeight[head]
                distTail = currentWeight[tail]
                if head not in mstNodes: #inserisco solo i nodi che portano
                                         #verso vertici non ancora scelti
                    pq.insert((head, edge), distTail + weight)
                    if currWeight == INFINITE:
                        currentWeight[head] = distTail + weight
                    elif distTail + weight < currWeight:
                        currentWeight[head] = distTail + weight
                currNode = currNode.next
        return  currentWeight


    def buildGraph():
          g = Graph()
          ginfo = ((0, 1, 3.0), (0, 3, 1.0), (1, 3, 2.0), (1, 2, 4.0), (2, 3, 5.0))
          n = []
          for i in range(4):
              n.append(g.insertNode(i))
          for e in ginfo:
              g.insertEdge(n[e[0]].index, n[e[1]].index, e[2])
              g.insertEdge(n[e[1]].index, n[e[0]].index, e[2])
          return g

#todo------------------------------------------------------------------

    @staticmethod
    def newBuildGraph(node, edge, r_flag, e_flag):
        """Costruisce un grafo tramite liste di incidenza
          con i valori dei nodi , archi , passati dal Parsers."""
        g = Graph()
        tail = []
        head = []
        weight = []
        listEdge = ()
        n = []
        for i in range(node):
            n.append(g.insertNode(i))
        for x in range(edge):
            tail.append(random.randint(0, node - 1))
            head.append(random.randint(0, node - 1))
            weight = random.sample(range(1000000), edge)#Pesi random univoci
        if not (e_flag or r_flag):
            print('Pesi archi univoci=\n', weight,'\n')

        if e_flag:   #Flag a True creo archi con pesi uguali
            i=0
            while i < len(weight)-2:
                weight[i] = weight[i + 2]
                weight[i+1] = weight[i + 2]
                i += 3
            print('pesi archi uguali= \n',weight,'\n')

        if r_flag:        #Flag a True creo pesi random da perturbare
            weight.clear()
            for i in range(edge):  # sto perturbando l'arco
                weight.append(random.uniform(1, 100))

                val = weight.pop(i)
                _val = round(val + (random.random() * 10 ** -3), 5)
                weight.insert(i, _val)
            print('pesi archi random perturbati=\n', weight, '\n')

        for u in range(edge):
            listEdge += ((tail[u], head[u], weight[u]),)

        ginfo = listEdge

        for e in ginfo:
            if e[0] == e[1]:  # elimino gli archi A -> A
                continue
            g.insertEdge(n[e[0]].index, n[e[1]].index, e[2])
            g.insertEdge(n[e[1]].index, n[e[0]].index, e[2])
        GraphHelper.cleanGraph(g)  # Utilizzo la funzione cleanGraph

        return g




def main():
    #g = GraphHelper.buildGraph()
    g = ShortestPaths.newBuildGraph (10, 10, False, False)
    print("The graph:")
    g.printGraph()
    print("\tBellmanFordMoore:")
    d = ShortestPaths.BellmanFord(g, 0)
    print("\tDistances:", d)

    print("\tFloydWarshall:")
    d = ShortestPaths.FloydWarshall(g)
    print("\tDistances:")
    for i in range(len(d)):
        print("\t", d[i])
    print("\tDijkstra:")
    d = ShortestPaths.Dijkstra(g, 0)
    print("\tDistances:", d)

if __name__ == "__main__":
    main()
