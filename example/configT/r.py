from configparser import ConfigParser, ExtendedInterpolation

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('config.ini')

print(config['DEFAULT']['AWS_DEFAULT_REGION'])
print(config['TEST']['TEST_TIMEOUT'])
print(config['TEST']['URL'])
b = config['TEST'].getboolean('B')
print(type(b))
print(b)
