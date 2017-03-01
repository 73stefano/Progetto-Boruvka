#!/usr/bin/env python
#encoding: utf-8

import sys
sys.path.append("../")

from sorting.Sorting import quickSort
from unionFind.UnionFind_QuickUnion_PathCompression\
        import UnionFindQuickUnionPathCompression as UnionFind
from priorityQueue.PQbinaryHeap import PQbinaryHeap as PriorityQueue
from dictionary_tree.dictionary.dictTrees.trees.treeArrayList\
        import TreeArrayListNode
from tree.TreeMod import TreeMod
from tree.TreeNodeMod import  TreeNodeMod
from GraphHelper import GraphHelper
from graph.elements import Edge
from MyGraphHelper import MyGraphHelper
from mst_Parser import _parseargs
import time



INFINITE = float("inf")

class MST:
    """
    Contiene metodi che implementano vari algoritmi per il calcolo del minimum
    spanning tree, che prendono in input un grafo assunto come orientato
    (implementato con liste di incidenza).
    """

    @staticmethod
    def kruskal(graph):
        """Algoritmo di Kruskal per la ricerca del minimo albero ricoprente.

        Variante implementativa che utilizza strutture union-find.
        """
        uf = UnionFind()
        edges = GraphHelper.sortEdges(graph)  #lista di archi ordinato per peso
        mstEdges = []   #lista di archi scelti per il minimo albero ricoprente
        uf = UnionFind()
        for i in range(len(graph.nodes)):
            uf.makeset(graph.nodes[i])   #makeset per ogni nodo del grafo
        mstWeight = 0   #contatore per mantenere il peso totale del mst
        for edge in edges:   #cerca le due strutture
            r1 = uf.findRoot(uf.nodes[edge.tail])
            r2 = uf.findRoot(uf.nodes[edge.head])
            if r1 != r2:   #fondile se non sono gia' unite e aggiungi l'arco
                           #corrente al mst
                uf.union(r1, r2)
                mstEdges.append(edge)
                mstWeight += edge.weight
        return mstWeight, mstEdges

    @staticmethod
    def prim(graph):
        """Algoritmo di Prim per la ricerca del minimo albero ricoprente.

        Variante che utilizza un albero binario per la gestione della frontiera
        tramite coda con priorita'.
        """
        n = len(graph.nodes)
        currentWeight = n * [INFINITE]  #imposta il peso degli archi a infinito
        pq = PriorityQueue()   #rappresenta la frontiera dell'albero generato
        root = 0    #scelgo arbitrariamente il nodo 0 come radice
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
            if(vertex[0]) not in mstNodes:   #nodo non ancora aggiunto al mst
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

                if head not in mstNodes: #inserisco solo i nodi che portano
                                         #verso vertici non ancora scelti
                    pq.insert((head, edge), weight)
                    if currWeight == INFINITE:
                        currentWeight[head] = weight
                    elif weight < currWeight:
                        currentWeight[head] = weight
                currNode = currNode.next
        return mstWeight, tree


    @staticmethod
    def boruvka(graph):
        """Algoritmo di Boruvka per la ricerca del minimo albero ricoprente.

        Variante implementativa che utilizza strutture union-find.
        """
        uf = UnionFind()
        sentinel = MyGraphHelper.edgeSentinel()#arco a inf per il controllo
        listEdge = MyGraphHelper.listEdge(graph)  #lista di archi per nodo
        mstWeight = 0 #contatore per mantenere il peso totale del mst
        numTree = len(graph.nodes) #num degli alberi uno per nodo
        tempMstEdges = [sentinel] * len(graph.nodes)#lista di archi temporanei\
                                    #scelti per il minimo albero ricoprente
        mstEdges = [] #lista archi MST

        for i in range(len(graph.nodes)):
            uf.makeset(graph.nodes[i])  #makeset per ogni nodo del grafo


        while numTree > 1 : #quando sarà un unico albero corrisponderà al mst

            for edge in listEdge:

                r1 = uf.findRoot(uf.nodes[edge.tail])
                r2 = uf.findRoot(uf.nodes[edge.head])
                r3 = uf.find(r1)
                r4 = uf.find(r2)

                if r1 != r2:    #Se i due nodi appartengono allo stesso \
                    # albero ignora l'arco,per ogni nodo controlla se il \
                    # corrente arco è di peso inferiore del precedente

                    if tempMstEdges[r3.elem] == edge:#controllo gli archi di
                                                        #peso uguale
                        temporaryEdge = tempMstEdges[r3.elem]
                        if listEdge.index(temporaryEdge) > \
                                listEdge.index(edge):
                            tempMstEdges[r3] = edge

                    #seleziono l'arco di peso più piccolo
                    if tempMstEdges[r3.elem] == sentinel or \
                                    tempMstEdges[r3.elem] > edge:
                        tempMstEdges[r3.elem] = edge

                    if tempMstEdges[r4.elem] == edge:#controllo gli archi di
                                                        #peso uguali
                        temporaryEdge = tempMstEdges[r4.elem]
                        if listEdge.index(temporaryEdge) > \
                                listEdge.index(edge):
                            tempMstEdges[r4] = edge

                    # seleziono l'arco di peso più piccolo
                    if tempMstEdges[r4.elem] == sentinel or \
                                    tempMstEdges[r4.elem] > edge:
                        tempMstEdges[r4.elem] = edge


            for node in graph.nodes:#Controlla gli archi di costo minimo \
                                # sopra selezionati e li aggiunge al MST \
                                # escludendo gli archi interni ad ogni \
                                # nuovo albero

                if tempMstEdges[node] != sentinel:

                    r1 = uf.findRoot(uf.nodes[tempMstEdges[node].tail])
                    r2 = uf.findRoot(uf.nodes[tempMstEdges[node].head])

                    if r1 != r2 :

                 # union degli alberi per arrivare ad un unico albero -> MST

                        uf.union(r1, r2)
                        mstWeight += tempMstEdges[node].weight
                        mstEdges.append(tempMstEdges[node])
                        numTree = numTree -1

            tempMstEdges = [sentinel] * len(graph.nodes)

        return mstWeight, mstEdges




def main():
    _args = _parseargs()
    node = _args.nodi
    edge = _args.archi
    r_flag = _args.random
    e_flag = _args.equal
    g = MyGraphHelper.fastBuildGraph(node, edge, r_flag, e_flag)

    #g = MyGraphHelper.buldGraph(node, edge, r_flag, e_flag)


    print("The graph:")
    g.printGraph()

    print("\nKruskal:")
    start = time.clock()
    w, mst = MST.kruskal(g)
    elapsed = time.clock() - start
    mstKruskal=mst
    print("weight:", w)
    print("list of edges:")
    print([str(item) for item in mst])
    print("time =",elapsed,"\n")


    print("Prim:")
    start = time.clock()
    w2, mst = MST.prim(g)
    elapsed = time.clock() - start
    print("weight:", w2)
    bfs = mst.BFS()
    print("BFS on returning mst:")
    print([str(item) for item in bfs])
    print("time =", elapsed, "\n")


    print("Boruvka:")
    start = time.clock()
    w3, mst = MST.boruvka(g)
    elapsed = time.clock() - start
    mstBoruvka = mst
    print("weight:", w3)
    print("list of edges:")
    print([str(item) for item in mst])
    print("time =", elapsed, "\n")

    #if e_flag:
    #    print('controllo archi uguali ; se Kruskal e Boruvka prendono gli '\
    #          'stessi archi: \n')
    #    quickSort(mstBoruvka)
    #    print('mstBoruvka:')
    #    print([str(item) for item in mstBoruvka])
    #    print("mstKruskal:")
    #    print([str(item) for item in mstKruskal],'\n')



    if(w ==  w3):
        print("Computato stesso peso dai 3 algoritmi.")
    else:
        print("Error! I tre algoritmi tornano un peso totale differente!\n")
    #    print("Lista del mstBoruvka ordinata per confrontare gli archi con "\
    #          "mstKruskal:\n")
    #    quickSort(mst)
    #    print([str(item) for item in mst])
    #    print("mstKruskal:")
    #    print([str(item)for item in mstKruskal])

if __name__ == "__main__":
    main()
