import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from oracle_server.app import create_app
from oracle_server.config.hashicorp import OpenBaoApiClient

FLASK_PORT = 5003
FLASK_HOST = '0.0.0.0'

DEFAULT_BAO_ADDRESS = 'http://127.0.0.1:8200'
DEFAULT_BAO_VAULT_TOKEN = 'dev-only-token'
SECRETS_PATH = 'test'

SQLALCHEMY_DB_ENGINE = 'postgresql'
SQLALCHEMY_DATABASE_NAME = 'babylon'
MONGO_DATABASE_NAME = ''

# Secrets
SQLALCHEMY_DB_HOST = 'localhost'
SQLALCHEMY_DB_PORT = '5433'
SQLALCHEMY_DB_USER = 'user'
SQLALCHEMY_DB_PASS = 'password'
MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_USERNAME = 'admin'
MONGO_PASSWORD = 'password'

os.environ['BAO_ADDR'] = DEFAULT_BAO_ADDRESS
os.environ['OPENBAO_SECRETS_PATH'] = SECRETS_PATH
os.environ['VAULT_TOKEN'] = DEFAULT_BAO_VAULT_TOKEN
os.environ['SQLALCHEMY_INIT_TABLES'] = "True"
os.environ['SQLALCHEMY_DATABASE_NAME'] = SQLALCHEMY_DATABASE_NAME
os.environ['MONGO_DATABASE_NAME'] = MONGO_DATABASE_NAME
os.environ['SQLALCHEMY_DB_ENGINE'] = SQLALCHEMY_DB_ENGINE
os.environ['LOG_LEVEL'] = 'DEBUG'
os.environ['LOG_TYPE'] = 'stream'

def main():
    """
    Main function to parse command line arguments and run the Flask application.
    """
    def _set_secrets():
        openbao = OpenBaoApiClient()
        openbao.add_secret_value(
            path=SECRETS_PATH,
            secret={
                'DB_HOST': SQLALCHEMY_DB_HOST,
                'DB_PORT': SQLALCHEMY_DB_PORT,
                'DB_USERNAME': SQLALCHEMY_DB_USER,
                'DB_PASSWORD': SQLALCHEMY_DB_PASS,
                'MONGO_PORT': MONGO_PORT,
                'MONGO_HOST': MONGO_HOST,
                'MONGO_USERNAME': MONGO_USERNAME,
                'MONGO_PASSWORD': MONGO_PASSWORD
            }
        )
        print('Done writing mock secrets!')
    _set_secrets()
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    # -h conflicts, so using -n for hostname flag instead of -h
    parser.add_argument('-n', dest='host', default=FLASK_HOST, help="Hostname")
    parser.add_argument('-p', dest='port', type=int, default=FLASK_PORT, help="Port")

    args, extras = parser.parse_known_args()

    app = create_app()

    app.run(host=args.host, port=args.port)

if __name__ == '__main__':
    main()
