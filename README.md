# SRA_Metadata
Get, parse, and extract information from the SRA metadata files

## About the SRA metadata

The SRA contains over 1.5 million samples, and each sample contains lots of runs. The metadata is really key to understanding that data, but the metadata is difficult to organize and understand. Here we collate the metadata information available from the SRA to make it easier to search and find things.

## TL;DR

You can download all the SRA Metadata in [JSON format](https://edwards.sdsu.edu/data/sra/current.tar.gz) and then read the README.txt file in that archive. We have some tools here to help parse those JSON files, but `grep` and `jq` will get you a long way.

## See also

You might also look at our [collection of blog posts](https://edwards.sdsu.edu/research/sra) about the SRA that explain the organization of the SRA data, and provide alternate mechanisms to download the data, and so on.

# Downloading the SRA metadata

There are several components to the SRA data that we are going to download.

## SRA_Accessions.tab

This tab separated file can be downloaded directly from the NCBI: [ftp://ftp.ncbi.nlm.nih.gov/sra/reports/Metadata/SRA_Accessions.tab](ftp://ftp.ncbi.nlm.nih.gov/sra/reports/Metadata/SRA_Accessions.tab). 

This file lists all the submissions to the SRA, and lists every accession number associated with each submission. It tells you the status of the datasets.

It contains the following columns:

* Accession
* Submission
* Status
* Updated
* Published
* Received
* Type
* Center
* Visibility
* Alias
* Experiment
* Sample
* Study
* Loaded
* Spots
* Bases
* Md5sum
* BioSample
* BioProject
* ReplacedBy

The key columns here are Accession, Submission, and Status.

The data in this file is replicated. A single submission may occur mutliple times, represented once for each of the accessions associated with it.

At the time of writing there were 27,838,771 entries (lines) in that file. However, there are only 1,413,223 unique submission IDs. 

From those 1,413,223 unique submission IDs, the `Status` field reports

* 1,290,528 live
* 161,652 suppressed
* 92,103 unpublished
* 10 withdrawn

(These numbers don't quite add up because there are some projects where the project maybe be live, but the runs or other parts of the data release may be suppressed or unpublished.)

# XML Metadata

The XML metadata is available for download from [ftp://ftp.ncbi.nlm.nih.gov/sra/reports/Metadata/](ftp://ftp.ncbi.nlm.nih.gov/sra/reports/Metadata/). There are daily files, and then once per month, or so, there is a complete release. 

For example, this file was downloaded:

```bash
curl -o NCBI_SRA_Metadata_Full.tgz ftp://ftp.ncbi.nlm.nih.gov/sra/reports/Metadata/NCBI_SRA_Metadata_Full_20180205.tar.gz
```

When you extract these files, you will get 1,000,000+ directories! Each directory is a single submission, and contains several files describing the data. I extract these using a command like: 

```bash
mkdir xml
tar -C xml/ -zxf NCBI_SRA_Metadata_Full.tar.gz
```

There are several [XML Schema Definition files](https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?view=xml_schemas) that define the data sets. Currently, there are `.xsd` files for:

1. SRA Common
2. SRA Submission
3. SRA Study
4. SRA Sample
5. SRA Experiment
6. SRA Run
7. SRA Analysis

# Converting the XML files to JSON

We batch process the XML files and convert them to JSON, using [a Python script](xml2json/xml_dir2json_random.py). This code uses the XML Schema Definition files to validate the XML files, and then dumps a single file per submission in JSON format.

This version chooses a file at random from the XML directory, checks to see if it has already been processed, and if not, it processes it. This allows us to run the code in parallel (using the awesome [GNU parallel](https://www.gnu.org/software/parallel/) and process lots of XML files all at once. For example, to process this code using 30 different processors, we can do:

```bash
echo "xml_dir2json_random.py -s $HOME/SRA/SRAdb/XML/Schemas/ -d xml -o json -m srr_sra_ids.tsv" > ./run_xml.sh
seq 1 30 | parallel ./run_xml.sh {}
```

This command creates a directory called `json` with three subdirectories, one each for `SRA`, `ERA`, `DRA`. Within those three directories, there are directories for each run, starting with the first three numbers. We use this structure because (a) it mirrors the structure at NCBI and elsewhere, and (b) breaking up the files into multiple subdirectories is much better for your filesystem. There are over 1,000,000 files, and so it takes commands like `ls` a long time to read the [inodes](http://www.grymoire.com/Unix/Inodes.html). By splitting the files out, we can more readily access and process them.


> *Tip:* If you have an SRA ID such as `SRR=SRA889255` you can access the appropriate file with, for example, `ls json/${SRR:0:3}/${SRR:0:6}/$SRR.json`.

This command also creates an *id mapping* file called `srr_sra_ids.tsv` that has two columns, the SRA submission ID (or ERA/DBA ID) and the SRA Run ID. The most common association we are looking for is from SRR -> SRA. For example, we usually know the SRR IDs associated with a sequence run, and would like to explore the metadata associated with that run. Alternatively, we know a sample we would like to get the DNA sequences associated with. This mapping provides that connection, and you can quickly look for either a run or a submission using `grep`.

In addition, we create a file called `XML_validation_errors.txt` that reports any improper XML data that does not match the XML Schema Defintions. 

We now have a directory with all the metadata as json objects that you can analyze in different ways. 

# Download preconverted JSON files

We strive to make the latest versions of this metadata available for [download from our website](https://edwards.sdsu.edu/data/sra/current.tar.gz). That tar archive contains the JSON files, arranged as described above, the SRA -> SRR mapping file, and a README.txt file describing the data.

# JSON

We have some [JSON](json/) parsing code to help you explore the data. Before you begin, however, take a look at the [json_examples](json_examples/) data directory. These are ten samples chosen completely at random from the August 2019 metadata to demonstrate the organization of the metadata there.

I also recommend using [jq](https://stedolan.github.io/jq/) for processing the data on the command line.

Here are a couple of examples from our [partie](https://github.com/linsalrob/partie) analysis of SRA datasets.

First , find all the submissions that are metagenomes or microbiomes using grep. You could also do this with the XML files, there is nothing specific about this grep and json.

```bash
egrep -rli 'metagenome|microbiome' json | perl -pe 's#json/##; s#.json##' > metagenomes.txt 
```

We now have a file, called `metagenomes.txt` that has one SRA submission per line where somewhere in the file it has the words `metagenome` or `microbiome`.

Now we can use [jq](https://stedolan.github.io/jq/) to extract just the run identifiers from these files:

```bash
cat metagenomes.txt | xargs -i jq -r "try .RUN[].IDENTIFIERS.PRIMARY_ID" json/{}.json > metagenome_runs.txt
```

In this command, we cat the file of IDs, and for each file, we use `jq` to parse the json data. We look for any `RUN` and from that pull the `IDENTIFIERS` entry, and then the `PRIMARY_ID` for that run. This prints out one `PRIMARY_ID` per line. The `try` in that command is a jq option that is basic error handling. We could add both a `try` and a `catch`, and use that to report on any JSON files that do not have a RUN associated with them, however, at the moment we don't care about those ... we just ignore them!

I don't know how to succinctly parse the XML to get this information (though you could probably do it with `grep`).


