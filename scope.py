SCOPE_NAME = "hawthorn"


def create_name(name):
    return '{scope}.{name}'.format(scope=SCOPE_NAME, name=name)


queue_dict = {
    "log": create_name('log'),
    "jenkins": create_name('jenkins'),
    "result": create_name('result'),
    "mail": create_name('mail'),
}

exchange_dict = {
    "build": create_name('build'),
    "built": create_name('built'),
}
