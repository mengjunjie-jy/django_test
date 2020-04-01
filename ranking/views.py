from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views import View
from ranking.models import Rank


class Fraction(View):
    def post(self, request):
        request_data = request.POST
        client_name = request_data.get("client_name")
        fraction = request_data.get("fraction")
        if not all([client_name, fraction]):
            return HttpResponse('缺少必要参数', status=400)
        print(client_name, fraction)
        current_client = Rank.objects.filter(client_name=client_name).first()
        # 如果存在更新，不存在新增
        if current_client:
            Rank.objects.filter(client_name=client_name).update(fraction=fraction)
        else:
            rank_obj = Rank(client_name=client_name, fraction=fraction)
            rank_obj.save()
        return HttpResponse('上传成功', status=200)

    def get(self, request):
        request_params = request.GET
        client_name = request_params.get("client_name")
        if not client_name:
            return HttpResponse('缺少客户端名称', 400)
        current_page = int(request_params.get("p", 1))
        count = request_params.get("count", 10)
        rank_obj = Rank.objects.all().order_by("-fraction")
        paginator = Paginator(rank_obj, count)
        num_pages = paginator.num_pages
        print(num_pages)
        if current_page > num_pages:
            current_page = 1
        page = paginator.page(current_page)  # 获取第一页数据，从1开始
        total = paginator.count
        start_index = (current_page - 1) * 10 + 1
        current_obj = None
        s_index = 1
        list = []
        for index, obj in enumerate(page):
            if client_name == obj.client_name:
                current_obj = obj
            list.append({"index": start_index + index, "id": obj.id, "client_name": obj.client_name, "fraction": obj.fraction})
        if not current_obj:
            current_obj = Rank.objects.filter(client_name=client_name).first()
        if current_obj:
            list.append({
                "index": s_index,
                "id": current_obj.id,
                "client_name": current_obj.client_name,
                "fraction": current_obj.fraction,
            })

        data = {
            "page": current_page,
            "count": count,
            "total": total,
            "data": list
        }

        return HttpResponse(content=data, status=200)
