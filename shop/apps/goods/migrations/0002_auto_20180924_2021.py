# Generated by Django 2.1.1 on 2018-09-24 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'verbose_name': '商品SKU', 'verbose_name_plural': '商品SKU'},
        ),
        migrations.AlterField(
            model_name='goods',
            name='name',
            field=models.CharField(max_length=20, verbose_name='商品SKU名称'),
        ),
    ]
