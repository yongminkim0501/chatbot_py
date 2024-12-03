from django.shortcuts import render
from .service import StockService
import pandas as pd
def index(request):
    if request.method == 'POST':
        stock_code = request.POST.get('stock_code')
        # 여기서 API 호출 및 데이터 처리
        service = StockService()
        result = service.get_stock_info(stock_code)
        if isinstance(result, pd.DataFrame):
            result = result.to_html()
        return render(request, 'main/index.html', {
            'result': result,
            'has_result': True
        })
    return render(request, 'main/index.html')