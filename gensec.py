import os.path
import random
import string
import base64

def get_random_secret(length):
    secret_key = ''.join(random.choice(string.ascii_uppercase) for x in range(round(length / 4)))
    secret_key = secret_key + ''.join(random.choice("~!@#$%^&*()_+") for x in range(round(length / 4)))
    secret_key = secret_key + ''.join(random.choice(string.ascii_lowercase) for x in range(round(length / 4)))
    return secret_key + ''.join(random.choice(string.digits) for x in range(round(length / 4)))


# This is the secret key used by Flask session management
SECRET_KEY = repr(os.environ.get('SECRET_KEY', get_random_secret(32).encode('utf8')))

# You should consider storing these separately from your config
LEMUR_TOKEN_SECRET = repr(os.environ.get('LEMUR_TOKEN_SECRET',
                                         base64.b64encode(get_random_secret(32).encode('utf8'))))
# This must match the key for whichever DB the container is using - this could be a dump of dev or test, or a unique key
LEMUR_ENCRYPTION_KEYS = repr(os.environ.get('LEMUR_ENCRYPTION_KEYS',
                                            base64.b64encode(get_random_secret(32).encode('utf8')).decode('utf8')))

names = ['SECRET_KEY', 'LEMUR_TOKEN_SECRET', 'LEMUR_ENCRYPTION_KEYS']

for name in names:
    text_file = open("./lemur_keys/" + name, "w")
    n = text_file.write(globals()[name])
    text_file.close()