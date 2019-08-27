"""
Read a directory of XML files and convert the output to JSON.
We write the JSON object to a file. By default, we do not
overwrite existing files, but you can force that with the -o 
flag.
"""

import os
import sys
import argparse
from roblib import bcolors
import xmlschema
from xmlschema.validators.exceptions import XMLSchemaValidationError
import json
import random
from pprint import pprint
__author__ = 'Rob Edwards'


def validation_errors(sample, error, verbose=False):
    """
    Log the validation error to a file. We append to the file.

    :param sample: The sample ID
    :param error: The python Error object
    :param verbose: More output
    """

    if verbose:
        sys.stderr.write(f"{bcolors.PINK}Logging error for {sample}{bcolors.ENDC}\n")

    with open("XML_validation_errors.txt", "a") as out:
        out.write(f"\n=== BEGIN {sample} ===\n")
        out.write(str(error))
        out.write(f"\n=== END {sample} ===\n")

def read_schemas(schemadir, verbose=True):
    """
    Read the XML Schema defintion files, and return a dict of schema objects.
    :param verbose: more output
    :return: dict of schema objects
    """

    #  known XML Schemas
    schema_types = {"analysis" : "SRA.analysis.xsd", "common" : "SRA.common.xsd",
        "experiment" : "SRA.experiment.xsd", "package" : "SRA.package.xsd", 
        "run" : "SRA.run.xsd", "sample" : "SRA.sample.xsd", "study": "SRA.study.xsd",
        "submission" : "SRA.submission.xsd"}


    schemas = {}

    for s in schema_types:
        if verbose:
            sys.stderr.write(f"{bcolors.GREEN}Schema parsing{bcolors.ENDC} {s}\n")
        schemas[s] = xmlschema.XMLSchema(os.path.join(schemadir, schema_types[s]))

    return schemas

def read_directory(basedir, subdir, schemas, verbose=False):
    """
    Read a directory and create a single dict for that directory
  
    :param basedir: The base directory of all the XML files
    :param subdir: The sample directory with each of the individual XML files
    :param schemas: The dictionary of XML Schema Definitions
    :param verbose: more output
    :return: a dict of all the data
    """
    
    data = {}
    for s in schemas:
        sc = schemas[s]
        if not os.path.exists(os.path.join(basedir, subdir, f"{subdir}.{s}.xml")):
            if verbose and s not in ['analysis', 'common', 'package']:
                sys.stderr.write(f"{bcolors.RED}WARN: {basedir}/{subdir}/{subdir}.{s}.xml not found\n")
            continue
        
        try:
            xm = schemas[s].to_dict(os.path.join(basedir, subdir, f"{subdir}.{s}.xml"), decimal_type=str)
        except XMLSchemaValidationError as e:
            validation_errors(subdir, e, verbose)
            continue

        #data[s.upper()] = xm[s.upper()]
        if 'submission' == s:
            data['SUBMISSION'] = xm
        else:
            data[s.upper()] = xm[s.upper()]
    
    return data

def write_json(xml, outfile, verbose=False):
    """
    Write the dictionary to a JSON file
    
    :param xml: The dictionary of the XML object
    :param outfile: The file to write to
    :param verbose: more output
    """

    with open(outfile, 'w') as out:
        out.write(json.dumps(xml, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse a directory or directories and create a json output for each one')
    parser.add_argument('-d', help='directory to parse', required=True)
    parser.add_argument('-o', help='where to put the json files.', required=True)
    parser.add_argument('-s', help='Schema directory', required=True)
    parser.add_argument('-f', help='force writing of the file, even if it exists', action='store_true')
    parser.add_argument('-v', help='verbose output', action='store_true')
    args = parser.parse_args()


    # read all the known schemas
    if not os.path.exists(args.s):
        sys.stderr.write(f"{bcolors.RED}FATAL: Schemas/ directory with known xml schemas not found{bcolors.ENDC}\n")
        sys.exit(-1)
    schemas = read_schemas(args.s, args.v)

    if not os.path.exists(args.o):
        os.mkdir(args.o)
    
    # read all the files in the base directory and randomize the order. This is so
    # we can run multiple instances in parallel
    fs = os.listdir(args.d)
    random.shuffle(fs)
    for submission in fs:
        outfile = os.path.join(args.o, f"{submission}.json")
        if (not args.f) and os.path.exists(outfile):
            continue
        # we create the semaphore file that is empty so we don't try and do this twice
        with open(outfile, 'w') as w:
            w.write("")


        if args.v:
            sys.stderr.write(f"{bcolors.GREEN}Parsing {bcolors.ENDC} {submission}\n")

        data = read_directory(args.d, submission, schemas, args.v)

        if args.v:
            sys.stderr.write(f"{bcolors.BLUE}Writing {bcolors.ENDC} {submission}\n")
        write_json(data, outfile, args.v)

