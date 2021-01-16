def format_dict(dict_: dict) -> str:
    """Method to take a dictionary and
    return a string of comma seperated key, value
    in below format

    >>> d = {"key1": "value1", "key2": "value2"}
    >>> s = format_dict(d)
    >>> assert s == "key1=value1, key2=value2"
    """    
    pairs = []
    for key, value in dict_.items():
        pairs.append(f"{key}={value}")

    return ', '.join(pairs)
