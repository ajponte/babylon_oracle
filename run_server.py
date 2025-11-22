import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from dotenv import load_dotenv
import uvicorn
from oracle_server.config.hashicorp import OpenBaoApiClient

load_dotenv()

FLASK_PORT = 5003
FLASK_HOST = '0.0.0.0'

# Secrets
SQLALCHEMY_DB_HOST = 'localhost'
SQLALCHEMY_DB_PORT = '5433'
SQLALCHEMY_DB_USER = 'user'
SQLALCHEMY_DB_PASS = 'password'
MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_USERNAME = 'admin'
MONGO_PASSWORD = 'password'

def _set_secrets():
    openbao = OpenBaoApiClient()
    openbao.add_secret_value(
        path=os.environ.get('OPENBAO_SECRETS_PATH'),
        secret={
            'MONGO_DB_HOST': MONGO_HOST,
            'MONGO_DB_PORT': MONGO_PORT,
            'MONGO_DB_USER': MONGO_USERNAME,
            'MONGO_DB_PASSWORD': MONGO_PASSWORD
        }
    )
    print('Done writing mock secrets!')

_set_secrets()


def main():
    """
    Main function to parse command line arguments and run the Flask application.
    """
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    # -h conflicts, so using -n for hostname flag instead of -h
    parser.add_argument('-n', dest='host', default=FLASK_HOST, help="Hostname")
    parser.add_argument('-p', dest='port', type=int, default=FLASK_PORT, help="Port")

    args = parser.parse_args()

    uvicorn.run(
        "oracle_server.app:create_app",
        host=args.host,
        port=args.port,
        factory=True,
        reload=True,
    )

if __name__ == '__main__':
    main()