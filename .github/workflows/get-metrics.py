import logging
import os

import google
from google.analytics.data_v1beta import BetaAnalyticsDataClient

PRIVATE_KEY_ID = os.environ.get('PRIVATE_KEY_ID')
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')

credentials_dict = {
    'type': 'service_account',
    'project_id': 'cisl-vast-pythia',
    'private_key_id': PRIVATE_KEY_ID,
    'private_key': PRIVATE_KEY,
    'client_email': 'pythia-metrics-api@cisl-vast-pythia.iam.gserviceaccount.com',
    'client_id': '113402578114110723940',
    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
    'token_uri': 'https://oauth2.googleapis.com/token',
    'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
    'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/pythia-metrics-api%40cisl-vast-pythia.iam.gserviceaccount.com',
    'universe_domain': 'googleapis.com',
}

try:
    client = BetaAnalyticsDataClient.from_service_account_info(credentials_dict)
except google.auth.exceptions.MalformedError as e:
    print('Malformed Error:', repr(e))
    logging.error('Malformed Error:', repr(e))
    logging.error('Credentials dict:', credentials_dict)

    print(credentials_dict)
