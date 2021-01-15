def format_dict(dict_: dict) -> str:
    pairs = []
    for key, value in dict_.items():
        pairs.append(f"{key}={value}")

    return ', '.join(pairs)
