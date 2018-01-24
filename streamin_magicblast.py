import sys
import argparse
from textwrap import dedent


def check_cutoff(seq_read, score_cutoff):
    length = len(seq_read[9])
    found_score = int(seq_read[12].split(":")[-1])
    score_cutoff_list = score_cutoff.split(",")
    score_cutoff_list = [float(i) for i in score_cutoff_list]
    if len(score_cutoff_list) == 2:
        target_score = (score_cutoff_list[0]*length) + score_cutoff_list[1]
    else:
        target_score = score_cutoff_list[0]
    if found_score >= target_score:
        return True
    return False


def read_stdin(score_cutoff):
    """
    Read stdin() and check whether
    a) line is a read or not
    b) if a read check cutoff value
    """
    for line in sys.stdin:
        la = line.strip().split("\t")
        if (len(la)) == 14:
            # yep, this is a read
            if check_cutoff(la, score_cutoff):
                sys.stdout.write(line)
                sys.stdout.flush()
        else:
            # todo: this should contain the output for the header
            # lines
            sys.stdout.write(line)
            sys.stdout.flush()


def __main__():
    try:
        description = dedent("""
        This takes a streamed SAM file as input and filters alignments based
        on the alignment score. The score can be given either as a uniform
        score or as a linear function of the form score = a * Length + b
        where Length describes the read length
        """)
        parser = argparse.ArgumentParser(
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        score_help = dedent("""Score, can be given as single number or as a linear
        formula as described by 'score = a * Length + b'. If you want to give a
        formula provide the a & b as '--score a,b'
        """)
        parser.add_argument('-s', '--score', default="0.001353,25",
                            help=score_help)

        args = parser.parse_args()
        read_stdin(args.score)

    except BrokenPipeError:
        # pipe error (e.g., when head is used)
        sys.stderr.close()
        sys.stdout.close()
        exit(0)


if __name__ == "__main__":
    __main__()
