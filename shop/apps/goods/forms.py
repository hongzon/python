from django import forms
from .models import GoodsType
class GoodsForm(forms.ModelForm):
    name = forms.CharField(required=True,error_messages={'required':'商品名称不能为空'},label = '商品名称')
    price = forms.DecimalField(required=True,max_digits = 9,error_messages={'required':'商品价格不能为空'},label='价格')
    market_price = forms.DecimalField(required=True,max_digits=9,error_messages={'required':'商品市场价不能为空'},label='市场价')
    storage = forms.IntegerField(required=True,error_messages={'required':'商品库存不能为空'},label='库存')
    detail = forms.CharField(widget=forms.Textarea(attrs={'cols':20}),label = '商品详情',required=False)
    category = forms.ModelChoiceField(queryset = GoodsType.objects.all(),label='分类')