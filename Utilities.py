def chunks(my_list: list, columns: int) -> list:
    """
    Adapted from https://stackoverflow.com/a/1751478
    :param my_list: start list
    :param columns: number of columns per list
    :return: list of lists that have <columns> of max element
    """
    return [my_list[i:i + columns] for i in range(0, len(my_list) or 1, columns)]
