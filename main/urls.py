from django.urls import path
from . import views

urlpatterns = [
    path('', views.stock_view, name='stock_view'),  # index를 stock_view로 변경
]