from django.contrib import admin
from django.core.cache import cache
from apps.goods.models import GoodsType, IndexPromotionBanner, IndexGoodsBanner,  IndexTypeGoodsBanner,GoodsSKU,Goods
from django.urls import path
from django.template.response import TemplateResponse
# Register your models here.
from .forms import GoodsForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.conf.urls import url
class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """新增或更新时调用"""
        # 调用ModelAdmin中save_model来实现更新或新增
        super().save_model(request, obj, form, change)
        # 附加操作：发出生成静态首页的任务
        # from celery_tasks.tasks import generate_static_index_html
        # print('发出重新生成静态首页的任务')
        # generate_static_index_html.delay()
        #
        # # 附加操作: 清除首页缓存
        # cache.delete('index_page_data')

    def delete_model(self, request, obj):
        """删除数据时调用"""
        # 调用ModelAdmin中delete_model来实现删除操作
        super().delete_model(request, obj)
        # 附加操作：发出生成静态首页的任务
        # from celery_tasks.tasks import generate_static_index_html
        # generate_static_index_html.delay()
        #
        # # 附加操作: 清除首页缓存
        # cache.delete('index_page_data')


class GoodsTypeAdmin(BaseModelAdmin):
    """商品种类模型admin管理类"""
    pass


class IndexGoodsBannerAdmin(BaseModelAdmin):
    """首页轮播商品模型admin管理类"""
    pass


class IndexTypeGoodsBannerAdmin(BaseModelAdmin):
    """首页分类商品展示模型admi管理类"""
    pass


class IndexPromotionBannerAdmin(BaseModelAdmin):
    pass
class GoodsAdmin(BaseModelAdmin):
    form  = GoodsForm
    # change_form_template = 'sku.html'
    # add_form_template = 'sku.html'
    # def get_changelist_form(self, request, **kwargs):
    #     return GoodsForm
    # def get_form(self, request, obj=None, change=False, **kwargs):
    #     kwargs['form'] = GoodsForm
    #     return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        # print type(form.Meta.fields)
        print(obj)
        print(form.cleaned_data['is_delete'])
        print(request)
        name = request.POST.get('name')  # 获取自定义表单提交的值
        print(name)
        price = request.POST.get('price')  # 获取自定义表单提交的值
        market_price = request.POST.get('market_price')
        storage = request.POST.get('storage')
        desc = request.POST.get('detail')
        category = request.POST.get('category')
        print('category:',category)
        obj.save()
        print(obj.id)
        m = GoodsSKU(name=name,desc=desc,price=price,stock=storage,goods_id=obj.id,category_id = category)
        m.save()

class MyModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = super().get_urls()
        my_urls = [
            path('add/', self.my_view),
        ]
        return my_urls + urls

    def my_view(self, request):
        # ...
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            key='3344',
        )
        return TemplateResponse(request, "test.html", context)
def my_view(request):
    return HttpResponse("Hello!")

# def get_admin_urls(urls):
#     def get_urls():
#         my_urls = [
#             url(r'^my_view/$', admin.site.admin_view(my_view))
#         ]
#         return my_urls + urls
#     return get_urls
#
# admin_urls = get_admin_urls(admin.site.get_urls())
# admin.site.get_urls = admin_urls

admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)
admin.site.register(Goods, MyModelAdmin)
