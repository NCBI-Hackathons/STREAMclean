# NanoporeMapper
A simple command line tool to map nanopore reads with high accuracy


## example call to download human ref genome

`ncbi-genome-download -F fasta -t 9606 -R reference vertebrate_mammalian`
(c.f. https://github.com/kblin/ncbi-genome-download)

## template script to chain some commands together  
`./mapper_wrapper.sh -d test1`

This will:
1. Download specified reference genomes using the [ncbi-genome-download package](https://github.com/kblin/ncbi-genome-download).
2. Create a [magic-blast](https://ncbi.github.io/magicblast/) database of the collected reference genomes.

