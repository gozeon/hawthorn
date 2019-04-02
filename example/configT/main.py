import os

from config import Config

BASE_ROOT = os.path.dirname(os.path.realpath(__file__))
Config.init_config(os.path.join(BASE_ROOT, 'config.ini'))

# output: localhost
os.environ['COMMON_HOST'] = 'localhost'
host_address = Config.get_or_else('common', 'HOST', '127.0.0.1')
print(host_address)

# output: 0.0.0.0
local_address = Config.get_or_else('common', 'BIND_ADDRESS', '127.0.0.1')
print(local_address)

# output: True False False True
a = Config.getboolean_or_else('test', 'A', False)
b = Config.getboolean_or_else('test', 'B', False)
c = Config.getboolean_or_else('test', 'C', False)
d = Config.getboolean_or_else('test', 'D', False)
print(a, b, c, d)

# output: 5242880
MAX_IMAGE_SIZE = Config.getint_or_else('default', 'MAX_IMAGE_SIZE', 2)
print(MAX_IMAGE_SIZE)

# output: 20.0
TEST_TIMEOUT = Config.getfloat_or_else('test', 'TEST_TIMEOUT', 2.0)
print(TEST_TIMEOUT)
