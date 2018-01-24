#!/bin/bash
# This script will magicblast a list of SRA accessions and create
# a .csv of read lengths and alignment scores

NANO_HOME="$(pwd)"

while getopts ":d:m:n:o:s:w:" o; do
    case "${o}" in
        d)
	    BLAST_DB_NAME=${OPTARG}
	    ;;
	m)
	    MAGIC_BLAST_DIR=${OPTARG}
	    ;;
	n)
	    NANO_HOME=${OPTARG}
	    ;;
	o)
	    OUTDIR=${OPTARG}
	    ;;
	s)
	    SRA_ACCS=${OPTARG}
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

while read SRA_ACC; do
  echo $SRA_ACC
  "$MAGIC_BLAST_DIR"/bin/magicblast -sra "$SRA_ACC" -db "$BLAST_DB_NAME" -gapextend 0 >"$SRA_ACC"_magicblast.sam 
done <"$SRA_ACCS"

# outputs a csv with alignment score and read lengths
python "$NANO_HOME"/cutoff_design/cutoff_plots.py >sra_accessions.sam_statistics.csv

# viz script
#Rcmd ~/kevin/NanoporeMapper/cutoff_desing/score_length_visualization.R
