# JSON Examples

These are some example data from the August 2019 SRA metadata that were chosen at random. Quite literally! 

I used this command:

```bash
for F in $(find . grep json$ | sort -R | head); do mkdir -p json_examples/json/${F:2:3}/${F:2:6}; cp $F json_examples/json/${F:2:3}/${F:2:6}; done
```

(`sort -R` is a good command to have up your sleeves. The construct ${F:2:3} takes characters 3-6 of the string $F.)

These ten files represent a random selection of metadata, and hopefully will have some of the variation we see in the whole directory (but probably not all of it). They are good to use with the code in [the json directory](../json) to see what the contents of typical json files are.

Note that the directory structure mirrors that of the complete [metadata in JSON format](https://edwards.sdsu.edu/data/sra/current.tar.gz) we make available:

```text
json/
├── ERA
│   ├── ERA570
│   │   └── ERA570895.json
│   └── ERA693
│       └── ERA693801.json
└── SRA
    ├── SRA245
    │   └── SRA245334.json
    ├── SRA268
    │   └── SRA268165.json
    ├── SRA490
    │   └── SRA490640.json
    ├── SRA563
    │   └── SRA563707.json
    ├── SRA575
    │   └── SRA575213.json
    ├── SRA609
    │   └── SRA609343.json
    └── SRA889
        └── SRA889255.json
```

We use this structure to reduce the number of files per directory and make commands like `ls` work!