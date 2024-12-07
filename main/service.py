#서비스 구현을 위한 py 파일
import requests
import os
import pandas as pd
from .CacheDataManage import CacheImpl

class kosdaq:
    def __init__(self):
        self.count = 0
        self.table = pd.DataFrame()
        self.cache_impl = CacheImpl()
        self.DART_API_TOKEN = ""
        self.dart_url = ""

    def get_token(self):
        self.DART_API_TOKEN = os.environ.get('dart_token')

    def manage_path_financial(self, data_path):
        self.dart_url = data_path

    def get_table(self, num):
        result_all = pd.DataFrame()
        page_no = 0
        page_count = 0
        while True:
            url = self.dart_url
            params = {
                'crtfc_key': self.DART_API_TOKEN,
                'page_no': str(page_no),
                'page_count': str(page_count),
            }
            result = requests.get(url, params=params, verify=False).json()
            results_df = pd.DataFrame(result['list'])

            kosdaq_df = results_df[results_df['corp_cls'] == 'K']
            result_all = pd.concat([result_all, kosdaq_df])

            kosdaq_count = len(result_all)

            if kosdaq_count >= num:
                result_all = result_all.head(num)
                break

            if page_no == 300:
                break

            page_no += 1
        self.table = result_all
        self.cache_impl.ConnectDataCache(self.table)
        print(self.table)

    def search_table(self, code):
        kosdaq_df = pd.DataFrame()
        try:
            cached_data = self.cache_impl.GetCache()
            if isinstance(cached_data, int) and cached_data == 0:
                kosdaq_df = self.table[self.table['stock_code'] == code]
                if kosdaq_df.empty:
                    return pd.DataFrame({'message':['해당 코드의 주식이 존재 하지 않습니다.']})
                return kosdaq_df
            else:
                kosdaq_df = self.cache_impl.GetCache()
                result = kosdaq_df[kosdaq_df['stock_code']==code]
                if result.empty:
                    return pd.DataFrame({'message':['해당 코드의 주식이 존재 하지 않습니다.']})
                return result
        except Exception as e:
            print(f"검색 에러: {e}")
            return pd.DataFrame({'error':[str(e)]})

    def sender_html(self, kosdaq_df_data):
        table_html = kosdaq_df_data.to_html(classes='table table-striped', index=False)
        return table_html
