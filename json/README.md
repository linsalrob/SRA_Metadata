# Parse JSON Files

Each of these examples uses the JSON data in the [json examples](../json_examples) directory. 


To extract all the run IDs and accession IDs, you can use:

```bash
python3 json/extract_runs.py -d json_examples/
```

To take a look at the fields in a specific file, you can use:

```bash
python3 json/print_json_fields.py -f json_examples/SRA575213.json | less
```