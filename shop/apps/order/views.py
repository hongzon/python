from django.shortcuts import render,redirect,reverse
from django.views.generic import View
from django_redis import get_redis_connection
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.user.models import Address
from apps.goods.models import GoodsSKU
from django.http import JsonResponse
from apps.order.models import *
from django.db import transaction
# Create your views here.

class OrderPlaceView(LoginRequiredMixin, View):
    """提交订单页面"""

    def post(self, request):
        # 获取用户
        user = request.user

        # 获取提交时被选中的商品id
        sku_ids = request.POST.getlist('sku_ids')
        # print('sku_ids: ', sku_ids)

        # 若没有商品，则直接跳回首页
        if len(sku_ids) == 0:
            return redirect(reverse('goods:index'))

        # 获取收货地址

        addrs = Address.objects.filter(user=user)

        # 拼接key
        cart_key = 'cart_%d' % user.id

        # 连接redis
        conn = get_redis_connection('default')
        # 遍历sku_ids获取用户所要购买的商品的信息
        skus = []
        total_count = 0
        total_amount = 0
        for sku_id in sku_ids:
            # 根据id查找商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)

            # 从redis中获取用户所要购买的商品的数量
            count = conn.hget(cart_key, sku_id)

            count = int(count)
            # 计算商品的小计
            amount = sku.price * count

            # 给sku对象增加属性count和amount
            # 分别保存用户要购买的商品的数目和小计
            sku.count = count
            sku.amount = amount

            # 追加商品的信息
            skus.append(sku)

            # 累加计算用户要购买的商品的总件数和总金额
            total_count += int(count)
            total_amount += amount

        # 运费: 运费表: 100-200  假设为10
        transit_price = 10

        # 实付款
        total_pay = total_amount + transit_price

        # 组织模板上下文
        context = {
            'addrs': addrs,
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'transit_price': transit_price,
            'total_pay': total_pay,
            'sku_ids': ','.join(sku_ids)
        }

        # 使用模板
        return render(request, 'place_order.html', context)
class OrderCommitView(View):
    """订单创建"""

    @transaction.atomic
    def post(self, request):
        # 判断用户是否登录
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})

        # 接收参数
        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('sku_ids')  # 以,分隔的字符串 3,4

        # 参数校验
        if not all([addr_id, pay_method, sku_ids]):
            return JsonResponse({'res': 1, 'errmsg': '参数不完整'})

        # 校验地址id
        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '地址信息错误'})

        # 校验支付方式
        if pay_method not in OrderInfo.PAY_METHODS.keys():
            return JsonResponse({'res': 3, 'errmsg': '非法的支付方式'})

        # 组织订单信息
        # 组织订单id: 20180316115930+用户id
        from datetime import datetime
        order_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(user.id)

        # 运费
        transit_price = 10

        # 总数目和总价格
        total_count = 0
        total_price = 0

        # 设置事务保存点
        sid = transaction.savepoint()

        try:
            # 向df_order_info中添加一条记录
            order = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                addr=addr,
                pay_method=pay_method,
                total_count=total_count,
                total_price=total_price,
                transit_price=transit_price
            )

            # 订单中包含几个商品需要向df_order_goods中添加几条记录
            # 获取redis链接
            conn = get_redis_connection('default')
            # 拼接key
            cart_key = 'cart_%d' % user.id

            # 将sku_ids分割成一个列表
            sku_ids = sku_ids.split(',')  # [3,4]

            # 遍历sku_ids，向df_order_goods中添加记录
            for sku_id in sku_ids:
                for i in range(3):
                    # 根据id获取商品的信息
                    try:
                        # select * from df_goods_sku where id=<sku_id>;
                        sku = GoodsSKU.objects.get(id=sku_id)
                    except GoodsSKU.DoesNotExist:
                        # 回滚事务到sid保存点
                        transaction.savepoint_rollback(sid)
                        return JsonResponse({'res': 4, 'errmsg': '商品信息错误'})

                    # 从redis中获取用户要购买的商品的数量
                    count = conn.hget(cart_key, sku_id)

                    # 判断商品的库存
                    if int(count) > sku.stock:
                        # 回滚事务到sid保存点
                        transaction.savepoint_rollback(sid)
                        return JsonResponse({'res': 6, 'errmsg': '商品库存不足'})

                    # 减少商品库存，增加销量
                    orgin_stock = sku.stock
                    new_stock = orgin_stock - int(count)
                    new_sales = sku.sales + int(count)

                    # print('user:%d times:%d stock:%d' % (user.id, i, orgin_stock))
                    # import time
                    # time.sleep(10)

                    # update from df_goods_sku
                    # set stock=<new_stock>, sales=<new_sales>
                    # where id=<sku_id> and stock=<orgin_stock>
                    # update方法返回数字，代表更新的行数
                    res = GoodsSKU.objects.filter(id=sku_id, stock=orgin_stock).update(stock=new_stock, sales=new_sales)

                    if res == 0:
                        if i == 2:
                            # 回滚事务到sid保存点
                            transaction.savepoint_rollback(sid)
                            # 连续尝试了3次，仍然下单失败，下单失败
                            return JsonResponse({'res': 7, 'errmsg': '下单失败2'})
                        # 更新失败，重新进行尝试
                        continue

                    # 向df_order_goods中添加一条记录
                    OrderGoods.objects.create(
                        order=order,
                        sku=sku,
                        count=count,
                        price=sku.price
                    )

                    # 累加计算订单中商品的总数目和总价格
                    total_count += int(count)
                    total_price += sku.price * int(count)

                    # 更新成功，跳出循环
                    break

            # 更新订单信息中商品的总数目和总价格
            order.total_count = total_count
            order.total_price = total_price
            order.save()
        except Exception as e:
            # 回滚事务到sid保存点
            transaction.savepoint_rollback(sid)
            return JsonResponse({'res': 7, 'errmsg': '下单失败1'})

            # 删除购物车中对应的记录
        # hdel(key, *args)
        conn.hdel(cart_key, *sku_ids)

        # 返回应答
        return JsonResponse({'res': 5, 'errmsg': '订单创建成功'})