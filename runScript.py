import argparse
import json
from checker_class import Checker
from headerGen import HGenerate
from visualiseGen import VGenerate

parser = argparse.ArgumentParser()
parser.add_argument("--json_file", type=str, help="input JSON filename with extension")
parser.add_argument("--schema", type=str, help="input JSON filename with schema")
parser.add_argument("--header_name", type=str, help="input new file name", required=False)
parser.add_argument("--visual_name", type=str, help="input new file name", required=False)
args = parser.parse_args()

def convert_json_to_python(file1, file2):
    # Convert json to python object.
    with open(file1) as to_check:
        _json = json.load(to_check)
    with open(file2) as to_schema:
        my_schema = json.load(to_schema)
    # Validate will raise exception if given json is not
    # what is described in schema.
    return _json, my_schema


python_json, python_schema = convert_json_to_python(args.json_file, args.schema)
check = Checker(python_json, python_schema, args.json_file)
if check.run_checks(check.json_object):
    if args.header_name is not None:
        genFile = HGenerate(args.header_name)
        genFile.write_to_file(python_json)
    if args.visual_name is not None:
        visual = VGenerate(args.visual_name)
        visual.write_to_file(python_json)
    exit(0)
else:
    exit(1)
