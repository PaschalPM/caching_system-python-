from os import getenv, getcwd, unlink
from os.path import join, abspath, dirname, getctime, exists
from time import time
import re
from json import dump, load
from glob import glob
from uuid import uuid4

class Cache:

    __key = ''
    __expiry = 60
    __cache_store = {}
    __cache_storage_path = abspath('.')+'/storage/.cache'

    def __init__(self):
        self.reload()
        {self.__revalidate(key) for key, value in list(self.__cache_store.items())}
        self.__commit()

    def __revalidate(self, key):
        if self.has(key):
            expiry = self.__cache_store.get(key).get('expiry')
            self.__cache_store.pop(key) if time() > expiry else None


    def has(self, key):
        self.reload()
        return True if self.__cache_store.get(key, None) else False

    def put(self, key, data, expiry=int(getenv('CACHE_DURATION', 10))):
        self.__key = key
        self.__expiry *= expiry 

        if (self.__expiry):
            self.__cache_store[key] = {'data': data, 'expiry': time() +  self.__expiry}
            self.__commit()
    
    def pull(self, key):
        self.reload()
        try:
            data, expiry = self.__cache_store.pop(key).items()
            self.__commit()
            return data[1]
        except:
            return None
        
    def flush(self):
        try:
            unlink(self.__cache_storage_path)
            return (True)
        except:
            return (False)

    def __retrieve(self):
        if exists(self.__cache_storage_path):
            with open(self.__cache_storage_path, 'r') as fp:
                return load(fp)
        return {}

    def reload(self):
        ''' Reloads the cache_store once module is loaded up '''
        self.__cache_store = self.__retrieve()
    
    def __commit(self):
        ''' commit to the cache '''
        with open(self.__cache_storage_path, 'w') as fp:
                return dump(self.__cache_store, fp, indent=4)
    
cache = Cache()
cache.reload()