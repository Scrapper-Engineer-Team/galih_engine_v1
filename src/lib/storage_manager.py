import json
import s3fs
import configparser
import os
from loguru import logger
import greenstalk

class StorageManager:
    def __init__(self, key=None, secret=None, ip=None, port=None, config_path=None, beanstalk_ip=None, beanstalk_port=None):
        config = configparser.ConfigParser()
        if config_path:
            config.read(config_path)
        else:
            config.read(os.path.join(os.path.dirname(__file__), '../../config.ini'))

        self.key = key or config.get('s3', 'key')
        self.secret = secret or config.get('s3', 'secret')
        self.ip = ip or config.get('s3', 'ip')
        self.port = port or config.get('s3', 'port')
        self.beanstalk_ip = config.get('beanstalk', 'beanstalk_ip')
        self.beanstalk_port = config.get('beanstalk', 'beanstalk_port')

        self.beanstalk_client = greenstalk.Client((self.beanstalk_ip, int(self.beanstalk_port)))

        self.s3 = s3fs.S3FileSystem(
            key=self.key,
            secret=self.secret,
            client_kwargs={'endpoint_url': f'http://{self.ip}:{self.port}'}
        )

    def save(self, path_file, response):
        if path_file.startswith('s3://'):
            with self.s3.open(path_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.success(f'Downloaded to s3 : {path_file}')
        else:
            directory = os.path.dirname(path_file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f'Created directory: {directory}')
            
            with open(path_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.success(f'Downloaded to local : {path_file}')

    def save_json(self, path_file, data):
        if path_file.startswith('s3://'):
            with self.s3.open(path_file, 'w') as f:
                f.write(json.dumps(data, indent=4, ensure_ascii=False))
            logger.success(f'Saved JSON to s3 :{path_file}')
        else:
            directory = os.path.dirname(path_file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f'Created directory: {directory}')
            
            with open(path_file, 'w') as f:
                f.write(json.dumps(data, indent=4, ensure_ascii=False))
            logger.success(f'Saved JSON to local :{path_file}')

    def send_beanstalk(self, data, tube):
        try:
            logger.info(f"Sending data to Beanstalk tube: {tube}")
            self.beanstalk_client.use(tube)
            self.beanstalk_client.put(json.dumps(data))
            logger.info(f"Successfully sent data to Beanstalk tube: {tube}")
        except Exception as e:
            logger.error(f"Failed to send data to Beanstalk: {str(e)}")

    def get_beanstalk(self, tube):
        try:
        # Membuka koneksi ke Beanstalk menggunakan context manager
            with greenstalk.Client((self.beanstalk_ip, self.beanstalk_port), watch=tube) as greenstalk_client:
                return greenstalk_client
        except greenstalk.ConnectionError as e:
            print(f"Error connecting to Beanstalk at {self.beanstalk_ip}:{self.beanstalk_port} - {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None