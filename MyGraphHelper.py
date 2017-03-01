#!/usr/bin/env python
#encoding: utf-8

import sys
sys.path.append("../")
from sorting.Sorting import quickSort
from graph.Graph_IncidenceList import GraphIncidenceList as Graph
from graph.elements import Edge
import random
from GraphHelper import GraphHelper
from tree.CmpEdge import CmpEdge


INFINITE = float("inf")


class MyGraphHelper(GraphHelper):

    @staticmethod
    def listEdge(graph):
        """Costruisce una lista di archi per la funzione Boruvka"""
        l = []
        for i in range(len(graph.nodes)):
            curr = graph.inc[i].getFirstRecord()
            while curr != None:
                edge = CmpEdge(curr.elem.tail, curr.elem.head,
                               curr.elem.weight)
                if edge.head < edge.tail:  # sto prendendo solo meta' dei nodi
                    l.append(edge)
                curr = curr.next
        return l



    @staticmethod
    def buildGraph(node, edge, r_flag, e_flag):
        """Costruisce un grafo tramite liste di incidenza
          con i valori dei nodi , archi , passati dal Parsers.
        """
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



    @staticmethod
    def fastBuildGraph(node, edge, r_flag, e_flag):
        """Costruisce un grafo tramite liste di incidenza
          con i valori dei nodi , archi , passati dal Parsers,
          funzione asintoticamente più veloce della precedente
        """
        g = Graph()
        n = []
        for i in range(node):
            n.append(g.insertNode(i))

        for j in range(edge):

            tail = random.randint(0, node - 1)
            head = random.randint(0, node - 1)

            if r_flag:          # Flag a True creo pesi random da perturbare
                weight = round(random.randint(0, 1000) +   \
                        (random.random() * (10 ** -3)), 5)

            elif e_flag:        # Flag a True creo archi con pesi uguali

                weight = random.choice(range(0,10))

            else:
                weight = random.choice(range(0,1000,2))

            if tail == head:             # elimino gli archi A -> A
                continue
            g.insertEdge(n[tail].index, n[head].index, weight)
            g.insertEdge(n[head].index, n[tail].index, weight)

        GraphHelper.cleanGraph(g)  # Utilizzo la funzione cleanGraph

        return g



    @staticmethod
    def edgeSentinel():
        """Costruisce un arco confrontabile"""
        edgeSent = CmpEdge(0, 0, INFINITE)
        return edgeSent



if __name__ == '__main__':
    print("I moduli sono stati importati correttamente. Nessun test " \
          "presente.\n")

    #g = MyGraphHelper.buildGraph(100, 100, False, False)
    #g.printGraph()

    g=MyGraphHelper.fastBuildGraph(1000, 1000, True, False)
    g.printGraph()
