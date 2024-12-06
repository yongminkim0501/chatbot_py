from django.db import models
# # postgreSQL 구성 예정
# # Create your models here.
# class stock(models.Model):
#     StockCode = models.CharField(max_length=7) # kosdaq 주식 검색을 위한 주식 코드
#     StockCls = models.CharField(max_length=3) # kosdaq 주식인 지 확인을 위한 corp_cls
#     ReportName = models.TextField() # 공시 한 내용
#     StockName = models.TextField() # 해당 주식의 이름
#
# '''
# PostgreSQL 구성을 위해서
# pip install psycopg2 (도구) - 어댑터
# '''