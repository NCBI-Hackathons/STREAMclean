import sys


def check_cutoff(seq_read):
    length = len(seq_read[9])
    found_score = int(seq_read[12].split(":")[-1])
    target_score = (0.001353*length) + 25
    if found_score >= target_score:
        return True
    return False


def read_stdin():
    """
    Read stdin() and check whether
    a) line is a read or not
    b) if a read check cutoff value
    """
    for line in sys.stdin:
        la = line.strip().split("\t")
        if (len(la)) == 14:
            # yep, this is a read
            if check_cutoff(la):
                sys.stdout.write(line)
        else:
            # todo: this should contain the output for the header
            # lines
            sys.stdout.write(line)


def __main__():
    read_stdin()


if __name__ == "__main__":
    __main__()
