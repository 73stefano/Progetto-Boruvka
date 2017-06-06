#!/usr/bin/env python
#encoding: utf-8

import argparse


def _parseargs():
    parser = argparse.ArgumentParser(description='parser per creare grafi, '\
                'è possibile creare pesi, univoci (senza inserire '\
                'argomenti opzionali),random , uguali')

    parser.add_argument('nodi', type=int, help='inserire il numero di nodi ,'
                                               ' un intero > di 0')

    parser.add_argument('archi', type=int,help='inserire il numero di archi,'\
                        ' almeno uno per nodo, altrimenti la funzione '\
                        'cleanGraph aggiungerà i mancanti')


    parser.add_argument('-r','--random', action='store_true',help='questo '\
                            'flag  abilita l\'inserimento di valori random')

    parser.add_argument('-e','--equal', action='store_true',help='questo '\
                            'flag abilita l\'inserimento di valori uguali '\
                            'per averli inserici almeno 3 archi e 3 nodi')

    args = parser.parse_args()

    if args.nodi  <= 0:
        parser.print_help()
        parser.error('Stai cercando di creare un grafo con un valore <= a 0 '\
                     'nodi \n\t nodi and archi : must be positive > 0')
    if args.archi <= 0:
        parser.print_help()
        parser.error('Stai cercando di creare un grafo con un valore <= a 0 '\
                     'archi,\n\t nodi and archi : must be positive > 0')
    if args.random == True and args.equal == True:
        parser.print_help()
        parser.error('stai tentando di creare, pesi degli archi, sia random '\
                     'che uguali')



    return args

def main(args):
    print(args)




if __name__ == "__main__":
    _args = _parseargs()

    main(_args)

