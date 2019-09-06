"""
Explore the contents of a JSON file. This code prints all the headings in the file, in a tree format
so you can see the relationship between elements. There is a new line between root elements in the tree
so you know which elements you can call directly.

"""

import os
import sys
import argparse

from sra_metadata_libs import bcolors
import json

def print_str(s, l, verbose=False):
    """
    Print the string at level l
    :param s: string to print
    :param l: level to print it
    :param verbose: more output
    :return:
    """

    lo = l * '.'
    print(f"{lo} {s}")

def get_keys(js, l, verbose=False):
    """
    Get the keys at this level, and test for more dicts
    :param js: the json object
    :param l: the current level
    :param verbose: more output
    :return:
    """

    for k in js:
        print_str(k, l, verbose)
        if isinstance(js[k], dict):
            get_keys(js[k], l+1, verbose)
        elif isinstance(js[k], list):
            get_keys(js[k][0], l+1, verbose)
        if l == 0:
            print()



def print_json(jf, verbose=False):
    """
    Parse and print the fields
    :param jf: JSON file to parse
    :param verbose: more output
    :return:
    """

    if verbose:
        sys.stderr.write(f"{bcolors.GREEN}Parsing {jf}{bcolors.ENDC}\n")

    with open(jf, 'r') as ji:
        data = json.load(ji)

    get_keys(data, 0, verbose)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', help='JSON file to query', required=True)
    parser.add_argument('-v', help='verbose output', action='store_true')
    args = parser.parse_args()

    print_json(args.f)
