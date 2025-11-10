from urllib.parse import quote
from typing import TypedDict
import json
import logging

class ConfigDict(TypedDict):
    id: str
    pw: str
    host: str
    port: str
    dbName: str
    dbSchema: str
    poolSize: int
    maxOverflow: int
    poolRecycle: int
    poolPrePing: bool

def GenerateEmptyConfigDict() -> ConfigDict:
    return {
        "id": "", 
        "pw": "", 
        "host": "", 
        "port": "", 
        "dbName": "", 
        "dbSchema": "", 
        "poolSize": -1, 
        "maxOverflow": -1, 
        "poolRecycle": -1, 
        "poolPrePing": False
    }

class DbConfigManager:
    def __init__(self, path: str='db-config-local-gathering.json'):
        self.__config: ConfigDict = GenerateEmptyConfigDict()
        self.__load_config(path)

    def __load_config(self, path: str) -> None:
        try:
            with open(path, 'r', encoding='utf-8') as config_file:
                self.__config = json.load(config_file)
                print(self.__config)
        except OSError as os_error:
            logging.critical(f'config file 파일을 오픈하는 과정에서 에러 발생. {os_error}')
            self.__config = GenerateEmptyConfigDict()
            self.__is_valid = False

    def is_valid(self):
        return self.__is_valid
    
    def get_config(self) -> ConfigDict:
        return self.__config
    
    def get_encode_pw(self) -> str:
        return quote(self.__config["pw"])
