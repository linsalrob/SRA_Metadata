"""
Read all the json files in a directory and extract the runs associated with each ID
"""

import json
import os
import sys
import argparse

from roblib import bcolors

def extract_runs(jf, verbose=False):
    """
    Extract the run information
    :param jf: The JSON file to parse
    :param verbose: more information
    :return: prints out the Submission @accession and the run
    """

    with open(jf, 'r') as json_in:
        data = json.load(json_in)
        if 'SUBMISSION' in data:
            acc = data['SUBMISSION']['@accession']
        else:
            if verbose:
                sys.stderr.write(f"{bcolors.RED}No @accession found in {jf}{bcolors.ENDC}\n")
            return

        if 'RUN' in data:
            for r in data['RUN']:
                if 'PRIMARY_ID' in r['IDENTIFIERS']:
                    print(f"{acc}\t{r['IDENTIFIERS']['PRIMARY_ID']}")
        elif verbose:
            sys.stderr.write(f"{bcolors.PINK}No runs found in {acc}{bcolors.ENDC}")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-d', help='Directory of json files', required=True)
    parser.add_argument('-v', help='verbose output', action='store_true')
    args = parser.parse_args()

    for j in os.listdir(args.d):
        extract_runs(os.path.join(args.d, j))
