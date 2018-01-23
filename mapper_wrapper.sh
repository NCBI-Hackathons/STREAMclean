#!/bin/bash

MAGIC_BLAST_DIR=/home/ubuntu/bastian/ncbi-magicblast-1.3.0
WORK_DIR="$(pwd)"
programname=$0

function usage {
	echo "usage:  $programname [-d existingDBName] [-e excludeList] [-i includeList] [-m  magicBlastDir] [-o outDir] [-w workDir]"
	echo "  -d existingDBName	Specify an existing database for makeblast to look at, to avoid downloading genomes."
	echo "  -e excludeList	Blacklist of taxonomy indicators - magicBlast will produce only [pieces] that are not included in these genomes."
	echo "  -i includeList	Whitelist of taxonomy indicators - magicBlast will produce only [pieces] that are included in these genomes."
	echo "			Blacklist and whitelist should be of the following format: [Add format options]."
	echo ""
	echo "  -m magicBlastDir	Specify the directory that contains the bin/magicblast - default is "$WORK_DIR
	echo "  -o outDir		Specify the directory for output. [What goes here?]"
	echo "  -w workDir		Specify the working directory to create the genome database in - default is the current directory."
}

if [ $# -eq 0 ]; then
	usage
	exit 0
fi


while getopts ":d:e:i:m:o:w:" o; do
    case "${o}" in
        d)
	    BLAST_DB_NAME=${OPTARG}
	    ;;
	e)
            EXCLUDE_TAX=${OPTARG}
            ;;
        i)
            INCLUDE_TAX=${OPTARG}
            ;;
	m)
	    MAGIC_BLAST_DIR=${OPTARG}
	    ;;
	o)
	    OUTDIR=${OPTARG}
	    ;;
	w)
	    WORK_DIR=${OPTARG}
	    ;;
	:)
	   echo  "Invalid option: $OPTARG requires an argument"
	   usage
	   exit 0
	   ;;
        \?)
            usage
	    exit 0
            ;;
    esac
done
shift $((OPTIND-1))

# nice validation to do:  Require exactly one of d, e, i  flags

if [ ! -d "$WORK_DIR" ]; then
  echo "$WORK_DIR" does not exist - exiting.
  exit 0
fi

echo combined fasta and db files will be in this working directory: "$WORK_DIR"
echo "$BLAST_DB_NAME"

# ncbi-genome-download will be a dependency
#ncbi-genome-download -format fasta "$EXCLUDE_TAX",""$INCLUDE_TAX
# for testing
ncbi-genome-download --format fasta --taxid 199310 bacteria
wait

# concat the FASTA files (currently only working with FASTA format)
find refseq/ -name '*.fna.gz' | xargs zcat >>"$WORK_DIR"/"$BLAST_DB_NAME".fna
# I couldn't get makeblastdb accept gzipped FASTAs, uncomment when we alter the makeblastdb command to accept gzip.
# find refseq/ -name '*.fna.gz' | xargs cat >"$WORK_DIR"/"$BLAST_DB_NAME".fna.gz

# build the magic-blast database
"$MAGIC_BLAST_DIR"/bin/makeblastdb -in "$WORK_DIR"/"$BLAST_DB_NAME".fna -dbtype nucl -parse_seqids -out "$BLAST_DB_NAME"

# magic-blast alignments

# filter magic-blasted reads

# use samtools to combine results

# output 
