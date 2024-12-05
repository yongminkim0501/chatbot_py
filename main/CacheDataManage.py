from django.core.cache import cache
import pandas as pd
class CacheImpl:
    def __init__(self):
        self.CACHE_KEY = 'kosdaq_table'
        self.CACHE_TIMEOUT = 60*60
        self.cachedTable = []

    def ConnectDataCache(self, x): # Cache 데이터에 x로 인자를 받아 연결함
        # Cache에다가 해당 데이터를 저장, pd.Dataframe 형태로 받을 예정
        cache.set(self.CACHE_KEY, x, self.CACHE_TIMEOUT)

    def GetCache(self):
        self.cachedTable = cache.get(self.CACHE_KEY)
        if self.cachedTable is not None: #Cache가 존재할 경우
            CacheResultFinancial = pd.DataFrame(self.cachedTable)
            return CacheResultFinancial #DataFrame 형태로 반환
        else: # 존재하지 않으면 0을 반환
            return 0

    def ClearCache(self):
        cache.clear()