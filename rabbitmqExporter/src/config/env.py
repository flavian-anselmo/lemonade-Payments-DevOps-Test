import configparser
class Config:
    @staticmethod
    def load_config(file_path='config.conf'):
        config = configparser.ConfigParser()
        config.read(file_path)
        exporter_port = config.getint('exporter','EXPORTER_PORT',fallback='9125')
        rabbitmq_host = config.get('rabbitmq','RABBITMQ_HOST',fallback='rabbitmq')
        rabbitmq_user = config.get('rabbitmq','RABBITMQ_USER',fallback='admin')
        rabbitmq_password = config.get('rabbitmq','RABBITMQ_PASSWORD',fallback='password123')
        rabbitmq_api_port = config.get('rabbitmq','RABBITMQ_API_PORT',fallback='15672')


        return {
            'EXPORTER_PORT': exporter_port,
            'RABBITMQ_HOST':rabbitmq_host,
            'RABBITMQ_USER': rabbitmq_user,
            'RABBITMQ_PASSWORD': rabbitmq_password,
            'RABBITMQ_API_PORT': rabbitmq_api_port
        }

config = Config.load_config()

# env variable set up 
EXPORTER_PORT = config['EXPORTER_PORT']
RABBITMQ_HOST = config['RABBITMQ_HOST']
RABBITMQ_USER = config['RABBITMQ_USER']
RABBITMQ_PASSWORD = config['RABBITMQ_PASSWORD']
RABBITMQ_API_PORT = config['RABBITMQ_API_PORT']