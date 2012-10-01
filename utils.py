import re
alphanum_pattern = re.compile('[\W_]+')


def reduce_to_alphanumeric(some_str):
    return alphanum_pattern.sub('',some_str)
