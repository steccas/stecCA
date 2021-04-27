import os.path
import random
import string
from celery.schedules import crontab

import base64

_basedir = os.path.abspath(os.path.dirname(__file__))

# See the Lemur docs (https://lemur.readthedocs.org) for more information on configuration

LOG_LEVEL = str(os.environ.get('LOG_LEVEL', 'DEBUG'))
LOG_FILE = str(os.environ.get('LOG_FILE', '/home/lemur/.lemur/lemur.log'))
LOG_JSON = True

CORS = os.environ.get("CORS") == "True"
debug = os.environ.get("DEBUG") == "True"


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

REDIS_HOST = 'redis'
REDIS_PORT = 6379
REDIS_DB = 0
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}'
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
CELERY_IMPORTS = ('lemur.common.celery')
CELERYBEAT_SCHEDULE = {
    # All tasks are disabled by default. Enable any tasks you wish to run.
    # 'fetch_all_pending_acme_certs': {
    #     'task': 'lemur.common.celery.fetch_all_pending_acme_certs',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(minute="*"),
    # },
    # 'remove_old_acme_certs': {
    #     'task': 'lemur.common.celery.remove_old_acme_certs',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour=8, minute=0, day_of_week=5),
    # },
    # 'clean_all_sources': {
    #     'task': 'lemur.common.celery.clean_all_sources',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour=5, minute=0, day_of_week=5),
    # },
    # 'sync_all_sources': {
    #     'task': 'lemur.common.celery.sync_all_sources',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour="*/2", minute=0),
    #     # this job is running 30min before endpoints_expire which deletes endpoints which were not updated
    # },
    # 'sync_source_destination': {
    #     'task': 'lemur.common.celery.sync_source_destination',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour="*/2", minute=15),
    # },
    # 'report_celery_last_success_metrics': {
    #     'task': 'lemur.common.celery.report_celery_last_success_metrics',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(minute="*"),
    # },
    # 'certificate_reissue': {
    #     'task': 'lemur.common.celery.certificate_reissue',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour=9, minute=0),
    # },
    # 'certificate_rotate': {
    #     'task': 'lemur.common.celery.certificate_rotate',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour=10, minute=0),
    # },
    # 'endpoints_expire': {
    #     'task': 'lemur.common.celery.endpoints_expire',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour="*/2", minute=30),
    #     # this job is running 30min after sync_all_sources which updates endpoints
    # },
    # 'get_all_zones': {
    #     'task': 'lemur.common.celery.get_all_zones',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(minute="*/30"),
    # },
    'check_revoked': {
        'task': 'lemur.common.celery.check_revoked',
        'options': {
            'expires': 180
        },
        'schedule': crontab(hour=10, minute=0),
    }
    # 'enable_autorotate_for_certs_attached_to_endpoint': {
    #     'task': 'lemur.common.celery.enable_autorotate_for_certs_attached_to_endpoint',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour=10, minute=0),
    # }
    # 'notify_expirations': {
    #     'task': 'lemur.common.celery.notify_expirations',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour=10, minute=0),
    #  },
    # 'notify_authority_expirations': {
    #     'task': 'lemur.common.celery.notify_authority_expirations',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour=10, minute=0),
    # },
    # 'send_security_expiration_summary': {
    #     'task': 'lemur.common.celery.send_security_expiration_summary',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour=10, minute=0, day_of_week='mon-fri'),
    # }
}
CELERY_TIMEZONE = 'UTC'

SQLALCHEMY_ENABLE_FLASK_REPLICATED = False
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql://lemur:lemur@localhost:5432/lemur')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
SQLALCHEMY_POOL_RECYCLE = 499
SQLALCHEMY_POOL_TIMEOUT = 20

LEMUR_EMAIL = 'lemur@example.com'
LEMUR_SECURITY_TEAM_EMAIL = ['security@example.com']
LEMUR_SECURITY_TEAM_EMAIL_INTERVALS = [15, 2]
LEMUR_DEFAULT_EXPIRATION_NOTIFICATION_INTERVALS = [30, 15, 2]
LEMUR_EMAIL_SENDER = 'smtp'

# mail configuration
# MAIL_SERVER = 'mail.example.com'

PUBLIC_CA_MAX_VALIDITY_DAYS = 397
DEFAULT_VALIDITY_DAYS = 365

LEMUR_OWNER_EMAIL_IN_SUBJECT = False

LEMUR_DEFAULT_COUNTRY = str(os.environ.get('LEMUR_DEFAULT_COUNTRY', 'US'))
LEMUR_DEFAULT_STATE = str(os.environ.get('LEMUR_DEFAULT_STATE', 'California'))
LEMUR_DEFAULT_LOCATION = str(os.environ.get('LEMUR_DEFAULT_LOCATION', 'Los Gatos'))
LEMUR_DEFAULT_ORGANIZATION = str(os.environ.get('LEMUR_DEFAULT_ORGANIZATION', 'Example, Inc.'))
LEMUR_DEFAULT_ORGANIZATIONAL_UNIT = str(os.environ.get('LEMUR_DEFAULT_ORGANIZATIONAL_UNIT', ''))

LEMUR_DEFAULT_AUTHORITY = str(os.environ.get('LEMUR_DEFAULT_AUTHORITY', 'ExampleCa'))

LEMUR_DEFAULT_ROLE = 'operator'

ACTIVE_PROVIDERS = []
METRIC_PROVIDERS = []

# Authority Settings - These will change depending on which authorities you are
# using
current_path = os.path.dirname(os.path.realpath(__file__))

# DNS Settings

# exclude logging missing SAN, since we can have certs from private CAs with only cn, prod parity
LOG_SSL_SUBJ_ALT_NAME_ERRORS = False

ACME_DNS_PROVIDER_TYPES = {"items": [
    {
        'name': 'route53',
        'requirements': [
            {
                'name': 'account_id',
                'type': 'int',
                'required': True,
                'helpMessage': 'AWS Account number'
            },
        ]
    },
    {
        'name': 'cloudflare',
        'requirements': [
            {
                'name': 'email',
                'type': 'str',
                'required': True,
                'helpMessage': 'Cloudflare Email'
            },
            {
                'name': 'key',
                'type': 'str',
                'required': True,
                'helpMessage': 'Cloudflare Key'
            },
        ]
    },
    {
        'name': 'dyn',
    },
    {
        'name': 'ultradns',
    },
]}

# Authority plugins which support revocation
SUPPORTED_REVOCATION_AUTHORITY_PLUGINS = ['acme-issuer']
CFSSL_URL ="http://ca.stecca.lan:8888"
CFSSL_ROOT ="""-----BEGIN CERTIFICATE-----
MIICBjCCAaygAwIBAgIUYf414VsF8l2wveqhAgs2EQVDLC0wCgYIKoZIzj0EAwIw
YDELMAkGA1UEBhMCSVQxETAPBgNVBAcTCEFjaXJlYWxlMRkwFwYDVQQKExBMdWNh
IFN0ZWNjYW5lbGxhMQwwCgYDVQQLEwNDU0QxFTATBgNVBAMTDFN0ZWMgUm9vdCBD
QTAgFw0yMTA0MjcxNzUwMDBaGA8yMDUxMDQyMDE3NTAwMFowYDELMAkGA1UEBhMC
SVQxETAPBgNVBAcTCEFjaXJlYWxlMRkwFwYDVQQKExBMdWNhIFN0ZWNjYW5lbGxh
MQwwCgYDVQQLEwNDU0QxFTATBgNVBAMTDFN0ZWMgUm9vdCBDQTBZMBMGByqGSM49
AgEGCCqGSM49AwEHA0IABOSClgSS0Im2P//ZlVrBPhGmXI39F6Y0exSnajBT999D
d+QQHVSTfUJlvaG/hqVPWiT1QyOMeJofH7xtp1/OKk+jQjBAMA4GA1UdDwEB/wQE
AwIBBjAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBTh9FdhT50+vXRLV0IuAZ1x
F3oVLDAKBggqhkjOPQQDAgNIADBFAiANIzRvJbi+DMIOWMS2wD9mt5Fj9boTEQe3
NWOXz8N5FwIhAOW03Zaafnhn0qfg340hH8q7MCrvmtECAxUyRhKbEnC5
-----END CERTIFICATE-----"""
CFSSL_INTERMEDIATE ="""-----BEGIN CERTIFICATE-----
MIICmTCCAj+gAwIBAgIUN/qEOCAKJItuPoqATw9KWWjDzxAwCgYIKoZIzj0EAwIw
YDELMAkGA1UEBhMCSVQxETAPBgNVBAcTCEFjaXJlYWxlMRkwFwYDVQQKExBMdWNh
IFN0ZWNjYW5lbGxhMQwwCgYDVQQLEwNDU0QxFTATBgNVBAMTDFN0ZWMgUm9vdCBD
QTAeFw0yMTA0MjcxNzUwMDBaFw0yNDA0MjYxNzUwMDBaMGgxCzAJBgNVBAYTAklU
MREwDwYDVQQHEwhBY2lyZWFsZTEZMBcGA1UEChMQTHVjYSBTdGVjY2FuZWxsYTEM
MAoGA1UECxMDQ1NEMR0wGwYDVQQDExRTdGVjIEludGVybWVkaWF0ZSBDQTBZMBMG
ByqGSM49AgEGCCqGSM49AwEHA0IABBzH0hqIxtzK+30Xb2PVKgFdOPnzgsuWoG5u
RITUXSFNr9Ohyy7lLXC6e4HlnmaN+/9lmlaMKuTVA3JqI9YJqTCjgc4wgcswDgYD
VR0PAQH/BAQDAgEGMBIGA1UdEwEB/wQIMAYBAf8CAQAwHQYDVR0OBBYEFH5tiFd2
iUUWbbwPekhvm3hteesuMB8GA1UdIwQYMBaAFOH0V2FPnT69dEtXQi4BnXEXehUs
MDUGCCsGAQUFBwEBBCkwJzAlBggrBgEFBQcwAYYZaHR0cDovL2NhLnN0ZWNjYS5s
YW46ODg4OTAuBgNVHR8EJzAlMCOgIaAfhh1odHRwOi8vY2Euc3RlY2NhLmxhbjo4
ODg4L2NybDAKBggqhkjOPQQDAgNIADBFAiEAkehXhyBDJlWLghkuVCkBexa7etDw
rgrVIykMasaDTDkCIHGotGdUC+wWNcWGSowDc3T2xkB9prmVr4sFwR1YhOxg
-----END CERTIFICATE-----"""
