import sys
import argparse
from textwrap import dedent


def check_cutoff(seq_read, score_cutoff, match_behaviour, found_score):
    length = len(seq_read[9])
    score_cutoff_list = score_cutoff.split(",")
    score_cutoff_list = [float(i) for i in score_cutoff_list]
    if len(score_cutoff_list) == 2:
        target_score = (score_cutoff_list[0]*length) + score_cutoff_list[1]
    else:
        target_score = score_cutoff_list[0]
    if match_behaviour == "include":
        if found_score >= target_score:
            return True
        return False
    if match_behaviour == "exclude":
        if found_score <= target_score:
            return True
        return False


def read_stdin(score_cutoff, match_behaviour):
    """
    Read stdin() and check whether
    a) line is a read or not
    b) if a read check cutoff value
    """
    read_name = None
    score_sum = 0
    read_list = []
    for line in sys.stdin:
        la = line.strip().split("\t")
        if (len(la)) == 14:
            # yep, this is a read
            if read_name:
                # current read is the same as line before
                if la[0] == read_name:
                    score_sum += int(la[12].split(":")[-1])
                    read_list.append(line)
                else:
                    if check_cutoff(read_list[-1].split("\t"),
                                    score_cutoff,
                                    match_behaviour,
                                    score_sum):
                        # print all the data in read_list
                        for i in read_list:
                            sys.stdout.write(i)
                            sys.stdout.flush()
                    read_name = la[0]
                    read_list = [line]
                    score_sum = int(la[12].split(":")[-1])
            # first read!
            else:
                read_name = la[0]
                score_sum += int(la[12].split(":")[-1])
                read_list.append(line)
        # unmapped read
        elif la[2] == "*":
            if match_behaviour == "exclude":
                sys.stdout.write(line)
                sys.stdout.flush()

        else:
            sys.stdout.write(line)
            sys.stdout.flush()


def __main__():
    try:
        description = dedent("""
        This takes a streamed SAM file as input and filters alignments based
        on the alignment score. The score can be given either as a uniform
        score or as a linear function of the form score = a * Length + b
        where Length describes the read length.
        You can also decide whether reads that fulfill your score threshold
        should be included or excluded.
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
        match_help = dedent("""Select whether the reads matching the threshold
        should be included or excluded. If included is chosen only matching
        reads are kept. If excluded is chosen only the reads _not_ matching
        the treshold are kept. Valid options: 'include' and 'exclude'.
        """)
        parser.add_argument('-m', '--matches', default="include",
                            help=match_help)

        args = parser.parse_args()
        if args.matches not in ['include', 'exclude']:
            sys.stderr.write("Wrong Argument.\
            --matches needs to be 'include' or 'exclude'\n")
        read_stdin(args.score, args.matches)

    except BrokenPipeError:
        # pipe error (e.g., when head is used)
        sys.stderr.close()
        sys.stdout.close()
        exit(0)


if __name__ == "__main__":
    __main__()
