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


## Comparing bwa and magicblast

We downloaded the read sets and reference genomes for E. coli ST131 (`SRR5629778` and `HG941718.1`) and Homo sapiens (`SRR2848544` and `GRCh38.p7 Primary Assembly`). Each read set was aligned against its own reference genome and the opposing reference using `bwa 0.7.12-r1039` and `ncbi-magicblast-1.3.0`.

### Self-comparison

#### E.coli

#### Homo sapiens

`bwa`:

**mapped reads**
```
samtools view -bS SRR2848544_bwa.sam |samtools view -F 4 -|cut -f 1|sort|uniq |wc -l
2910
```

**unmapped reads**
```
samtools view -bS SRR2848544_bwa.sam |samtools view -f 4 -|cut -f 1|sort|uniq |wc -l
2
```

`magicblast`:

**mapped reads**
```
samtools view -bS SRR2848544_magicblast_default.sam |samtools view -F 4 -|cut -f 1|sort|uniq |wc -l
2912
```

**unmapped reads**
```
samtools view -bS SRR2848544_magicblast_default.sam |samtools view -f 4 -|cut -f 1|sort|uniq |wc -l
2
```
