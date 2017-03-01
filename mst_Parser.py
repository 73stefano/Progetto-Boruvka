#!/usr/bin/env python
#encoding: utf-8

import argparse


def _parseargs():
    parser = argparse.ArgumentParser(description='Parser che permette '\
                'di controllare la compatibilità dei parametri da passare '\
                "alla funzione buildGraph. E' possibile creare pesi, univoci"\
                '(senza inserire argomenti opzionali), random(perturbati) '\
                                     'o uguali')

    parser.add_argument('nodi', type=int, help='Rappresenta il numero di nodi,'\
                                               ' un intero > di 0')

    parser.add_argument('archi', type=int,help='Rappresenta il numero di archi'\
                        ', almeno uno per nodo, altrimenti la funzione '\
                        'cleanGraph aggiungerà i mancanti')


    parser.add_argument('-r','--random', action='store_true',help='questo '\
                            "flag abilita il perturbamento dei pesi")

    parser.add_argument('-e','--equal', action='store_true',help='questo '\
                        "flag abilita l'inserimento di pesi uguali")

    args = parser.parse_args()

    if args.nodi  <= 0:
        parser.print_help()
        parser.error('Stai cercando di creare un grafo con un valore <= di 0 '\
                     'di nodi \n\t nodi e archi : devono essere positivi')
    if args.archi <= 0:
        parser.print_help()
        parser.error('Stai cercando di creare un grafo con un valore <= di 0 '\
                     'di archi \n\t nodi e archi : devono essere positivi')
    if args.random == True and args.equal == True:
        parser.print_help()
        parser.error('Stai tentando di creare, pesi degli archi, sia random '\
                     'che uguali')



    return args

def main(args):
    print(args)




if __name__ == "__main__":
    _args = _parseargs()

    main(_args)

