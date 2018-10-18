from django.conf.urls import url
from apps.goods.views import IndexView, DetailView, ListView
from django.urls import path
app_name = 'goods'
urlpatterns = [
    path(r'', IndexView.as_view(), name='index'),  # 首页
    # url(r'^index$', IndexView.as_view(), name='index'),  # 首页
    path(r'goods/<int:sku_id>', DetailView.as_view(), name='detail'),  # 详情页
    path(r'list/<int:type_id>/<int:page>', ListView.as_view(), name='list'), # 列表页
]