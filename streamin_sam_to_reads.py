import sys

import argparse
from textwrap import dedent


def write_fasta_stdout(sam_row):
    """
    take SAM row and convert it to fasta.
    """
    sys.stdout.write(">{}\n".format(sam_row[0]))
    sys.stdout.write("{}\n".format(sam_row[9]))
    sys.stdout.flush()


def write_fastq_stdout(sam_row):
    """
    take SAM row and convert it to fastq.
    This doesn't work with magicblast 1.4.0 or earlier due to a lack
    of quality scores
    """
    sys.stdout.write("@{}\n".format(sam_row[0]))
    sys.stdout.write("{}\n".format(sam_row[9]))
    sys.stdout.write("+{}\n".format(sam_row[0]))
    sys.stdout.write("{}\n".format(sam_row[10]))
    sys.stdout.flush()


def read_stdin(format='fasta'):
    """
    Read stdin() and check whether
    a) line is a read or not
    b) if a read: convert to fasta/fastq
    """
    last_written_read = ""
    for line in sys.stdin:
        la = line.strip().split("\t")
        if (len(la)) == 14 and last_written_read != la[0]:
            # yep, this is a read
            if format == "fasta":
                write_fasta_stdout(la)
            if format == "fastq":
                write_fastq_stdout(la)
            last_written_read = la[0]
        else:
            pass


def __main__():

    try:
        description = dedent("""
        This takes a streamed SAM file as input and converts the output
        into a fasta or fastq file.
        """)
        parser = argparse.ArgumentParser(
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('-f', '--format', default="fasta",
                            help=('Output format. Can be '
                                  '"fasta" or "fastq"'))

        args = parser.parse_args()
        if args.format not in ['fasta', 'fastq']:
            sys.stderr.write("Wrong Argument.\
 Format needs to be 'fasta' or 'fastq'\n")
            sys.exit(1)
        read_stdin(args.format)

    except BrokenPipeError:
        # pipe error (e.g., when head is used)
        sys.stderr.close()
        sys.stdout.close()
        exit(0)


if __name__ == "__main__":
    __main__()
