from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel
class User(AbstractUser,BaseModel):
    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class AddressManager(models.Manager):
    def get_all_address(self, User):

        try:
            address = self.filter(user = User)
        except self.model.DoesNotExist:
            address = None
        return address
    def get_default_address(self, User):
        try:
            # address = Address.objects.get(user=user, is_default=True)
            address = self.get(user=User, is_default=True)
        # except Address.DoesNotExist:
        except self.model.DoesNotExist:
            address = None

        # 返回address
        return address
class Address(BaseModel):
    user = models.ForeignKey('User', verbose_name='所属账户', on_delete=models.CASCADE)
    receiver = models.CharField(max_length=20,verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6,blank=True,verbose_name='邮编')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    is_default = models.BooleanField(default=False, verbose_name='是否默认地址')

    objects = AddressManager()

    class Meta:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = '地址'



