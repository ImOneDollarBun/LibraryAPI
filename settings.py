from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    class App:
        API_PREFIX = '/api'
        APP_HOST = '127.0.0.1'
        APP_PORT = 8000

    class DB:
        DB_NAME = os.getenv('DB_NAME')
        DB_HOST = os.getenv('DB_HOST')
        DB_PORT = os.getenv('DB_PORT')
        DB_USERNAME = os.getenv('DB_USERNAME')
        DB_PASSWORD = os.getenv('DB_PASSWORD')

        DB_URL = (f'postgresql+psycopg2://{DB_USERNAME}'
                  f':{DB_PASSWORD}'
                  f'@{DB_HOST}'
                  f':{DB_PORT}'
                  f'/{DB_NAME}')

    class auth_jwt:
        algorithm = 'RS256'
        public_key_path = os.path.join('app', 'utils', 'certs', 'public_key.pem')
        private_key_path = os.path.join('app', 'utils', 'certs', 'private_key.pem')


settings = Settings()
