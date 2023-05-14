from os import getenv, getcwd, unlink
from os.path import join, realpath, dirname, getctime, exists
from time import time
import re
from json import dump, load
from glob import glob

class Cache:
    __expiry__ = int(getenv('CACHE_DURATION', 10)) * 60
    __cache_file_name__ = ''
    __cache_dir__ = realpath(join(dirname('.'),'storage/caches'))
    
    def __init__(self, key_as_path=False):
        self.key_as_path = key_as_path
        
    def tranform_key(self, key):
        if self.key_as_path:
            cache_file_name = re.sub(r'/', '__', key)
            self.__cache_file_name__ = join(self.__cache_dir__, cache_file_name)
        else:   
             self.__cache_file_name__ = join(self.__cache_dir__, key)        
    
    def revalidate(self, key):
        if self.has(key):
            diff_secs = time() - getctime(self.__cache_file_name__)
            print(diff_secs)
            unlink(self.__cache_file_name__) if diff_secs > self.__expiry__ else None
   
    def put(self, key, data):
        if not self.has(key):
            with open(self.__cache_file_name__, 'w') as fp:
                dump(data, fp)
                return data

    def get(self, key):
        self.tranform_key(key)
        with open(self.__cache_file_name__, 'r') as fp:
            return load(fp)
        
    def has(self, key):
        self.tranform_key(key)
        return exists(self.__cache_file_name__)
        
    def __all(self):
        return glob(self.__cache_dir__+'/*')
        
        
    @classmethod
    def DBResource(cls, req_path, cb):
        cache = cls(req_path)
        if cache.is_cached:
            return cache.get()
        else:
            cache.set(cb())
            return cb()

    @classmethod
    def ExtResource(cls, req_path, server_req_obj):
        cache = cls(req_path)
        if cache.is_cached:
            return cache.get()
        else:
            if server_req_obj().status_code == 200:
                cache.set(server_req_obj().json())
                return server_req_obj().json()
        
    @classmethod
    def empty(cls):
        [unlink(file) for file in glob(cls.__cache_dir__+'/*')]
 

        
    
    
    