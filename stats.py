#!/usr/bin/env python
#encoding: utf-8
""" Tool per generare statistiche su un determinato file."""
import pstats
import argparse

def _parseargs():
    parser = argparse.ArgumentParser('Generatore di statistiche di un profiler')
    parser.add_argument('filename', type=str, help='profiler di input')
    args = parser.parse_args()
    return args


def main(args):
    p = pstats.Stats(args.filename)
    p.strip_dirs().sort_stats('time').print_stats()

if __name__ == "__main__":
    _args = _parseargs()
    main(_args)
