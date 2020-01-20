"""
serialize the schema so we can time loading it. We need it in a quicker format.
"""

import os
import sys
import argparse
import json
from random import randint
import time
import pickle
import xmlschema
from roblib import bcolors
__author__ = 'Rob Edwards'

def read_schemas(schemadir, verbose=True):
    """
    Read the XML Schema defintion files, and return a dict of schema objects.
    :param schemadir: directory with all the schemas in it.
    :param verbose: more output
    :return: dict of schema objects
    """

    #  known XML Schemas
    schema_types = {"analysis" : "SRA.analysis.xsd", "common" : "SRA.common.xsd",
        "experiment" : "SRA.experiment.xsd", "package" : "SRA.package.xsd", 
        "run" : "SRA.run.xsd", "sample" : "SRA.sample.xsd", "study": "SRA.study.xsd",
        "submission" : "SRA.submission.xsd"}


    schemas = {}
    if verbose:
        sys.stderr.write(f"Reading schemas\n")

    for s in schema_types:
        if verbose:
            sys.stderr.write(f"Schema parsing {s}\n")
        schemas[s] = xmlschema.XMLSchema(os.path.join(schemadir, schema_types[s]))
    
    if verbose:
        sys.stderr.write(f"Done reading schemas\n")

    return schemas


def write_json(schemas, jsonfile, verbose=False):
    """
    Write the json file
    """

    if verbose:
        sys.stderr.write(f"Writing json file {jsonfile}\n")

    with open(jsonfile, 'w') as f:
        json.dump(dict(schemas), f)

def read_json(jsonfile, verbose=False):
    """
    Read the json file
    """

    if verbose:
        sys.stderr.write(f"Reading json file {jsonfile}\n")

    with open(jsonfile, 'r') as f:
        schemas = json.load(f)
    
    return schemas


def write_pickle(schemas, picklefile, verbose=False):
    """
    Write the pickle file
    """
    if verbose:
        sys.stderr.write(f"Writing pickle file {picklefile}\n")

    with open(picklefile, 'wb') as f:
        pickle.dump(schemas, f)


def read_pickle(picklefile, verbose=False):
    """
    Read the pickle file
    """
    if verbose:
        sys.stderr.write(f"Reading pickle file {picklefile}\n")

    with open(picklefile, 'rb') as f:
        schemas = pickle.load(f)

    return schemas



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=' ')
    parser.add_argument('-x', help='xml schema directory', required=True)
    parser.add_argument('-j', help='json output to write')
    parser.add_argument('-p', help='pickle to write')
    parser.add_argument('-v', help='verbose output', action='store_true')
    args = parser.parse_args()

    schemas = read_schemas(args.x, args.v)

    """
    write_json(schemas, args.j, args.v)
    for i in range(5):
        start = time.time()
        s = read_json(args.j, args.v)
        end = time.time()
        print(f"JSON: {end - start}")
    """

    write_pickle(schemas, args.p, args.v)
    pick = []
    xml = []
    for i in range(5):
        if randint(0,10) < 5:
            sys.stderr.write("PICKLE\n")
            start = time.time()
            s = read_pickle(args.p, False)
            end = time.time()
            pick.append(end - start)
            sys.stderr.write("XML\n")
            start = time.time()
            s = read_schemas(args.x, False)
            end = time.time()
            xml.append(end - start)
        else:
            sys.stderr.write("XML\n")
            start = time.time()
            s = read_schemas(args.x, False)
            end = time.time()
            xml.append(end - start)
            sys.stderr.write("PICKLE\n")
            start = time.time()
            s = read_pickle(args.p, False)
            end = time.time()
            pick.append(end - start)

    print(f"Pickle: {sum(pick)/len(pick)} XML: {sum(xml)/len(xml)}\n")




