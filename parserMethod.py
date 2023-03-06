from abc import ABC, abstractmethod
import requests
import pandas

class House591Parser(ABC):
    @staticmethod
    def getSession():
        __s=requests.Session()
        return __s

    @abstractmethod
    def getCSRF(self):
        pass

    @abstractmethod    
    def gethouselist(self, __region, __page, __error):
        pass
    
    @staticmethod
    def data2Csv(self, __df):
        __df.to_excel('output.xlsx', index=False)

    