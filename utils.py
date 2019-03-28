def upper_key_dict(d):
    """
    字典 key 大写
    :param d: dict {"a": 1}
    :return:  dict {"A": 1}
    """
    return dict((k.upper(), v) for k, v in d.items())
