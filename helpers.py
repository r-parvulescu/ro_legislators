"""Handy helper functions."""


def deduplicate_list_of_lists(list_of_lists):
    """
    Remove duplicate rows from table as list of lists quicker than list comparison: turn all rows to strings,
    put them in a set, them turn set elements to list and add them all to another list.

    :param list_of_lists: what it sounds like
    :return list of lists without duplicate rows (i.e. duplicate inner lists)
    """
    # inner list comprehension turns everything to a string to avoid concat errors, e.g. string + int
    uniques = set(['|'.join([str(entry) for entry in row]) for row in list_of_lists])
    return [row.split('|') for row in uniques]
