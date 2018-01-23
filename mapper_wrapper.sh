#!/bin/bash

MAGIC_BLAST_DIR=/home/ubuntu/bastian/ncbi-magicblast-1.3.0
WORK_DIR="$(pwd)"

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
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

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
