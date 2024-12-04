from django.shortcuts import render
from .service import kosdaq


def stock_view(request):
    kd = kosdaq()
    kd.connect_token_path('C:\\Users\\user\\PycharmProjects\\pythonProject2\\token\\dart_token.txt')
    kd.manage_path_financial('http://opendart.fss.or.kr/api/list.json')
    kd.get_token()

    if request.method == 'POST':
        stock_code = request.POST.get('stock_code', '')
        num = int(request.POST.get('num', 300))  # 기본값 300

        kd.get_table(num)  # 사용자가 입력한 num값으로 테이블 가져오기
        data = kd.search_table(stock_code)
        html_data = kd.sender_html(data)

        context = {
            'result': html_data,
            'has_result': True
        }
        return render(request, 'index.html', context)

    return render(request, 'index.html', {'has_result': False})