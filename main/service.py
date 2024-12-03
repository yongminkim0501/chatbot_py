#서비스 구현을 위한 py 파일
import requests
import os
import pandas as pd
from django.conf import settings
#
# token_path = os.path.join(settings.BASE_DIR, 'token', 'dart_token.txt')
# with open(token_path, 'r') as file:
#     token = file.read().strip()

def get_kosdaq(token):
    results_all = pd.DataFrame()  # 전체결과 DataFrame, kosdaq 기업 중 100개의 기업을 불러와서 저장 반환함.
    kosdaq_count = 0  # 코스닥 기업 카운터
    page_no = 0
    page_count = 0
    while True:
        try:
            url = 'https://opendart.fss.or.kr/api/list.json'
            params = {
                'crtfc_key': token,
                'page_no': str(page_no),
                'page_count': str(page_count),
                'begin_de' : '20240101',
                'end_de' : '20241231'
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                return f"API 오류 : {response.status_code}"
            results = response.json()
            results_df = pd.DataFrame(results['list'])

            # K인 경우만 필터링해서 추가
            kosdaq_df = results_df[results_df['corp_cls'] == 'K']
            results_all = pd.concat([results_all, kosdaq_df])

            # 현재까지 수집된 코스닥 기업 수 업데이트
            kosdaq_count = len(results_all)

            # 100개 이상 수집됐으면 중단
            if kosdaq_count >= 100:
                # 정확히 100개만 남기기
                results_all = results_all.head(100)
                break

            # total_page = results['total_page']
            if page_no == 300:
                print(page_no, ',', 300)
                break

            page_no = page_no + 1
        except requests.exceptions.RequestException as e:
            return f'API 연결 오류 : {str(e)}'
    return results_all
# results_all : 코스닥 기업 저장함.
'''
corp_code, corp_name, stock_code, corp_cls, report_nm, rcept_no, flr_nm, rcept_dt, rm...
'''
class NoCodeException(Exception):
    def __str__(self):
        return ": 코드는 코스닥 100개 안에 존재하지 않음"

class StockService:
    def __init__(self):
        self.stock = self.make_stock()
    def make_stock(self):
        token_path = os.path.join(settings.BASE_DIR, 'token', 'dart_token.txt')
        with open(token_path, 'r') as file:
            token = file.read().strip()
        self.stock = get_kosdaq(token)
        return self.stock
    def get_stock_info(self, stock_code):
        try:
            if stock_code in self.stock['stock_code'].values:
                return self.stock['stock_code']
        except NoCodeException as e:
            return str(e)