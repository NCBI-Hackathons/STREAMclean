import sys


def write_fasta_stdout(sam_row):
    """
    take SAM row and convert it to fastq.
    """
    sys.stdout.write(">{}\n".format(sam_row[0]))
    sys.stdout.write("{}\n".format(sam_row[9]))
    sys.stdout.flush()


def read_stdin():
    """
    Read stdin() and check whether
    a) line is a read or not
    b) if a read: convert to fastq
    """
    for line in sys.stdin:
        la = line.strip().split("\t")
        if (len(la)) == 14:
            # yep, this is a read
            write_fasta_stdout(la)
        else:
            pass


def __main__():
    try:
        read_stdin()

    except BrokenPipeError:
        # pipe error (e.g., when head is used)
        sys.stderr.close()
        sys.stdout.close()
        exit(0)



if __name__ == "__main__":
    __main__()
